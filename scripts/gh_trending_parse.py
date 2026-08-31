# -*- coding: utf-8 -*-
import re, html, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    articles = re.findall(r'<article class="Box-row">(.*?)</article>', content, re.DOTALL)
    repos = []
    for a in articles:
        href_m = re.search(r'<h2[^>]*>.*?href="/([^"]+?)"', a, re.DOTALL)
        if not href_m:
            continue
        name = href_m.group(1)
        desc_m = re.search(r'<p class="col-9 color-fg-muted[^"]*">\s*(.*?)\s*</p>', a, re.DOTALL)
        desc = html.unescape(re.sub(r'<[^>]+>', '', desc_m.group(1))).strip() if desc_m else ''
        lang_m = re.search(r'itemprop="programmingLanguage">([^<]+)</span>', a)
        lang = lang_m.group(1).strip() if lang_m else ''
        # total stars: inside stargazers link, text after svg
        stars = '?'
        sg_m = re.search(r'href="/' + re.escape(name) + r'/stargazers"[^>]*>.*?<svg.*?</svg>\s*([\d,]+)', a, re.DOTALL)
        if sg_m:
            stars = sg_m.group(1)
        # stars today/this week
        delta = ''
        d_m = re.search(r'([\d,]+)\s+stars?\s+(?:today|this week)', a)
        if d_m:
            delta = d_m.group(1)
        repos.append({'name': name, 'desc': desc[:220], 'stars': stars, 'lang': lang, 'delta': delta})
    return repos

daily = parse('trending_daily.html')
weekly = parse('trending_weekly.html')

print('=== DAILY ===')
for r in daily:
    print("%s | %s total | +%s today | %s | %s" % (r['name'], r['stars'], r['delta'], r['lang'], r['desc'][:100]))
print()
print('=== WEEKLY ===')
for r in weekly:
    print("%s | %s total | +%s wk | %s | %s" % (r['name'], r['stars'], r['delta'], r['lang'], r['desc'][:100]))
