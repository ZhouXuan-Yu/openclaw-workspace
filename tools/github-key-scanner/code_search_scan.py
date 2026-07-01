"""
GitHub 代码搜索 - 外贸/跨境关键词密钥扫描 (最终版)
输出：scan_results.json → 供生成 Excel
"""
import requests, time, json, re, sys

GITHUB_TOKEN = sys.argv[1] if len(sys.argv) > 1 else ""
if not GITHUB_TOKEN:
    print("用法: python code_search_scan.py <TOKEN>")
    sys.exit(1)

headers = {
    "Accept": "application/vnd.github.v3.text-match+json",
    "Authorization": f"token {GITHUB_TOKEN}",
}

placeholders = ["your_key", "xxxx", "placeholder", "example", "test", "dummy", "fake",
                "sample", "insert", "replace", "changeme", "sk-xxx", "TODO", "PASTE",
                "ENTER", "PUT_YOUR", "REPLACE_ME", "CHANGE_ME", "your_api", "your_openai",
                "your_key_here", "your-key", "abc123", "123456", "***", "null", "none",
                "false", "true", "env", "config", "xxxxxxxx"]

def is_placeholder(v):
    lower = v.lower().strip()
    if len(v.strip()) < 10:
        return True
    return any(p.lower() in lower for p in placeholders)

def detect_and_extract(text, repo="", path=""):
    results = []
    patterns = [
        ("OpenAI", r"OPENAI_API_KEY\s*[=:]\s*['\"]?(sk-[A-Za-z0-9\-]{20,})"),
        ("DeepSeek", r"DEEPSEEK_API_KEY\s*[=:]\s*['\"]?(sk-[a-f0-9]{20,})"),
        ("Anthropic", r"ANTHROPIC_API_KEY\s*[=:]\s*['\"]?(sk-ant-[A-Za-z0-9\-]{20,})"),
        ("Moonshot/Kimi", r"MOONSHOT_API_KEY\s*[=:]\s*['\"]?(sk-[a-zA-Z0-9]{20,})"),
        ("DashScope", r"DASHSCOPE_API_KEY\s*[=:]\s*['\"]?(sk-[a-f0-9]{20,})"),
        ("ZhipuAI/GLM", r"ZHIPUAI_API_KEY\s*[=:]\s*['\"]?([a-f0-9]{32}\.[a-zA-Z0-9]{10,})"),
        ("SiliconFlow", r"SILICONFLOW_API_KEY\s*[=:]\s*['\"]?(sk-[a-zA-Z0-9]{20,})"),
        ("Qwen", r"QWEN_API_KEY\s*[=:]\s*['\"]?(sk-[a-f0-9]{20,})"),
        ("Baichuan", r"BAICHUAN_API_KEY\s*[=:]\s*['\"]?(sk-[a-f0-9]{20,})"),
        ("Spark/讯飞", r"SPARK_API_KEY\s*[=:]\s*['\"]?([a-f0-9]{32})"),
        ("MiniMax", r"MINIMAX_API_KEY\s*[=:]\s*['\"]?(eyJ[A-Za-z0-9\-_\.]{20,})"),
        ("Step/阶跃", r"STEPFUN_API_KEY\s*[=:]\s*['\"]?(sk-[a-zA-Z0-9]{20,})"),
        ("Yi/零一", r"YI_API_KEY\s*[=:]\s*['\"]?([a-f0-9]{32})"),
        ("SenseNova/商汤", r"SENSETIME_API_KEY\s*[=:]\s*['\"]?([a-f0-9]{32})"),
        ("Hunyuan/腾讯", r"HUNYUAN_SECRET_KEY\s*[=:]\s*['\"]?([a-f0-9]{32})"),
        ("Groq", r"GROQ_API_KEY\s*[=:]\s*['\"]?(gsk_[A-Za-z0-9]{20,})"),
        ("Replicate", r"REPLICATE_API_TOKEN\s*[=:]\s*['\"]?(r8_[A-Za-z0-9]{20,})"),
        ("Together", r"TOGETHER_API_KEY\s*[=:]\s*['\"]?([a-f0-9]{64})"),
        ("Fireworks", r"FIREWORKS_API_KEY\s*[=:]\s*['\"]?(fw_[A-Za-z0-9]{20,})"),
        ("Perplexity", r"PERPLEXITY_API_KEY\s*[=:]\s*['\"]?(pplx-[a-f0-9]{20,})"),
        ("HuggingFace", r"HUGGING_FACE_HUB_TOKEN\s*[=:]\s*['\"]?(hf_[A-Za-z0-9]{20,})"),
        ("Mistral", r"MISTRAL_API_KEY\s*[=:]\s*['\"]?([a-zA-Z0-9]{32})"),
        ("OpenRouter", r"OPENROUTER_API_KEY\s*[=:]\s*['\"]?(sk-or-[A-Za-z0-9\-]{20,})"),
        # 通用 fallback - 从片段中直接匹配
        ("Unknown(sk-ant)", r"(sk-ant-[A-Za-z0-9\-]{20,})"),
        ("Unknown(sk-or)", r"(sk-or-[A-Za-z0-9\-]{20,})"),
    ]
    for provider, pattern in patterns:
        for m in re.finditer(pattern, text):
            key = m.group(1) if m.lastindex else m.group(0)
            key = key.strip("'\"")
            if not is_placeholder(key) and len(key) > 15:
                results.append({"provider": provider, "key": key})
    return results

# 搜索查询 - 多维度覆盖
queries = [
    # 核心外贸关键词 × 主流供应商
    '"外贸" "OPENAI_API_KEY"',
    '"外贸" "DEEPSEEK_API_KEY"',
    '"外贸" "ANTHROPIC_API_KEY"',
    '"外贸" "MOONSHOT_API_KEY"',
    '"外贸" "DASHSCOPE_API_KEY"',
    '"外贸" "ZHIPUAI_API_KEY"',
    '"外贸" "SILICONFLOW_API_KEY"',
    '"waimao" "OPENAI_API_KEY"',
    '"waimao" "DEEPSEEK_API_KEY"',
    '"waimao" "API_KEY"',
    # 跨境电商
    '"跨境" "OPENAI_API_KEY"',
    '"跨境" "DEEPSEEK_API_KEY"',
    '"跨境电商" "API_KEY"',
    # .env 文件直接搜
    '"外贸" filename:.env',
    '"waimao" filename:.env',
    '"跨境" filename:.env',
    # 配置文件
    '"外贸" filename:config.yaml "API_KEY"',
    '"外贸" filename:config.json "api_key"',
    # 更多关键词
    '"外贸客户" "sk-"',
    '"外贸开发信" "API_KEY"',
    '"外贸邮件" "OPENAI"',
    '"foreign+trade" "OPENAI_API_KEY"',
]

all_findings = []
seen = set()
rate_limit_hits = 0

for qi, q in enumerate(queries):
    print(f"\n[{qi+1}/{len(queries)}] {q}", flush=True)

    for attempt in range(2):
        try:
            r = requests.get("https://api.github.com/search/code", headers=headers,
                            params={"q": q, "per_page": 10}, timeout=15)
        except Exception as e:
            print(f"  请求异常: {e}", flush=True)
            time.sleep(5)
            continue

        if r.status_code == 403:
            reset = int(r.headers.get("X-RateLimit-Reset", 0))
            wait = max(reset - int(time.time()), 5)
            if wait > 120:
                print(f"  限速太久 ({wait}s)，跳过", flush=True)
                break
            print(f"  限速，等 {wait}s...", flush=True)
            rate_limit_hits += 1
            time.sleep(wait + 1)
            continue
        if r.status_code == 401:
            print("  Token 无效!", flush=True)
            sys.exit(1)
        if r.status_code == 422:
            print(f"  查询格式无效，跳过", flush=True)
            break
        break
    else:
        continue

    if r.status_code != 200:
        print(f"  状态 {r.status_code}: {r.text[:100]}", flush=True)
        time.sleep(3)
        continue

    data = r.json()
    total = data.get("total_count", 0)
    items = data.get("items", [])
    print(f"  命中 {total} 个，本页 {len(items)}", flush=True)

    for item in items:
        repo = item["repository"]["full_name"]
        path = item["path"]
        html_url = item.get("html_url", "")
        owner = item["repository"]["owner"]["login"]
        repo_url = item["repository"]["html_url"]
        is_private = item["repository"].get("private", False)

        dedup = f"{repo}|{path}"
        if dedup in seen:
            continue
        seen.add(dedup)

        # 从 text_matches 提取片段
        fragments = ""
        for tm in item.get("text_matches", []):
            fragments += tm.get("fragment", "") + "\n"

        findings = detect_and_extract(fragments, repo, path)
        if not findings:
            # 如果片段没匹配到，尝试拉文件内容
            if not is_private:
                try:
                    fr = requests.get(
                        f"https://api.github.com/repos/{repo}/contents/{path}",
                        headers=headers, timeout=10
                    )
                    if fr.status_code == 200:
                        fdata = fr.json()
                        if fdata.get("encoding") == "base64":
                            import base64
                            content = base64.b64decode(fdata["content"]).decode("utf-8", errors="ignore")
                            findings = detect_and_extract(content, repo, path)
                    time.sleep(1)
                except:
                    pass

        for f in findings:
            key = f["key"]
            masked = key[:8] + "..." + key[-4:] if len(key) > 16 else key[:4] + "..."
            all_findings.append({
                "provider": f["provider"],
                "repo": repo,
                "owner": owner,
                "file": path,
                "key_preview": masked,
                "repo_url": repo_url,
                "file_url": html_url,
                "is_private": is_private,
            })
            print(f"  ✅ {f['provider']:20s} | {repo}/{path} | {masked}", flush=True)

    time.sleep(3)

# 去重 (repo+provider+key_preview)
final = []
final_seen = set()
for f in all_findings:
    dk = f"{f['repo']}|{f['provider']}|{f['key_preview']}"
    if dk not in final_seen:
        final_seen.add(dk)
        final.append(f)

with open("scan_results.json", "w", encoding="utf-8") as fp:
    json.dump(final, fp, ensure_ascii=False, indent=2)

print(f"\n{'='*60}", flush=True)
print(f"扫描完成!", flush=True)
print(f"  查询数: {len(queries)}", flush=True)
print(f"  限速次数: {rate_limit_hits}", flush=True)
print(f"  发现泄露: {len(final)} 个", flush=True)
print(f"\n供应商分布:", flush=True)
from collections import Counter
for p, c in Counter(f["provider"] for f in final).most_common():
    print(f"  {p}: {c}", flush=True)
