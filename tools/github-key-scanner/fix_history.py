"""修复 scan_history.json 中的重复日期日志，合并为一条"""
import json
from pathlib import Path

hist = json.loads(Path("tools/github-key-scanner/scan_history.json").read_text(encoding="utf-8"))
entries = hist["log_entries"]

# 合并同一天的日志
seen_dates = {}
for e in entries:
    d = e["date"]
    if d not in seen_dates:
        seen_dates[d] = e
    else:
        # 合并
        existing = seen_dates[d]
        existing["total_found"] = max(existing["total_found"], e["total_found"])
        existing["new_found"] = max(existing["new_found"], e["new_found"])
        existing_entries = {f"{r['repo']}|{r['file']}|{r['key_preview']}": r for r in existing["entries"]}
        for r in e["entries"]:
            key = f"{r['repo']}|{r['file']}|{r['key_preview']}"
            if key not in existing_entries:
                existing_entries[key] = r
        existing["entries"] = list(existing_entries.values())

hist["log_entries"] = sorted(seen_dates.values(), key=lambda x: x["date"])
Path("tools/github-key-scanner/scan_history.json").write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"✅ 合并完成: {len(entries)} -> {len(hist['log_entries'])} 条")

# 重新生成 MD
from datetime import datetime
from collections import Counter

sk = hist["seen_keys"]
lines = []
lines.append("# GitHub 密钥扫描记录\n")
lines.append("> 每日扫描：每天 12:00 自动执行  \n")
lines.append("> 扫描范围：GitHub 公开仓库中的 AI 大模型 API 密钥泄露  \n")
lines.append("> 覆盖供应商：OpenAI / Anthropic / DeepSeek / 通义千问 / 智谱 / Moonshot / Groq / Replicate 等 20+ 家\n")
lines.append("---\n")
lines.append(f"## 总览\n")
lines.append(f"- **累计发现泄露**: {len(sk)} 个密钥\n")
lines.append(f"- **涉及仓库**: {len(set(v['repo'] for v in sk.values()))} 个\n")
lines.append(f"- **最后扫描**: {hist.get('last_scan', 'N/A')}\n")
lines.append("\n### 供应商分布\n\n| 供应商 | 泄露数量 |\n|--------|----------|\n")
for prov, cnt in Counter(v["provider"] for v in sk.values()).most_common():
    lines.append(f"| {prov} | {cnt} |\n")
lines.append("\n---\n## 历史记录（按日期）\n\n")

for entry in reversed(hist["log_entries"]):
    de = entry["entries"]
    lines.append(f"### {entry['date']}\n")
    if de:
        lines.append(f"> 发现 **{len(de)}** 个密钥（其中 **{entry['new_found']}** 个新增）\n\n")
        lines.append("| # | 供应商 | 模型 | 仓库 | 文件路径 | 密钥预览 | 链接 |\n|---|--------|------|------|----------|----------|------|\n")
        for i, r in enumerate(de, 1):
            link = f"[查看]({r['file_url']})" if r.get("file_url") else "-"
            lines.append(f"| {i} | {r['provider']} | {r['model']} | {r['repo']} | `{r['file']}` | `{r['key_preview']}` | {link} |\n")
    else:
        lines.append("> 无新发现\n")
    lines.append("\n")

lines.append(f"---\n> 最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
Path("docs/github-key-scan-log.md").write_text("".join(lines), encoding="utf-8")
print("✅ MD 已更新")
