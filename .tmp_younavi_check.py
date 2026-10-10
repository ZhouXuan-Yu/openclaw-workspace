# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Users\ZhouXuan\.openclaw\workspace\tools")
from younavi_bridge import YouNavi

yn = YouNavi()

def data_of(res):
    d = res.get("data") or {}
    return d.get("data")

tasks = data_of(yn.task_list()) or []
files = data_of(yn.file_list()) or []

from collections import Counter
print("TASKS:", len(tasks))
print("status:", dict(Counter(t.get("status") for t in tasks)))
print("types:", dict(Counter(t.get("task_type") for t in tasks)))
print()
print("--- tasks sorted by created_at (latest 15) ---")
for t in sorted(tasks, key=lambda x: x.get("created_at") or "", reverse=True)[:15]:
    cmd = (t.get("command_message") or "").replace("\n", " ")[:70]
    print(t.get("created_at"), "|", t.get("status"), "|", t.get("task_type"), "|", cmd)
print()
print("FILES:", len(files))
print("types:", dict(Counter(f.get("file_type") for f in files)))
print("sources:", dict(Counter(f.get("source") for f in files)))
print()
print("--- files sorted by created_at (latest 25) ---")
for f in sorted(files, key=lambda x: x.get("created_at") or "", reverse=True)[:25]:
    print(f.get("created_at"), "|", f.get("file_type"), "|", f.get("source"), "|", f.get("name"))
print()
print("--- audio-ish files ---")
for f in files:
    ft = (f.get("file_type") or "").lower()
    nm = (f.get("name") or "").lower()
    if ft in ("audio","mp3","m4a","wav","aac","amr","opus","flac") or any(nm.endswith(e) for e in (".mp3",".m4a",".wav",".aac",".amr",".opus",".flac")):
        print(f.get("created_at"), "|", ft, "|", f.get("name"), "|", f.get("absolute_path"))
