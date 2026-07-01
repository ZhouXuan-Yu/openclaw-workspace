"""查看各目录下的文件列表"""
import requests, sys

repo = "x1xhlol/system-prompts-and-models-of-ai-tools"
dirs = [
    "Claude Code",  # Anthropic
    "Cursor Prompts",
    "Devin AI",
    "Manus Agent Tools & Prompt",
    "VSCode Agent",
    "Windsurf",
    "Trae",
    "Kiro",
    "Augment Code",
    "Replit",
]

for d in dirs:
    print(f"\n{'='*50}")
    print(f"📁 {d}")
    print('='*50)
    try:
        r = requests.get(f"https://api.github.com/repos/{repo}/contents/{d}", timeout=10)
        if r.status_code == 200:
            for item in r.json():
                t = 'DIR' if item['type'] == 'dir' else 'FILE'
                size = item.get('size', 0)
                print(f"  {t} {item['name']} ({size} bytes)")
        else:
            print(f"  状态: {r.status_code}")
    except Exception as e:
        print(f"  异常: {e}")
