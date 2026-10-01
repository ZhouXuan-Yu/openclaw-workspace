import re, sys, html

def parse(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    blocks = re.split(r'<article[^>]*>', raw)[1:]
    out = []
    for b in blocks:
        m = re.search(r'<h2[^>]*>(.*?)</h2>', b, re.S)
        if not m:
            continue
        h = m.group(1)
        links = re.findall(r'href="/([^"/]+)/([^"/]+)"', h)
        repo = "/".join(links[-1]) if links else "?"
        dm = re.search(r'<p class="[^"]*color-fg-muted[^"]*"[^>]*>\s*(.*?)</p>', b, re.S)
        desc = re.sub(r'<[^>]+>', '', dm.group(1)).strip() if dm else ""
        desc = html.unescape(re.sub(r'\s+', ' ', desc))
        lang = re.search(r'itemprop="programmingLanguage">([^<]+)<', b)
        total = ""
        st = re.search(r'href="/%s/stargazers"[^>]*>(.*?)</a>' % re.escape(repo), b, re.S)
        if st:
            nums = re.sub(r'<[^>]+>', ' ', st.group(1))
            tot = re.search(r'([\d,]+)', nums)
            total = tot.group(1) if tot else ""
        tm = re.search(r'([\d,]+)\s+stars?\s+(today|this week)', b, re.S)
        out.append((repo, desc, lang.group(1) if lang else "", total, tm.group(1) if tm else ""))
    return out

for p in sys.argv[1:]:
    print("=====", p)
    for r in parse(p):
        print("%-45s %-14s total:%-8s recent:%s" % (r[0], r[2], r[3], r[4]))
        print("    ", r[1][:200])
