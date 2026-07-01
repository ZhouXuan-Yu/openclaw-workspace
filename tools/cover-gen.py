#!/usr/bin/env python3
"""配图生成器 — 本地 Pillow 渐变背景 + 文字"""
import sys
import os
from PIL import Image, ImageDraw, ImageFont

def create_cover(text: str, output: str, size=(1024, 1024), style="gradient"):
    """生成封面图"""
    w, h = size
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)

    # 渐变背景
    if style == "gradient":
        for y in range(h):
            r = int(60 + 195 * (y / h))
            g = int(120 + 60 * (1 - y / h))
            b = int(200 + 55 * (y / h))
            draw.line([(0, y), (w-1, y)], fill=(r, g, b))
    elif style == "warm":
        for y in range(h):
            r = int(255 * (1 - y/h * 0.3))
            g = int(180 * (y/h))
            b = int(100 * (y/h))
            draw.line([(0, y), (w-1, y)], fill=(r, g, b))
    elif style == "dark":
        for y in range(h):
            r = int(30 + 20 * (y/h))
            g = int(30 + 30 * (y/h))
            b = int(50 + 40 * (y/h))
            draw.line([(0, y), (w-1, y)], fill=(r, g, b))

    # 文字
    try:
        font_large = ImageFont.truetype('msyh.ttc', 56)
        font_small = ImageFont.truetype('msyh.ttc', 36)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 居中文字
    lines = text.split('\n')
    total_height = len(lines) * 70
    start_y = (h - total_height) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_large if i == 0 else font_small)
        text_w = bbox[2] - bbox[0]
        x = (w - text_w) // 2
        y = start_y + i * 70
        # 阴影
        draw.text((x+2, y+2), line, fill='black', font=font_large if i == 0 else font_small)
        draw.text((x, y), line, fill='white', font=font_large if i == 0 else font_small)

    os.makedirs(os.path.dirname(output), exist_ok=True)
    img.save(output, 'PNG')
    return output

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "AI 内容创作"
    output = sys.argv[2] if len(sys.argv) > 2 else "cover.png"
    style = sys.argv[3] if len(sys.argv) > 3 else "gradient"
    result = create_cover(text, output, style=style)
    print(f"✅ 生成: {result} ({os.path.getsize(result)//1024}KB)")
