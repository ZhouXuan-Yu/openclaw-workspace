#!/usr/bin/env python3
"""每日工作恢复检查 — 纯本地运行，零网络依赖
检查任务：
  1. 昨日日志是否存在（判断是否关机/离线）
  2. 待办队列中的未完成任务
  3. Cron 状态标记文件中的失败记录
输出：打印报告 + 写入 memory/daily/recovery-status.json"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent.parent
DAILY_DIR = WORKSPACE / "memory" / "daily"
TOPICS_DIR = WORKSPACE / "memory" / "topics"
RECOVERY_STATUS = DAILY_DIR / "recovery-status.json"

def get_date_str(days_ago=0):
    return (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

def check_yesterday_log():
    """检查昨日日志是否存在"""
    yesterday = get_date_str(1)
    log_file = DAILY_DIR / f"{yesterday}.md"
    if log_file.exists():
        content = log_file.read_text(encoding="utf-8")
        # 检查是否为空或只有模板内容
        has_content = len(content.strip()) > 50
        return {"exists": True, "has_content": has_content, "size": len(content)}
    return {"exists": False, "has_content": False, "size": 0}

def check_pending_tasks():
    """检查待办队列中的未完成任务"""
    pending_file = DAILY_DIR / "pending_tasks.json"
    if not pending_file.exists():
        return {"pending_count": 0, "tasks": []}
    
    data = json.loads(pending_file.read_text(encoding="utf-8"))
    today = get_date_str()
    pending = [t for t in data.get("tasks", []) if t.get("status") != "done"]
    return {"pending_count": len(pending), "tasks": pending[:20]}

def check_recovery_status():
    """检查上次恢复状态"""
    if RECOVERY_STATUS.exists():
        return json.loads(RECOVERY_STATUS.read_text(encoding="utf-8"))
    return {"last_check": None, "pending_cron_jobs": [], "recovered": False}

def save_recovery_status(data):
    """保存恢复状态"""
    RECOVERY_STATUS.parent.mkdir(parents=True, exist_ok=True)
    RECOVERY_STATUS.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def generate_report():
    """生成纯文本报告"""
    yesterday_log = check_yesterday_log()
    pending = check_pending_tasks()
    status = check_recovery_status()
    today = get_date_str()
    yesterday = get_date_str(1)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    lines = []
    lines.append(f"# 📋 工作恢复检查 — {today}")
    lines.append(f"> 检查时间: {now}")
    lines.append("")
    
    # 1. 离线检测
    lines.append("## 1️⃣ 离线检测")
    if yesterday_log["exists"] and yesterday_log["has_content"]:
        lines.append("✅ 昨日有正常会话记录")
        lines.append(f"   日志: memory/daily/{yesterday}.md ({yesterday_log['size']} bytes)")
    elif yesterday_log["exists"] and not yesterday_log["has_content"]:
        lines.append("⚠️ 昨日日志存在但无实质内容 — 可能仅启动了会话")
    else:
        lines.append("⚠️ **昨日日志不存在** — 确认曾经离线/关机未启动")
        lines.append("   建议: 下次开机后自动检查常驻定时任务是否需要补跑")
    lines.append("")
    
    # 2. 待办任务
    lines.append("## 2️⃣ 待办任务")
    if pending["pending_count"] > 0:
        lines.append(f"⚠️ 有 {pending['pending_count']} 个任务待完成:")
        for i, t in enumerate(pending["tasks"][:10], 1):
            lines.append(f"   {i}. {t.get('text', str(t))[:120]}")
    else:
        lines.append("✅ 无待办任务")
    lines.append("")
    
    # 3. Cron 状态
    lines.append("## 3️⃣ Cron 恢复状态")
    pending_crons = status.get("pending_cron_jobs", [])
    if pending_crons:
        lines.append(f"⚠️ {len(pending_crons)} 个定时任务有待恢复:")
        for pc in pending_crons:
            lines.append(f"   - {pc.get('name', 'unknown')}: {pc.get('reason', '')}")
        lines.append("")
        lines.append("   恢复策略:")
        lines.append("   1. 深度调研(每日新闻): 下次成功运行时自动补发前日内容")
        lines.append("   2. 社交内容(daily-social-content): 跳过已过期的日程，恢复今日")
        lines.append("   3. GitHub 趋势: 每日独立，跳过已过期，今日正常执行")
    else:
        lines.append("✅ 无待恢复的定时任务（或上次已恢复）")
    lines.append("")
    
    # 4. 恢复建议
    lines.append("## 4️⃣ 建议操作")
    lines.append("| 优先级 | 任务 | 操作 |")
    lines.append("|--------|------|------|")
    if not yesterday_log["exists"]:
        lines.append("| P0 | 检查各定时任务是否需要补跑 | 阅读昨日 cron 失败详情 |")
    if pending["pending_count"] > 0:
        lines.append("| P1 | 处理待办队列 | 确认哪些仍需执行 |")
    if pending_crons:
        lines.append("| P1 | 补发深度调研 | 按需主动触发一次 |")
    lines.append("| P2 | 确认网络状态 | 检查模型 API 是否已恢复 |")
    lines.append("")
    
    # 5. 恢复标记
    recovery_time = status.get("last_check")
    if recovery_time:
        lines.append(f"📌 上次恢复检查: {recovery_time}")
    
    return "\n".join(lines)

def main():
    report = generate_report()
    print(report)
    
    # 保存状态
    status = {
        "last_check": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "today": get_date_str(),
        "yesterday_log_exists": check_yesterday_log()["exists"],
        "pending_tasks": check_pending_tasks(),
        "recovered": False  # 标记为未恢复，等待用户确认
    }
    save_recovery_status(status)
    
    # 写入 review 文件供 agent 读取
    yesterday = get_date_str(1)
    review_file = DAILY_DIR / f"review-{yesterday}.md"
    review_file.write_text(report, encoding="utf-8")
    
    print(f"\n📁 报告已存储: memory/daily/review-{yesterday}.md")
    
    # 如果有离线/P0，返回非0退出码让调用方知道
    yesterday_log = check_yesterday_log()
    pending = check_pending_tasks()
    if not yesterday_log["exists"] or pending["pending_count"] > 0:
        sys.exit(10)  # 有需恢复的任务

if __name__ == "__main__":
    main()
