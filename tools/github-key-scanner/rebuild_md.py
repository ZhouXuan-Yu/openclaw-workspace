"""从 scan_history.json 重新生成 docs/github-key-scan-log.md"""
import json
from datetime import datetime
from pathlib import Path
from collections import Counter

hist = json.loads(Path("tools/github-key-scanner/scan_history.json").read_text(encoding="utf-8"))
sk = hist["seen_keys"]
entries = hist["log_entries"]

lines = []
lines.append("# GitHub 密钥扫描记录\n")
lines.append("> 每日扫描：每天 12:00 自动执行  \n")
lines.append("> 扫描范围：GitHub 公开仓库中的 AI 大模型 API 密钥泄露  \n")
lines.append("> 覆盖供应商：OpenAI / Anthropic / DeepSeek / 通义千问 / 智谱 / Moonshot / Groq / Replicate 等 20+ 家\n")
lines.append("---\n")

total_unique = len(sk)
total_repos = len(set(v["repo"] for v in sk.values()))
lines.append(f"## 总览\n")
lines.append(f"- **累计发现泄露**: {total_unique} 个密钥\n")
lines.append(f"- **涉及仓库**: {total_repos} 个\n")
lines.append(f"- **最后扫描**: {hist.get('last_scan', 'N/A')}\n")

lines.append("\n### 供应商分布\n\n")
lines.append("| 供应商 | 泄露数量 |\n")
lines.append("|--------|----------|\n")
for prov, cnt in Counter(v["provider"] for v in sk.values()).most_common():
    lines.append(f"| {prov} | {cnt} |\n")

lines.append("\n---\n")
lines.append("## 历史记录（按日期）\n\n")

for entry in reversed(entries):
    de = entry["entries"]
    lines.append(f"### {entry['date']}\n")
    lines.append(f"> 本次扫描发现 **{entry['total_found']}** 个密钥，其中 **{entry['new_found']}** 个为新增\n\n")
    if de:
        lines.append("| # | 供应商 | 模型 | 仓库 | 文件路径 | 密钥预览 | 链接 |\n")
        lines.append("|---|--------|------|------|----------|----------|------|\n")
        for i, r in enumerate(de, 1):
            link = f"[查看]({r['file_url']})" if r.get("file_url") else "-"
            lines.append(f"| {i} | {r['provider']} | {r['model']} | {r['repo']} | `{r['file']}` | `{r['key_preview']}` | {link} |\n")
    lines.append("\n")

lines.append("---\n")
lines.append(f"> 最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

Path("docs/github-key-scan-log.md").write_text("".join(lines), encoding="utf-8")
print("✅ Markdown 已更新")
print(f"总密钥: {total_unique}, 仓库: {total_repos}")
