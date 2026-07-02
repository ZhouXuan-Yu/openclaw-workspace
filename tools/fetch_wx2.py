import requests, re

url = 'https://mp.weixin.qq.com/s/F5bm2MxNwPp196hs6VlBBQ'
r = requests.get(url, verify=False, timeout=15,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
html = r.text

# Title
tm = re.search(r'var\s+msg_title\s*=\s*["\'](.+?)["\']', html)
nk = re.search(r'var\s+nickname\s*=\s*["\'](.+?)["\']', html)
print(f'Title: {tm.group(1) if tm else "?"}')
print(f'Author: {nk.group(1) if nk else "?"}')

# Find all image URLs
imgs = re.findall(r'data-src="(https://mmbiz\.qpic\.cn/[^"]+)"', html)
print(f'Images found: {len(imgs)}')
for i, img in enumerate(imgs):
    print(f'  [{i+1}] {img}')

# Content
m = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<script', html, re.DOTALL)
if not m:
    m = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*</div', html, re.DOTALL)

if m:
    body = re.sub(r'<[^>]+>', ' ', m.group(1))
    body = re.sub(r'&nbsp;', ' ', body)
    body = re.sub(r'\s+', ' ', body).strip()
    print(f'\nContent length: {len(body)}')
    print(body[:12000])
else:
    print('Content NOT FOUND')
