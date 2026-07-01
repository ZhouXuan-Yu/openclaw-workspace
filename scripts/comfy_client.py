"""
comfyui-skill 核心客户端
提供 txt2img 和 img2img 能力，直接调用 ComfyDesktop HTTP API
"""
import requests
import json
import uuid
import time
import sys
from pathlib import Path

BASE = "http://127.0.0.1:8188"
WORKSPACE = Path(__file__).parent.parent.parent
OUTPUT_DIR = Path.home() / "ComfyUI-Shared" / "output"

# ===== 预定义 Workflow 模板 =====

TXT2IMG = {
    "unet_loader": {"inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}, "class_type": "UNETLoader"},
    "clip_loader": {"inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "qwen_image", "device": "default"}, "class_type": "CLIPLoader"},
    "vae_loader": {"inputs": {"vae_name": "ae.safetensors"}, "class_type": "VAELoader"},
    "pos": {"inputs": {"text": "", "clip": ["clip_loader", 0]}, "class_type": "CLIPTextEncode"},
    "neg": {"inputs": {"text": "low quality, blurry, distorted, ugly, watermark", "clip": ["clip_loader", 0]}, "class_type": "CLIPTextEncode"},
    "latent": {"inputs": {"width": 1024, "height": 1024, "batch_size": 1}, "class_type": "EmptyLatentImage"},
    "sampler": {"inputs": {"seed": 42, "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0, "model": ["unet_loader", 0], "positive": ["pos", 0], "negative": ["neg", 0], "latent_image": ["latent", 0]}, "class_type": "KSampler"},
    "decode": {"inputs": {"samples": ["sampler", 0], "vae": ["vae_loader", 0]}, "class_type": "VAEDecode"},
    "save": {"inputs": {"filename_prefix": "comfy_txt2img", "images": ["decode", 0]}, "class_type": "SaveImage"},
}

IMG2IMG = {
    "unet_loader": {"inputs": {"unet_name": "z_image_turbo_bf16.safetensors", "weight_dtype": "default"}, "class_type": "UNETLoader"},
    "clip_loader": {"inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "qwen_image", "device": "default"}, "class_type": "CLIPLoader"},
    "vae_loader": {"inputs": {"vae_name": "ae.safetensors"}, "class_type": "VAELoader"},
    "load_image": {"inputs": {"image": ""}, "class_type": "LoadImage"},
    "vae_encode": {"inputs": {"pixels": ["load_image", 0], "vae": ["vae_loader", 0]}, "class_type": "VAEEncode"},
    "pos": {"inputs": {"text": "", "clip": ["clip_loader", 0]}, "class_type": "CLIPTextEncode"},
    "neg": {"inputs": {"text": "low quality, blurry, distorted", "clip": ["clip_loader", 0]}, "class_type": "CLIPTextEncode"},
    "sampler": {"inputs": {"seed": 42, "steps": 4, "cfg": 2.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 0.35, "model": ["unet_loader", 0], "positive": ["pos", 0], "negative": ["neg", 0], "latent_image": ["vae_encode", 0]}, "class_type": "KSampler"},
    "decode": {"inputs": {"samples": ["sampler", 0], "vae": ["vae_loader", 0]}, "class_type": "VAEDecode"},
    "save": {"inputs": {"filename_prefix": "comfy_enhance", "images": ["decode", 0]}, "class_type": "SaveImage"},
}


def submit(workflow):
    r = requests.post(f"{BASE}/prompt", json={"prompt": workflow, "client_id": str(uuid.uuid4())[:8]}, timeout=30)
    data = r.json()
    if "error" in data and "prompt_id" not in data:
        raise RuntimeError(json.dumps(data["error"], ensure_ascii=False))
    return data["prompt_id"]

def wait(prompt_id, timeout_sec=60):
    for i in range(timeout_sec // 2):
        time.sleep(2)
        r = requests.get(f"{BASE}/history/{prompt_id}", timeout=10)
        if prompt_id in r.json():
            h = r.json()[prompt_id]
            if h.get("status", {}).get("completed"):
                return h
            if h.get("status", {}).get("status_str") == "error":
                raise RuntimeError(f"Generation failed: {h.get('status')}")
    raise TimeoutError("Generation timed out")


def txt2img(prompt, negative=None, seed=None, width=1024, height=1024, steps=4, cfg=1.0, filename_prefix="comfy_txt2img"):
    """生成图片，返回输出路径列表"""
    wf = json.loads(json.dumps(TXT2IMG))  # deep copy
    wf["pos"]["inputs"]["text"] = prompt
    if negative:
        wf["neg"]["inputs"]["text"] = negative
    wf["latent"]["inputs"]["width"] = width
    wf["latent"]["inputs"]["height"] = height
    wf["sampler"]["inputs"]["seed"] = seed if seed is not None else hash(prompt) % 2**31
    wf["sampler"]["inputs"]["steps"] = steps
    wf["sampler"]["inputs"]["cfg"] = cfg
    wf["save"]["inputs"]["filename_prefix"] = filename_prefix

    prompt_id = submit(wf)
    result = wait(prompt_id)
    outputs = []
    for node_id in result.get("outputs", {}):
        for img in result["outputs"][node_id].get("images", []):
            outputs.append(str(OUTPUT_DIR / img["filename"]))
    return outputs


def img2img(image_path, prompt, denoise=0.35, seed=None, steps=4, filename_prefix="comfy_enhance"):
    """图生图/精修，对输入图片做风格增强"""
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Input image not found: {image_path}")

    # 先上传图片到 ComfyUI input 目录
    input_dir = Path.home() / "ComfyUI-Shared" / "input"
    import shutil
    dst = input_dir / f"input_{uuid.uuid4().hex[:8]}.png"
    shutil.copy2(image_path, dst)

    wf = json.loads(json.dumps(IMG2IMG))
    wf["load_image"]["inputs"]["image"] = dst.name
    wf["pos"]["inputs"]["text"] = prompt
    wf["sampler"]["inputs"]["denoise"] = denoise
    wf["sampler"]["inputs"]["seed"] = seed if seed is not None else hash(prompt) % 2**31
    wf["sampler"]["inputs"]["steps"] = steps
    wf["save"]["inputs"]["filename_prefix"] = filename_prefix

    prompt_id = submit(wf)
    result = wait(prompt_id)
    outputs = []
    for node_id in result.get("outputs", {}):
        for img in result["outputs"][node_id].get("images", []):
            outputs.append(str(OUTPUT_DIR / img["filename"]))
    return outputs


def enhance_video_frame(frame_path, preserve_strength=0.75):
    """对视频帧做轻量画质增强（高保真模式）"""
    return img2img(
        image_path=frame_path,
        prompt="masterpiece, best quality, high resolution, crystal clear, professional photography, detailed texture, vibrant colors, sharp focus",
        denoise=1.0 - preserve_strength,  # 保真度越高，去噪越低
        steps=4,
        filename_prefix="enhanced_frame"
    )


# ===== CLI =====
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python comfy_client.py <t2i|i2i|enhance> [options]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "t2i":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "A beautiful landscape"
        seed = int(sys.argv[3]) if len(sys.argv) > 3 else None
        outputs = txt2img(prompt=prompt, seed=seed)
        for o in outputs:
            print(f"output: {o}")

    elif cmd == "i2i":
        image_path = sys.argv[2]
        prompt = sys.argv[3] if len(sys.argv) > 3 else "enhance, high quality"
        denoise = float(sys.argv[4]) if len(sys.argv) > 4 else 0.35
        outputs = img2img(image_path=image_path, prompt=prompt, denoise=denoise)
        for o in outputs:
            print(f"output: {o}")

    elif cmd == "enhance":
        import glob
        frame_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        preserve = float(sys.argv[3]) if len(sys.argv) > 3 else 0.75
        frames = sorted(glob.glob(f"{frame_dir}/*.png")) + sorted(glob.glob(f"{frame_dir}/*.jpg"))
        if not frames:
            print("No frames found.")
            sys.exit(1)
        print(f"Enhancing {len(frames)} frames...")
        results = []
        for f in frames:
            try:
                out = enhance_video_frame(f, preserve_strength=preserve)
                results.append((f, out[0], "ok"))
                print(f"  [ok] {Path(f).name}")
            except Exception as e:
                results.append((f, None, str(e)))
                print(f"  [fail] {Path(f).name}: {e}")
        ok = sum(1 for r in results if r[2] == "ok")
        print(f"Done: {ok}/{len(frames)} enhanced")
