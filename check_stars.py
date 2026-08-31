import re

c = open('trending_daily.html', encoding='utf-8').read()
# For each repo, find stargazers link and the following number
for repo in ['mattpocock/skills', 'obra/superpowers', 'addyosmani/agent-skills', 'PrimeIntellect-ai/prime-agent', 'cloudflare/computer', '666ghj/MiroFish', 'goauthentik/authentik']:
    i = c.find('/' + repo + '/stargazers')
    if i == -1:
        print(repo, 'NOT FOUND')
        continue
    seg = c[i:i+3000]
    nums = re.findall(r'([\d,]+)', seg)
    # The star count usually appears as aria-label="X users starred" or plain number after svg
    m = re.search(r'aria-label="([\d,]+)[^"]*starred', seg)
    if not m:
        # plain number right after the svg path end
        m2 = re.search(r'</svg>\s*</span>\s*<span[^>]*>\s*([\d,]+)', seg) or re.search(r'</svg>\s*([\d,]+)', seg)
        val = m2.group(1) if m2 else '?'
    else:
        val = m.group(1)
    print(repo, '=>', val)
