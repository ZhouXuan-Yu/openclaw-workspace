import json, sys
sys.path.insert(0, r"C:\Users\ZhouXuan\.openclaw\workspace\tools")
from younavi_bridge import YouNavi
yn = YouNavi()
tl = yn.task_list()
rows = (tl.get("data") or {}).get("data") or []
out = []
for t in rows:
    out.append({
        "id": t.get("task_id"),
        "type": t.get("task_type"),
        "status": t.get("status"),
        "msg": (t.get("command_message") or "")[:80],
        "created": t.get("created_at"),
        "err": t.get("error_message"),
    })
open(r"C:\Users\ZhouXuan\.openclaw\workspace\.tmp_tasks.json","w",encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
fl = yn.file_list()
open(r"C:\Users\ZhouXuan\.openclaw\workspace\.tmp_files.json","w",encoding="utf-8").write(json.dumps(fl.get("data"), ensure_ascii=False, indent=1)[:8000])
print("tasks:", len(out))
