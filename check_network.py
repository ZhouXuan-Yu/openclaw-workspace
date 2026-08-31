import urllib.request, json, sys, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

sites = [
    "https://news.ycombinator.com/",
    "https://api.github.com/search/repositories?q=AI+agent&sort=stars&order=desc&per_page=5",
    "https://www.google.com/",
    "https://baidu.com/",
]

for url in sites:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=8, context=ssl_ctx)
        data = resp.read()
        print(f"[OK] {url[:50]}... -> {len(data)} bytes")
        if "api.github" in url:
            items = json.loads(data).get('items', [])
            for r in items[:5]:
                print(f"  [{r['full_name']}] ⭐{r['stargazers_count']} - {r.get('description','N/A')[:100]}")
    except Exception as e:
        print(f"[FAIL] {url[:50]}... -> {type(e).__name__}: {e}")
