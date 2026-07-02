import requests, re, warnings
warnings.filterwarnings('ignore')

r = requests.get(
    'https://mp.weixin.qq.com/s/08V4LPTEJe6n_AGxJHnaKw',
    verify=False, timeout=15,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)
html = r.text

# Extract title
title_m = re.search(r'var\s+msg_title\s*=\s*["\'](.+?)["\']', html)
if title_m:
    print(f'Title: {title_m.group(1)}')

# Extract nickname
nick = re.search(r'var\s+nickname\s*=\s*["\'](.+?)["\']', html)
if nick:
    print(f'Author: {nick.group(1)}')

# Extract js_content inner text
match = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
if match:
    body = re.sub(r'<[^>]+>', ' ', match.group(1))
    body = re.sub(r'&nbsp;', ' ', body)
    body = re.sub(r'\s+', ' ', body).strip()
    print(f'Content length: {len(body)}')
    print(f'\n=== CONTENT ===\n{body[:8000]}')
else:
    print('js_content not found, trying alternatives...')
    alt = re.search(r'id="js_content"[^>]*>(.*?)</div>', html, re.DOTALL)
    if alt:
        print(f'Alt match len: {len(alt.group(1))}')
        print(alt.group(1)[:1000])
    else:
        print('No matches at all')
        # search for any Chinese text
        chinese = re.findall(r'[\u4e00-\u9fff]{10,}', html)
        print(f'Chinese fragments: {chinese[:20]}')
