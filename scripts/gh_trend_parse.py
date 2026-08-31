import re, html, os

def parse(path, since_tag):
    raw = open(path, encoding='utf-8', errors='ignore').read()
    arts = re.split(r'<article', raw)[1:]
    out = []
    for a in arts:
        m = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', a)
        if not m:
            continue
        full = html.unescape(m.group(1)).strip()
        tm = re.search(r'([\d,\.]+k?) stars ' + since_tag, a)
        cnt = tm.group(1) if tm else '?'
        sm = re.search(r'aria-label="([\d,\.]+k?) stars"', a)
        total = sm.group(1) if sm else '?'
        dm = re.search(r'<p[^>]*class="col-9[^"]*"[^>]*>(.*?)</p>', a, re.S)
        desc = re.sub(r'<[^>]+>', '', dm.group(1)) if dm else ''
        lm = re.search(r'itemprop="programmingLanguage">([^<]+)<', a)
        lang = lm.group(1).strip() if lm else ''
        out.append((full, total, cnt, lang, html.unescape(desc).strip()[:90]))
    return out

for f, tag in [(r'%TEMP%\trending_daily.html', 'today'), (r'%TEMP%\trending_weekly.html', 'this week')]:
    path = os.path.expandvars(f)
    if not os.path.exists(path):
        print('missing', path)
        continue
    print('=' * 10, tag)
    for r in parse(path, tag)[:20]:
        print(' | '.join(r))
