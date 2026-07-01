import requests, base64, os
repo = 'x1xhlol/system-prompts-and-models-of-ai-tools'
out_dir = 'prompts_dump'
os.makedirs(out_dir, exist_ok=True)

for folder, prefix in [('Claude Code', 'Claude_Code'), ('Cursor Prompts', 'Cursor')]:
    print(f'\n{folder}:')
    r = requests.get(f'https://api.github.com/repos/{repo}/contents/{folder}', timeout=10)
    print(f'  Status: {r.status_code}')
    if r.status_code != 200:
        print(f'  Body: {r.text[:200]}')
        continue
    data = r.json()
    if isinstance(data, dict):
        print(f'  Got dict instead of list: {list(data.keys())[:5]}')
        continue
    for f in data:
        name = f.get('name', '?')
        size = f.get('size', 0)
        print(f'  {name} ({size} bytes)')
        if name.endswith('.txt') or name.endswith('.md'):
            fr = requests.get(f.get('url', ''), timeout=10)
            if fr.status_code == 200:
                fdata = fr.json()
                if fdata.get('encoding') == 'base64':
                    content = base64.b64decode(fdata['content']).decode('utf-8', errors='ignore')
                    with open(os.path.join(out_dir, f'{prefix}__{name}'), 'w', encoding='utf-8') as fp:
                        fp.write(content)
                    print(f'    -> saved {len(content)} chars')
