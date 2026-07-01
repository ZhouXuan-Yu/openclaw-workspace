"""未完成任务追踪 — 每天检查昨日未完成项并推送"""
import json
from pathlib import Path
from datetime import datetime, timedelta
import re

TASK_DIR = Path("memory/daily")
TASK_FILE = TASK_DIR / "pending_tasks.json"

def get_yesterday_date():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")

def load_pending():
    if TASK_FILE.exists():
        return json.loads(TASK_FILE.read_text(encoding="utf-8"))
    return {"tasks": [], "last_check": ""}

def save_pending(data):
    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASK_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def scan_task_keywords(content):
    """扫描文件中的待办标记"""
    patterns = [
        r'❌\s*(.+?)(?:\n|$)',           # ❌ 标记
        r'⬜\s*(.+?)(?:\n|$)',           # ⬜ 未完成
        r'TODO:\s*(.+?)(?:\n|$)',        # TODO:
        r'待(?:完成|做|办)[：:]\s*(.+?)(?:\n|$)',  # 待完成/待做
        r'[【\[]待办[】\]]\s*(.+?)(?:\n|$)',        # 【待办】
    ]
    tasks = []
    for pat in patterns:
        for m in re.finditer(pat, content):
            task = m.group(1).strip()
            if 3 < len(task) < 200:  # 合理的任务长度
                tasks.append(task)
    return tasks

def check_yesterday():
    yesterday = get_yesterday_date()
    daily = TASK_DIR / f"{yesterday}.md"
    
    results = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "yesterday": yesterday,
        "file_found": False,
        "tasks_found": [],
        "cron_failures": [],
        "notes": [],
    }
    
    # Check 1: 昨天的日志是否存在
    if daily.exists():
        content = daily.read_text(encoding="utf-8")
        results["file_found"] = True
        results["tasks_found"] = scan_task_keywords(content)
    else:
        results["notes"].append(f"昨日日志 {yesterday}.md 不存在 — 可能未启动或会话中断")
    
    # Check 2: 检查 cron 失败（从 cron list 中查）
    # cron 状态由调用方（cron agent turn）传入
    
    # Check 3: 检查昨日是否有记录的待办未完成
    pending = load_pending()
    yesterday_pending = [t for t in pending["tasks"] if t.get("created_date") == yesterday]
    for t in yesterday_pending:
        if t.get("status") != "done":
            results["tasks_found"].append(t["text"])
    
    return results

def generate_report(results):
    yesterday = results["yesterday"]
    lines = [f"# 📋 昨日({yesterday})未完成任务清单", "", f"> 检查时间: {results['date']}", ""]
    
    if not results["file_found"]:
        lines.append("⚠️ **昨日日志不存在**")
        lines.append(f"- 可能原因：未启动、关机中断、网络中断导致无会话记录")
        lines.append(f"- 文件路径: `memory/daily/{yesterday}.md`")
        lines.append("")
    
    tasks = results["tasks_found"]
    if tasks:
        lines.append(f"## 📌 待完成 ({len(tasks)} 项)")
        lines.append("")
        for i, t in enumerate(tasks, 1):
            lines.append(f"| {i} | {t[:100]} |")
        lines.append("")
    else:
        lines.append("✅ 昨日无待办任务")
        lines.append("")
    
    if results["cron_failures"]:
        lines.append("## ⚠️ Cron 失败")
        lines.append("")
        for cf in results["cron_failures"]:
            lines.append(f"- **{cf['name']}**: {cf.get('error', 'unknown')}")
        lines.append("")
    
    if results["notes"]:
        lines.append("## 📝 备注")
        lines.append("")
        for n in results["notes"]:
            lines.append(f"- {n}")
        lines.append("")
    
    return "\n".join(lines)

if __name__ == "__main__":
    results = check_yesterday()
    report = generate_report(results)

    # Save report
    report_file = TASK_DIR / f"review-{results['yesterday']}.md"
    report_file.write_text(report, encoding="utf-8")
    print(report)
    print(f"\n📁 报告已存储: {report_file}")
