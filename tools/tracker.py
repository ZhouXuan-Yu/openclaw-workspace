#!/usr/bin/env python3
"""数据追踪器 — 记录各平台发布数据"""
import json
import os
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/memory/evolution")

def log_publish_result(topic: str, platform: str, status: str, url: str = "", error: str = ""):
    """记录单个平台发布结果"""
    log_file = os.path.join(DATA_DIR, "publish-metrics.json")
    
    # 读取现有数据
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"version": 1, "records": []}
    
    # 添加新记录
    record = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "platform": platform,
        "status": status,  # success / failed / skipped
        "url": url,
        "error": error
    }
    data["records"].append(record)
    
    # 保存
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return record

def get_stats(topic: str = None):
    """获取发布统计"""
    log_file = os.path.join(DATA_DIR, "publish-metrics.json")
    
    if not os.path.exists(log_file):
        return {"total": 0, "success": 0, "failed": 0}
    
    with open(log_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = data["records"]
    if topic:
        records = [r for r in records if r["topic"] == topic]
    
    total = len(records)
    success = len([r for r in records if r["status"] == "success"])
    failed = len([r for r in records if r["status"] == "failed"])
    
    return {
        "total": total,
        "success": success,
        "failed": failed,
        "skipped": total - success - failed,
        "by_platform": {}
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python tracker.py <topic> <platform> <status> [url]")
        sys.exit(1)
    
    topic = sys.argv[1]
    platform = sys.argv[2]
    status = sys.argv[3]
    url = sys.argv[4] if len(sys.argv) > 4 else ""
    
    result = log_publish_result(topic, platform, status, url)
    print(f"✅ 记录: {platform} - {status}")
    
    stats = get_stats(topic)
    print(f"📊 统计: {stats['success']}/{stats['total']} 成功")
