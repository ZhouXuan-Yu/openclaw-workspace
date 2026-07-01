"""用 Token 查找失败文件并下载 (修复编码)"""
import requests, base64, os, time

repo = "x1xhlol/system-prompts-and-models-of-ai-tools"
base_dir = r"E:\Obsidian仓库\ZhouXuan私人领域\prompt学习提示词\AI工具SystemPrompt"
GITHUB_TOKEN = "github\u20268f5J"

# 尝试不同 token 格式
tokens_to_try = [
    GITHUB_TOKEN,
    GITHUB_TOKEN.replace("\u2026", ""),
    GITHUB_TOKEN.replace("\u2026", "..."),
]

# 先测试哪个 token 能用
working_token = None
for tk in tokens_to_try:
    try:
        h = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {tk}"}
        r = requests.get("https://api.github.com/user", headers=h, timeout=10)
        print(f"Token '{tk[:10]}...' -> {r.status_code}", flush=True)
        if r.status_code == 200:
            working_token = tk
            break
    except Exception as e:
        print(f"Token '{tk[:10]}...' -> ERR: {e}", flush=True)

if not working_token:
    # 用无 token 方式（限速但能用）
    print("No valid token, using unauthenticated (rate limited)", flush=True)
    headers = {"Accept": "application/vnd.github.v3+json"}
else:
    print(f"Using token: {working_token[:10]}...", flush=True)
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {working_token}"}

failed_map = {
    "Cursor Prompts": ("01_编程Agent", "Cursor"),
    "Qoder": ("01_编程Agent", "Qoder"),
    "Comet Assistant": ("02_通用Agent", "Comet"),
    "Cluely": ("02_通用Agent", "Cluely"),
    "Poke": ("02_通用Agent", "Poke"),
    "Lovable": ("03_应用生成", "Lovable"),
    "Leap.new": ("03_应用生成", "Leap_new"),
    "Orchids.app": ("03_应用生成", "Orchids"),
    "Xcode": ("05_代码补全", "Xcode"),
    "CodeBuddy Prompts": ("05_代码补全", "CodeBuddy"),
    "Z.ai Code": ("06_其他", "Z_ai_Code"),
}

stats = {"ok": 0, "fail": 0}

for d, (cat, prefix) in failed_map.items():
    cat_dir = os.path.join(base_dir, cat)
    os.makedirs(cat_dir, exist_ok=True)
    
    print(f"\n{d} -> {cat}/", flush=True)
    try:
        r = requests.get(f"https://api.github.com/repos/{repo}/contents/{d}", headers=headers, timeout=15)
        if r.status_code == 403:
            reset = int(r.headers.get("X-RateLimit-Reset", 0))
            wait = max(reset - int(time.time()), 10)
            print(f"  Rate limited, waiting {wait}s...", flush=True)
            time.sleep(wait + 1)
            r = requests.get(f"https://api.github.com/repos/{repo}/contents/{d}", headers=headers, timeout=15)
        
        if r.status_code != 200:
            print(f"  LIST FAIL: {r.status_code}", flush=True)
            stats["fail"] += 1
            continue
        
        for f in r.json():
            name = f["name"]
            if not (name.endswith(".txt") or name.endswith(".json") or name.endswith(".md")):
                continue
            
            fr = requests.get(f["url"], headers=headers, timeout=15)
            if fr.status_code != 200:
                print(f"  FAIL {name} ({fr.status_code})", flush=True)
                stats["fail"] += 1
                continue
            
            fdata = fr.json()
            if fdata.get("encoding") != "base64":
                print(f"  SKIP {name}", flush=True)
                continue
            
            content = base64.b64decode(fdata["content"]).decode("utf-8", errors="ignore")
            safe_name = prefix + "__" + name.replace(" ", "_")
            out_path = os.path.join(cat_dir, safe_name)
            
            with open(out_path, "w", encoding="utf-8") as fp:
                fp.write(content)
            
            print(f"  OK   {name} -> {safe_name} ({len(content)} chars)", flush=True)
            stats["ok"] += 1
            time.sleep(1)
    
    except Exception as e:
        print(f"  ERR: {e}", flush=True)
        stats["fail"] += 1
    
    time.sleep(2)

print(f"\nDone! OK={stats['ok']} Fail={stats['fail']}", flush=True)
