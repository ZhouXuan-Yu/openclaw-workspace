"""Quick script to search leaked Gemini/Google AI keys on GitHub"""
import urllib.request, json

TOKEN = "ghp_PWmzAMGWvyCKuRx0XLiJCC7gFnSM9jf0DA6"
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'Bearer {TOKEN}'
}

queries = [
    ('AIzaSy', 'Google AI / Gemini'),
    ('sk-proj-', 'OpenAI Project Key'),
    ('sk-svc', 'OpenAI Service Key'),
]

for query, label in queries:
    url = f'https://api.github.com/search/code?q={query}+extension:env+extension:txt+extension:md&per_page=5'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        print(f'\n## {label} (query: {query})')
        print(f'Total: {data.get("total_count", 0)}')
        for item in data.get('items', [])[:5]:
            print(f'  [{item["repository"]["full_name"]}] {item["path"]}')
            print(f'    → {item["html_url"]}')
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f'\n## {label} — RATE LIMITED')
        elif e.code == 422:
            print(f'\n## {label} — Invalid query (likely too short)')
        else:
            print(f'\n## {label} — Error {e.code}')

print('\nDone!')
