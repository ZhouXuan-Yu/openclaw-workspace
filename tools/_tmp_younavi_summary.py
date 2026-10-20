#!/usr/bin/env python3
# Temporary helper: compact YouNavi summary (safe to delete)
import json, sys, subprocess, os, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from younavi_bridge import YouNavi

CLI = r"D:\YouNavi\resources\backend\agent-cli.exe"
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"
env["PYTHONUTF8"] = "1"

def run(args, timeout=120):
    try:
        r = subprocess.run([CLI] + args, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"

mode = sys.argv[1] if len(sys.argv) > 1 else "tasks"

if mode == "tasks":
    yn = YouNavi()
    res = yn.task_list()
    root = res.get("data")
    def dig(d):
        if isinstance(d, list):
            return d
        if isinstance(d, dict):
            for k in ("tasks", "items", "data", "list", "records"):
                if k in d:
                    r = dig(d[k])
                    if r is not None:
                        return r
        return None
    tasks = dig(root) or []
    print("TOTAL_TASKS", len(tasks))
    for t in tasks:
        print("|".join([
            str(t.get("created_at", ""))[:19],
            t.get("task_type", ""),
            t.get("status", ""),
            (t.get("command_message", "") or "")[:80].replace("\n", " "),
            str(t.get("error_message", "") or "")[:60],
        ]))
elif mode == "files":
    yn = YouNavi()
    res = yn.file_list()
    print(json.dumps(res.get("data"), ensure_ascii=False)[:3000])
elif mode == "syncall":
    rc, out, err = run(["channel", "sync", "--all", "--no-follow"], timeout=180)
    print("RC", rc)
    print(out[-3000:])
    if err:
        print("ERR", err[-1000:])
elif mode == "channellog":
    rc, out, err = run(["channel", "log"], timeout=120)
    print("RC", rc)
    print(out[-3000:])
elif mode == "status":
    rc, out, err = run(["channel", "status"], timeout=120)
    print("RC", rc)
    print(out[-2000:])
