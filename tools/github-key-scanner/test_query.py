import requests
t = "GH_PAT_REMOVED"
h = {"Accept": "application/vnd.github.v3.text-match+json", "Authorization": f"token {t}"}
queries = [
    "OPENAI_API_KEY filename:.env",
    "sk- filename:.env",
    "ANTHROPIC_API_KEY",
    "DEEPSEEK_API_KEY filename:.env",
    "GEMINI_API_KEY filename:.env",
    "api_key filename:config.py",
    "api_key filename:constants",
    "sk-ant- language:python",
]
for q in queries:
    r = requests.get("https://api.github.com/search/code", headers=h, params={"q": q, "per_page": 5}, timeout=15)
    if r.ok:
        tc = r.json().get("total_count", 0)
        items = r.json().get("items", [])
        if items:
            item = items[0]
            print(f"[OK] {q[:55]:<55} {tc:>6} results  first: {item['repository']['full_name']}/{item['path']}")
        else:
            print(f"[OK] {q[:55]:<55} {tc:>6} results")
    else:
        print(f"[{r.status_code}] {q[:55]:<55} {r.text[:100]}")
