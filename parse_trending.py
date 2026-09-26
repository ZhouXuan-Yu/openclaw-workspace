import re, sys, html

def parse(path):
    with open(path, encoding='utf-8') as f:
        t = f.read()
    # split by article rows
    rows = re.split(r'<article class="Box-row"', t)[1:]
    out = []
    for r in rows:
        # repo name: <h2 ...><a href="/owner/repo" ...>
        m = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', r)
        name = m.group(1) if m else '?'
        # description
        d = re.search(r'<p class="col-9[^"]*"[^>]*>(.*?)</p>', r, re.S)
        desc = html.unescape(re.sub(r'<[^>]+>', '', d.group(1))).strip() if d else ''
        # stars: total
        s = re.findall(r'href="/[^"]+/stargazers"[^>]*>(.*?)</a>', r, re.S)
        stars = ''
        if s:
            stars = re.sub(r'<[^>]+>', '', s[0]).strip()
        # today's stars
        tdy = re.search(r'([\d,]+)\s*stars?\s*today', r)
        tdyw = re.search(r'([\d,]+)\s*stars?\s*this week', r)
        delta = (tdy.group(1) if tdy else (tdyw.group(1) if tdyw else ''))
        # language
        lang = re.search(r'<span itemprop="programmingLanguage">([^<]+)</span>', r)
        lang = lang.group(1) if lang else ''
        out.append((name, stars, delta, lang, desc[:160]))
    return out

for p in sys.argv[1:]:
    print('==== ' + p)
    for i, row in enumerate(parse(p), 1):
        print(f'{i}. {row[0]} | star={row[1]} | delta={row[2]} | {row[3]} | {row[4]}')
