# TOOLS.md - Local Notes

## 记忆检索
search-memory.ps1 "关键词" → 按需读 topic/daily

## 浏览器策略
手动/扩展 → Edge | Playwright → Chromium | Wechatsync → Edge

## 关键路径
MEMORY.md / memory/topics/ / memory/daily/ / memory/evolution/ / E:\Obsidian仓库\ZhouXuan私人领域 / agent.yaml / RULES.md / workflows/ / hooks/ / knowledge/ / examples/

## Cron
memory-consolidation 02:00 / memory-health-sync 02:15 / memory-patrol 09:00 / memory-reflection 23:30 / security-check 10:00 / task-heartbeat 按需 / daily-social-content 10:00

## 工具箱速查
| 工具 | 路径 | 用法 |
|------|------|------|
| 截图 | `tools/screenshot.ps1` | `powershell -ExecutionPolicy Bypass -File tools\screenshot.ps1` |
| 视频生成 | `skills/hyperframes-video/` | edge-tts + FFmpeg + HyperFrames CLI |
| 平台检查 | `tools/check_all_platforms.py` | `python tools/check_all_platforms.py` |
| 内审 | `skills/self-audit/` | 触发词：内审/审查/反思/复盘 |
| 多平台发布 | `tools/social-auto-upload/` | CLI: `sau`，需 activate venv |
| 安全扫描 | `tools/SkillSpector/` | `skillspector scan <dir>` |
| 文章同步 | `wechatsync` | `wechatsync sync article.md -p zhihu,juejin` |
| YouNavi | `tools/younavi_bridge.py` | `yn.research_full("主题")` |

详细用法 → 读对应 SKILL.md 或 docs/CLI.md

## Git 提交规范
feat/fix/refactor/docs/security/evolution/meta/snapshot
