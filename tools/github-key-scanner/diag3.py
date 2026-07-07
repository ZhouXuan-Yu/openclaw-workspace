import os, requests, warnings, json
warnings.filterwarnings("ignore")

token = os.environ.get("GITHUB_TOKEN", "")
headers = {"Authorization": f"token {token}"}

# Same query as daily_scan.py uses
cutoff = "2026-01-02"
q1 = f"sk-or-v1- language:python pushed:>={cutoff}"

r = requests.get("https://api.github.com/search/code", headers=headers,
                 params={"q": q1, "per_page": 3}, timeout=15, verify=False)
d = r.json()
print(f"status={r.status_code} total={d.get('total_count')} items={len(d.get('items',[]))}")
if d.get('items'):
    for it in d['items'][:2]:
        print(f"  {it['repository']['full_name']}/{it['path']}")
        tms = it.get('text_matches', [])
        if tms:
            frag = "".join(tm.get('fragment', '') for tm in tms)
            # Check if our regex matches
            import re
            keys = re.findall(r"sk-or-v1-[A-Za-z0-9]{20,}", frag)
            print(f"    regex match in fragment: {len(keys)} keys: {keys[:2]}")
        else:
            print(f"    NO text_matches")
else:
    print(f"  response keys: {list(d.keys())}")
    if 'errors' in d:
        print(f"  errors: {d['errors']}")
