"""全量测试并标记 Gemini 密钥有效性"""
import json, requests, warnings, time
warnings.filterwarnings("ignore")

HISTORY = r"C:\Users\ZhouXuan\.openclaw\workspace\tools\github-key-scanner\scan_history.json"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

with open(HISTORY, encoding="utf-8") as f:
    data = json.load(f)

sk = data["seen_keys"]
gemini_keys = {k: v for k, v in sk.items() if v.get("provider") == "Google Gemini"}

print(f"测试 {len(gemini_keys)} 个 Gemini 密钥...\n")
valid, invalid, quota = 0, 0, 0

for idx, (kid, info) in enumerate(gemini_keys.items(), 1):
    key = info["key_full"]
    try:
        r = requests.post(
            f"{API_URL}?key={key}",
            json={"contents": [{"parts": [{"text": "hi"}]}]},
            timeout=12, verify=False
        )
        if r.status_code == 200:
            info["verified"] = "valid"
            valid += 1
            print(f"  [{idx}/{len(gemini_keys)}] ✅ {key[:16]}...{key[-4:]}")
        elif r.status_code == 403 or r.status_code == 429:
            info["verified"] = "quota"
            quota += 1
            print(f"  [{idx}/{len(gemini_keys)}] 🔒 {r.status_code}")
        else:
            info["verified"] = "invalid"
            invalid += 1
            print(f"  [{idx}/{len(gemini_keys)}] ❌ {r.status_code}", end="\r")
    except Exception as e:
        info["verified"] = "error"
        invalid += 1
        print(f"  [{idx}/{len(gemini_keys)}] ⚠️ {e}", end="\r")
    time.sleep(0.15)

# save
with open(HISTORY, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"总计: {len(gemini_keys)} | ✅ 有效:{valid} | 🔒 限额:{quota} | ❌ 失效:{invalid}")
