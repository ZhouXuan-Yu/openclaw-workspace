#!/usr/bin/env python3
"""深度调研待恢复队列管理 — 零网络依赖
当每日新闻生成失败时，写 pending 状态；
下次成功生成时，检查并补发错过的内容。"""

import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent.parent
DAILY_DIR = WORKSPACE / "memory" / "daily"
PENDING_FILE = DAILY_DIR / "news-pending.json"

def mark_failed(reason="network error"):
    """标记一次失败的生成"""
    data = _load()
    today = datetime.now().strftime("%Y-%m-%d")
    
    entry = {
        "date": today,
        "failed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "reason": reason,
        "recovered": False
    }
    
    # 避免重复记录同一天
    if not any(e["date"] == today for e in data["failed_days"]):
        data["failed_days"].append(entry)
    
    data["last_failure"] = entry["failed_at"]
    data["consecutive_failures"] = data.get("consecutive_failures", 0) + 1
    _save(data)
    return True

def mark_recovered():
    """标记已恢复（清空失败队列）"""
    data = _load()
    failed_dates = [e["date"] for e in data["failed_days"] if not e["recovered"]]
    for e in data["failed_days"]:
        e["recovered"] = True
    data["consecutive_failures"] = 0
    data["last_recovery"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    _save(data)
    return failed_dates

def get_pending():
    """获取待恢复的日期列表"""
    data = _load()
    return [e["date"] for e in data["failed_days"] if not e["recovered"]]

def summary():
    """获取简要状态"""
    data = _load()
    pending = [e for e in data["failed_days"] if not e["recovered"]]
    return {
        "consecutive_failures": data.get("consecutive_failures", 0),
        "pending_days": len(pending),
        "pending_dates": [e["date"] for e in pending],
        "last_failure": data.get("last_failure"),
        "last_recovery": data.get("last_recovery")
    }

def _load():
    if PENDING_FILE.exists():
        return json.loads(PENDING_FILE.read_text(encoding="utf-8"))
    return {"failed_days": [], "consecutive_failures": 0, "last_failure": None, "last_recovery": None}

def _save(data):
    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    PENDING_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    if cmd == "mark_failed":
        reason = sys.argv[2] if len(sys.argv) > 2 else "network error"
        mark_failed(reason)
        print(f"❌ 已标记 {datetime.now().strftime('%Y-%m-%d')} 为失败: {reason}")
    elif cmd == "mark_recovered":
        dates = mark_recovered()
        print(f"✅ 已恢复 {len(dates)} 天: {', '.join(dates)}")
    elif cmd == "pending":
        p = get_pending()
        if p:
            print(f"⏳ 待恢复: {', '.join(p)}")
        else:
            print("✅ 无待恢复")
    else:
        s = summary()
        print(f"连续失败: {s['consecutive_failures']}")
        print(f"待恢复天数: {s['pending_days']}")
        print(f"待恢复日期: {', '.join(s['pending_dates']) if s['pending_dates'] else '无'}")
        print(f"最后失败: {s['last_failure']}")
        print(f"最后恢复: {s['last_recovery']}")
