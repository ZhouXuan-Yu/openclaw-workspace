"""外贸仓库密钥泄露检查"""
import requests, time, json, re, base64

headers = {"Accept": "application/vnd.github.v3+json"}
placeholders = ["your_key", "xxxx", "placeholder", "example", "test", "dummy", "fake", "sample", "insert", "replace", "changeme", "sk-xxx", "TODO", "PASTE", "ENTER", "PUT_YOUR"]

def is_placeholder(v):
    lower = v.lower()
    return any(p.lower() in lower for p in placeholders)

def check_repo(repo):
    findings = []
    print(f"\n检查仓库: {repo}")
    
    # 检查常见文件
    check_files = [
        ".env", ".env.local", ".env.example", ".env.production",
        "config/.env", "src/.env", "app/.env",
        "config.py", "src/config.py", "main.py", "app.py",
        "config.json", "config.yaml", "config.yml",
        "src/config.json", "src/config.yaml",
    ]
    
    for fname in check_files:
        url = f"https://api.github.com/repos/{repo}/contents/{fname}"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code != 200:
                continue
            data = r.json()
            if data.get("encoding") != "base64":
                continue
            content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
            
            patterns = [
                ("OpenAI", r"OPENAI_API_KEY\s*=\s*(sk-[A-Za-z0-9\-]+)"),
                ("DeepSeek", r"DEEPSEEK_API_KEY\s*=\s*(sk-[a-f0-9]+)"),
                ("Anthropic", r"ANTHROPIC_API_KEY\s*=\s*(sk-ant-[A-Za-z0-9\-]+)"),
                ("Moonshot", r"MOONSHOT_API_KEY\s*=\s*(sk-[a-zA-Z0-9]+)"),
                ("DashScope", r"DASHSCOPE_API_KEY\s*=\s*(sk-[a-f0-9]+)"),
                ("ZhipuAI", r"ZHIPUAI_API_KEY\s*=\s*([a-f0-9]{32}\.[a-zA-Z0-9]+)"),
                ("SiliconFlow", r"SILICONFLOW_API_KEY\s*=\s*(sk-[a-zA-Z0-9]+)"),
                ("Qwen", r"QWEN_API_KEY\s*=\s*(sk-[a-f0-9]+)"),
                # 通用硬编码
                ("OpenAI(hardcoded)", r"[^a-zA-Z](sk-[A-Za-z0-9]{20,})"),
                ("Anthropic(hardcoded)", r"[^a-zA-Z](sk-ant-[A-Za-z0-9\-]{20,})"),
            ]
            
            for provider, pattern in patterns:
                matches = re.findall(pattern, content)
                for m in matches:
                    if not is_placeholder(m) and len(m) > 15:
                        masked = m[:8] + "..." + m[-4:]
                        findings.append({
                            "provider": provider,
                            "file": fname,
                            "key_preview": masked,
                            "repo": repo,
                        })
                        print(f"  !! {provider} in {fname}: {masked}")
        except Exception:
            pass
    
    return findings

# 搜索外贸相关仓库
print("=== 搜索外贸相关仓库 ===")
repos = []

for q in ["外贸+language:python", "waimao+language:python", "外贸+ai+agent", "外贸+openai"]:
    try:
        r = requests.get("https://api.github.com/search/repositories", headers=headers,
                        params={"q": q, "per_page": 8, "sort": "updated"}, timeout=15)
        if r.status_code == 200:
            data = r.json()
            for item in data.get("items", []):
                fn = item["full_name"]
                desc = (item.get("description") or "")[:60]
                stars = item.get("stargazers_count", 0)
                repos.append((fn, desc, stars))
                print(f"  {fn} ({stars}*) - {desc}")
        else:
            print(f"  搜索失败: {r.status_code}")
        time.sleep(3)
    except Exception as e:
        print(f"  搜索异常: {e}")

# 去重
seen = set()
unique = []
for r in repos:
    if r[0] not in seen:
        seen.add(r[0])
        unique.append(r)

print(f"\n共 {len(unique)} 个仓库，开始逐个检查...")

all_findings = []
for repo, desc, stars in unique[:15]:
    findings = check_repo(repo)
    all_findings.extend(findings)
    time.sleep(2)

print(f"\n{'='*50}")
print(f"扫描完成: 共发现 {len(all_findings)} 个疑似密钥泄露")
for f in all_findings:
    print(f"  {f['provider']:20s} | {f['repo']:35s} | {f['file']:20s} | {f['key_preview']}")

# 保存结果
with open("scan_results.json", "w", encoding="utf-8") as fp:
    json.dump(all_findings, fp, ensure_ascii=False, indent=2)
print(f"\n结果已保存 scan_results.json")
