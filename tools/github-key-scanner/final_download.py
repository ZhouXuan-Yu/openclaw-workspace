"""用 raw URL 批量下载剩余文件（正确文件名）"""
import requests, os, time

base_dir = r"E:\Obsidian仓库\ZhouXuan私人领域\prompt学习提示词\AI工具SystemPrompt"
raw = "https://raw.githubusercontent.com/x1xhlol/system-prompts-and-models-of-ai-tools/main"

files = [
    # 01_编程Agent
    (f"{raw}/Cursor%20Prompts/Agent%20CLI%20Prompt%202025-08-07.txt", "01_编程Agent", "Cursor__Agent_CLI_Prompt.txt"),
    (f"{raw}/Qoder/Quest%20Action.txt", "01_编程Agent", "Qoder__Quest_Action.txt"),
    (f"{raw}/Qoder/Quest%20Design.txt", "01_编程Agent", "Qoder__Quest_Design.txt"),
    # 02_通用Agent
    (f"{raw}/Comet%20Assistant/System%20Prompt.txt", "02_通用Agent", "Comet__System_Prompt.txt"),
    (f"{raw}/Comet%20Assistant/tools.json", "02_通用Agent", "Comet__tools.json"),
    (f"{raw}/Cluely/Default%20Prompt.txt", "02_通用Agent", "Cluely__Default_Prompt.txt"),
    (f"{raw}/Cluely/Enterprise%20Prompt.txt", "02_通用Agent", "Cluely__Enterprise_Prompt.txt"),
    (f"{raw}/Poke/Poke%20agent.txt", "02_通用Agent", "Poke__agent.txt"),
    (f"{raw}/Poke/Poke_p1.txt", "02_通用Agent", "Poke__p1.txt"),
    (f"{raw}/Poke/Poke_p2.txt", "02_通用Agent", "Poke__p2.txt"),
    # 03_应用生成
    (f"{raw}/Lovable/Agent%20Prompt.txt", "03_应用生成", "Lovable__Agent_Prompt.txt"),
    (f"{raw}/Lovable/Agent%20Tools.json", "03_应用生成", "Lovable__Agent_Tools.json"),
    (f"{raw}/Leap.new/Prompts.txt", "03_应用生成", "Leap_new__Prompts.txt"),
    (f"{raw}/Leap.new/tools.json", "03_应用生成", "Leap_new__tools.json"),
    (f"{raw}/Orchids.app/Decision-making%20prompt.txt", "03_应用生成", "Orchids__Decision_making.txt"),
    (f"{raw}/Orchids.app/System%20Prompt.txt", "03_应用生成", "Orchids__System_Prompt.txt"),
    # 05_代码补全
    (f"{raw}/Xcode/DocumentAction.txt", "05_代码补全", "Xcode__DocumentAction.txt"),
    (f"{raw}/Xcode/ExplainAction.txt", "05_代码补全", "Xcode__ExplainAction.txt"),
    (f"{raw}/Xcode/MessageAction.txt", "05_代码补全", "Xcode__MessageAction.txt"),
    (f"{raw}/Xcode/PlaygroundAction.txt", "05_代码补全", "Xcode__PlaygroundAction.txt"),
    (f"{raw}/Xcode/PreviewAction.txt", "05_代码补全", "Xcode__PreviewAction.txt"),
    (f"{raw}/Xcode/System.txt", "05_代码补全", "Xcode__System.txt"),
    (f"{raw}/CodeBuddy%20Prompts/Chat%20Prompt.txt", "05_代码补全", "CodeBuddy__Chat_Prompt.txt"),
    (f"{raw}/CodeBuddy%20Prompts/Craft%20Prompt.txt", "05_代码补全", "CodeBuddy__Craft_Prompt.txt"),
    # 06_其他
    (f"{raw}/Z.ai%20Code/prompt.txt", "06_其他", "Z_ai_Code__prompt.txt"),
]

ok, fail = 0, 0
for url, cat, fname in files:
    cat_dir = os.path.join(base_dir, cat)
    os.makedirs(cat_dir, exist_ok=True)
    out = os.path.join(cat_dir, fname)
    
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            with open(out, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"OK   {cat}/{fname} ({len(r.text)} chars)", flush=True)
            ok += 1
        else:
            print(f"FAIL {fname} ({r.status_code})", flush=True)
            fail += 1
    except Exception as e:
        print(f"ERR  {fname}: {e}", flush=True)
        fail += 1
    time.sleep(0.5)

print(f"\nDone! OK={ok} Fail={fail}", flush=True)
