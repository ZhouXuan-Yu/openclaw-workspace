import requests, time, json
r = requests.get('https://api.github.com/rate_limit', timeout=10)
d = r.json()['resources']['core']
remaining = d['remaining']
reset = d['reset']
now = int(time.time())
wait = max(reset - now, 0)
print(f"Remaining: {remaining}/{d['limit']}")
print(f"Reset in: {wait}s ({wait//60}m)")
