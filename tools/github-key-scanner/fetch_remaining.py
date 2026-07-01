import requests, base64, os
repo = 'x1xhlol/system-prompts-and-models-of-ai-tools'
out_dir = 'prompts_dump'
os.makedirs(out_dir, exist_ok=True)

# Claude Code
r = requests.get(f'https://api.github.com/repos/{repo}/contents/Claude Code', timeout=10)
print('Claude Code:')
for f in r.json():
    print(f'  {f["name"]} ({f.get("size",0)} bytes)')
    if f['name'].endswith('.txt'):
        fr = requests.get(f['url'], timeout=10)
        if fr.status_code == 200:
            data = fr.json()
            content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
            with open(os.path.join(out_dir, 'Claude_Code__' + f['name']), 'w', encoding='utf-8') as fp:
                fp.write(content)
            print(f'    -> saved {len(content)} chars')

# Cursor
r = requests.get(f'https://api.github.com/repos/{repo}/contents/Cursor Prompts', timeout=10)
print('\nCursor:')
for f in r.json():
    print(f'  {f["name"]} ({f.get("size",0)} bytes)')
    if f['name'].endswith('.txt'):
        fr = requests.get(f['url'], timeout=10)
        if fr.status_code == 200:
            data = fr.json()
            content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
            with open(os.path.join(out_dir, 'Cursor__' + f['name']), 'w', encoding='utf-8') as fp:
                fp.write(content)
            print(f'    -> saved {len(content)} chars')
