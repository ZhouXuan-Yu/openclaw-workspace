import json

checks = {}

# SKILL.md
with open(r'C:\Users\ZhouXuan\.openclaw\workspace\skills\guizang-social-card\SKILL.md', 'r', encoding='utf-8') as f:
    c = f.read()
checks['Density Gate in SKILL.md'] = 'Density Gate' in c and 'data-components' in c

# layout-recipes
with open(r'C:\Users\ZhouXuan\.openclaw\workspace\skills\guizang-social-card\references\layout-recipes.md', 'r', encoding='utf-8') as f:
    lr = f.read()
for r in ['S13', 'S14', 'S15', 'KPI Tower', 'H-Bar Comparison', 'Comparison Matrix']:
    checks[f'S13-S15: {r}'] = r in lr

# components
with open(r'C:\Users\ZhouXuan\.openclaw\workspace\skills\guizang-social-card\references\components.md', 'r', encoding='utf-8') as f:
    comp = f.read()
for cls in ['.kpi-insight', '.h-bar-group', '.h-bar', '.compare-matrix', '.change-up', '.change-down']:
    checks[f'component: {cls}'] = cls in comp

# qa-checklist
with open(r'C:\Users\ZhouXuan\.openclaw\workspace\skills\guizang-social-card\references\qa-checklist.md', 'r', encoding='utf-8') as f:
    qa = f.read()
for d in ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']:
    checks[f'qa: {d}'] = d in qa

# template
with open(r'C:\Users\ZhouXuan\.openclaw\workspace\skills\guizang-social-card\assets\template-swiss-card.html', 'r', encoding='utf-8') as f:
    tmpl = f.read()
for cls in ['kpi-stack', 'h-bar-group', 'compare-matrix', 'change-up']:
    checks[f'template: {cls}'] = cls in tmpl

# data-components + density-gate existence
import os
checks['data-components.md exists'] = os.path.exists(r'C:\Users\ZhouXuan\.openclaw\workspace\skills\guizang-social-card\references\data-components.md')
checks['density-gate.md exists'] = os.path.exists(r'C:\Users\ZhouXuan\.openclaw\workspace\skills\guizang-social-card\references\density-gate.md')

all_pass = all(checks.values())
for k, v in checks.items():
    print(f'  {"OK" if v else "FAIL"} {k}')
print(f'\nTotal: {len(checks)} checks, {sum(1 for v in checks.values() if v)} pass, {sum(1 for v in checks.values() if not v)} fail')
print(f'Result: {"ALL PASS" if all_pass else "SOME FAILED - see above"}')
