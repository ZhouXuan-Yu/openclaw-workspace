# GitHub AI 密钥扫描工具

扫描 GitHub 公开仓库中暴露的大模型 API 密钥，生成 Excel 报告。

## 快速开始

```bash
# 1. 安装依赖
pip install openpyxl requests

# 2. （推荐）在 scanner.py 顶部填入 GitHub Token
#    不填也能用，但每分钟只能搜 10 次
#    Token 权限只需 public_repo (read)

# 3. 运行
python scanner.py
```

## 输出

- `github_keys_report.xlsx` — 两个 Sheet：
  - **密钥扫描报告**：完整列表（供应商/仓库/文件/密钥预览/链接）
  - **供应商统计**：按供应商汇总

## 覆盖供应商

| 国际 | 国产 |
|------|------|
| OpenAI (GPT-4/o1/o3) | DeepSeek |
| Anthropic (Claude) | Moonshot/Kimi |
| Google AI (Gemini) | 通义千问/Qwen |
| Cohere | 智谱/GLM |
| HuggingFace | 百川智能 |
| Mistral AI | MiniMax |
| Groq | 讯飞星火 |
| Replicate | SiliconFlow |
| Together AI | 零一万物/Yi |
| Fireworks AI | 阶跃星辰/Step |
| Perplexity | 商汤 SenseNova |
| | 腾讯混元 |

## 自定义

在 `scanner.py` 中修改 `SEARCH_PATTERNS` 字典添加新关键词：
```python
'"YOUR_ENV_VAR=sk-"': ("供应商名", r"sk-[a-z0-9]{20,}", "模型名"),
```

## 注意事项

- **速率限制**：无 Token 每分钟 10 次搜索，有 Token 30 次
- **脱敏处理**：输出的密钥只显示前8位+后4位
- **合法用途**：仅用于安全提醒，不用于恶意利用
