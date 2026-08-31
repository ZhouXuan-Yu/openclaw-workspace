#!/usr/bin/env python3
"""Fallback collector: GitHub trending + Chinese RSS (when web_search is down)."""
import urllib.request, re, html, json, sys

def get(url, timeout=15):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    })
    return urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8', 'ignore')

out = {"github_trending": [], "rss": {}}

# GitHub trending
try:
    h = get('https://github.com/trending?since=weekly')
    # repo rows: article with h2 a href="/owner/name"
    blocks = re.findall(r'<article class="Box-row">(.*?)</article>', h, re.S)
    if not blocks:
        blocks = re.split(r'<article', h)[1:]
    for b in blocks[:20]:
        m = re.search(r'href="/([^"/]+/[^"/]+)"', b)
        if not m:
            continue
        name = m.group(1)
        desc_m = re.search(r'<p class="col-9[^"]*"[^>]*>(.*?)</p>', b, re.S)
        desc = html.unescape(re.sub(r'<[^>]+>', '', desc_m.group(1))).strip() if desc_m else ''
        lang_m = re.search(r'itemprop="programmingLanguage">([^<]+)<', b)
        lang = lang_m.group(1).strip() if lang_m else ''
        stars_m = re.search(r'([\d,]+)\s+stars', b)
        stars = stars_m.group(1) if stars_m else ''
        out["github_trending"].append({"repo": name, "lang": lang, "stars": stars, "desc": desc[:160]})
    print("GH_OK", len(out["github_trending"]))
except Exception as e:
    print("GH_ERR", str(e)[:100])

# RSS feeds
feeds = {
    'jiqizhixin': 'https://www.jiqizhixin.com/rss',
    '36kr': 'https://36kr.com/feed',
    'ithome': 'https://www.ithome.com/rss/',
    'qbitai': 'https://www.qbitai.com/feed',
}
try:
    import feedparser
    for name, u in feeds.items():
        try:
            d = feedparser.parse(u)
            entries = [{"title": e.get('title', '')[:120], "link": e.get('link', '')[:200]} for e in d.entries[:10]]
            out["rss"][name] = entries
            print("RSS_OK", name, len(entries))
        except Exception as e:
            print("RSS_ERR", name, str(e)[:80])
except ImportError:
    print("NO_FEEDPARSER")

with open('memory/daily/research/fallback-collect.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("SAVED")
