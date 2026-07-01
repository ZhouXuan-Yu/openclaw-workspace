"""分级 Decay 衰减扫描脚本
用于 memory-consolidation cron 中调用。
逻辑：检查每个 fact 的 last_accessed，超过 tier decay_days → trust *= 0.9
"""
import json
import sys
from datetime import datetime, timezone, timedelta

TRUST_FILE = r"C:\Users\ZhouXuan\.openclaw\workspace\memory\evolution\trust-registry.json"

def load():
    with open(TRUST_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(reg):
    with open(TRUST_FILE, 'w', encoding='utf-8') as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)

def decay_scan(dry_run=False):
    reg = load()
    now = datetime.now(timezone.utc)
    tz = timezone(timedelta(hours=8))
    now_str = now.astimezone(tz).isoformat()
    
    decayed = []
    skipped_iron = []
    skipped_fresh = []
    
    for key, fact in reg['facts'].items():
        tier_name = fact['tier']
        tier = reg['tiers'][tier_name]
        
        # iron_law 永久跳过
        if not tier.get('editable', True):
            skipped_iron.append(key)
            continue
        
        # 无 decay_days 跳过
        decay_days = tier.get('decay_days')
        if not decay_days:
            continue
        
        # 解析最后访问时间
        la_str = fact.get('last_accessed', fact['history'][-1]['date'])
        try:
            la = datetime.fromisoformat(la_str)
            if la.tzinfo is None:
                la = la.replace(tzinfo=tz)
        except:
            continue
        
        # 检查是否过期
        days_since = (now - la).total_seconds() / 86400
        if days_since < decay_days:
            skipped_fresh.append(key)
            continue
        
        # 执行衰减
        old_trust = fact['trust']
        tier_min = tier['min_trust']
        new_trust = round(max(old_trust * 0.9, tier_min), 2)
        
        if not dry_run:
            fact['trust'] = new_trust
            fact['history'].append({
                'date': now_str,
                'action': 'decayed',
                'trust': new_trust,
                'prev_trust': old_trust,
                'days_since_accessed': round(days_since, 1)
            })
        
        decayed.append({
            'key': key,
            'tier': tier_name,
            'old_trust': old_trust,
            'new_trust': new_trust,
            'days_since': round(days_since, 1),
            'decay_days': decay_days
        })
    
    if not dry_run and decayed:
        reg['lastUpdated'] = now_str
        save(reg)
    
    # 输出报告
    print(f"分级 Decay 扫描 {now_str}")
    print(f"{'='*50}")
    print(f"iron_law 跳过: {len(skipped_iron)}")
    print(f"未过期跳过: {len(skipped_fresh)}")
    print(f"衰减执行: {len(decayed)}")
    print()
    
    if decayed:
        for d in decayed:
            flag = "DRY-RUN " if dry_run else ""
            print(f"  {flag}{d['key']} ({d['tier']}): {d['old_trust']} -> {d['new_trust']} "
                  f"({d['days_since']}d / {d['decay_days']}d)")
    else:
        print("  无需衰减")
    
    return decayed

if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    decay_scan(dry)
