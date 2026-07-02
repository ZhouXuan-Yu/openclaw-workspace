import requests

token = "GH_PAT_REMOVED"
headers = {
    "Accept": "application/vnd.github.v3.text-match+json",
    "Authorization": f"token {token}"
}

# Test with and without pushed filter
tests = [
    ("sk-or-v1- language:python", "no-date"),
    ("sk-or-v1- language:python pushed:>=2026-06-02", "date-jun"),
    ("OPENAI_API_KEY filename:.env pushed:>=2026-01-02", "date-jan"),
]

for q, label in tests:
    r = requests.get("https://api.github.com/search/code", headers=headers,
                     params={"q": q, "per_page": 5}, timeout=15)
    d = r.json()
    items = len(d.get("items", []))
    total = d.get("total_count", "?")
    limit_rem = r.headers.get("X-RateLimit-Remaining", "?")
    print(f"[{label}] status={r.status_code} total={total} items={items} rate_limit_rem={limit_rem}")
    if r.status_code != 200:
        print(f"  errors: {d.get('errors', d.get('message', '?'))}")
