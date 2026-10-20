import json
from tools.younavi_bridge import YouNavi
yn = YouNavi()

full = {}
full["sync_all_raw"] = yn._run(["channel", "sync", "--all"])
full["sync_tc_raw"] = yn._run(["channel", "sync", "--name", "tencent_meeting"])
full["help_channel"] = yn._run(["channel", "--help"])
full["help_sync"] = yn._run(["channel", "sync", "--help"])
full["task_list_fresh"] = yn._run(["task", "list"])

# strip giant task list
tl = full["task_list_fresh"]
d = tl.get("data", {})
if isinstance(d, dict) and isinstance(d.get("data"), list):
    d["data"] = f"<list len={len(d['data'])}>"

with open("tmp_yn_raw.json", "w", encoding="utf-8") as f:
    json.dump(full, f, ensure_ascii=False, indent=2)
print("done")
