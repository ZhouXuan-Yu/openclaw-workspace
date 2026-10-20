#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Summarize YouNavi task_list / file_list without dumping full payload."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from younavi_bridge import YouNavi

yn = YouNavi()
mode = sys.argv[1] if len(sys.argv) > 1 else "both"

def p(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

if mode in ("tasks", "both"):
    r = yn.task_list()
    d = r.get("data") or {}
    tasks = (d.get("data") or {}).get("tasks") if isinstance(d.get("data"), dict) else d.get("data")
    if not isinstance(tasks, list):
        # try other shapes
        tasks = (d.get("data") or {}).get("items") or []
    tasks = tasks or []
    print("=== TASKS ===")
    print("count:", len(tasks))
    def key(t): return t.get("created_at") or ""
    for t in sorted(tasks, key=key, reverse=True)[:6]:
        print(f"{t.get('created_at')} | {t.get('task_type')} | {t.get('status')} | {str(t.get('command_message'))[:80]}")

if mode in ("files", "both"):
    r = yn.file_list()
    d = r.get("data") or {}
    inner = d.get("data") if isinstance(d.get("data"), dict) else {}
    files = inner.get("files") if isinstance(inner, dict) else None
    if files is None:
        files = d.get("files") if isinstance(d, dict) else []
    files = files or []
    print("=== FILES ===")
    print("count:", len(files))
    def fkey(f): return f.get("created_at") or ""
    for f in sorted(files, key=fkey, reverse=True)[:10]:
        print(f"{f.get('created_at')} | {f.get('source')}/{f.get('source_info')} | {f.get('file_type')} | {str(f.get('name'))[:70]}")

if mode in ("audio", "both"):
    r = yn.file_list()
    d = r.get("data") or {}
    inner = d.get("data") if isinstance(d.get("data"), dict) else {}
    files = (inner.get("files") if isinstance(inner, dict) else None) or []
    print("=== AUDIO ===")
    aud = [f for f in files if (f.get("file_type") in ("m4a","mp3","wav","aac","flac","amr","ogg","m4b"))]
    for f in sorted(aud, key=lambda x: x.get("created_at") or "", reverse=True)[:10]:
        print(f"{f.get('created_at')} | {f.get('name')}")
