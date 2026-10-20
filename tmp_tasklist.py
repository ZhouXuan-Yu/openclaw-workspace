import json, sys
sys.path.insert(0, 'tools')
from younavi_bridge import YouNavi
yn = YouNavi()
r = yn.task_list()
d = r.get('data') or {}
items = d.get('data') or []
print('TOTAL', len(items))
for t in items[:12]:
    print(t.get('created_at','')[:16], '|', t.get('status'), '|', t.get('task_type'), '|', (t.get('command_message') or '').replace('\n',' ')[:70])
print('--- newest created_at:', max(x.get('created_at','') for x in items) if items else None)
print()
r2 = yn.file_list()
d2 = r2.get('data') or {}
items2 = d2.get('data') or []
print('FILES type', type(items2), len(items2) if hasattr(items2,'__len__') else '')
print(json.dumps(d2, ensure_ascii=False)[:1500])
