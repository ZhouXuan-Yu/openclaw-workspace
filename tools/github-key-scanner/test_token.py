import os, requests
t = os.environ.get("GITHUB_TOKEN", "")
h = {"Accept": "application/vnd.github.v3.text-match+json", "Authorization": f"token {t}"}
queries = [
    "api_key filename:.env pushed:>2026-06-25",
    "sk- filename:.env pushed:>2026-06-25",
    "OPENAI_API_KEY language:python pushed:>2026-06-26",
    "sk-ant- pushed:>2026-06-26",
    "api_key filename:config.py pushed:>2026-06-25",
    "secret filename:.env pushed:>2026-06-26",
    "api_key dockerfile pushed:>2026-06-26",
]
for q in queries:
    r = requests.get("https://api.github.com/search/code", headers=h, params={"q": q, "per_page": 3}, timeout=15)
    tc = r.json().get("total_count", "err")
    rate = r.headers.get("X-RateLimit-Remaining", "?")
    print(f"[{r.status_code}] {q[:65]:<65} {tc:>8} results  rate={rate}")
