import json, sys
sys.path.insert(0, "tools")
from younavi_bridge import YouNavi
yn = YouNavi()
tl = yn.task_list()
d = tl.get("data") or {}
def describe(o, depth=0):
    if isinstance(o, dict):
        return {k: describe(v, depth+1) for k,v in list(o.items())[:12]} if depth<2 else "dict"
    if isinstance(o, list):
        return [f"list[{len(o)}]"] if depth>=2 else ("list["+str(len(o))+"]" if o else "list[0]")
    return type(o).__name__
print(json.dumps(describe(d), ensure_ascii=False, indent=2)[:2000])
