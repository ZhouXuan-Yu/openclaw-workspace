"""Test SiliconFlow key with full key from config"""
import urllib.request, json, os
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

with open(os.path.expanduser("~/.openclaw/openclaw.json"), encoding='utf-8') as f:
    cfg = json.load(f)

key = cfg['models']['providers']['siliconflow']['apiKey']
print(f"Key: {key[:15]}...{key[-8:]} len={len(key)}")

url = 'https://api.siliconflow.cn/v1/chat/completions'
body = json.dumps({
    'model': 'deepseek-ai/DeepSeek-V3',
    'messages': [{'role':'user','content':'say hi'}],
    'max_tokens': 10
}).encode('utf-8')

req = urllib.request.Request(url, data=body, method='POST')
req.add_header('Authorization', f'Bearer {key}')
req.add_header('Content-Type', 'application/json')

try:
    resp = urllib.request.urlopen(req, timeout=20)
    data = json.loads(resp.read())
    print('Key works! Reply:', data['choices'][0]['message']['content'].strip())
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'HTTP {e.code}: {body[:300]}')
except Exception as e:
    print(f'Error: {e}')
