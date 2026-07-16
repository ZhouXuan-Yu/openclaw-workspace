#!/usr/bin/env python3
"""Debug YouNavi connection"""
from tools.younavi_bridge import YouNavi
import json, os

yn = YouNavi()

# Test auth
print("=== auth_me ===")
r = yn.auth_me()
print(f"ok={r.get('ok')}, rc={r.get('rc')}")
if r.get('data'):
    if isinstance(r['data'], dict):
        print(f"  msg={r['data'].get('message','')[:200]}")
        if 'data' in r['data']:
            print(f"  data present: {type(r['data']['data'])}")
    else:
        print(f"  raw data type: {type(r['data'])}")
        print(f"  data[:200]: {str(r['data'])[:200]}")

# Try with explicit error handling
print("\n=== convo_list ===")
try:
    r2 = yn.convo_list()
    print(f"Full response: {json.dumps(r2, ensure_ascii=False)[:500]}")
except Exception as e:
    print(f"Exception: {e}")
