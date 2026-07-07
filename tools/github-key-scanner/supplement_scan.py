"""补扫第一批中断的供应商"""
import os, requests, re, time, json, base64
from datetime import datetime
from pathlib import Path

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def gh_headers():
    h = {"Accept": "application/vnd.github.v3.text-match+json"}
    if GITHUB_TOKEN: h["Authorization"] = f"token {GITHUB_TOKEN}"
    return h

def search_gh(query, per_page=15):
    for a in range(3):
        try:
            r = requests.get("https://api.github.com/search/code", headers=gh_headers(), params={"q":query,"per_page":per_page}, timeout=15)
            if r.status_code == 403:
                reset = int(r.headers.get("X-RateLimit-Reset",0))
                wait = max(reset - int(time.time()), 10)
                if wait > 120: return []
                print(f"  限速等待 {wait}s...", flush=True)
                time.sleep(wait); continue
            if r.status_code == 422: return []
            r.raise_for_status()
            return r.json().get("items",[])
        except Exception as e:
            print(f"  Error: {e}", flush=True)
            time.sleep(5)
    return []

def fetch_content(repo, path, ref=None):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    if ref: url += f"?ref={ref}"
    try:
        r = requests.get(url, headers=gh_headers(), timeout=10)
        if r.status_code==200:
            d = r.json()
            if d.get("encoding")=="base64" and d.get("content"):
                return base64.b64decode(d["content"]).decode("utf-8", errors="ignore")
    except: pass
    return ""

PH = ["your_key_here","your_api_key","xxxxxx","placeholder","example","test","dummy","fake","sample","insert","replace_me","changeme","sk-xxx","TODO","FIXME"]
def extract_keys(text, pat):
    return [m for m in re.findall(pat, text) if not any(kw.lower() in m.lower() for kw in PH)]

def mask_key(k):
    return k[:8]+"..."+k[-4:] if len(k)>16 else k[:6]+"..."

queries = [
    ('"MISTRAL_API_KEY="', "Mistral AI", r"[a-zA-Z0-9]{32}", "Mistral"),
    ('"COHERE_API_KEY="', "Cohere", r"[a-zA-Z0-9]{40}", "Command R+"),
    ('"TOGETHER_API_KEY="', "Together AI", r"[a-f0-9]{64}", "Together"),
    ('"SPARK_API_KEY="', "讯飞星火", r"[a-f0-9]{32}", "Spark"),
    ('"YI_API_KEY="', "零一万物", r"[a-f0-9]{32}", "Yi"),
    ('"SENSETIME_API_KEY="', "商汤", r"[a-f0-9]{32}", "SenseNova"),
    ('"HUNYUAN_SECRET_KEY="', "腾讯混元", r"[a-f0-9]{32}", "Hunyuan"),
]

results = []
seen = set()

for q, prov, regex, model in queries:
    print(f"{prov} ...", flush=True)
    items = search_gh(q)
    print(f"  {len(items)} 个文件", flush=True)
    for item in items:
        repo = item["repository"]["full_name"]
        fp = item["path"]
        dedup = f"{repo}|{fp}|{prov}"
        if dedup in seen: continue
        seen.add(dedup)
        frag = "".join(tm.get("fragment","")+"\n" for tm in item.get("text_matches",[]))
        keys = extract_keys(frag, regex)
        if not keys:
            c = fetch_content(repo, fp, item.get("sha",""))
            if c: keys = extract_keys(c, regex)
        if not keys: continue
        for k in keys:
            results.append({"provider":prov,"model":model,"repo":repo,"file":fp,"key_preview":mask_key(k),"file_url":item.get("html_url","")})
    time.sleep(2)

# 合并到历史
hist = Path("tools/github-key-scanner/scan_history.json")
h = json.loads(hist.read_text(encoding="utf-8")) if hist.exists() else {"seen_keys":{},"log_entries":[]}
sk = h["seen_keys"]
new_entries = []
for r in results:
    did = f"{r['repo']}:{r['file']}|{r['key_preview']}"
    if did not in sk:
        sk[did] = {"provider":r["provider"],"model":r["model"],"repo":r["repo"],"file":r["file"],"key_preview":r["key_preview"]}
        new_entries.append(r)

if new_entries:
    # 更新今天的日志条目
    today = datetime.now().strftime("%Y-%m-%d")
    for e in h["log_entries"]:
        if e["date"] == today:
            e["entries"].extend(new_entries)
            e["total_found"] = e.get("total_found",0) + len(new_entries)
            e["new_found"] = e.get("new_found",0) + len(new_entries)
            break
    h["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    hist.write_text(json.dumps(h, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n新增 {len(new_entries)} 个:")
    for r in new_entries:
        print(f"  [{r['provider']}] {r['repo']}/{r['file']} -> {r['key_preview']}")
else:
    print("\n无新增")
print("完成!")
