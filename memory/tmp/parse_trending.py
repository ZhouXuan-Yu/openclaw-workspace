import json, sys

def parse(fn, limit=15):
    with open(fn, encoding='utf-8') as f:
        data = json.load(f)
    print(f"== {fn} total={data.get('total_count')}")
    for r in data['items'][:limit]:
        desc = (r.get('description') or '').replace('\n', ' ')[:110]
        lang = r.get('language') or '?'
        print(f"{r['full_name']} | {r['stargazers_count']}star | {lang} | created {r['created_at'][:10]} | {desc}")

if __name__ == '__main__':
    parse(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 15)
