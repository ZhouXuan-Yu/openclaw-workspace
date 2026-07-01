"""查找剩余目录的实际文件名"""
import requests, time

repo = "x1xhlol/system-prompts-and-models-of-ai-tools"
headers = {"Accept": "application/vnd.github.v3+json"}

dirs_to_check = [
    "Cursor Prompts", "Qoder", "Comet Assistant", "Cluely", "Poke",
    "Lovable", "Leap.new", "Orchids.app", "Xcode", "CodeBuddy Prompts", "Z.ai Code"
]

for d in dirs_to_check:
    # 用 tree API
    url = f"https://api.github.com/repos/{repo}/git/trees/main?recursive=1"
    break

# 一次性获取整个树
print("Fetching repo tree...", flush=True)
r = requests.get(url, headers=headers, timeout=15)
print(f"Status: {r.status_code}", flush=True)

if r.status_code == 200:
    tree = r.json().get("tree", [])
    for d in dirs_to_check:
        prefix = d + "/"
        files = [t["path"] for t in tree if t["path"].startswith(prefix) and t["type"] == "blob"]
        print(f"\n{d}:", flush=True)
        for f in files:
            print(f"  {f}", flush=True)
elif r.status_code == 403:
    # Rate limited, try web
    print("Rate limited, trying web...", flush=True)
    for d in dirs_to_check:
        print(f"\n{d}: (check manually)", flush=True)
else:
    print(r.text[:200], flush=True)
