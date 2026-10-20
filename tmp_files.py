import json, sys
sys.path.insert(0, 'tools')
from younavi_bridge import YouNavi
yn = YouNavi()
r = yn.file_list()
items = (r.get('data') or {}).get('data') or []
items.sort(key=lambda x: x.get('created_at') or '', reverse=True)
print('FILES', len(items))
for f in items[:15]:
    print((f.get('created_at') or '')[:16], '|', f.get('file_type'), '|', f.get('source'), '|', (f.get('name') or '')[:60])
aud = [f for f in items if (f.get('file_type') or '').lower() in ('m4a','mp3','wav','aac','flac')]
print('AUDIO COUNT', len(aud))
for f in aud[:10]:
    print('  AUDIO', (f.get('created_at') or '')[:16], f.get('name'), f.get('absolute_path'))
