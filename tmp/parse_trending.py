import re, sys, html

def parse(path):
    with open(path, encoding='utf-8', errors='ignore') as f:
        t = f.read()
    out = []
    blocks = re.split(r'<article\b', t)[1:]
    for b in blocks:
        h2 = re.search(r'<h2.*?</h2>', b, re.S)
        if not h2:
            continue
        repo_m = re.search(r'href="/([^"/]+/[^"?]+)"', h2.group(0))
        if not repo_m:
            continue
        repo = repo_m.group(1)
        desc = ''
        dm = re.search(r'<p class="col-9 color-fg-muted my-1 (?:tmp-)?pr-4">\s*(.*?)\s*</p>', b, re.S)
        if dm:
            desc = html.unescape(re.sub(r'<[^>]+>', '', dm.group(1))).strip()
        stars = ''
        sm = re.search(r'href="/%s/stargazers"[^>]*>\s*(?:<svg.*?</svg>)?\s*([\d,]+)' % re.escape(repo), b, re.S)
        if sm:
            stars = sm.group(1)
        today = ''
        tm = re.search(r'([\d,]+)\s*stars?\s*(today|this week)', b)
        if tm:
            today = tm.group(1)
        lang = ''
        lm = re.search(r'itemprop="programmingLanguage">([^<]+)<', b)
        if lm:
            lang = lm.group(1).strip()
        out.append((repo, stars, today, lang, desc))
    return out

for path, label in [(sys.argv[1], 'DAILY'), (sys.argv[2], 'WEEKLY')]:
    print('==== %s ====' % label)
    for r in parse(path):
        print(' | '.join(r))
