import re, html, json, os

def parse(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    # Each repo block: <h2 class="h3 lh-condensed">...<a href="/owner/repo">
    # Extract article blocks
    articles = re.findall(r'<article class="Box-row">(.*?)</article>', content, re.S)
    repos = []
    for a in articles:
        m = re.search(r'href="/([^/"]+)/([^/"]+)"', a)
        if not m: continue
        owner, name = m.group(1), m.group(2)
        desc_m = re.search(r'<p class="col-9[^"]*">\s*(.*?)\s*</p>', a, re.S)
        desc = html.unescape(re.sub(r'<[^>]+>', '', desc_m.group(1))).strip() if desc_m else ''
        lang_m = re.search(r'itemprop="programmingLanguage">([^<]+)<', a)
        lang = lang_m.group(1) if lang_m else ''
        stars_m = re.search(r'([\d,.]+)\s+stars', a)
        stars = stars_m.group(1) if stars_m else ''
        forks_m = re.search(r'([\d,.]+)\s+forks', a)
        forks = forks_m.group(1) if forks_m else ''
        today_m = re.search(r'<span class="d-inline-block float-sm-right">([\d,.]+)\s+stars', a)
        today = today_m.group(1) if today_m else ''
        repos.append({'owner': owner, 'name': name, 'desc': desc, 'lang': lang,
                      'stars': stars, 'forks': forks, 'delta': today})
    return repos

d = parse(os.environ['TEMP'] + r'\trending_daily.html')
w = parse(os.environ['TEMP'] + r'\trending_weekly.html')
print("=== DAILY ===")
for r in d[:15]:
    print(f"{r['owner']}/{r['name']} | ⭐{r['stars']} (+{r['delta']}) | {r['lang']} | {r['desc'][:110]}")
print("\n=== WEEKLY ===")
for r in w[:15]:
    print(f"{r['owner']}/{r['name']} | ⭐{r['stars']} (+{r['delta']}) | {r['lang']} | {r['desc'][:110]}")
