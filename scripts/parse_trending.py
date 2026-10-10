import re, sys, html, json

def parse(path):
    s = open(path, encoding='utf-8').read()
    arts = re.split(r'<article class="Box-row">', s)[1:]
    out = []
    for a in arts:
        m = re.search(r'href="/([^"/]+/[^"/]+)"\s+data-view-component="true" class="Link"', a)
        if not m:
            m = re.search(r'<h2[^>]*>.*?href="/([^"/]+/[^"/]+)"', a, re.S)
        if not m: continue
        repo = m.group(1)
        d = re.search(r'<p class="col-9 color-fg-muted my-1 tmp-pr-4">\s*(.*?)\s*</p>', a, re.S)
        desc = re.sub(r'<[^>]+>', '', d.group(1)).strip() if d else ''
        lang = re.search(r'itemprop="programmingLanguage">([^<]+)</span>', a)
        lang = lang.group(1) if lang else ''
        stars = re.search(r'/stargazers"[^>]*>.*?</svg>\s*([\d,]+)', a, re.S)
        total = stars.group(1) if stars else '?'
        gain = re.search(r'([\d,]+)\s*stars?\s*(today|this week)', a)
        gain = gain.group(0).replace('\n',' ').strip() if gain else ''
        out.append({'repo':repo,'desc':html.unescape(desc),'lang':lang,'stars':total,'gain':gain})
    return out

if __name__ == '__main__':
    data = parse(sys.argv[1])
    print(json.dumps(data, ensure_ascii=False, indent=1))
