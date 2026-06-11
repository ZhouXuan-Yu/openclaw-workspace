# TOOLS.md - Local Notes

> 最后更新：2026-06-11

---

## 🔍 记忆检索（Memory Recall）

当用户问及过去的事情、决策、偏好时，按以下顺序执行：

```powershell
# 搜索 workspace 文件
powershell -File "C:\Users\ZhouXuan\.openclaw\workspace\search-memory.ps1" "关键词"

# 如果找不到，在 Obsidian Vault 搜索
Select-String -Path "E:\Obsidian仓库\ZhouXuan私人领域\prompt学习提示词\**\*.md" -Pattern "关键词"

# 看今日/昨日日志
Get-ChildItem "C:\Users\ZhouXuan\.openclaw\workspace\memory\*.md"
```

## 📝 写记忆日志（Write to Memory）

当用户说「记住这个」「记一下」或对话框自然结束时：

```powershell
# 追加到今日日志
$date = Get-Date -Format "yyyy-MM-dd"
$file = "C:\Users\ZhouXuan\.openclaw\workspace\memory\$date.md"
$"## $(Get-Date -Format 'HH:mm') — 决策 | 记录内容\n\n...\n" | Add-Content $file
```

## 🗂️ 关键路径（Quick Reference）

| 路径 | 用途 |
|------|------|
| `C:\Users\ZhouXuan\.openclaw\workspace\USER.md` | 用户档案 |
| `C:\Users\ZhouXuan\.openclaw\workspace\MEMORY.md` | 长时记忆索引（<200行） |
| `C:\Users\ZhouXuan\.openclaw\workspace\memory\topics\` | 主题记忆（preferences/projects/learnings） |
| `C:\Users\ZhouXuan\.openclaw\workspace\memory\daily\YYYY-MM-DD.md` | 每日日志 |
| `C:\Users\ZhouXuan\.openclaw\workspace\search-memory.ps1` | 全文搜索脚本 |
| `E:\Obsidian仓库\ZhouXuan私人领域\prompt学习提示词\Memory记忆架构\` | 记忆体迭代文件夹 |
| `E:\Obsidian仓库\ZhouXuan私人领域\prompt学习提示词\Memory记忆架构\记忆看板.md` | 全局看板 |

## ⏰ Cron 任务

| 任务 | 时间 | 作用 |
|------|------|------|
| memory-consolidation | 每天 02:00 CST | 自动整合 memory/ 日志到 MEMORY.md |

## 🔌 端口 & 服务（备用）

| 服务 | 端口 | 说明 |
|------|------|------|
| agentmemory（可选） | 3111 | 未来使用的语义记忆服务器 |
| agentmemory viewer | 3113 | 记忆可视化面板 |

---
