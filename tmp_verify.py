# -*- coding: utf-8 -*-
import io, sys, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r'C:\Users\ZhouXuan\.openclaw\workspace'
# verify json
with open(os.path.join(base, r'memory\evolution\.skill-quality.json'), encoding='utf-8') as fh:
    j = json.load(fh)
mr = j['skills']['memory-reflection']
print('JSON OK | memory-reflection total:', mr['totalCalls'], 'success:', mr['successCalls'], '| lastUpdated:', j['lastUpdated'])
# verify daily tail
with open(os.path.join(base, r'memory\daily\2026-09-02.md'), encoding='utf-8') as fh:
    d = fh.read()
print('daily has #68:', '#68' in d, '| 反思 23:30' in d)
# verify evolution-log head
with open(os.path.join(base, r'memory\evolution\evolution-log.md'), encoding='utf-8') as fh:
    e = fh.read()
print('evolution-log has #68:', 'memory-reflection #68' in e)
# verify portrait
with open(r'E:\Obsidian仓库\ZhouXuan私人领域\人物画像.md', encoding='utf-8') as fh:
    p = fh.read()
print('portrait last_updated:', 'last_updated: 2026-09-02T23:30:00+08:00' in p, '| has #68 section:', '09-02 复盘（反射 #68）' in p)
# cleanup temp files
for fn in ['tmp_find_portrait.ps1', 'tmp_tail.ps1', 'tmp_tail.py', 'tmp_update_portrait.py']:
    fp = os.path.join(base, fn)
    if os.path.exists(fp):
        os.remove(fp)
print('temp cleaned')
