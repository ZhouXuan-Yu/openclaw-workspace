import re, html

targets = ['tt-a1i/archify', 'freestylefly/awesome-gpt-image-2', 'THU-MAIC/OpenMAIC',
           'K-Dense-AI/scientific-agent-skills', 'tashfeenahmed/freellmapi',
           'omacom/omarchy', 'openai/codex', 'tinyhumansai/openhuman',
           'Alishahryar1/free-claude-code', 'every-app/open-seo', 'p-e-w/heretic',
           'apache/maka', 'mvanhorn/last30days-skill', 'livekit/agents']

for f in ['trending_weekly.html', 'trending_daily.html']:
    data = open(f, encoding='utf-8', errors='ignore').read()
    rows = re.findall(r'<article class="Box-row">(.*?)</article>', data, re.S)
    for r in rows:
        m = re.search(r'href="/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"', r)
        if not m:
            continue
        name = m.group(1)
        if name in targets:
            desc = re.search(r'<p[^>]*>(.*?)</p>', r, re.S)
            d = html.unescape(re.sub(r'<[^>]+>', '', desc.group(1))).strip() if desc else ''
            stars = re.search(r'([\d,]+)\s+stars', r)
            s = stars.group(1) if stars else '?'
            print(f'[{f[9:14]}] {name} | {s} | {d}')
            targets.remove(name)
