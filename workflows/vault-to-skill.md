# Vault-to-Skill 工作流

## 概览
将 Obsidian vault 内的书籍/PDF/主题笔记目录转化为 OpenClaw 可调用的 Agent Skill。

## 触发方式

| 方式 | 命令 | 场景 |
|------|------|------|
| 🖐️ 主动 | `python vault_bridge.py extract <path> --slug <slug>` | 手动指定源 |
| 📋 浏览 | `python vault_bridge.py list` | 查看 vault 可转换候选 |
| 📖 书籍选择 | `python vault_bridge.py extract --vault book` | 列出 vault 内可转的 PDF/EPUB |
| 📁 主题选择 | `python vault_bridge.py extract --vault topic` | 列出 vault 可转的主题目录 |
| 📊 状态 | `python vault_bridge.py status` | 查看所有已提取技能状态 |

## 完整流程

```
用户触发 → Phase 1: 提取（vault-bridge）
                │
                ▼
          _analysis.json + full_text.txt
                │
                ▼
         Phase 2: 生成（Agent）
                │
                ├── 读分析报告
                ├── 读全文（按章节分块）
                ├── 生成 chapters/ 每章文件
                ├── 生成 glossary.md
                ├── 生成 cheatsheet.md
                └── 生成 SKILL.md
                │
                ▼
         Phase 3: 注册（skill_workshop）
                │
                ├── 新建/更新 skill
                └── 标记 vault 索引笔记为 ✅
```

## Phase 1 — 提取（完全自动化）

```powershell
cd tools/vault-bridge
python vault_bridge.py extract "E:\Obsidian仓库\ZhouXuan私人领域\顶级UI设计" --slug top-ui-design
```

产出：
- `skills/top-ui-design/_analysis.json`
- `skills/top-ui-design/chapters/`（空目录，待填充）
- `E:\Obsidian仓库\ZhouXuan私人领域\_skills/top-ui-design.md`（索引笔记）

## Phase 2 — 生成（Agent 执行）

用户说「生成 Skill: top-ui-design」，Agent 执行：

1. 读 `_analysis.json` → 确认 token 规模 + 章节数
2. 读 `full_text.txt` → 分析结构
3. 生成 `chapters/ch01-*.md` ... `ch0N-*.md`
4. 生成 `glossary.md` + `cheatsheet.md`
5. 生成 `SKILL.md`

## Phase 3 — 注册（Agent 执行）

```python
skill_workshop action="create" name="top-ui-design"
```

或 update（如果已有）：

```python
skill_workshop action="update" skill_name="top-ui-design"
```

## 目录映射

```
vault                                            OpenClaw skills/
├── Literature/某书.pdf     ──→  skills/某书/
├── 顶级UI设计/             ──→  skills/top-ui-design/
│   ├── 原则1.md                  ├── SKILL.md
│   ├── 模式2.md                  ├── chapters/
│   └── 组件库.md                  │   ├── ch01-原则.md
│                                  │   └── ch02-模式.md
│                                  ├── glossary.md
│                                  └── cheatsheet.md
│
└── _skills/                      └── _analysis.json
    └── top-ui-design.md (索引)
```

## 快速命令速查

```powershell
# 1. 查看 vault 可转换源
python tools/vault-bridge/vault_bridge.py list

# 2. 提取书籍
python tools/vault-bridge/vault_bridge.py extract "E:\Obsidian仓库\...\book.pdf" --slug my-book

# 3. 提取主题目录
python tools/vault-bridge/vault_bridge.py extract "E:\Obsidian仓库\...\主题目录" --slug topic-name

# 4. 查看转换状态
python tools/vault-bridge/vault_bridge.py status
```

## 注意事项

- 提取后的 `full_text.txt` 在临时目录，`_analysis.json` 建议保留
- 主题目录转换时，markdown 文件无需额外解析器
- 50K+ token 的书不要一次性读取全文，按章节分块
