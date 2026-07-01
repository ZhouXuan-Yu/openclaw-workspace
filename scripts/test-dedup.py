"""Semantic Dedup 单元测试（关键词指纹版）"""
import re, tempfile, shutil, os

def kw_fingerprint(text, min_len=2, max_len=4):
    clean = re.sub(r"[^\u4e00-\u9fff]", "", text.lower())
    if len(clean) < min_len:
        return set()
    kws = set()
    for l in range(min_len, max_len + 1):
        for i in range(len(clean) - l + 1):
            kws.add(clean[i:i + l])
    return kws

def overlap_ratio(a_set, b_set):
    inter = a_set & b_set
    union = a_set | b_set
    return len(inter) / len(union) if union else 0.0

TOPIC_DIR = r"C:\Users\ZhouXuan\.openclaw\workspace\memory\topics"
passed = 0

# ==== 测试 1: 实际数据无误报 ====
print("=== 测试 1: 实际数据 (threshold=0.5) ===")
entries = []
for fname in sorted(os.listdir(TOPIC_DIR)):
    if not fname.endswith(".md") or fname.startswith("_"):
        continue
    path = os.path.join(TOPIC_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    sections = re.split(r"\n(?=#{2,3}\s)", content)
    for si, section in enumerate(sections):
        text = section.strip()
        if len(text) < 80:
            continue
        entries.append({
            "file": fname, "kw": kw_fingerprint(text), "text": text[:80]
        })

high = 0
for i in range(len(entries)):
    for j in range(i + 1, len(entries)):
        r = overlap_ratio(entries[i]["kw"], entries[j]["kw"])
        if r >= 0.5:
            high += 1
assert high == 0, f"{high} 组高重叠误报"
print(f"OK: {len(entries)} entries, 0 dupes")
passed += 1

# ==== 测试 2: 同义事实 ====
print("\n=== 测试 2: 同义事实 ===")
a = "记忆架构采用 4 层文件系统方案，包含索引层、主题层、日志层、会话层"
b = "记忆架构用了四层文件系统，分别是索引、主题、日志、会话四个层次"
r = overlap_ratio(kw_fingerprint(a), kw_fingerprint(b))
assert r > 0.1, f"同义事实 overlap={r} 应 > 0.1"
print(f"OK: overlap={r:.3f}")
passed += 1

# ==== 测试 3: 同一事实 ====
print("\n=== 测试 3: 同一事实 ===")
a = "小红书改用草稿箱模式发布，避免 AI 托管检测封禁"
b = "小红书上需要手动发布到草稿箱，防止 AI 内容检测被封号"
r = overlap_ratio(kw_fingerprint(a), kw_fingerprint(b))
assert r > 0.05, f"同一事实 overlap={r} 应 > 0.05"
print(f"OK: overlap={r:.3f}")
passed += 1

# ==== 测试 4: 完全重复 ====
print("\n=== 测试 4: 完全重复 ===")
a = "pip install openclaw 是安装 OpenClaw 的标准方式"
b = "pip install openclaw 是安装 OpenClaw 的标准方式"
r = overlap_ratio(kw_fingerprint(a), kw_fingerprint(b))
assert r == 1.0, f"完全重复 overlap={r} 应为 1.0"
print(f"OK: overlap={r}")
passed += 1

# ==== 测试 5: 完全无关 ====
print("\n=== 测试 5: 完全无关 ===")
a = "统一使用 Edge 浏览器不装 Chrome"
b = "微信视频号 cookie 过期需要重新扫码登录"
r = overlap_ratio(kw_fingerprint(a), kw_fingerprint(b))
assert r < 0.1, f"无关 overlap={r} 应 < 0.1"
print(f"OK: overlap={r:.3f}")
passed += 1

# ==== 测试 6: 同一文件内不构成同一 section 的相似内容 ====
print("\n=== 测试 6: 同文件不同 section 不误报 ===")
a = "VS Code 是主要编辑器，配置了 Python 和 TypeScript 开发环境"
b = "开发流程中需要手动测试后提交代码到 Git 仓库"
r = overlap_ratio(kw_fingerprint(a), kw_fingerprint(b))
assert r < 0.5, f"无关同文件 overlap={r}"
print(f"OK: overlap={r:.3f}")
passed += 1

print(f"\n{'='*40}")
print(f"结果: {passed}/6 通过")
