path = r'C:\Users\ZhouXuan\.openclaw\workspace\tools\github-key-scanner\daily_scan.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# line 298 has emoji: print("\U0001f4c1 No verified valid keys to export")
old = content[content.index('def export_obsidian():'):content.index('def export_obsidian():') + 700]

# Find the exact block
lines = content.splitlines()
start = None
for i, line in enumerate(lines):
    if 'def export_obsidian():' in line:
        start = i
        break

# The block is lines 291-302 (0-indexed: 290-301)
block_lines = lines[290:302]
print(f"Block is {len(block_lines)} lines")
for l in block_lines:
    print(repr(l))
print()

# verify the line 298 emoji
print(f"Line 298: {repr(lines[297])}")
