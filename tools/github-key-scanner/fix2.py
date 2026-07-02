path = r'C:\Users\ZhouXuan\.openclaw\workspace\tools\github-key-scanner\daily_scan.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace lines 291-302 (0-indexed: 290-301) with new block
new_block = [
    'def export_obsidian():\n',
    '    """Export ALL keys to Obsidian vault, grouped by provider + verification status"""\n',
    '    h = load_history()\n',
    '    sk = h["seen_keys"]\n',
    '    if not sk:\n',
    '        print("No keys to export")\n',
    '        return\n',
    '    by_provider = defaultdict(list)\n',
    '    for k, v in sk.items():\n',
    '        by_provider[v["provider"]].append({**v, "key_id": k})\n',
]

lines[290:302] = new_block

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('OK')
