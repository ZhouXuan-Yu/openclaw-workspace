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
| 决策 | `topics/decisions.md` |
| 人物 | `topics/people.md` |
| 工具 | `topics/work-tools.md` |
| 任务日历 | `topics/task-calendar.md` |

| 进化 | `evolution/EVOLUTION-PROTOCOL.md` (v4) |
| 变更影响 | `docs/change-impact-checklist.md` |
| ADR | `docs/adr/` |
| 智能检索 | `memory/retrieval-strategy.md` + `topics/_graph.json` |
| OpenSpec 分析 | `topics/openspec-analysis.md` |
| 架构增强 | `topics/openspec-arch-enhancements.md` |
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
| Wechatsync | `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\Wechatsync-CLI使用手册.md` |
| 社交自动化决策树 | `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\社交自动化决策树.md` |
| YouNavi CLI | `D:\YouNavi\resources\backend\agent-cli.exe`（见 topics/work-tools.md） |
| YouNavi 桥梁 | `tools/younavi_bridge.py`（Python封装，解决编码问题） |
| YouNavi Skill | `skills/younavi-integration/SKILL.md` |
| 每日社交内容 | `workflows/daily-social-content.md`（cron: daily-social-content, 10:00）|
| 用户画像 | `E:\Obsidian仓库\ZhouXuan私人领域\人物画像.md`（每日复盘更新+每周日周报）|
| 画像追踪方案 | `E:\Obsidian仓库\ZhouXuan私人领域\顶级UI设计\用户画像追踪实现方案.md` |
| 早间推送 | cron: morning-task-brief (09:00) |
| 晚间规划 | cron: evening-plan-reminder (23:30) |
| 每日复盘 | cron: memory-reflection (23:45, 含画像更新) |
| 周度复盘 | cron: weekly-portrait-review (周日23:30) |

## Tag 索引
`#memory-architecture` `#skill-evolution` `#claude-fable5` `#openclaw-skills` `#obsidian-notes` `#openspec` `#opengap` `#security-scan` `#workflows` `#github-trends`

## Promoted From Short-Term Memory (2026-06-21)

<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:27:28 -->
- 小红书封号修复: `tools/social-auto-upload/uploader/xiaohongshu_uploader/main.py` — XiaoHongShuNote 类; `tools/social-auto-upload/sau_cli.py` — CLI --draft 参数 [score=0.807 recalls=0 avg=0.620 source=memory/2026-06-15.md:27-28]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:31:34 -->
- 01:05 多平台发布结果: 抖音: ✅ 自动发布成功; 快手: ✅ 定时发布 (03:11); B站: ✅ biliup 上传成功; 视频号: ❌ cookie过期，需重新扫码 [score=0.807 recalls=0 avg=0.620 source=memory/2026-06-15.md:31-34]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:35:35 -->
- 01:05 多平台发布结果: 小红书: 📝 草稿箱待手动发布（AI声明+微调） [score=0.807 recalls=0 avg=0.620 source=memory/2026-06-15.md:35-35]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:37:39 -->
- 01:05 多平台发布结果: **视频信息**: evolution_v2.mp4, 4.2MB, 4.2min **卡片风格**: Swiss International (guizang-social-card) **配音**: zh-CN-YunyangNeural (沉稳男声) [score=0.807 recalls=0 avg=0.620 source=memory/2026-06-15.md:37-39]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:45:45 -->
- 01:50 GitHub 5月热门项目分析: 分析了逛逛GitHub公众号推荐的10个项目，逐个看README，写入 `topics/github-may-2026-projects.md`。 [score=0.807 recalls=0 avg=0.620 source=memory/2026-06-15.md:45-45]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:47:47 -->
- 01:50 GitHub 5月热门项目分析: **重点学习**: [score=0.807 recalls=0 avg=0.620 source=memory/2026-06-15.md:47-47]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:27:27 -->
- v5/v5.1 架构进化: Agent Skills: Doubt-Driven Development + Incremental Implementation（源�?Addy Osmani�?- 反偷懒表: Agent 常用借口 + 反驳 [score=0.801 recalls=0 avg=0.620 source=memory/2026-06-16.md:27-27]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:33:34 -->
- System Prompt 收集: **范围**: 20+ 工具�?6 个文�?**工具列表**: Dify, Coze, FastGPT, Cursor, Windsurf, Claude Code, Lovable, Bolt, Replit, Devin, OpenHands, SWE-Agent, Augment Code, GitHub Copilot, Trae, Roo Code, Cline, Kilo Code, Kiro, Aider, Goose, Open Interpreter, Amazon Q Developer, Gemini Code Assist, Tabnine, Qodo, Microsoft Copilot **存储位置**: `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\` 下按工具名建文件�? [score=0.801 recalls=0 avg=0.620 source=memory/2026-06-16.md:33-34]

## Promoted From Short-Term Memory (2026-06-22)

<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:37:40 -->
- Agent Skills 深度解析: **来源**: Addy Osmani (Google Chrome 团队) **内容**: 24 �?Skill 覆盖完整开发生命周�?(DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP) **最值得复用**: doubt-driven-development, incremental-implementation, context-engineering, spec-driven-development, anti-rationalization **文档位置**: `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\Addy-Osmani-Agent-Skills深度解析.md` [score=0.854 recalls=0 avg=0.620 source=memory/2026-06-16.md:37-40]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:44:45 -->
- AI Agent 未来发展方向报告: **产出**: `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\AI-Agent未来发展方向研究报告.md` **六大方向**: 记忆系统 / Skill驱动工作�?/ 多智能体协作 / 自进�?/ 可信Agent / 具身�?**数据来源**: YouNavi深度研究×2 + Agent Skills分析 + v5/v5.1实战 + 20+工具System Prompt + GitHub热门项目 [score=0.854 recalls=0 avg=0.620 source=memory/2026-06-16.md:44-45]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:49:50 -->
- security-check cron 超时修复: **问题**: timeout 60s 导致大量命令执行失败 **修复**: timeout 60s �?300s，payload 增加 timeout 字段 [score=0.854 recalls=0 avg=0.620 source=memory/2026-06-16.md:49-50]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:24:24 -->
- v5/v5.1 架构进化: **v5 组件**: [score=0.836 recalls=0 avg=0.620 source=memory/2026-06-16.md:24-24]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:26:26 -->
- 小红书封号修复: **修改文件**: [score=0.827 recalls=0 avg=0.620 source=memory/2026-06-15.md:26-26]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:29:29 -->
- v5/v5.1 架构进化: **健康检�?*: 89/98 (A) [score=0.822 recalls=0 avg=0.620 source=memory/2026-06-16.md:29-29]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:5:5 -->
- 记忆巡检: **时间**: 09:00 [score=0.816 recalls=0 avg=0.620 source=memory/2026-06-16.md:5-5]

## Promoted From Short-Term Memory (2026-06-23)

<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:26:26 -->
- v5/v5.1 架构进化: **v5.1 组件**: [score=0.805 recalls=0 avg=0.620 source=memory/2026-06-16.md:26-26]
