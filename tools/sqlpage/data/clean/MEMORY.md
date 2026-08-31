# MEMORY.md — 长时记忆索引
保持 <200行。详情见 `memory/topics/`。

## 浏览器策略（统一 Edge）

| 场景 | 浏览器 | 说明 |
|------|--------|------|
| 手动操作/扩展加载 | Edge | 系统默认，兼容Chrome扩展 |
| Playwright 自动化 | Chromium（内嵌） | 不可改，不影响 |
| Wechatsync 扩展 | Edge | 加载到 Edge 扩展程序 |

**规则**：所有需手动操作的场景统一用 Edge，不装 Chrome。文章同步用 Wechatsync CLI（不封装 MCP），保持和 social-auto-upload CLI 一致的工具链风格。

## 用户
| 项 | 值 |
|---|---|
| Name | ZhouXuan |
| 风格 | 简洁·直接·实事求是 |
| Vault | `E:\Obsidian仓库\ZhouXuan私人领域` |

## 星标记忆
| 日期 | 内容 |
|------|------|
| 06-25 | v3架构升级: 惰性检测器+长任务循环+hooks.yaml v3+RuleMaturity |
| 06-11 | 记忆架构是进化的关键 |
| 06-11 | Phase 2-5 已完成验证 |
| 06-12 | 自进化引擎: FIX/DERIVED/CAPTURED |
| 06-12 | OpenSpec 分析: Delta 变更追踪+验证前置可借鉴 |
| 06-12 | 多平台自动化: social-auto-upload 5平台CLI验证通过 |
| 06-12 | SkillSpector: 安全扫描集成，5个Skill扫描完成 |
| 06-12 | OpenGAP: 14个设计模式优化架构，agent.yaml+RULES.md+workflows/ |
| 06-13 | 智能检索升级: 先想后查+topic关联图+跨周期推理 |
| 06-14 | 视频号上传: locator超时先检查URL重定向，不是元素不可见 |
| 06-15 | GitHub热门项目分析: 10个项目，Agent工程化趋势（skills/codegraph/agentmemory） |
| 06-15 | v5进化: Think Tool(Devin)+Mode Router(Kiro)+Self-Verify(Devin), 健康检查89/98(A) |
| 06-15 | v5.1: Agent Skills(Doubt-Driven+Incremental Impl)融入RULES.md, 反偷懒表
| 07-07 | ⭐ GitHub 每日推送：每次修改立即 git push，不攒批，优先级最高 |
| 07-22 | ⭐ 技术文档存放规则：`E:\Obsidian仓库\ZhouXuan私人领域\Agent学习\技术文档\YYYY-MM\`，按月分目录 |
| 07-26 | ⭐ AgentChat 集成决策：Q1 图片生成首选→网页AI(AgentChat)；废弃 image_generate API；Chrome CDP 开机自启；已固化到社交自动化链路 |
| 07-26 | ⭐ 社交内容面向群体：中国大陆开发者/技术用户，中文表达，使用国内常见技术栈和平台参考 |

## 主题索引
| 主题 | 位置 |
|------|------|
| 术语表 | `CONTEXT.md` |
| 偏好 | `topics/preferences.md` |
| 项目 | `topics/projects.md` |
| 多平台发布 | `tools/social-auto-upload/` (见 topics/work-tools.md) |
| 社交内容生产链路 | `topics/work-tools.md`（Q0-Q5 完整流程，2026-06-16 固化）|
| 安全扫描 | `tools/SkillSpector/` (见 topics/work-tools.md) |
| 社交内容设计 | `skills/guizang-social-card/` (Codex CLI 生成图片/视频时必用) |
| 学习 | `topics/learnings.md` |
| OpenClaw 更新日志 | `topics/openclaw-update-log.md` |
| 决策 | `topics/decisions.md` |
| 人物 | `topics/people.md` |
| 实用工具 | `E:\Obsidian仓库\ZhouXuan私人领域\实用工具收录\` |
| 工具 | `topics/work-tools.md` |
| 任务日历 | `topics/task-calendar.md` |

| 进化 | `evolution/EVOLUTION-PROTOCOL.md` (v4) |
| 变更影响 | `docs/change-impact-checklist.md` |
| ADR | `docs/adr/` |
| 智能检索 | `memory/retrieval-strategy.md` + `topics/_graph.json` |
| OpenSpec 分析 | `topics/openspec-analysis.md`（已归档）|
| 架构增强 | `topics/openspec-arch-enhancements.md`（已归档）|
| GitHub 热门项目 | `topics/github-may-2026-projects.md` |
| UI设计系统交叉分析 | `topics/design-systems-analysis.md` |
| 战略思维伙伴 | `knowledge/strategic-thinking-partner.md`（MBB框架集+思维模型）|
| 进化引擎 | `evolution/EVOLUTION-PROTOCOL.md` |
| Skill 自进化 | `evolution/skill-evolution.md` + `evolution/skill-traces/` |
| Trust Scoring | `evolution/trust-registry.json` (v1, from duMem) |
| Decay 衰减 | `evolution/trust-registry.json` + `scripts/decay-scanner.py` (v1, from duMem) |
| Semantic Dedup | `scripts/dedup-scanner.py` (v1, from duMem) |
| 自举协议 | `evolution/SELF-IMPROVE-PROTOCOL.md` |
| 测试历史 | `evolution/test-history.json` |
| OpenGAP | `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\OpenGAP核心要点.md` |
| agent.yaml | `agent.yaml` Agent 清单 |
| RULES.md | `RULES.md` 硬约束 |
| workflows | `workflows/` YAML 工作流 |
| hooks | `hooks/` 生命周期钩子 |
| 惰性检测器 | `hooks/laziness-detectors.yaml`（v3, 7种检测器）|
| 长任务循环 | `hooks/task-loop.md`（v3, RECEIVE→ALIGN→SLICE→EXECUTE→VERIFY→REPORT）|
| knowledge | `knowledge/` 知识索引 |
| examples | `examples/` few-shot 示例 |
| 图片处理 | ⚠️ 收到图片→本地OCR→模型推理（见 topics/work-tools.md） |
| 图片生成 | AgentChat(网页AI) 优先 → Codex CLI → ComfyUI → image_generate API兜底 |
| Wechatsync | `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\Wechatsync-CLI使用手册.md` |
| 社交自动化决策树 | `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\社交自动化决策树.md` |
| YouNavi CLI | `D:\YouNavi\resources\backend\agent-cli.exe`（见 topics/work-tools.md） |
| YouNavi 桥梁 | `tools/younavi_bridge.py`（Python封装，解决编码问题） |
| YouNavi Skill | `skills/younavi-integration/SKILL.md` |
| 每日社交内容 | `workflows/daily-social-content.md`（cron: daily-social-content, 10:00）|
| GitHub 趋势推送 | 每日 16:00 → WeChat |
| GitHub 周度趋势报告 | 周日 16:30 → Obsidian Vault + WeChat 摘要 |
| 用户画像 | `E:\Obsidian仓库\ZhouXuan私人领域\人物画像.md`（每日复盘更新+每周日周报）|
| 画像追踪方案 | `E:\Obsidian仓库\ZhouXuan私人领域\顶级UI设计\用户画像追踪实现方案.md` |
| 早间推送 | cron: morning-task-brief (09:00) |
| 晚间规划 | cron: evening-plan-reminder (23:30) |
| GitHub 趋势推送 | cron: github-trends-daily (16:00) |
| GitHub 周度趋势报告 | cron: github-trends-weekly (周日 16:30) |
| 每日复盘 | cron: memory-reflection (23:45, 含画像更新) |
| 周度复盘 | cron: weekly-portrait-review (周日23:30) |

## Tag 索引
`#memory-architecture` `#skill-evolution` `#claude-fable5` `#openclaw-skills` `#obsidian-notes` `#openspec` `#opengap` `#security-scan` `#workflows` `#github-trends`

## 短期记忆（2026-07-13 整合）

- **子 Agent 蜂群模式**（sessions_spawn）: 适合批量读文件/并行搜索/数据抓取/格式转换（机械任务不需要判断力）；多方向分析（各自分析→汇总）质量中等
- **限制**: context=isolated 冷启动无背景，context=fork 则 Token 翻倍；子 Agent 间不能通信；依赖模型配额（并发多可能429）
- **用法**: 单回合 `sessions_spawn` 派多个 → `sessions_yield` 等全部返回
- **注意**: 每次修改后立即 git push（已入星标）
