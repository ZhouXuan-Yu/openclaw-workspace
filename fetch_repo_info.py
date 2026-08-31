import urllib.request, json

repos = ['cloudflare/computer','TencentCloud/TencentDB-Agent-Memory','firecrawl/pdf-inspector',
         'esengine/DeepSeek-Reasonix','obra/superpowers','uber/ADR','huangruiteng/loopx',
         'different-ai/openwork','citrolabs/ego-lite','zhaoxuya520/reverse-skill',
         'virgiliojr94/book-to-skill','addyosmani/agent-skills','block/buzz','1jehuang/jcode']
for r in repos:
    try:
        req = urllib.request.Request('https://api.github.com/repos/'+r,
                                     headers={'User-Agent':'Mozilla/5.0','Accept':'application/vnd.github+json'})
        d = json.load(urllib.request.urlopen(req, timeout=15))
        desc = (d.get('description') or '')[:90]
        print(f"{r} | stars={d['stargazers_count']} | created={d['created_at'][:10]} | pushed={d['pushed_at'][:10]} | lang={d.get('language')} | {desc}")
    except Exception as e:
        print(r, 'ERR', e)
