"""拉取关键 System Prompt 文件"""
import requests, base64, json, os

repo = "x1xhlol/system-prompts-and-models-of-ai-tools"
out_dir = "prompts_dump"
os.makedirs(out_dir, exist_ok=True)

files_to_fetch = [
    ("Claude Code", "Prompt.txt"),
    ("Cursor Prompts", "Prompt.txt"),
    ("Devin AI", "Prompt.txt"),
    ("Manus Agent Tools & Prompt", "Prompt.txt"),
    ("Manus Agent Tools & Prompt", "Agent loop.txt"),
    ("Manus Agent Tools & Prompt", "Modules.txt"),
    ("VSCode Agent", "Prompt.txt"),
    ("Windsurf", "Prompt Wave 11.txt"),
    ("Trae", "Builder Prompt.txt"),
    ("Kiro", "Vibe_Prompt.txt"),
    ("Kiro", "Spec_Prompt.txt"),
    ("Replit", "Prompt.txt"),
    ("Augment Code", "claude-4-sonnet-agent-prompts.txt"),
]

for folder, filename in files_to_fetch:
    path = f"{folder}/{filename}"
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("encoding") == "base64":
                content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
                safe_name = folder.replace(" ", "_") + "__" + filename.replace(" ", "_")
                out_path = os.path.join(out_dir, safe_name)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"OK {path} -> {len(content)} chars")
            else:
                print(f"SKIP {path} (encoding: {data.get('encoding')})")
        else:
            print(f"FAIL {path} ({r.status_code})")
    except Exception as e:
        print(f"ERR {path}: {e}")

print("\nDone!")
