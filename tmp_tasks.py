from tools.younavi_bridge import YouNavi
import json
yn = YouNavi()
r = yn.task_list()
d = r.get("data")
items = d.get("data") if isinstance(d, dict) else None
if isinstance(items, dict):
    items = items.get("tasks") or items.get("items") or []
tasks = items or []
print("total:", len(tasks))
for t in tasks[:8]:
    print("-", t.get("created_at"), t.get("task_type"), t.get("status"), (t.get("command_message") or "")[:60].replace("\n"," "))
