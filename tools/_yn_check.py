import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from younavi_bridge import YouNavi

yn = YouNavi()
out = {}

auth = yn.auth_me()
out["auth_ok"] = auth.get("ok")
out["auth_data"] = auth.get("data")

tl = yn.task_list()
rows = []
d = tl.get("data") or {}
if isinstance(d, dict):
    rows = d.get("data") or []
out["task_count"] = len(rows)
tasks = []
for t in rows:
    tasks.append({
        "created": t.get("created_at"),
        "type": t.get("task_type"),
        "status": t.get("status"),
        "msg": (t.get("command_message") or "")[:120],
    })
tasks.sort(key=lambda x: x.get("created") or "")
out["tasks_latest5"] = tasks[-5:]

fl = yn.file_list()
fd = (fl.get("data") or {})
frows = fd.get("data") if isinstance(fd, dict) else fd
if isinstance(frows, dict):
    frows = frows.get("files") or frows.get("data") or []
if not isinstance(frows, list):
    frows = []
out["file_raw"] = frows[:3]
out["file_count"] = len(frows)

dl = yn.dir_list()
out["dir_list"] = dl.get("data")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_yn_check.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("done")
