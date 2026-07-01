"""
二次扫描：直接拉取 .env 文件内容检查
"""
import requests, time, json, re, base64, sys
from datetime import datetime

GITHUB_TOKEN = sys.argv[1] if len(sys.argv) > 1 else ""
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}",
}

placeholders = ["your_key", "xxxx", "placeholder", "example", "test", "dummy", "fake",
                "sample", "insert", "replace", "changeme", "sk-xxx", "TODO", "PASTE",
                "ENTER", "PUT_YOUR", "REPLACE_ME", "CHANGE_ME", "your_api", "your_openai",
                "your_key_here", "your-key", "abc123", "123456", "***", "null", "none",
                "false", "true", "env", "config", "xxxxxxxx", "my_key", "your_glm",
                "your_key_glm", "test_key", "demo", "xxx"]

def is_placeholder(v):
    lower = v.lower().strip()
    if len(v.strip()) < 10:
        return True
    return any(p.lower() in lower for p in placeholders)

def extract_keys(content):
    findings = []
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
    ]
    for provider, pattern in patterns:
        for m in re.finditer(pattern, content):
            key = m.group(1).strip("'\"")
            if not is_placeholder(key) and len(key) > 15:
                findings.append({"provider": provider, "key": key})
    return findings

def search_and_check(query, label):
    """搜索 .env 文件并检查内容"""
    results = []
    print(f"\n[{label}] 搜索: {query}", flush=True)
    try:
        r = requests.get("https://api.github.com/search/code", headers=headers,
                        params={"q": query, "per_page": 10}, timeout=15)
    except Exception as e:
        print(f"  请求异常: {e}", flush=True)
        return results

    if r.status_code == 403:
        reset = int(r.headers.get("X-RateLimit-Reset", 0))
        wait = max(reset - int(time.time()), 5)
        print(f"  限速，等 {wait}s...", flush=True)
        time.sleep(wait + 1)
        return results

    if r.status_code != 200:
        print(f"  状态 {r.status_code}", flush=True)
        return results

    data = r.json()
    items = data.get("items", [])
    print(f"  命中 {data.get('total_count', 0)} 个，检查 {len(items)} 个文件", flush=True)

    for item in items:
        repo = item["repository"]["full_name"]
        path = item["path"]
        owner = item["repository"]["owner"]["login"]
        repo_url = item["repository"]["html_url"]
        html_url = item.get("html_url", "")
        is_private = item["repository"].get("private", False)

        # 拉文件内容
        try:
            fr = requests.get(
                f"https://api.github.com/repos/{repo}/contents/{path}",
                headers=headers, timeout=10
            )
            if fr.status_code != 200:
                continue
            fdata = fr.json()
            if fdata.get("encoding") != "base64":
                continue
            content = base64.b64decode(fdata["content"]).decode("utf-8", errors="ignore")
        except:
            continue

        findings = extract_keys(content)
        for f in findings:
            key = f["key"]
            masked = key[:8] + "..." + key[-4:] if len(key) > 16 else key[:4] + "..."
            results.append({
                "provider": f["provider"],
                "repo": repo,
                "owner": owner,
                "file": path,
                "key_preview": masked,
                "repo_url": repo_url,
                "file_url": html_url,
                "is_private": is_private,
                "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            print(f"  ✅ {f['provider']:20s} | {repo}/{path} | {masked}", flush=True)

        time.sleep(1)
    return results

# 主扫描
all_findings = []
seen = set()

queries = [
    # .env 文件 (最高优先级)
    ('"外贸" filename:.env', '外贸/.env'),
    ('"跨境" filename:.env', '跨境/.env'),
    ('"waimao" filename:.env', 'waimao/.env'),
    ('"外贸" filename:.env.local', '外贸/.env.local'),
    ('"跨境" filename:.env.local', '跨境/.env.local'),
    # 配置文件
    ('"外贸" filename:config.yaml "KEY"', '外贸/config.yaml'),
    ('"外贸" filename:config.json "key"', '外贸/config.json'),
    ('"跨境" filename:config.yaml "KEY"', '跨境/config.yaml'),
    ('"跨境" filename:config.json "key"', '跨境/config.json'),
    # Python 文件中的硬编码
    ('"外贸" "OPENAI_API_KEY" language:python', '外贸/py/openai'),
    ('"外贸" "DEEPSEEK_API_KEY" language:python', '外贸/py/deepseek'),
    ('"跨境" "OPENAI_API_KEY" language:python', '跨境/py/openai'),
    ('"跨境" "DEEPSEEK_API_KEY" language:python', '跨境/py/deepseek'),
    # JS/TS 文件
    ('"外贸" "OPENAI_API_KEY" language:javascript', '外贸/js/openai'),
    ('"跨境" "OPENAI_API_KEY" language:javascript', '跨境/js/openai'),
    # 更多
    ('"外贸客户" filename:.env', '外贸客户/.env'),
    ('"外贸开发信" "API_KEY"', '外贸开发信'),
    ('"外贸邮件" "OPENAI"', '外贸邮件'),
    ('"waimao" "OPENAI_API_KEY" language:python', 'waimao/py'),
]

for query, label in queries:
    findings = search_and_check(query, label)
    for f in findings:
        dk = f"{f['repo']}|f['file']|{f['provider']}"
        if dk not in seen:
            seen.add(dk)
            all_findings.append(f)
    time.sleep(3)

# 保存
with open("scan_results.json", "w", encoding="utf-8") as fp:
    json.dump(all_findings, fp, ensure_ascii=False, indent=2)

print(f"\n{'='*60}", flush=True)
print(f"二次扫描完成!", flush=True)
print(f"  发现泄露: {len(all_findings)} 个", flush=True)
if all_findings:
    print(f"\n供应商分布:", flush=True)
    from collections import Counter
    for p, c in Counter(f["provider"] for f in all_findings).most_common():
        print(f"  {p}: {c}", flush=True)
    print(f"\n详细列表:", flush=True)
    for f in all_findings:
        print(f"  {f['provider']:20s} | {f['repo']:40s} | {f['file']:25s} | {f['key_preview']}", flush=True)
