#!/usr/bin/env python3
"""Temp script to check YouNavi status"""
from tools.younavi_bridge import YouNavi
import json

yn = YouNavi()

# Only check conversations (reliable method)
r = yn.convo_list()
if r.get('ok') and r['data'].get('success'):
    convos = r['data']['data']
    recent = [c for c in convos if '2026-07' in c.get('updated_at','')]
    today = [c for c in convos if '2026-07-08' in c.get('updated_at','')]
    print("July convos:", len(recent))
    for c in recent:
        title = c['title']
        updated = c['updated_at'][:16]
        src = c['source']
        print(f"  [{src}] {title} | {updated}")
    print("Today convos:", len(today))
    for c in today:
        print(f"  [{c['source']}] {c['title']}")
else:
    print("convo_list failed")
