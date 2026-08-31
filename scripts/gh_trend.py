import json, urllib.request, sys

def fetch(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "Mozilla/5.0 (research)",
    })
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# 1. New repos (last 30 days) by stars
try:
    d = fetch("https://api.github.com/search/repositories?q=created:%3E2026-07-13&sort=stars&order=desc&per_page=30")
    print("=== NEW REPOS (30d) ===")
    for r in d.get("items", []):
        desc = (r.get("description") or "").replace("\n", " ")[:120]
        print(f"{r['full_name']} | {r['stargazers_count']} | {(r.get('language') or '?')} | {desc}")
except Exception as e:
    print("ERR new repos:", e)

# 2. Trending via api.github.com/search (proxy for trending) - hot repos last week
try:
    d = fetch("https://api.github.com/search/repositories?q=pushed:%3E2026-08-06+stars:%3E500&sort=stars&order=desc&per_page=30")
    print("\n=== HOT REPOS (pushed this week, >500 stars) ===")
    for r in d.get("items", []):
        desc = (r.get("description") or "").replace("\n", " ")[:120]
        print(f"{r['full_name']} | {r['stargazers_count']} | {(r.get('language') or '?')} | {desc}")
except Exception as e:
    print("ERR hot repos:", e)
