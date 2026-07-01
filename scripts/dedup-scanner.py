"""Semantic Dedup 扫描脚本
基于中文关键词指纹重叠率检测重复条目。
不调 embedding API，纯本地计算。
"""
import os
import re
import sys
from collections import Counter

TOPIC_DIR = r"C:\Users\ZhouXuan\.openclaw\workspace\memory\topics"
OVERLAP_THRESHOLD = 0.50  # 关键词指纹重叠率阈值


def kw_fingerprint(text, min_len=2, max_len=4):
    """中文关键词指纹：2-4 字滑动窗口所有子串集合"""
    clean = re.sub(r"[^\u4e00-\u9fff]", "", text.lower())
    if len(clean) < min_len:
        return set()
    kws = set()
    for l in range(min_len, max_len + 1):
        for i in range(len(clean) - l + 1):
            kws.add(clean[i:i + l])
    return kws


def overlap_ratio(a_set, b_set):
    inter = a_set & b_set
    union = a_set | b_set
    return len(inter) / len(union) if union else 0.0


def scan(dry_run=True):
    entries = []
    
    for fname in sorted(os.listdir(TOPIC_DIR)):
        if not fname.endswith('.md') or fname.startswith('_'):
            continue
        path = os.path.join(TOPIC_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = re.split(r'\n(?=#{2,3}\s)', content)
        for si, section in enumerate(sections):
            text = section.strip()
            if len(text) < 80:
                continue
            entries.append({
                'file': fname,
                'section': si,
                'text': text[:200],
                'full_text': text,
                'kw_set': kw_fingerprint(text)
            })
    
    print(f"扫描 {len(entries)} 个条目 (阈值: {OVERLAP_THRESHOLD})")
    print("=" * 50)
    
    dupes = []
    
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            a = entries[i]
            b = entries[j]
            
            r = overlap_ratio(a['kw_set'], b['kw_set'])
            if r >= OVERLAP_THRESHOLD:
                dupes.append({
                    'overlap': round(r, 3),
                    'entry_a': {'file': a['file'], 'section': a['section'], 'preview': a['text'][:120]},
                    'entry_b': {'file': b['file'], 'section': b['section'], 'preview': b['text'][:120]}
                })
    
    dupes.sort(key=lambda d: -d['overlap'])
    
    if not dupes:
        print("未发现重复条目")
        return []
    
    for di, d in enumerate(dupes):
        print(f"\n[Dedupe #{di+1}] 重叠率: {d['overlap']}")
        print(f"  A [{d['entry_a']['file']}]: {d['entry_a']['preview'][:100]}")
        print(f"  B [{d['entry_b']['file']}]: {d['entry_b']['preview'][:100]}")
    
    return dupes

if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    result = scan(dry)
    if result:
        print(f"\n共 {len(result)} 组疑似重复，请人工审核")
