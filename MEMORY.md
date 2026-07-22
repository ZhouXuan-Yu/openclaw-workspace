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

## Promoted From Short-Term Memory (2026-07-13)

<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:69:69 -->
- 质量评估: **子 Agent 的上下文缺失问题**： [score=0.906 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:69-69]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:76:79 -->
- 适合蜂群的场景 ✅: | 场景 | 质量 | 说明 | |------|------|------| | 批量读文件 | ✅ 好 | 读 20 个文件各自独立，不需要背景 | | 批量搜索（不同关键词） | ✅ 好 | 每个搜索自包含 | [score=0.906 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:76-79]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:80:82 -->
- 适合蜂群的场景 ✅: | 并行数据抓取 | ✅ 好 | 爬多个 URL 独立 | | 批量格式转换 | ✅ 好 | 机械任务，不需要判断力 | | 多方向分析 | ⚠️ 中等 | 每个 Agent 各自分析，我再汇总 | [score=0.906 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:80-82]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:3:5 -->
- Session: 2026-07-07 14:14:54 GMT+8: **Session Key**: agent:main:openclaw-weixin:87f48d3a5105-im-bot:direct:o9cq809s5mwppkptln8ewptnlvzm@im.wechat; **Session ID**: 5073f5a9-bdde-461f-98fd-ff3b8107c5f8; **Source**: openclaw-weixin [score=0.874 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:3-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:32:34 -->
- Conversation Summary: ✅ **README.md** 已补充并推送; ✅ **每次修改后立即 git push** — 刚推送的 2 个 commit 都是即时执行的; ✅ **MEMORY.md 星标记录** — 今后每次会话都会读到这条硬要求 [score=0.874 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:32-34]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:36:38 -->
- Conversation Summary: 以后每次修改完直接 commit + push，不攒批。 user: 你能够启动蜂群模式吗？比如一下开启数十个子agent完成任务吗 assistant: 当前没有现成的「蜂群模式」。不过用 `sessions_spawn` 可以做到**并行派发多个子 Agent**，策略如下： [score=0.874 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:36-38]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:40:40 -->
- Conversation Summary: **单批可并行数量**：取决于模型配额和任务复杂度，理论上一次可以派发十几个到几十个。 [score=0.874 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:40-40]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:45:45 -->
- Conversation Summary: 一回合内多次 sessions_spawn → sessions_yield 等全部完成 [score=0.874 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:45-45]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:48:48 -->
- Conversation Summary: **示例场景（假设需要并行处理 20 个文件）**： [score=0.874 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:48-48]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:51:52 -->
- Conversation Summary: sessions_spawn(task="分析文件1", ...) sessions_spawn(task="分析文件2", ...) [score=0.874 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:51-52]

## Promoted From Short-Term Memory (2026-07-14)

<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:59:61 -->
- Conversation Summary: 模型速率限制（并发太多可能 429）; 每个子 Agent 消耗 Token; 子 Agent 间不能互相通信（各自独立完成任务） [score=0.933 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:59-61]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:63:65 -->
- Conversation Summary: **要我试一次蜂群吗？** 比如你给一个具体任务（批量分析文件夹中的所有文件、批量搜索多个关键词、批量处理数据），我可以一次性派发多个子 Agent 并行执行。给个场景我就跑。 user: 有意义吗？质量会不会很差 assistant: 实话实说，**有意义但场景有限**。 [score=0.933 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:63-65]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:70:72 -->
- 质量评估: 默认 `context="isolated"` → 只有工作区文件，没有当前对话背景，不知道 SOUL.md 的身份规则; 需要 `context="fork"` 继承对话 → 但 Token 消耗翻倍; 每个子 Agent 都是**冷启动**，没有我们之间的默契和上下文积累 [score=0.933 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:70-72]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:54:55 -->
- Conversation Summary: sessions_spawn(task="分析文件20", ...) sessions_yield() → 等全部结果回来 [score=0.901 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:54-55]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:9:9 -->
- Conversation Summary: assistant: Token 已暴露在 Git 历史中，需要： [score=0.901 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:9-9]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:22:22 -->
- Conversation Summary: **⚠️ 注意事项** [score=0.891 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:22-22]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:42:42 -->
- Conversation Summary: **实现方式**： [score=0.891 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:42-42]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07-1414.md:58:58 -->
- Conversation Summary: **实际限制**： [score=0.891 recalls=0 avg=0.620 source=memory/2026-07-07-1414.md:58-58]
