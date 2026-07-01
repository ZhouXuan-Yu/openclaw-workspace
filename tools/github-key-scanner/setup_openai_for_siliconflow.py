"""Rewrite OpenClaw config: use siliconflow as openai provider for image generation"""
import json, os

config_path = os.path.expanduser("~/.openclaw/openclaw.json")

with open(config_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

# Remove old siliconflow provider
d['models']['providers'].pop('siliconflow', None)

# Set openai provider to SiliconFlow
d['models']['providers']['openai'] = {
    'api': 'openai-images',
    'baseUrl': 'https://api.siliconflow.cn/v1',
    'apiKey': 'sk-rnl…cmsl',
    'models': [
        {'id': 'Qwen/Qwen-Image', 'name': 'Qwen Image'},
        {'id': 'Tongyi-MAI/Z-Image-Turbo', 'name': 'Z-Image Turbo'},
    ]
}

# Update imageGenerationModel to use Qwen Image via siliconflow
d['agents']['defaults']['imageGenerationModel'] = {
    'primary': 'openai/Qwen/Qwen-Image',
    'timeoutMs': 180000
}

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("✅ openai provider → SiliconFlow!")
