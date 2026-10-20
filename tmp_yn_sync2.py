import sys, io, json, os
from tools.younavi_bridge import YouNavi
yn = YouNavi()

out = {}
out["all"] = yn.channel_sync_all()
for ch in ["tencent_meeting", "feishu_miaoji", "dingding_shanji", "plaud", "plaudcn"]:
    out[ch] = yn.channel_sync(ch)

def summarize(r):
    if not isinstance(r, dict):
        return r
    d = r.get("data")
    if isinstance(d, dict):
        msg = d.get("message")
        inner = d.get("data")
        if isinstance(inner, list):
            inner = f"<list len={len(inner)}>"
        elif isinstance(inner, dict):
            keys = list(inner.keys())
            inner = f"<dict keys={keys}>"
        return {"ok": r.get("ok"), "rc": r.get("rc"), "msg": msg, "inner": inner, "err": r.get("stderr")}
    return r

summary = {k: summarize(v) for k, v in out.items()}
with open("tmp_yn_sync_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print("done")
