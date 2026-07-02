#!/usr/bin/env python3
"""taskcal — 轻量任务日历CLI，通过追加 daily 文件与 Agent 通信"""

import argparse
import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# 配置
# ============================================================
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
TASKS_FILE = WORKSPACE / "memory" / "topics" / "task-calendar.md"
DAILY_DIR = WORKSPACE / "memory" / "daily"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%Y-%m-%d %H:%M"

P0_ADVANCE_MIN = 15
P1_ADVANCE_MIN = 5
P2_ADVANCE_MIN = 0


def now():
    return datetime.now()


# ============================================================
# 任务存储
# ============================================================
def parse_tasks_from_md():
    if not TASKS_FILE.exists():
        return []

    tasks = []
    current_date = None
    lines = TASKS_FILE.read_text(encoding="utf-8").splitlines()

    for line in lines:
        line = line.strip()
        if line.startswith("## ") and not line.startswith("## 历史"):
            m = re.search(r'(\d{4}-\d{2}-\d{2})', line[3:])
            if m:
                current_date = m.group(1)
            continue

        if line.startswith("## 历史"):
            break

        if line.startswith("|") and ":" in line and current_date:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 3 and ":" in parts[0]:
                time_part = parts[0].replace("~", "").strip()
                msg = parts[1].strip().strip("**")
                priority = parts[2] if len(parts) > 2 else "P1"

                at = f"{current_date} {time_part}"
                tid = f"{current_date}T{time_part.replace(':', '-')}"

                tasks.append({
                    "id": tid,
                    "msg": msg,
                    "at": at,
                    "priority": priority,
                    "status": parts[3] if len(parts) > 3 else "⬜",
                })

    return tasks


def list_tasks(tasks):
    if not tasks:
        print("📭 没有待办任务")
        return

    today = now().strftime(DATE_FORMAT)
    print(f"\n📅 任务日历"
          f" — {today}")
    print("-" * 60)

    for t in tasks:
        icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}.get(t["priority"], "⚪")
        status = t.get("status", "⬜")
        done = "✅" if status in ("✅", "已完成") else "⬜"
        print(f"  [{t['id']}] {icon} {done} {t['at']} — {t['msg']} ({t['priority']})")


# ============================================================
# 提醒：追加到今日 daily，Agent 下次交互自然看到
# ============================================================
def fire_reminder(task):
    """到点后追加提醒到今日 daily 文件"""
    at = datetime.strptime(task["at"], TIME_FORMAT)
    advance = {"P0": P0_ADVANCE_MIN, "P1": P1_ADVANCE_MIN}.get(task["priority"], P2_ADVANCE_MIN)
    trigger_time = at - timedelta(minutes=advance)

    if now() < trigger_time:
        print(f"⏳ 尚未到提醒时间: {task['at']} (提前 {advance} min)")
        return False

    daily_file = DAILY_DIR / f"{at.strftime(DATE_FORMAT)}.md"
    icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}.get(task["priority"], "⚪")

    line = f"\n{icon} **TaskCal 提醒** [{task['priority']}] {task['msg']} — {task['at']} (提前 {advance}min 触发)\n"

    if daily_file.exists():
        content = daily_file.read_text(encoding="utf-8")
        if line.strip() in content:
            print(f"⏭️ 已提醒过，跳过: {task['msg']}")
            return True
        daily_file.write_text(content.rstrip() + line, encoding="utf-8")
    else:
        daily_file.write_text(f"# {at.strftime(DATE_FORMAT)}\n{line}", encoding="utf-8")

    print(f"🔔 已提醒: [{task['priority']}] {task['msg']} — {task['at']}")
    print(f"   写入 → {daily_file}")
    return True


# ============================================================
# Windows 任务计划
# ============================================================
def register_schtask(task):
    """为单个任务注册 Windows 一次性定时器"""
    at = datetime.strptime(task["at"], TIME_FORMAT)
    advance = {"P0": P0_ADVANCE_MIN, "P1": P1_ADVANCE_MIN}.get(task["priority"], P2_ADVANCE_MIN)
    trigger_time = at - timedelta(minutes=advance)

    if trigger_time <= now():
        print(f"⏰ 时间已过，直接触发: {task['msg']}")
        fire_reminder(task)
        return

    task_name = f"TaskCal_{task['id'].replace(':', '-')}"
    trigger_str = trigger_time.strftime("%H:%M")
    trigger_date = trigger_time.strftime("%Y-%m-%d")
    script = str(Path(__file__).resolve())
    cmd = f'python "{script}" fire --id "{task["id"]}"'

    # 删除已有的同名任务
    os.system(f'schtasks /delete /tn "{task_name}" /f 2>nul')

    result = os.system(
        f'schtasks /create /tn "{task_name}" '
        f'/tr "{cmd}" '
        f'/sc once /st {trigger_str} /sd {trigger_date} '
        f'/f'
    )

    if result == 0:
        print(f"✅ 已注册计划: {task_name}")
        print(f"   ⏰ {trigger_str} → {cmd}")
    else:
        print(f"❌ 注册失败 (err={result})，改为直接 fire:")
        fire_reminder(task)


def unregister_all():
    """删除所有 TaskCal 计划任务"""
    result = os.popen('schtasks /query /fo csv /nh').read()
    deleted = 0
    for line in result.splitlines():
        if "TaskCal_" in line:
            name = line.split(",")[0].strip('"')
            os.system(f'schtasks /delete /tn "{name}" /f')
            deleted += 1
    print(f"🗑️ 已清理 {deleted} 个 TaskCal 计划任务")


# ============================================================
# CLI 命令
# ============================================================
def cmd_list(args):
    tasks = parse_tasks_from_md()
    list_tasks(tasks)


def cmd_fire(args):
    """到点触发：由 Windows 计划任务调用"""
    tasks = parse_tasks_from_md()
    for t in tasks:
        if t["id"] == args.id:
            fire_reminder(t)
            return
    print(f"❌ 未找到任务: {args.id}")


def cmd_schedule(args):
    """为所有未完成任务注册 Windows 计划"""
    tasks = parse_tasks_from_md()
    pending = [t for t in tasks if t["status"] not in ("✅", "已完成")]
    if not pending:
        print("📭 没有待提醒的任务")
        return

    print(f"📋 注册 {len(pending)} 个提醒...\n")
    for t in pending:
        register_schtask(t)
    print(f"\n✅ 完成。查看: schtasks /query | findstr TaskCal")


def cmd_unschedule(args):
    unregister_all()


def cmd_add(args):
    at = datetime.strptime(args.at, TIME_FORMAT)
    date_str = at.strftime(DATE_FORMAT)
    time_str = at.strftime("%H:%M")
    priority = args.priority.upper()
    msg = args.msg

    if TASKS_FILE.exists():
        content = TASKS_FILE.read_text(encoding="utf-8")
    else:
        content = "# 任务日历\n\n"

    date_marker = f"## {date_str}"
    insert_line = f"| {time_str} | {msg} | {priority} | ⬜ | CLI添加 |"

    if date_marker in content:
        section = "上午" if at.hour < 13 else "下午"
        lines = content.splitlines()
        new_lines = []
        inserted = False
        in_target_section = False

        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip().startswith("### ") and section in line:
                in_target_section = True
            if in_target_section and line.startswith("|") and not inserted:
                new_lines.insert(-1, insert_line)
                inserted = True
                in_target_section = False

        if not inserted:
            new_lines = lines[:]
            idx = None
            for i, line in enumerate(lines):
                if date_marker in line:
                    idx = i
                    break
            if idx is not None:
                new_lines.insert(idx + 2, f"### {section}")
                new_lines.insert(idx + 3, "| 时间 | 任务 | 优先级 | 状态 | 来源 |")
                new_lines.insert(idx + 4, insert_line)

        content = "\n".join(new_lines)
    else:
        section = "上午" if at.hour < 13 else "下午"
        block = f"\n{date_marker}\n\n### {section}\n| 时间 | 任务 | 优先级 | 状态 | 来源 |\n{insert_line}\n"
        content += block

    TASKS_FILE.write_text(content, encoding="utf-8")
    tid = f"{date_str}T{time_str.replace(':', '-')}"
    print(f"✅ 已添加: [{priority}] {msg} — {at.strftime(TIME_FORMAT)}")

    # 如果用户要求，顺便注册计划
    if args.schedule:
        register_schtask({
            "id": tid,
            "msg": msg,
            "at": at.strftime(TIME_FORMAT),
            "priority": priority,
        })


def cmd_done(args):
    if not TASKS_FILE.exists():
        print("❌ 任务文件不存在")
        return

    content = TASKS_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    matched = False
    for i, line in enumerate(lines):
        if args.id in line and "⬜" in line:
            lines[i] = line.replace("⬜", "✅", 1)
            matched = True
            break

    if matched:
        TASKS_FILE.write_text("\n".join(lines), encoding="utf-8")
        print(f"✅ 已标记完成: {args.id}")
    else:
        print(f"❌ 未找到任务: {args.id}")


# ============================================================
# Main
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="TaskCal — 任务日历CLI，通过 daily 文件与 Agent 通信")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="列出今日任务")

    p_add = sub.add_parser("add", help="添加任务")
    p_add.add_argument("msg", help="任务内容")
    p_add.add_argument("--at", required=True, help="提醒时间 YYYY-MM-DD HH:MM")
    p_add.add_argument("--priority", default="P1", choices=["P0", "P1", "P2"])
    p_add.add_argument("--schedule", action="store_true", help="同时注册 Windows 计划任务")

    sub.add_parser("schedule", help="为所有未完成任务注册 Windows 计划")
    sub.add_parser("unschedule", help="清理所有 TaskCal 计划任务")

    p_fire = sub.add_parser("fire", help="触发提醒（由计划任务调用）")
    p_fire.add_argument("--id", required=True, help="任务ID")

    p_done = sub.add_parser("done", help="标记完成")
    p_done.add_argument("id", help="任务ID")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "done":
        cmd_done(args)
    elif args.command == "schedule":
        cmd_schedule(args)
    elif args.command == "unschedule":
        cmd_unschedule(args)
    elif args.command == "fire":
        cmd_fire(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
