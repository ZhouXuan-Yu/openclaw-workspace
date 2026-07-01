"""用 Token 查找失败文件并下载"""
import requests, base64, os, time

repo = "x1xhlol/system-prompts-and-models-of-ai-tools"
base_dir = r"E:\Obsidian仓库\ZhouXuan私人领域\prompt学习提示词\AI工具SystemPrompt"
GITHUB_TOKEN = "github…8f5J"
headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {GITHUB_TOKEN}"}

# 失败的目录 → 目标分类
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
        if r.status_code != 200:
            print(f"  LIST FAIL: {r.status_code} {r.text[:100]}", flush=True)
            stats["fail"] += 1
            continue
        
        for f in r.json():
            name = f["name"]
            if not (name.endswith(".txt") or name.endswith(".json") or name.endswith(".md")):
                continue
            
            # 下载文件
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
