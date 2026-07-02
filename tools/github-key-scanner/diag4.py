import requests, warnings
warnings.filterwarnings("ignore")

token = "GH_PAT_REMOVED"
headers = {"Authorization": f"token {token}"}

tests = [
    "sk-or-v1- language:python",
    "sk-or-v1- language:python pushed:>=2026-01-02",
    "sk-or-v1- language:python pushed:>=2025-07-02",
    "OPENAI_API_KEY filename:.env",
    "OPENAI_API_KEY filename:.env pushed:>=2026-01-02",
]

for q in tests:
    r = requests.get("https://api.github.com/search/code", headers=headers,
                     params={"q": q, "per_page": 3}, timeout=15, verify=False)
    d = r.json()
    total = d.get("total_count", 0)
    items = len(d.get("items", []))
    print(f"[{total:>5} total, {items} items] {q[:60]}")
