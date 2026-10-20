import json, sys
sys.path.insert(0, "tools")
from younavi_bridge import YouNavi
yn = YouNavi(auto_start=True)

out = {}

auth = yn.auth_me()
d = auth.get("data") or {}
out["auth_ok"] = auth.get("ok")
out["user"] = d.get("data", {}).get("user_name") if isinstance(d.get("data"), dict) else d.get("user_name")

tl = yn.task_list()
td = tl.get("data") or {}
tasks = td.get("data", {}).get("tasks") if isinstance(td.get("data"), dict) else None
if tasks is None:
    tasks = td.get("tasks") if isinstance(td, dict) else None
if tasks is None:
    tasks = td if isinstance(td, list) else []
tasks_sorted = sorted(tasks, key=lambda t: t.get("created_at",""), reverse=True)
out["task_count"] = len(tasks)
out["latest_tasks"] = [{"created_at": t.get("created_at"), "type": t.get("task_type"), "status": t.get("status"), "msg": (t.get("command_message") or "")[:70]} for t in tasks_sorted[:5]]

fl = yn.file_list()
fd = fl.get("data") or {}
files = fd.get("data", {}).get("files") if isinstance(fd.get("data"), dict) else None
if files is None:
    files = fd.get("files") if isinstance(fd, dict) else None
if files is None:
    files = fd if isinstance(fd, list) else []
out["file_count"] = len(files)
def fk(f): return f.get("created_at") or f.get("modified") or f.get("updated_at") or ""
fs = sorted(files, key=fk, reverse=True)
out["latest_files"] = [{"created_at": fk(f), "name": (f.get("name") or f.get("file_name") or "")[:70]} for f in fs[:6]]

print(json.dumps(out, ensure_ascii=False, indent=2))
