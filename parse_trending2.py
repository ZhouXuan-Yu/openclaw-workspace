import re, html, json

def parse(fn):
    with open(fn, encoding='utf-8') as f:
        content = f.read()
    # Split articles
    articles = re.split(r'<article', content)[1:]
    results = []
    for a in articles:
        m = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', a)
        if not m:
            continue
        repo = m.group(1).strip()
        # description
        dm = re.search(r'<p[^>]*class="col-9[^"]*"[^>]*>(.*?)</p>', a, re.S)
        desc = re.sub(r'<[^>]+>', '', dm.group(1)) if dm else ''
        desc = html.unescape(re.sub(r'\s+', ' ', desc)).strip()
        # language
        lm = re.search(r'itemprop="programmingLanguage">([^<]+)<', a)
        lang = lm.group(1).strip() if lm else ''
        # stars today
        sm = re.search(r'([\d,]+)\s+stars today', a)
        stars_today = sm.group(1).replace(',', '') if sm else '0'
        # total stars
        tm = re.search(r'aria-label="([\d,]+) users starred this repository"', a)
        total = tm.group(1).replace(',', '') if tm else ''
        results.append({'repo': repo, 'desc': desc, 'lang': lang, 'stars_today': stars_today, 'total': total})
    return results

daily = parse('trending_daily.html')
weekly = parse('trending_weekly.html')

def clean(results):
    seen = []
    for r in results:
        r['repo'] = r['repo'].replace('"', '').strip()
        seen.append(r)
    return seen

daily = clean(daily)
weekly = clean(weekly)

print("=== DAILY TOP 15 ===")
for r in daily[:15]:
    print(f"{r['repo']} | ⭐{r['total']} (+{r['stars_today']}) | {r['lang']} | {r['desc'][:100]}")

print()
print("=== WEEKLY TOP 15 ===")
for r in weekly[:15]:
    print(f"{r['repo']} | ⭐{r['total']} (+{r['stars_today']}) | {r['lang']} | {r['desc'][:100]}")

with open('trending_data.json', 'w', encoding='utf-8') as f:
    json.dump({'daily': daily, 'weekly': weekly}, f, ensure_ascii=False, indent=1)
