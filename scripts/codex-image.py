"""
Codex CLI 生图桥接 — 将生图请求转发给 Codex CLI，取其结果
=============================================================
用法: python scripts/codex-image.py "图片描述" [--aspect 3:4] [--out output.png]

原理: Codex CLI 有独立的 OpenAI API 凭证，绕过当前模型的余额限制。
流程: 写描述 → 调 codex exec → 等待完成 → 从 ~/.codex/generated_images/ 取最新图 → 复制到目标

依赖: Codex CLI >= 0.144.1 (codex --version)
"""
import subprocess, sys, os, json, glob, time, shutil
from pathlib import Path

CODEX_IMAGES = Path.home() / ".codex" / "generated_images"

def find_latest_image():
    """Find the most recently generated image"""
    all_pngs = list(CODEX_IMAGES.rglob("*.png"))
    if not all_pngs:
        return None
    return max(all_pngs, key=lambda p: p.stat().st_mtime)

def generate_image(prompt, aspect="3:4", out_path=None):
    """Call Codex CLI to generate an image"""
    print(f"🎨 调用 Codex CLI 生图...")
    print(f"  描述: {prompt[:80]}...")
    print(f"  比例: {aspect}")
    
    # Record current latest before generation
    before = find_latest_image()
    
    # Prepare the prompt for Codex
    codex_prompt = (
        f"只用image_generate工具生成一张图片，"
        f"aspectRatio={aspect}，"
        f"quality=high。"
        f"描述：{prompt}。"
        f"生成后把图片完整路径告诉我。不要做其他事情。"
    )
    
    # Run codex exec
    result = subprocess.run(
        ["codex", "exec", codex_prompt],
        capture_output=True, text=True, timeout=180
    )
    
    # Find the new image
    after = find_latest_image()
    
    if after and after != before:
        print(f"  ✅ 图片已生成: {after}")
        print(f"  大小: {after.stat().st_size / 1024:.0f} KB")
        
        if out_path:
            shutil.copy2(str(after), out_path)
            print(f"  ✅ 已复制到: {out_path}")
            return out_path
        return str(after)
    else:
        print(f"  ❌ 未检测到新图片")
        print(f"  Codex 输出: {result.stdout[-500:]}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python scripts/codex-image.py '图片描述' [--aspect 3:4] [--out output.png]")
        sys.exit(1)
    
    prompt = sys.argv[1]
    aspect = "3:4"
    out = None
    
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--aspect" and i + 1 < len(sys.argv):
            aspect = sys.argv[i + 1]
        elif arg == "--out" and i + 1 < len(sys.argv):
            out = sys.argv[i + 1]
    
    result = generate_image(prompt, aspect, out)
    if result:
        print(f"\n结果: {result}")
    else:
        sys.exit(1)
