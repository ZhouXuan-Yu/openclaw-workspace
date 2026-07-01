import requests, json, time

token='GH_TOKEN_REMOVED'
headers={'Accept':'application/vnd.github.v3.text-match+json','Authorization':f'token {token}'}

qs = ['OPENAI_API_KEY','DEEPSEEK_API_KEY','ANTHROPIC_API_KEY','QWEN_API_KEY','GOOGLE_API_KEY','GROQ_API_KEY','SILICONFLOW_API_KEY','HUGGING_FACE_HUB_TOKEN','MOONSHOT_API_KEY','ZHIPUAI_API_KEY','MINIMAX_API_KEY','PERPLEXITY_API_KEY','MISTRAL_API_KEY','REPLICATE_API_TOKEN','TOGETHER_API_KEY','FIREWORKS_API_KEY','DASHSCOPE_API_KEY','BAICHUAN_API_KEY','STEPFUN_API_KEY','SPARK_API_KEY','YI_API_KEY','SENSETIME_API_KEY','HUNYUAN_SECRET_KEY']

for q in qs:
    try:
        query = f'"{q}=***"'
        r = requests.get('https://api.github.com/search/code', headers=headers, params={'q': query}, timeout=15)
        items = r.json().get('items', [])
        print(f'{q}: {r.status_code} {len(items)} items')
        if r.status_code == 422:
            err = r.json()
            print(f'  -> {err}')
        if r.status_code == 403:
            reset = r.headers.get("X-RateLimit-Reset","?")
            print(f'  -> rate limit reset: {reset}')
        if r.status_code == 200 and items:
            for item in items[:2]:
                tm = item.get('text_matches', [{}])
                frag = tm[0].get('fragment','')[:80] if tm else ''
                print(f'  [{item["repository"]["full_name"]}] {item["path"]}: {frag}')
    except Exception as e:
        print(f'{q}: ERROR {e}')
    time.sleep(1)

r2 = requests.get('https://api.github.com/rate_limit', headers=headers)
print(f'\nRate limit: {json.dumps(r2.json(), indent=2)[:500]}')
