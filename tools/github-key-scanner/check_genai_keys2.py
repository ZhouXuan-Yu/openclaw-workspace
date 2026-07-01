"""Quick script to search leaked Gemini/Google AI keys on GitHub"""
import urllib.request, json, os

os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

TOKEN = "ghp_PWmzAMGWvyCKuRx0XLiJCC7gFnSM9jf0DA6"
HEADERS = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f'Bearer {TOKEN}'
}

# Known leaked key to check against
known_key = "AIzaSyDU"

# Try to find if this key is still in repos
queries = [
    ('AIzaSyDU+nzDs', 'Known Google AI key'),
    ('AIzaSy', 'Google AI keys (generic)'),
]

urls = [
    'https://api.github.com/search/code?q=AIzaSyDU&per_page=5',
]

for url_str in urls:
    req = urllib.request.Request(url_str, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        print(f'Total found: {data.get("total_count", 0)}')
        for item in data.get('items', [])[:5]:
            print(f'  [{item["repository"]["full_name"]}] {item["path"]}')
            print(f'    → {item["html_url"]}')
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'ERROR {e.code}: {body[:200]}')

# Also try to get raw content of the key file to verify if key is still valid
print('\nChecking known leak file...')
file_url = 'https://raw.githubusercontent.com/Mahmoud2design/graphico-brief/5c76ea818158bb723b6bc49f18160e4a15977868/.env.txt'
req2 = urllib.request.Request(file_url)
try:
    resp2 = urllib.request.urlopen(req2)
    content = resp2.read().decode()
    print(f'File content:')
    print(content[:500])
except Exception as e:
    print(f'Cannot fetch: {e}')

print('\nDone!')
