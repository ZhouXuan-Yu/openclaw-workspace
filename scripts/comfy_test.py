"""
ComfyDesktop 连接测试 v2 - Z-Image-Turbo UNET 模式
使用 UNETLoader + CLIPLoader + VAELoader 替代 CheckpointLoaderSimple
"""
import requests, json, uuid, time, sys

BASE = "http://127.0.0.1:8188"

# Z-Image-Turbo 工作流：UNET + CLIP + VAE 独立加载
workflow = {
    # 加载 UNET (diffusion model)
    "unet_loader": {
        "inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"},
        "class_type": "UNETLoader",
        "_meta": {"title": "Load UNET"}
    },
    # 加载 CLIP (text encoder)
    "clip_loader": {
        "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "qwen_image", "device": "default"},
        "class_type": "CLIPLoader",
        "_meta": {"title": "Load CLIP"}
    },
    # 加载 VAE
    "vae_loader": {
        "inputs": {"vae_name": "ae.safetensors"},
        "class_type": "VAELoader",
        "_meta": {"title": "Load VAE"}
    },
    # Positive prompt
    "pos_prompt": {
        "inputs": {"text": "A beautiful mountain landscape at golden hour, professional photography, 4K, masterpiece, crystal clear", "clip": ["clip_loader", 0]},
        "class_type": "CLIPTextEncode",
        "_meta": {"title": "Positive Prompt"}
    },
    # Negative prompt
    "neg_prompt": {
        "inputs": {"text": "low quality, blurry, distorted, ugly, watermark", "clip": ["clip_loader", 0]},
        "class_type": "CLIPTextEncode",
        "_meta": {"title": "Negative Prompt"}
    },
    # Latent image
    "latent": {
        "inputs": {"width": 1024, "height": 1024, "batch_size": 1},
        "class_type": "EmptyLatentImage",
        "_meta": {"title": "Empty Latent"}
    },
    # KSampler
    "sampler": {
        "inputs": {"seed": 42, "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0, "model": ["unet_loader", 0], "positive": ["pos_prompt", 0], "negative": ["neg_prompt", 0], "latent_image": ["latent", 0]},
        "class_type": "KSampler",
        "_meta": {"title": "KSampler"}
    },
    # VAE Decode
    "decode": {
        "inputs": {"samples": ["sampler", 0], "vae": ["vae_loader", 0]},
        "class_type": "VAEDecode",
        "_meta": {"title": "VAE Decode"}
    },
    # Save
    "save": {
        "inputs": {"filename_prefix": "openclaw_test", "images": ["decode", 0]},
        "class_type": "SaveImage",
        "_meta": {"title": "Save Image"}
    }
}

prompt = {"prompt": workflow, "client_id": str(uuid.uuid4())[:8]}
print(f"Submitting Z-Image-Turbo workflow...")
r = requests.post(f"{BASE}/prompt", json=prompt, timeout=30)
result = r.json()

if ("node_errors" in result and result["node_errors"]) or ("error" in result and not "prompt_id" in result):
    print(f"Errors: {json.dumps(result, indent=2, ensure_ascii=False)}")
    # 尝试查找模型实际路径
    for k, v in result.get("node_errors", {}).items():
        for e in v.get("errors", []):
            if "not in" in e.get("message", ""):
                print(f"\nModel search path issue at node {k}")
    sys.exit(1)

prompt_id = result["prompt_id"]
print(f"Submitted, prompt_id: {prompt_id}")

for i in range(30):
    time.sleep(2)
    r = requests.get(f"{BASE}/history/{prompt_id}", timeout=10)
    history = r.json()
    if prompt_id in history:
        h = history[prompt_id]
        status = h.get("status", {})
        print(f"Status: {status.get('status_str', 'unknown')}")
        if status.get("completed") == True:
            outputs = h.get("outputs", {})
            node_ids = list(outputs.keys())
            for nid in node_ids:
                imgs = outputs[nid].get("images", [])
                for img in imgs:
                    fname = img["filename"]
                    full = f"C:\\Users\\ZhouXuan\\ComfyUI-Shared\\output\\{fname}"
                    print(f"Image: {fname}")
                    print(f"Full:  {full}")
            sys.exit(0)
        else:
            print(f"Failed: {status}")
            sys.exit(1)

    print(f"Poll {i+1}...")

print("Timeout")
