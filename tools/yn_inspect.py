#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from younavi_bridge import YouNavi
yn = YouNavi()
r = yn.file_list()
d = r.get("data")
print("top ok:", r.get("ok"), "rc:", r.get("rc"))
print("data type:", type(d))
if isinstance(d, dict):
    print("data keys:", list(d.keys()))
    inner = d.get("data")
    print("inner type:", type(inner))
    if isinstance(inner, dict):
        print("inner keys:", list(inner.keys()))
        for k, v in inner.items():
            if isinstance(v, list):
                print(f"  list {k}: len={len(v)}")
    elif isinstance(inner, list):
        print("inner list len:", len(inner))
