import requests, warnings
warnings.filterwarnings("ignore")

token = "GH_PAT_REMOVED"
headers = {"Accept": "application/vnd.github.v3.text-match+json", "Authorization": f"token {token}"}
proxy = {"http": "http://127.0.0.1:7898", "https": "http://127.0.0.1:7898"}

# Test 1: Search API with proxy
r = requests.get("https://api.github.com/search/code", headers=headers,
                 params={"q": "sk-or-v1- language:python", "per_page": 3},
                 proxies=proxy, timeout=15, verify=False)
print(f"[proxy + verify=false] status={r.status_code} total={r.json().get('total_count','?')} items={len(r.json().get('items',[]))}")

# Test 2: repo info with proxy
r2 = requests.get("https://api.github.com/repos/torvalds/linux", headers=headers,
                  proxies=proxy, timeout=10, verify=False)
print(f"[repo via proxy] status={r2.status_code}")
