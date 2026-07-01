"""查找失败文件的正确文件名"""
import requests, time

repo = "x1xhlol/system-prompts-and-models-of-ai-tools"
headers = {"Accept": "application/vnd.github.v3+json"}

failed_dirs = [
    "Cursor Prompts", "Qoder", "Comet Assistant", "Cluely", "Poke",
    "Lovable", "Leap.new", "Orchids.app", "Xcode", "CodeBuddy Prompts", "Z.ai Code"
]

for d in failed_dirs:
    try:
        r = requests.get(f"https://api.github.com/repos/{repo}/contents/{d}", headers=headers, timeout=10)
        if r.status_code == 200:
            files = r.json()
            print(f"\n{d}:")
            for f in files:
                print(f"  {f['type']:4s} {f['name']} ({f.get('size', 0)} bytes)")
        else:
            print(f"\n{d}: HTTP {r.status_code}")
    except Exception as e:
        print(f"\n{d}: {e}")
    time.sleep(1)
