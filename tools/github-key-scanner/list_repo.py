import requests, json
r = requests.get('https://api.github.com/repos/x1xhlol/system-prompts-and-models-of-ai-tools/contents/', timeout=15)
data = r.json()
for item in data:
    t = 'DIR' if item['type'] == 'dir' else 'FILE'
    print(f"{t} {item['name']}")
