import json, sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from younavi_bridge import YouNavi

yn = YouNavi()
t = yn.task_list()
d = (t.get("data") or {}).get("data")
tasks = []
if isinstance(d, dict):
    tasks = d.get("tasks") or d.get("items") or d.get("list") or []
elif isinstance(d, list):
    tasks = d

# audio-like files
f = yn.file_list()
fd = (f.get("data") or {}).get("data")
files = []
if isinstance(fd, dict):
    files = fd.get("files") or fd.get("items") or fd.get("list") or []
elif isinstance(fd, list):
    files = fd

print("TASKS:", len(tasks))
rows = []
for x in tasks:
    ca = x.get("created_at") or ""
    rows.append((ca, x.get("task_id"), x.get("task_type"), x.get("status"), (x.get("command_message") or "")[:60]))
rows.sort(reverse=True)
for r in rows[:12]:
    print(" | ".join(str(y) for y in r))

print("\nFILES:", len(files))
frows = []
for x in files:
    ca = x.get("created_at") or ""
    frows.append((ca, x.get("file_type"), x.get("name"), x.get("absolute_path")))
frows.sort(reverse=True)
for r in frows[:15]:
    print(" | ".join(str(y) for y in r))

# audio files list
audio = [x for x in files if (x.get("file_type") or "").lower() in ("m4a","mp3","wav","aac","amr","mp4")]
print("\nAUDIO FILES:", len(audio))
for x in audio[:15]:
    print(x.get("created_at"), x.get("name"))
