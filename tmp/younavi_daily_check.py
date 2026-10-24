import sys, os, json, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from younavi_bridge import YouNavi

yn = YouNavi()
out = {}

# --- tasks ---
r = yn.task_list()
tasks = (r.get("data") or {}).get("tasks") or (r.get("data") or {}).get("items") or []
if isinstance(r.get("data"), dict):
    for k in ("tasks", "list", "data"):
        if k in r["data"] and isinstance(r["data"][k], list):
            tasks = r["data"][k]
            break
recent = []
for t in tasks:
    ca = (t.get("created_at") or "")[:10]
    recent.append({
        "created": ca,
        "status": t.get("status"),
        "cmd": (t.get("command_message") or "")[:60].replace("\n", " "),
    })
recent.sort(key=lambda x: x["created"], reverse=True)
out["task_total"] = len(tasks)
out["tasks_recent"] = recent[:12]

# --- files ---
r2 = yn.file_list()
files = []
d = r2.get("data")
if isinstance(d, dict):
    for k in ("files", "list", "items", "data"):
        if isinstance(d.get(k), list):
            files = d[k]
            break
elif isinstance(d, list):
    files = d
audio_ext = (".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg", ".amr", ".mp4")
au = [f for f in files if (f.get("file_type") or "").lower() in [e.strip(".") for e in audio_ext]
      or os.path.splitext(f.get("name") or "")[1].lower() in audio_ext]
au.sort(key=lambda f: f.get("modified_at") or "", reverse=True)
out["file_total"] = len(files)
out["audio_recent"] = [{"name": f.get("name"), "mod": (f.get("modified_at") or "")[:19],
                        "size": f.get("size"), "abs": f.get("absolute_path")} for f in au[:10]]
newest = sorted(files, key=lambda f: f.get("modified_at") or "", reverse=True)[:8]
out["files_newest"] = [{"name": f.get("name"), "mod": (f.get("modified_at") or "")[:19],
                        "src": f.get("channel_name")} for f in newest]

print(json.dumps(out, ensure_ascii=False, indent=2))
