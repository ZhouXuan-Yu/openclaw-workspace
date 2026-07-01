"""Add SiliconFlow provider to OpenClaw config"""
import json, os

config_path = os.path.expanduser("~/.openclaw/openclaw.json")

with open(config_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

# Add siliconflow to providers
d.setdefault('models', {}).setdefault('providers', {})
d['models']['providers']['siliconflow'] = {
    'api': 'openai-completions',
    'baseUrl': 'https://api.siliconflow.cn/v1',
    'apiKey': 'sk-rnlnqlpmhvpafdnqdhwlkxoesfwdowsmefizeygmiotpcmsl',
    'models': [
        {'id': 'Qwen/Qwen-Image', 'name': 'Qwen Image', 'maxTokens': 4096},
        {'id': 'black-forest-labs/FLUX.1-schnell', 'name': 'FLUX.1-schnell', 'maxTokens': 4096},
        {'id': 'Kolors/Kolors', 'name': 'Kolors', 'maxTokens': 4096},
    ]
}

# Add imageGenerationModel config
d.setdefault('agents', {}).setdefault('defaults', {})
d['agents']['defaults']['imageGenerationModel'] = {
    'primary': 'siliconflow/Qwen/Qwen-Image',
    'timeoutMs': 180000
}

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("✅ SiliconFlow provider added!")
print(f"Primary model: siliconflow/Qwen/Qwen-Image")
