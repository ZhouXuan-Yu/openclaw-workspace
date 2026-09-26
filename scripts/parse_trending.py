import sys, re, json
from bs4 import BeautifulSoup

def parse(path):
    html = open(path, encoding='utf-8').read()
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('article.Box-row')
    out = []
    for r in rows:
        h2 = r.select_one('h2 a')
        if not h2:
            continue
        name = re.sub(r'\s+', '', h2.get_text())
        desc_el = r.select_one('p')
        desc = desc_el.get_text(' ', strip=True) if desc_el else ''
        # stars total
        star_link = r.select_one('a[href$="/stargazers"]')
        stars = star_link.get_text(strip=True) if star_link else ''
        # today/week stars
        today = ''
        for sp in r.select('span.d-inline-block.float-sm-right'):
            today = sp.get_text(' ', strip=True)
        lang_el = r.select_one('[itemprop="programmingLanguage"]')
        lang = lang_el.get_text(strip=True) if lang_el else ''
        out.append({'name': name, 'desc': desc, 'stars': stars, 'period': today, 'lang': lang})
    return out

for label, path in [('DAILY', sys.argv[1]), ('WEEKLY', sys.argv[2])]:
    print('=' * 20, label, '=' * 20)
    for i, it in enumerate(parse(path), 1):
        print(f"{i}. {it['name']} | {it['lang']} | total={it['stars']} | period={it['period']}")
        print(f"   {it['desc'][:200]}")
