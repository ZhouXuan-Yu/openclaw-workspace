"""从 raw URL 直接下载剩余文件"""
import requests, os, time

base_dir = r"E:\Obsidian仓库\ZhouXuan私人领域\prompt学习提示词\AI工具SystemPrompt"
raw_base = "https://raw.githubusercontent.com/x1xhlol/system-prompts-and-models-of-ai-tools/main"

# 剩余文件：raw_url -> (分类, 输出文件名)
remaining = {
    f"{raw_base}/Cursor%20Prompts/Prompt.txt": ("01_编程Agent", "Cursor__Prompt.txt"),
    f"{raw_base}/Qoder/Prompt.txt": ("01_编程Agent", "Qoder__Prompt.txt"),
    f"{raw_base}/Comet%20Assistant/Prompt.txt": ("02_通用Agent", "Comet__Prompt.txt"),
    f"{raw_base}/Cluely/Prompt.txt": ("02_通用Agent", "Cluely__Prompt.txt"),
    f"{raw_base}/Poke/Prompt.txt": ("02_通用Agent", "Poke__Prompt.txt"),
    f"{raw_base}/Lovable/Prompt.txt": ("03_应用生成", "Lovable__Prompt.txt"),
    f"{raw_base}/Leap.new/Prompt.txt": ("03_应用生成", "Leap_new__Prompt.txt"),
    f"{raw_base}/Orchids.app/Prompt.txt": ("03_应用生成", "Orchids__Prompt.txt"),
    f"{raw_base}/Xcode/Prompt.txt": ("05_代码补全", "Xcode__Prompt.txt"),
    f"{raw_base}/CodeBuddy%20Prompts/Prompt.txt": ("05_代码补全", "CodeBuddy__Prompt.txt"),
    f"{raw_base}/Z.ai%20Code/Prompt.txt": ("06_其他", "Z_ai_Code__Prompt.txt"),
}

stats = {"ok": 0, "fail": 0}

for url, (cat, fname) in remaining.items():
    cat_dir = os.path.join(base_dir, cat)
    os.makedirs(cat_dir, exist_ok=True)
    out_path = os.path.join(cat_dir, fname)
    
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"OK   {fname} ({len(r.text)} chars)", flush=True)
            stats["ok"] += 1
        else:
            print(f"FAIL {fname} ({r.status_code})", flush=True)
            stats["fail"] += 1
    except Exception as e:
        print(f"ERR  {fname}: {e}", flush=True)
        stats["fail"] += 1
    time.sleep(1)

print(f"\nDone! OK={stats['ok']} Fail={stats['fail']}", flush=True)
