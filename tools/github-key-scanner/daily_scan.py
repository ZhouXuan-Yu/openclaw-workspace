"""GitHub 密钥扫描 v4 — 完整密钥存储 + 活跃度过滤 + Obsidian 导出"""
import requests, re, time, json, base64, sys, os
import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
HISTORY_JSON = Path("tools/github-key-scanner/scan_history.json")
LOG_MD = Path("docs/github-key-scan-log.md")
OBSIDIAN_DIR = Path("E:/Obsidian仓库/ZhouXuan私人领域/密钥存储")

ACTIVE_MONTHS = 6  # 只扫描最近 6 个月内有 push 的仓库

SEARCH_QUERIES = [
    # 高命中率 query（不加特定文件名，搜全 GitHub 所有文件）
    ("sk-or-v1- language:python", r"sk-or-v1-[A-Za-z0-9]{20,}", "OpenRouter", 30),
    ("sk-or-v1- language:javascript", r"sk-or-v1-[A-Za-z0-9]{20,}", "OpenRouter", 20),
    ("\"sk-proj-\" language:python", r"sk-proj-[A-Za-z0-9_-]{20,}", "OpenAI Proj", 30),
    ("\"sk-ant-api03-\"", r"sk-ant-api03-[A-Za-z0-9\-_]{20,}", "Anthropic", 30),
    ("\"AIzaSy\" language:python", r"AIza[A-Za-z0-9_\-]{30,}", "Google Gemini", 30),
    ("\"AIzaSy\" language:javascript", r"AIza[A-Za-z0-9_\-]{30,}", "Google Gemini", 20),
    ("\"AIzaSy\" language:go", r"AIza[A-Za-z0-9_\-]{30,}", "Google Gemini", 20),
    # .env / config 类（命中稳定）
    ("OPENAI_API_KEY filename:.env", r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}", "OpenAI", 20),
    ("ANTHROPIC_API_KEY filename:.env", r"sk-ant-[A-Za-z0-9\-]{20,}", "Anthropic", 20),
    ("DEEPSEEK_API_KEY filename:.env", r"sk-[a-f0-9]{20,}", "DeepSeek", 20),
    ("GEMINI_API_KEY filename:.env", r"AIza[A-Za-z0-9_\-]{30,}", "Google Gemini", 20),
    ("HUGGINGFACE_TOKEN filename:.env", r"hf_[A-Za-z0-9]{20,}", "HuggingFace", 20),
    ("GROQ_API_KEY filename:.env", r"gsk_[A-Za-z0-9]{20,}", "Groq", 20),
    ("MOONSHOT_API_KEY filename:.env", r"sk-[a-zA-Z0-9]{20,}", "Moonshot Kimi", 20),
    ("SILICONFLOW_API_KEY filename:.env", r"sk-[a-zA-Z0-9]{20,}", "SiliconFlow", 20),
    ("REPLICATE_API_TOKEN filename:.env", r"r8_[A-Za-z0-9]{20,}", "Replicate", 15),
    ("PERPLEXITY_API_KEY filename:.env", r"pplx-[a-f0-9]{40,}", "Perplexity", 15),
    ("MISTRAL_API_KEY filename:.env", r"[a-zA-Z0-9]{32}", "Mistral", 15),
    ("COHERE_API_KEY filename:.env", r"[a-zA-Z0-9]{40}", "Cohere", 15),
    ("TOGETHER_API_KEY filename:.env", r"[a-f0-9]{64}", "Together", 15),
    ("FIREWORKS_API_KEY filename:.env", r"fw_[A-Za-z0-9]{20,}", "Fireworks", 15),
    ("QWEN_API_KEY filename:.env", r"sk-[a-f0-9]{20,}", "通义千问", 15),
    ("BAICHUAN_API_KEY filename:.env", r"sk-[a-f0-9]{20,}", "百川", 15),
    ("MINIMAX_API_KEY filename:.env", r"eyJ[A-Za-z0-9\-_]+", "MiniMax", 15),
    # config 文件泄露
    ("api_key filename:config.py", r"sk-[A-Za-z0-9_-]{20,}|AIza[A-Za-z0-9_\-]{30,}|hf_[A-Za-z0-9]{20,}|gsk_[A-Za-z0-9]{20,}|pplx-[a-f0-9]{40,}", "config.py", 20),
    ("api_key filename:config.js", r"sk-[A-Za-z0-9_-]{20,}|AIza[A-Za-z0-9_\-]{30,}|hf_[A-Za-z0-9]{20,}", "config.js", 20),
    ("api_key filename:constants", r"sk-[A-Za-z0-9_-]{20,}|AIza[A-Za-z0-9_\-]{30,}|hf_[A-Za-z0-9]{20,}", "constants", 20),
    ("API_KEY filename:.env", r"sk-[A-Za-z0-9_-]{20,}|AIza[A-Za-z0-9_\-]{30,}|hf_[A-Za-z0-9]{20,}", "通用 密钥", 20),
    ("secret_key filename:.env", r"sk-[A-Za-z0-9_-]{20,}|AIza[A-Za-z0-9_\-]{30,}", "通用 secret", 20),
]

PLACEHOLDER_KEYWORDS = [
    "your_key_here","your_api_key","xxxxxx","placeholder","example","test","dummy",
    "fake","sample","insert","replace_me","changeme","sk-xxx","sk-ant-xxx",
    "your_openai","your_anthropic","TODO","FIXME","PASTE_YOUR","ENTER_YOUR",
    "PUT_YOUR","your-key","your-","<your","<api","replace with","add your"
]

EXAMPLE_FILE_PATTERNS = ['.env-example', '.env.example', '.env.sample', '.env.template', 'example.env', 'sample.env']

PROVIDER_PATTERNS = {
    r"sk-ant-[A-Za-z0-9\-]{20,}": "Anthropic",
    r"sk-proj-[A-Za-z0-9_-]{20,}": "OpenAI Proj",
    r"sk-[A-Za-z0-9_-]{20,}": "OpenAI类",
    r"AIza[A-Za-z0-9_\-]{30,}": "Google Gemini",
    r"hf_[A-Za-z0-9]{20,}": "HuggingFace",
    r"gsk_[A-Za-z0-9]{20,}": "Groq",
    r"pplx-[a-f0-9]{40,}": "Perplexity",
    r"r8_[A-Za-z0-9]{20,}": "Replicate",
    r"fw_[A-Za-z0-9]{20,}": "Fireworks",
    r"eyJ[A-Za-z0-9\-_]+": "MiniMax JWT",
}

# Cache for repo activity checks
_repo_activity_cache = {}

def classify_provider(key):
    for pat, prov in PROVIDER_PATTERNS.items():
        if re.search(pat, key):
            return prov
    return "Unknown"

def mask_key(key):
    return key[:8]+"..."+key[-4:] if len(key) > 16 else key[:6]+"..."

def is_ph(value):
    return any(kw.lower() in value.lower() for kw in PLACEHOLDER_KEYWORDS)

def is_example_file(filepath):
    fname = Path(filepath).name.lower() if filepath else ""
    return any(pat.lower() in fname for pat in EXAMPLE_FILE_PATTERNS)

def gh_headers(with_text_match=True):
    h = {}
    if with_text_match:
        h["Accept"] = "application/vnd.github.v3.text-match+json"
    if GITHUB_TOKEN: h["Authorization"] = f"token {GITHUB_TOKEN}"
    return h

def search_gh(query, per_page=15):
    url = "https://api.github.com/search/code"
    # No pushed: filter in query (breaks on proxy). Filter per-result instead.
    for attempt in range(2):
        try:
            r = requests.get(url, headers=gh_headers(),
                params={"q": query, "per_page": per_page}, timeout=15, verify=False)
            if r.status_code == 403:
                reset = int(r.headers.get("X-RateLimit-Reset", 0))
                wait = max(reset - int(time.time()), 5)
                if wait > 60: return []
                time.sleep(wait)
                continue
            if r.status_code == 422: return []
            r.raise_for_status()
            return r.json().get("items", [])
        except:
            time.sleep(2)
    return []

def fetch_content(repo, path, ref=None):
    url = f"https://api.github.com/repos/{repo}/contents/{path}" + (f"?ref={ref}" if ref else "")
    try:
        r = requests.get(url, headers=gh_headers(), timeout=10, verify=False)
        if r.status_code == 200:
            d = r.json()
            if d.get("encoding") == "base64" and d.get("content"):
                return base64.b64decode(d["content"]).decode("utf-8", errors="ignore")
    except: pass
    return ""

def is_repo_active(repo_full_name):
    """Check if repo had a push in last ACTIVE_MONTHS months"""
    if repo_full_name in _repo_activity_cache:
        return _repo_activity_cache[repo_full_name]
    
    try:
        r = requests.get(f"https://api.github.com/repos/{repo_full_name}",
                        headers=gh_headers(), timeout=10, verify=False)
        if r.status_code == 200:
            d = r.json()
            pushed_at = d.get("pushed_at", "")
            if pushed_at:
                push_date = datetime.strptime(pushed_at[:10], "%Y-%m-%d")
                cutoff = datetime.now() - timedelta(days=ACTIVE_MONTHS * 30)
                active = push_date >= cutoff
                _repo_activity_cache[repo_full_name] = active
                return active
    except: pass
    _repo_activity_cache[repo_full_name] = False
    return False

def load_history():
    if HISTORY_JSON.exists():
        try: return json.loads(HISTORY_JSON.read_text(encoding="utf-8"))
        except: pass
    return {"seen_keys": {}, "log_entries": []}

def save_history(h):
    HISTORY_JSON.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_JSON.write_text(json.dumps(h, ensure_ascii=False, indent=2), encoding="utf-8")

def scan():
    results = []
    seen_dedup = set()
    total_queries = len(SEARCH_QUERIES)
    files_checked = 0
    skipped_inactive = 0

    for idx, (query, regex, label, pp) in enumerate(SEARCH_QUERIES, 1):
        sys.stdout.write(f"\r[{idx}/{total_queries}] {label[:30]:<30}")
        sys.stdout.flush()
        items = search_gh(query, per_page=pp)
        files_checked += len(items)

        for item in items:
            repo = item["repository"]["full_name"]
            fp = item["path"]
            url = item.get("html_url", "")
            repo_url = item["repository"]["html_url"]
            owner = item["repository"]["owner"]["login"]
            ref = item.get("sha", "")

            if is_example_file(fp): continue

            # Filter inactive repos (use pushed_at from search response, no extra API call)
            pushed_at = item["repository"].get("pushed_at", "")
            if pushed_at:
                try:
                    push_date = datetime.strptime(pushed_at[:10], "%Y-%m-%d")
                    cutoff_date = datetime.now() - timedelta(days=ACTIVE_MONTHS * 30)
                    if push_date < cutoff_date:
                        skipped_inactive += 1
                        continue
                except ValueError:
                    pass  # can't parse, let it through

            dedup = f"{repo}|{fp}"
            if dedup in seen_dedup: continue
            seen_dedup.add(dedup)

            frag = "".join(tm.get("fragment", "") + "\n" for tm in item.get("text_matches", []))
            keys = re.findall(regex, frag)
            if not keys:
                content = fetch_content(repo, fp, ref)
                if content: keys = re.findall(regex, content)

            for k in keys:
                if is_ph(k): continue
                prov = classify_provider(k)
                now = datetime.now()
                results.append({
                    "provider": prov,
                    "model": label,
                    "repo": repo,
                    "owner": owner,
                    "file": fp,
                    "key_full": k,               # v4: 完整密钥
                    "key_hash": k[-12:],
                    "key_preview": mask_key(k),
                    "repo_url": repo_url,
                    "file_url": url,
                    "is_private": False,
                    "date": now.strftime("%Y-%m-%d"),
                    "scan_time": now.strftime("%Y-%m-%d %H:%M"),
                    "search_query": query,
                })

        if len(results) >= 100:
            break
        time.sleep(1.5)

    print(f"\r✅ {total_queries} queries, {files_checked} files checked, {skipped_inactive} inactive skipped, {len(results)} keys found")
    return results

def merge(new_results):
    h = load_history()
    sk = h["seen_keys"]
    entries = h["log_entries"]
    new_entries = []

    for r in new_results:
        did = f"{r['repo']}:{r['file']}|{r['key_hash']}"
        if did not in sk:
            sk[did] = {
                "first_seen": r["date"], "last_seen": r["date"],
                "provider": r["provider"], "model": r["model"],
                "repo": r["repo"], "file": r["file"],
                "key_full": r["key_full"],
                "key_preview": r["key_preview"], "repo_url": r["repo_url"],
                "file_url": r["file_url"]
            }
            new_entries.append(r)
        else:
            sk[did]["last_seen"] = r["date"]

    today = datetime.now().strftime("%Y-%m-%d")
    entries.append({"date": today, "total_found": len(new_results),
                    "new_found": len(new_entries), "entries": new_entries})
    h["seen_keys"] = sk
    h["log_entries"] = entries
    h["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_history(h)
    return h, new_entries

def write_md(h, new_entries):
    sk = h["seen_keys"]
    lines = [
        "# GitHub 密钥扫描记录\n\n",
        "> 每日扫描：每天 12:00 | v4 活跃度过滤 (4月) | 目标 ≥5新增/天  \n\n---\n\n",
        f"## 总览\n- **累计**: {len(sk)} 密钥, {len(set(v['repo'] for v in sk.values()))} 仓库\n",
        f"- **最后**: {h.get('last_scan','N/A')}\n\n",
        "### 供应商分布\n\n| 供应商 | 泄露数 |\n|--------|--------|\n"
    ]
    for prov, cnt in Counter(v["provider"] for v in sk.values()).most_common():
        lines.append(f"| {prov} | {cnt} |\n")
    lines.append("\n---\n## 历史\n\n")

    for entry in reversed(h["log_entries"]):
        de = entry["entries"]
        lines.append(f"### {entry['date']}\n> 扫描 {entry['total_found']} 个，**新增 {entry['new_found']}** 个\n\n")
        if de:
            for i, r in enumerate(de, 1):
                link = f"[查看]({r['file_url']})" if r.get("file_url") else "-"
                lines.append(f"| {i} | {r['provider']} | {r['repo']} | `{r['file']}` | `{r['key_preview']}` | {link} |\n")
            lines.append("\n")

    lines.append(f"---\n> 更新于 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    LOG_MD.parent.mkdir(parents=True, exist_ok=True)
    LOG_MD.write_text("".join(lines), encoding="utf-8")
    return LOG_MD

def export_obsidian():
    """Export ALL keys to Obsidian vault, grouped by provider + verification status"""
    h = load_history()
    sk = h["seen_keys"]
    if not sk:
        print("No keys to export")
        return
    by_provider = defaultdict(list)
    for k, v in sk.items():
        by_provider[v["provider"]].append({**v, "key_id": k})

    OBSIDIAN_DIR.mkdir(parents=True, exist_ok=True)

    # Provider files
    for prov, items in sorted(by_provider.items()):
        prov_slug = prov.replace(" ", "_").replace("/", "-")
        fpath = OBSIDIAN_DIR / f"GitHub泄露-{prov_slug}.md"

        lines = [f"# GitHub 密钥泄露 - {prov}", "",
                 f"> 共 {len(items)} 个密钥 | 扫描: {h['last_scan']} | v4 活跃度过滤 ({ACTIVE_MONTHS}月)", "",
                 "| # | 仓库 | 文件 | 密钥（完整） | 发现日期 | 最后扫描 |",
                 "|----|------|------|-------------|----------|----------|"]
        for i, item in enumerate(items, 1):
            lines.append(f"| {i} | {item['repo']} | {item['file']} | `{item.get('key_full', item['key_preview'])}` | {item['first_seen']} | {item['last_seen']} |")

        lines.append("")
        lines.append("---")
        lines.append("## 详细记录")
        lines.append("")
        for i, item in enumerate(items, 1):
            lines.append(f"### {i}. {item['repo']}/{item['file']}")
            lines.append(f"- **仓库**: [{item['repo']}]({item['repo_url']})")
            lines.append(f"- **文件链接**: [查看]({item['file_url']})")
            lines.append(f"- **密钥**: `{item.get('key_full', item['key_preview'])}`")
            lines.append(f"- **首次发现**: {item['first_seen']}")
            lines.append(f"- **最后扫描**: {item['last_seen']}")
            lines.append("")

        with open(fpath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # Index file
    fpath = OBSIDIAN_DIR / "GitHub泄露-总览.md"
    total_repos = len(set(v['repo'] for v in sk.values()))
    verified_count = sum(1 for v in sk.values() if v.get("verified") == "valid")
    lines = ["# GitHub 密钥泄露 - 总览", "",
             f"> 总密钥: {len(sk)} | 已验证有效: {verified_count} | {total_repos} 仓库 | 更新: {h['last_scan']} | v4 ({ACTIVE_MONTHS}月活跃过滤)", "",
             "| 供应商 | 数量 | 有效 | 详细文件 |",
             "|--------|------|------|----------|"]
    for prov, items in sorted(by_provider.items()):
        ps = prov.replace(" ", "_").replace("/", "-")
        prov_verified = sum(1 for v in items if v.get("verified") == "valid")
        lines.append(f"| {prov} | {len(items)} | {prov_verified} | [[GitHub泄露-{ps}]] |")
    lines.append("")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Obsidian exported: {len(by_provider)} provider files, {len(sk)} keys ({verified_count} verified) -> {OBSIDIAN_DIR}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", action="store_true", help="Only export Obsidian files")
    ap.add_argument("--scan", action="store_true", help="Only scan (skip Obsidian export)")
    args = ap.parse_args()

    if args.export:
        export_obsidian()
        sys.exit(0)

    print("=" * 60)
    print(f"🔍 GitHub 密钥扫描 v4 | {datetime.now().strftime('%Y-%m-%d %H:%M')} | {ACTIVE_MONTHS}月活跃过滤")
    print("=" * 60)

    if not GITHUB_TOKEN:
        print("❌ no token")
        sys.exit(1)

    results = scan()
    h, new_entries = merge(results)

    print(f"📊 扫描={len(results)} 新增={len(new_entries)}")
    md = write_md(h, new_entries)

    sk = h["seen_keys"]
    print(f"📋 累计: {len(sk)} 密钥, {len(set(v['repo'] for v in sk.values()))} 仓库")
    for prov, cnt in Counter(v["provider"] for v in sk.values()).most_common():
        print(f"   {prov}: {cnt}")

    if new_entries:
        print(f"\n🆕 ({len(new_entries)}):")
        for r in new_entries:
            print(f"   [{r['provider']}] {r['repo']}/{r['file']} -> {r['key_preview']}")

    if not args.scan:
        export_obsidian()

    print("\n✅ done")
