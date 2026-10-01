import os, sys, time, glob
sys.path.insert(0, os.path.join(os.getcwd(), "tools"))
from younavi_bridge import YouNavi
yn = YouNavi()

# find today's task
r = yn.task_list()
tasks = (r.get("data") or {}).get("data") or []
today = [t for t in tasks if (t.get("created_at") or "").startswith("2026-10-01")]
print("today tasks:", len(today))
for t in today:
    print("task_id:", t.get("task_id"), "|", t.get("task_type"), "|", t.get("status"))
    print("  msg:", (t.get("command_message") or "")[:200].replace("\n", " "))

base = r"C:\Users\ZhouXuan\navi-ai\ZhouXuan_"
for sub in ("navi-records", "transcripts", "rendition"):
    d = os.path.join(base, sub)
    print(f"\n=== {sub} (recent 12) ===")
    if os.path.isdir(d):
        fs = [(os.path.getmtime(os.path.join(d,f)), os.path.join(d,f)) for f in os.listdir(d)]
        fs.sort(reverse=True)
        for m, fp in fs[:12]:
            print(time.strftime("%Y-%m-%d %H:%M", time.localtime(m)), os.path.getsize(fp), fp)

print("\n=== head of newest navi-record ===")
d = os.path.join(base, "navi-records")
if os.path.isdir(d):
    fs = sorted([os.path.join(d,f) for f in os.listdir(d)], key=os.path.getmtime, reverse=True)
    if fs:
        with open(fs[0], encoding="utf-8", errors="replace") as fh:
            print("FILE:", fs[0])
            print(fh.read(1500))
