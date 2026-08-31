import urllib.request, json, sys, ssl, re

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

# Try Chinese news sources
sites = [
    ("36氪 AI", "https://36kr.com/search/articles/AI"),
    ("知乎 AI 热榜", "https://www.zhihu.com/hot?type=ai"),
    ("机器之心", "https://www.jiqizhixin.com/"),
    ("雷锋网 AI", "https://www.leiphone.com/category/ai"),
    ("虎嗅 AI", "https://www.huxiu.com/tag/ai.html"),
]

for name, url in sites:
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10, context=ssl_ctx)
        html = resp.read().decode('utf-8', errors='replace')
        # Extract text content - strip tags
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"\n=== {name} ({url}) === [{len(html)} bytes]")
        # Print first meaningful content
        sections = text.split('。')
        count = 0
        for s in sections[:30]:
            s = s.strip()
            if len(s) > 20 and ('AI' in s or '模型' in s or '智能' in s or 'Agent' in s or '大模型' in s or '开源' in s):
                print(f"  · {s}。")
                count += 1
                if count >= 8:
                    break
    except Exception as e:
        print(f"\n[FAIL] {name}: {type(e).__name__}: {e}")
