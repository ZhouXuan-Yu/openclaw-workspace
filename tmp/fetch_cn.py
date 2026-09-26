import sys, urllib.request, re, html

def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    with urllib.request.urlopen(req, timeout=25) as r:
        raw = r.read()
    for enc in ('utf-8', 'gb18030'):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode('utf-8', 'ignore')

def clean(h):
    h = re.sub(r'(?is)<script.*?</script>', ' ', h)
    h = re.sub(r'(?is)<style.*?</style>', ' ', h)
    h = re.sub(r'(?s)<[^>]+>', ' ', h)
    h = html.unescape(h)
    h = re.sub(r'[ \t]+', ' ', h)
    h = re.sub(r'\n\s*\n+', '\n', h)
    return h.strip()

url = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else None
t = clean(fetch(url))
if out:
    open(out, 'w', encoding='utf-8').write(t)
    print('saved', out, len(t))
else:
    sys.stdout.buffer.write(t[:6000].encode('utf-8'))
