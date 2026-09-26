import re, html, sys, os
sys.stdout.reconfigure(encoding='utf-8')
tmp = os.environ['TEMP']

def parse(fn):
    t = open(os.path.join(tmp, fn), encoding='utf-8', errors='ignore').read()
    arts = re.findall(r'<article class="Box-row">(.*?)</article>', t, re.S)
    out = []
    for a in arts:
        m = re.search(r'<h2 class="h3 lh-condensed">.*?href="/([^"]+)"', a, re.S)
        name = m.group(1) if m else '?'
        d = re.search(r'<p class="col-9 color-fg-muted my-1[^"]*">(.*?)</p>', a, re.S)
        desc = html.unescape(re.sub('<[^>]+>', '', d.group(1))).strip() if d else ''
        st = re.search(r'([\d,]+)\s+stars?\s+(?:today|this week)', a)
        total = re.search(r'<a[^>]*href="/[^"]+/stargazers"[^>]*>(.*?)</a>', a, re.S)
        lang = re.search(r'itemprop="programmingLanguage">([^<]+)<', a)
        out.append((name, lang.group(1) if lang else '', (st.group(1) if st else '?'), (html.unescape(re.sub('<[^>]+>','',total.group(1))).strip() if total else '?'), desc))
    return out

for fn in ['gh_daily.html', 'gh_weekly.html']:
    print('=====', fn)
    for i, row in enumerate(parse(fn)[:25], 1):
        n, l, st, tot, d = row
        print(i, n, '|', l, '| +' + st, '| ' + tot, '|', d[:100])
