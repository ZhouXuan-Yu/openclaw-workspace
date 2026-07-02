"""测试 GitHub 扫描到的 Gemini 密钥是否可用"""
import json, requests, warnings, time
warnings.filterwarnings("ignore")

HISTORY = r"C:\Users\ZhouXuan\.openclaw\workspace\tools\github-key-scanner\scan_history.json"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

with open(HISTORY, encoding="utf-8") as f:
    data = json.load(f)

# 取 Gemini 密钥
gemini_keys = []
for k, v in data.get("seen_keys", {}).items():
    if v.get("provider") == "Google Gemini":
        gemini_keys.append(v["key_full"])

print(f"共 {len(gemini_keys)} 个 Gemini 密钥，测试前 10 个...\n")

valid = []
for i, key in enumerate(gemini_keys[10:30], 11):
    try:
        r = requests.post(
            f"{API_URL}?key={key}",
            json={"contents": [{"parts": [{"text": "Say hello in one word"}]}]},
            timeout=15, verify=False
        )
        if r.status_code == 200:
            valid.append(key)
            print(f"  [{i}] ✅ 有效  {key[:12]}...{key[-4:]}")
        elif r.status_code == 403:
            print(f"  [{i}] 🔒 403 (权限不足/配额用完)  {key[:12]}...{key[-4:]}")
        elif r.status_code == 400:
            print(f"  [{i}] ❌ 400 (无效密钥)  {key[:12]}...{key[-4:]}")
        else:
            print(f"  [{i}] ❓ {r.status_code}  {key[:12]}...{key[-4:]}")
    except Exception as e:
        print(f"  [{i}] ⚠️ 连接失败  {key[:12]}...{key[-4:]}: {e}")
    time.sleep(0.3)

print(f"\n{'='*50}")
print(f"结果: {len(valid)}/{len(gemini_keys[:10])} 个有效")
if valid:
    print(f"\n可用密钥:")
    for k in valid:
        print(f"  export GEMINI_API_KEY={k}")
