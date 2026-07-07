---
name: vault-to-skill
description: "Convert Obsidian vault books and topic directories into structured OpenClaw skills. Extract → analyze → generate → register."
version: 1.0.0
---

# Vault-to-Skill Converter

Turn vault content (books, PDFs, topic note directories) into interactive OpenClaw skills.

## Pipeline

```
用户触发 → vault-bridge extract → _analysis.json + full_text.txt
                               → [Agent] 生成 skill 文件
                               → skill_workshop 注册
```

## Step 1 — Extract (已完成)

用户先跑 `vault-bridge extract`，产出：
- `skills/<slug>/_analysis.json` — 分析报告
- 临时目录 `full_text.txt` — 全文提取

## Step 2 — 加载分析

读取 `skills/<slug>/_analysis.json`，获取：
- 源类型 (book/topic)
- Token 估算
- 章节数
- 提取模式 (text/technical)
- `full_text_path`

## Step 3 — 分析结构

读 `full_text.txt` 的前 8000 字符识别：
- 标题、作者（如有）
- 章节结构
- 核心主题

## Step 4 — 生成章节文件

对每个章节：
1. 从 `full_text.txt` 定位章节内容（grep/sed 或按偏移读取）
2. 按以下模板生成 `chapters/ch<NN>-<slug>.md`

```markdown
# Chapter N: <Full Title>

## Core Idea
<1–2 sentences>

## Frameworks Introduced
- **<Name>**: <exact formulation>
  - When to use: <situation>
  - How: <steps>

## Key Concepts
- **<Term>**: <definition>

## Key Takeaways
1. <actionable insight>
```

**Token 预算**（按提取模式）：
| 模式 | 每章 |
|------|------|
| text | 800–1200 tokens |
| technical | 1200–1800 tokens |

## Step 5 — 生成辅助文件

### glossary.md
- 书/主题中所有关键术语，字母排序
- 格式: `**Term** — definition (Ch N)`
- ≤ 1,500 tokens

### cheatsheet.md
- 决策规则、对比表、阈值
- ≤ 1,200 tokens
- 格式: 表 + 决策树

## Step 6 — 生成主 SKILL.md

```markdown
---
name: <slug>
description: "Knowledge base from \"<Title>\""
---

# <Title>
**来源**: <source> | **章节**: <N>

## Core Frameworks
<top frameworks>

## Chapter Index
| # | Title | Frameworks |
|---|-------|------------|

## Topic Index
- **<Term>** → ch<N>

## Files
- [glossary.md](glossary.md)
- [cheatsheet.md](cheatsheet.md)
```

≤ 4,000 tokens。重要内容优先。

## Step 7 — 注册

用 `skill_workshop` 创建/更新 skill：
- 已有 skill → 更新
- 新 skill → 创建

## Quality Rules

1. **提取结构，不写书评** — 命名框架、精确表述、反模式
2. **保留作者精确性** — "5 Whys" ≠ "多问几次为什么"
3. **密度优先** — 1000 token 精炼 > 10000 token 摘抄
4. **实践者语气** — "当 Y 时用 X" 不是"书中提到"
5. **不复制原文** — 综合、提炼、提取信号
