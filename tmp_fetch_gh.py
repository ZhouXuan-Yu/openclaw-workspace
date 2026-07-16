import requests
import re

# 1. Fetch the repo README
urls = [
    'https://api.github.com/repos/oso95/scroll-world/readme',
    'https://api.github.com/repos/oso95/scroll-world/contents',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/vnd.github.v3+json',
}

# Get README
r = requests.get(urls[0], headers=headers, timeout=15)
if r.status_code == 200:
    import base64
    data = r.json()
    content = base64.b64decode(data['content']).decode('utf-8')
    print(f'===== README ({len(content)} chars) =====')
    print(content[:8000])
else:
    print(f'README status: {r.status_code}')
    # Try raw url
    r2 = requests.get('https://raw.githubusercontent.com/oso95/scroll-world/main/README.md', headers=headers, timeout=15)
    print(f'Raw README status: {r2.status_code}')
    if r2.status_code == 200:
        print(r2.text[:8000])
    else:
        r3 = requests.get('https://raw.githubusercontent.com/oso95/scroll-world/master/README.md', headers=headers, timeout=15)
        print(f'Master README status: {r3.status_code}')
        if r3.status_code == 200:
            print(r3.text[:8000])

# 2. Get repo files list
print('\n\n===== REPO STRUCTURE =====')
r4 = requests.get(urls[1], headers=headers, timeout=15)
if r4.status_code == 200:
    for item in r4.json():
        print(f"  {'📁' if item['type']=='dir' else '📄'} {item['name']}  ({item['type']})")
else:
    print(f'Contents status: {r4.status_code}')
