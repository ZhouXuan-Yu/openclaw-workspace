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
| 06-15 | v5.1: Agent Skills(Doubt-Driven+Incremental Impl)融入RULES.md, 反偷懒表 |

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
| 沟通 | `topics/communication.md` |
| 进化 | `evolution/EVOLUTION-PROTOCOL.md` (v4) |
| 变更影响 | `docs/change-impact-checklist.md` |
| ADR | `docs/adr/` |
| 智能检索 | `memory/retrieval-strategy.md` + `topics/_graph.json` |
| OpenSpec 分析 | `topics/openspec-analysis.md` |
| 架构增强 | `topics/openspec-arch-enhancements.md` |
| GitHub 热门项目 | `topics/github-may-2026-projects.md` |
| 战略思维伙伴 | `knowledge/strategic-thinking-partner.md`（MBB框架集+思维模型）|
| 进化引擎 | `evolution/EVOLUTION-PROTOCOL.md` |
| Skill 自进化 | `evolution/skill-evolution.md` + `evolution/skill-traces/` |
| 自举协议 | `evolution/SELF-IMPROVE-PROTOCOL.md` |
| 测试历史 | `evolution/test-history.json` |
| OpenGAP | `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\OpenGAP核心要点.md` |
| agent.yaml | `agent.yaml` Agent 清单 |
| RULES.md | `RULES.md` 硬约束 |
| workflows | `workflows/` YAML 工作流 |
| hooks | `hooks/` 生命周期钩子 |
| knowledge | `knowledge/` 知识索引 |
| examples | `examples/` few-shot 示例 |
| 图片处理 | ⚠️ 收到图片→本地OCR→模型推理（见 topics/work-tools.md） |
| Wechatsync | `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\Wechatsync-CLI使用手册.md` |
| 社交自动化决策树 | `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\社交自动化决策树.md` |
| YouNavi CLI | `D:\YouNavi\resources\backend\agent-cli.exe`（见 topics/work-tools.md） |
| YouNavi 桥梁 | `tools/younavi_bridge.py`（Python封装，解决编码问题） |
| YouNavi Skill | `skills/younavi-integration/SKILL.md` |
| 每日社交内容 | `workflows/daily-social-content.md`（cron: daily-social-content, 10:00）|

## Tag 索引
`#memory-architecture` `#skill-evolution` `#claude-fable5` `#openclaw-skills` `#obsidian-notes` `#openspec` `#opengap` `#security-scan` `#workflows` `#github-trends`

## Promoted From Short-Term Memory (2026-06-17)

<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:20:21 -->
- 📱 社交发布全链路执行: **时间**: 01:00 - 02:00 **内容**: AI Agent 自进化主题，全链路（内容→卡片→视频→5平台发布） [score=0.854 recalls=0 avg=0.620 source=memory/2026-06-14.md:20-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:23:23 -->
- 📱 社交发布全链路执行: **发布结果**：小红书✅ 抖音✅ B站✅ 快手✅ 视频号✅（修复后） [score=0.854 recalls=0 avg=0.620 source=memory/2026-06-14.md:23-23]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:25:25 -->
- 📱 社交发布全链路执行: **用到的 Skill**：guizang-social-card、hyperframes-video、social-auto-upload [score=0.854 recalls=0 avg=0.620 source=memory/2026-06-14.md:25-25]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:12:14 -->
- 🔧 视频号上传修复（重要）: Playwright locator 超时 ≠ 元素不可见，**先检查 page.url 是否被重定向**; SPA 页面的 URL 重定向是常见反自动化手段; 视频号必须用 headed 模式（`conf.py` 中 `TENCENT_CHROME_HEADED = True`） [score=0.822 recalls=0 avg=0.620 source=memory/2026-06-14.md:12-14]
<!-- openclaw-memory-promotion:memory:memory/2026-06-11.md:12:15 -->
- 文件创建: 原文：`prompt学习提示词/Claude/Claude_Fable5_系统提示词_原文.md`; 精华：`prompt学习提示词/Claude/Claude_Fable5_系统提示词_精华提炼.md`; 进攻端：`prompt学习提示词/Claude/Claude_Fable5_进攻端实战技巧.md`; 对照：`prompt学习提示词/Claude/GGOB_自我优化对照.md` [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-11.md:12-15]
<!-- openclaw-memory-promotion:memory:memory/2026-06-11.md:18:21 -->
- 关键决策: 将 Claude Fable 5 的 4 个边界补丁（犯错处理、心理安全、立场均衡、防注入）加入 SOUL.md; 将 7 条「进攻端」工具调用原则加入 AGENTS.md; 完整重写 IDENTITY.md 角色定义; 记录在 MEMORY.md [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-11.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-11.md:27:27 -->
- 10:30 — 学习 | OpenClaw Skill 工程架构分析: 研究了 6 个工程型 Skill 的 SKILL.md 设计模式。 [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-11.md:27-27]
<!-- openclaw-memory-promotion:memory:memory/2026-06-11.md:3:3 -->
- 2026-06-11 工作日志: > 格式化：`## HH:MM — 类型 | 简述` · 类型 = 决策/学习/讨论/行动/待办 [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-11.md:3-3]
<!-- openclaw-memory-promotion:memory:memory/2026-06-11.md:30:31 -->
- 文件创建: `prompt学习提示词/skill自我进化openclaw/` — 7 个分析文件; 含 skill-creator / taskflow / planning-with-files / github / nano-pdf / gstack + 总览对比 [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-11.md:30-31]
<!-- openclaw-memory-promotion:memory:memory/2026-06-11.md:9:9 -->
- 10:00 — 学习 | Claude Fable 5 提示词深度研究: 研究了 elder-plinius/CL4R1T4S 仓库泄露的 Claude Fable 5 系统提示词（~120KB）。 [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-11.md:9-9]
