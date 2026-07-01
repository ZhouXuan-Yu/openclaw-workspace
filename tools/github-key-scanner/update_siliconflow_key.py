"""Update SiliconFlow API key in OpenClaw config"""
import json, os

config_path = os.path.expanduser("~/.openclaw/openclaw.json")

with open(config_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

d['models']['providers']['siliconflow']['apiKey'] = 'sk-rnl…cmsl'

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("✅ SiliconFlow key updated - full key configured")
