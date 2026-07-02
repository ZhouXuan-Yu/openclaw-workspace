import re

path = r'C:\Users\ZhouXuan\.openclaw\workspace\tools\github-key-scanner\daily_scan.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'def export_obsidian():\n    """Export only VERIFIED VALID keys to Obsidian vault"""\n    h = load_history()\n    sk = h["seen_keys"]\n    # Filter: only keys verified as valid\n    verified_sk = {k: v for k, v in sk.items() if v.get("verified") == "valid"}\n    if not verified_sk:\n        print("No verified valid keys to export")\n        return\n    by_provider = defaultdict(list)\n    for k, v in verified_sk.items():\n        by_provider[v["provider"]].append({**v, "key_id": k})'

new = 'def export_obsidian():\n    """Export ALL keys to Obsidian vault, grouped by provider + verification status"""\n    h = load_history()\n    sk = h["seen_keys"]\n    if not sk:\n        print("No keys to export")\n        return\n    by_provider = defaultdict(list)\n    for k, v in sk.items():\n        by_provider[v["provider"]].append({**v, "key_id": k})'

if old in content:
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK - replaced export_obsidian')
else:
    # check if it's already the new version
    if '"""Export ALL keys to Obsidian vault' in content:
        print('ALREADY PATCHED')
    else:
        print('NOT FOUND')
        for i, line in enumerate(content.splitlines()[290:303], 291):
            print(f'{i}: {repr(line)}')
