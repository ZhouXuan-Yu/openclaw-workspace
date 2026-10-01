import subprocess, json, os, sys

CLI = r"D:\YouNavi\resources\backend\agent-cli.exe"
env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"
env["PYTHONUTF8"] = "1"

def run(args, timeout=90):
    try:
        r = subprocess.run([CLI, "-f", "json"] + args, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env, timeout=timeout)
        out = r.stdout.strip()
        try:
            return json.loads(out)
        except Exception:
            return {"raw": out, "rc": r.returncode}
    except Exception as e:
        return {"error": str(e)}

print("=== CHANNEL FILES ===")
d = run(["channel", "files", "--all"])
if isinstance(d, dict) and d.get("data"):
    files = d["data"]
    print("total:", len(files))
    for f in files:
        print(f"- {f.get('channel_name')} | {f.get('created_at')} | {f.get('file_type')} | {f.get('size')} | {f.get('name')}")
else:
    print(json.dumps(d, ensure_ascii=False)[:800])

print("\n=== TASKS (recent) ===")
d = run(["task", "list"])
if isinstance(d, dict) and d.get("data"):
    tasks = d["data"].get("tasks", d["data"]) if isinstance(d["data"], dict) else d["data"]
    if isinstance(tasks, dict):
        tasks = tasks.get("tasks", [])
    print("total:", len(tasks))
    rows = sorted(tasks, key=lambda t: t.get("created_at", ""), reverse=True)[:15]
    for t in rows:
        print(f"- {t.get('created_at')} | {t.get('task_type')} | {t.get('status')} | {str(t.get('command_message'))[:60]}")
else:
    print(json.dumps(d, ensure_ascii=False)[:800])
