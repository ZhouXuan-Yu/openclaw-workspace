"""从 Vecteezy / CleanPNG 等无反爬站下载表情包"""
import requests
from pathlib import Path
import json, time

BASE_DIR = Path("E:/Obsidian仓库/ZhouXuan私人领域/表情包库")
BASE_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
}

# 使用 CleanPNG / Vecteezy 等对直链友好的站
STICKERS = [
    {
        "name": "猫咪开心",
        "url": "https://www.cleanpng.com/png-cat-emoji-sticker-whiskers-iphone-cat-emoji-wg5p0i/download-png.html",
        "tags": ["猫咪", "开心", "可爱"],
        "scene": "开心"
    },
    # 直接用已知可靠的 CDN
    {
        "name": "猫猫摸鱼",
        "url": "https://em-content.zobj.net/thumbs/120/apple/354/cat_1f431.png",
        "tags": ["猫咪", "摸鱼", "可爱"],
        "scene": "日常/摸鱼"
    },
    {
        "name": "猫猫哭泣",
        "url": "https://em-content.zobj.net/thumbs/120/apple/354/crying-cat_1f63f.png",
        "tags": ["猫咪", "哭泣", "委屈"],
        "scene": "委屈/安抚"
    },
    {
        "name": "猫猫开心笑",
        "url": "https://em-content.zobj.net/thumbs/120/apple/354/grinning-cat_1f638.png",
        "tags": ["猫咪", "大笑", "开心"],
        "scene": "开心"
    },
    {
        "name": "猫猫爱心眼",
        "url": "https://em-content.zobj.net/thumbs/120/apple/354/heart-eyes-cat_1f63b.png",
        "tags": ["猫咪", "爱心", "喜欢"],
        "scene": "喜欢/感谢"
    },
    {
        "name": "猫猫惊讶",
        "url": "https://em-content.zobj.net/thumbs/120/apple/354/screaming-cat_1f640.png",
        "tags": ["猫咪", "惊讶", "搞笑"],
        "scene": "震惊"
    },
    {
        "name": "猫猫生气",
        "url": "https://em-content.zobj.net/thumbs/120/apple/354/pouting-cat_1f63e.png",
        "tags": ["猫咪", "生气", "傲娇"],
        "scene": "生气/傲娇"
    },
    {
        "name": "猫猫疲惫",
        "url": "https://em-content.zobj.net/thumbs/120/apple/354/weary-cat_1f640.png",
        "tags": ["猫咪", "疲惫", "累"],
        "scene": "累瘫/加班"
    },
    # 加一些表情符号周边
    {
        "name": "狗狗可爱",
        "url": "https://em-content.zobj.net/thumbs/120/apple/354/dog_1f415.png",
        "tags": ["狗狗", "可爱"],
        "scene": "日常"
    },
    {
        "name": "点赞手势",
        "url": "https://em-content.zobj.net/thumbs/120/apple/354/thumbs-up_1f44d.png",
        "tags": ["点赞", "鼓励"],
        "scene": "表扬/认可"
    },
]

def download_sticker(item):
    fname = f"{item['name']}.png"
    fpath = BASE_DIR / fname
    if fpath.exists():
        return "exists", len(fpath.read_bytes())
    
    try:
        r = requests.get(item["url"], headers=HEADERS, timeout=20)
        if r.status_code == 200 and len(r.content) > 500:
            fpath.write_bytes(r.content)
            return "ok", len(r.content)
        else:
            return f"http_{r.status_code}", 0
    except Exception as e:
        return f"err: {str(e)[:30]}", 0

index = {}
ok, fail = 0, 0

print(f"📦 表情包库下载 | {len(STICKERS)} 个")
print("=" * 50)

for item in STICKERS:
    print(f"↓ {item['name']}...", end=" ", flush=True)
    status, size = download_sticker(item)
    if status == "ok":
        print(f"✅ {size}B")
        ok += 1
    elif status == "exists":
        print(f"📁 {size}B (已有)")
        ok += 1
    else:
        print(f"❌ {status}")
        fail += 1
    
    fname = f"{item['name']}.png"
    if (BASE_DIR / fname).exists():
        index[item["name"]] = {
            "file": fname,
            "tags": item["tags"],
            "scene": item["scene"]
        }
    
    time.sleep(0.4)

# Save index
idx = BASE_DIR / "index.json"
idx.write_text(json.dumps({
    "updated": time.strftime("%Y-%m-%d %H:%M"),
    "count": len(index),
    "stickers": index
}, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"\n✅ {ok} 可用, ❌ {fail} 失败")
count = len(list(BASE_DIR.glob("*.png")))
print(f"📁 本地表情包: {count} 个")
