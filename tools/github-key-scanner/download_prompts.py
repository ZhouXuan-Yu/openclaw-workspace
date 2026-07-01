"""
批量下载 GitHub 仓库中的 System Prompt 文件，按分类存入 Obsidian Vault
"""
import requests, base64, os, time

repo = "x1xhlol/system-prompts-and-models-of-ai-tools"
base_dir = r"E:\Obsidian仓库\ZhouXuan私人领域\prompt学习提示词\AI工具SystemPrompt"

# 分类定义
categories = {
    "01_编程Agent": [
        ("Devin AI", "Prompt.txt"),
        ("Cursor Prompts", "Prompt.txt"),
        ("Windsurf", "Prompt Wave 11.txt"),
        ("Windsurf", "Tools Wave 11.txt"),
        ("Trae", "Builder Prompt.txt"),
        ("Trae", "Chat Prompt.txt"),
        ("Trae", "Builder Tools.json"),
        ("VSCode Agent", "Prompt.txt"),
        ("Kiro", "Vibe_Prompt.txt"),
        ("Kiro", "Spec_Prompt.txt"),
        ("Kiro", "Mode_Clasifier_Prompt.txt"),
        ("Augment Code", "claude-4-sonnet-agent-prompts.txt"),
        ("Augment Code", "gpt-5-agent-prompts.txt"),
        ("Replit", "Prompt.txt"),
        ("Replit", "Tools.json"),
        ("Qoder", "Prompt.txt"),
    ],
    "02_通用Agent": [
        ("Manus Agent Tools & Prompt", "Prompt.txt"),
        ("Manus Agent Tools & Prompt", "Agent loop.txt"),
        ("Manus Agent Tools & Prompt", "Modules.txt"),
        ("Manus Agent Tools & Prompt", "tools.json"),
        ("Comet Assistant", "Prompt.txt"),
        ("Cluely", "Prompt.txt"),
        ("Poke", "Prompt.txt"),
    ],
    "03_应用生成": [
        ("v0 Prompts and Tools", "Prompt.txt"),
        ("Lovable", "Prompt.txt"),
        ("Leap.new", "Prompt.txt"),
        ("Same.dev", "Prompt.txt"),
        ("Orchids.app", "Prompt.txt"),
    ],
    "04_搜索研究": [
        ("Perplexity", "Prompt.txt"),
    ],
    "05_代码补全": [
        ("Xcode", "Prompt.txt"),
        ("Junie", "Prompt.txt"),
        ("CodeBuddy Prompts", "Prompt.txt"),
    ],
    "06_其他": [
        ("NotionAi", "Prompt.txt"),
        ("Warp.dev", "Prompt.txt"),
        ("Z.ai Code", "Prompt.txt"),
        ("dia", "Prompt.txt"),
        ("Emergent", "Prompt.txt"),
    ],
}

headers = {"Accept": "application/vnd.github.v3+json"}
stats = {"ok": 0, "fail": 0, "skip": 0}

for cat_name, files in categories.items():
    cat_dir = os.path.join(base_dir, cat_name)
    os.makedirs(cat_dir, exist_ok=True)
    
    for folder, filename in files:
        path = f"{folder}/{filename}"
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code != 200:
                print(f"FAIL {path} ({r.status_code})")
                stats["fail"] += 1
                continue
            
            data = r.json()
            if data.get("encoding") != "base64":
                print(f"SKIP {path} (encoding: {data.get('encoding')})")
                stats["skip"] += 1
                continue
            
            content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
            
            # 文件名处理：用 文件夹名__原文件名 避免冲突
            safe_name = folder.replace(" ", "_").replace("&", "and") + "__" + filename.replace(" ", "_")
            out_path = os.path.join(cat_dir, safe_name)
            
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"OK   {path} -> {cat_name}/{safe_name} ({len(content)} chars)")
            stats["ok"] += 1
            
        except Exception as e:
            print(f"ERR  {path}: {e}")
            stats["fail"] += 1
        
        time.sleep(1)

print(f"\nDone! OK={stats['ok']} Fail={stats['fail']} Skip={stats['skip']}")
