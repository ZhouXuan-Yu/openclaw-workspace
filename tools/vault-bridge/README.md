# vault-bridge

Obsidian vault → book-to-skill → OpenClaw Skill 桥接工具。

## 快速开始

```powershell
# 查看 vault 可转换候选
python vault_bridge.py list

# 提取一本书
python vault_bridge.py extract "E:\Obsidian仓库\...\书.pdf" --slug my-book

# 提取一个主题目录
python vault_bridge.py extract "E:\Obsidian仓库\...\主题目录" --slug topic-name

# 查看已提取的技能状态
python vault_bridge.py status

# 从 vault 自动发现 (交互式选择)
python vault_bridge.py extract --vault all
```

## 生成 Skill

提取完成后，告诉我：

> 「生成 Skill: auto-content」

我来完成技能文件（章节分析 + 术语 + 速查表 + 注册）。

## 文件结构

```
tools/vault-bridge/
├── vault_bridge.py        # 主桥接脚本 (Python)
├── vault-bridge.ps1       # PowerShell 入口
├── skill-index.json       # 技能索引
└── README.md

skills/<slug>/
├── _analysis.json         # 提取分析报告
├── chapters/              # 章节文件 (待Agent生成)
├── SKILL.md               # 主技能文件 (待Agent生成)
├── glossary.md            # 术语表 (待Agent生成)
└── cheatsheet.md          # 速查表 (待Agent生成)
```
