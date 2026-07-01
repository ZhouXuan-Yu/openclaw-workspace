"""快速测试：外贸关键词扫描"""
import requests, time, json, re, sys
from datetime import datetime

headers = {"Accept": "application/vnd.github.v3.text-match+json"}

queries = [
    '"外贸" "OPENAI_API_KEY"',
    '"外贸" "DEEPSEEK_API_KEY"',
    '"外贸" "API_KEY="',
    '"waimao" "OPENAI_API_KEY"',
    '"waimao" "API_KEY"',
    '"外贸" "sk-"',
    '"外贸" "ANTHROPIC_API_KEY"',
    '"外贸" "MOONSHOT_API_KEY"',
]

provider_map = {
    "OPENAI_API_KEY": ("OpenAI", r"sk-[A-Za-z0-9]{20,}"),
    "DEEPSEEK_API_KEY": ("DeepSeek", r"sk-[a-f0-9]{20,}"),
    "ANTHROPIC_API_KEY": ("Anthropic", r"sk-ant-[A-Za-z0-9\-]{20,}"),
    "MOONSHOT_API_KEY": ("Moonshot/Kimi", r"sk-[a-zA-Z0-9]{20,}"),
    "DASHSCOPE_API_KEY": ("阿里云DashScope", r"sk-[a-f0-9]{20,}"),
    "ZHIPUAI_API_KEY": ("智谱AI", r"[a-f0-9]{32}\.[a-zA-Z0-9]{20,}"),
    "QWEN_API_KEY": ("通义千问", r"sk-[a-f0-9]{20,}"),
    "SILICONFLOW_API_KEY": ("SiliconFlow", r"sk-[a-zA-Z0-9]{20,}"),
}

placeholders = ["your_key", "xxxx", "placeholder", "example", "test", "dummy", "fake", "sample", "insert", "replace", "changeme", "sk-xxx", "TODO", "PASTE", "ENTER", "PUT_YOUR"]

results = []
seen = set()

def is_placeholder(v):
    lower = v.lower()
    return any(p.lower() in lower for p in placeholders)

def detect_provider(text):
    for key, (name, regex) in provider_map.items():
        if key in text:
            return name, regex
    # fallback
    if "sk-ant-" in text:
        return "Anthropic", r"sk-ant-[A-Za-z0-9\-]{20,}"
    if "sk-" in text:
        return "Unknown(sk-)", r"sk-[A-Za-z0-9]{20,}"
    return None, None

for qi, q in enumerate(queries):
    print(f"\n[{qi+1}/{len(queries)}] 查询: {q}")
    try:
        r = requests.get("https://api.github.com/search/code", headers=headers, params={"q": q, "per_page": 10}, timeout=15)
    except Exception as e:
        print(f"  请求失败: {e}")
        time.sleep(6)
        continue

    if r.status_code == 403:
        reset = int(r.headers.get("X-RateLimit-Reset", 0))
        wait = max(reset - int(time.time()), 10)
        print(f"  限速，等待 {wait}s")
        time.sleep(wait)
        # retry once
        try:
            r = requests.get("https://api.github.com/search/code", headers=headers, params={"q": q, "per_page": 10}, timeout=15)
        except:
            time.sleep(6)
            continue

    if r.status_code != 200:
        print(f"  状态 {r.status_code}: {r.text[:150]}")
        time.sleep(6)
        continue

    data = r.json()
    total = data.get("total_count", 0)
    items = data.get("items", [])
    print(f"  总命中: {total}, 本页: {len(items)}")

    for item in items:
        repo = item["repository"]["full_name"]
        path = item["path"]
        html_url = item.get("html_url", "")
        owner = item["repository"]["owner"]["login"]
        is_private = item["repository"].get("private", False)

        dedup = f"{repo}|{path}"
        if dedup in seen:
            continue
        seen.add(dedup)

        # 从 text_matches 提取片段
        fragments = ""
        for tm in item.get("text_matches", []):
            fragments += tm.get("fragment", "") + "\n"

        provider, regex = detect_provider(fragments)
        if not provider:
            continue

        keys = re.findall(regex, fragments)
        keys = [k for k in keys if not is_placeholder(k)]

        if keys:
            for key in keys:
                masked = key[:8] + "..." + key[-4:] if len(key) > 16 else key[:4] + "..."
                results.append({
                    "provider": provider,
                    "repo": repo,
                    "owner": owner,
                    "path": path,
                    "key_preview": masked,
                    "file_url": html_url,
                    "private": is_private,
                })
                print(f"  ✅ {provider} | {repo}/{path} | {masked}")
        else:
            # 片段里有关键词但没提取到密钥，也记录一下
            if provider:
                print(f"  ⚠️ {provider} 命中但未提取到密钥: {repo}/{path}")

    time.sleep(6)

print(f"\n{'='*50}")
print(f"扫描完成: {len(results)} 个疑似密钥暴露")
for r in results:
    print(f"  {r['provider']:20s} | {r['repo']:30s} | {r['key_preview']}")

# 保存 JSON 供后续生成 Excel
with open("scan_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n结果已保存 scan_results.json")
