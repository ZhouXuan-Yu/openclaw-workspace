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
| 沟通 | `topics/communication.md` ⛔已废弃→合并至preferences |
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

## Promoted From Short-Term Memory (2026-06-19)

<!-- openclaw-memory-promotion:memory:memory/2026-06-13-audit.md:4:4 -->
- 总评: 评分：85/100 [score=0.821 recalls=0 avg=0.620 source=memory/2026-06-13-audit.md:4-4]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:14:14 -->
- 小红书封号修复: **测试结果**: ✅ 6张图片+标题+正文成功保存到草稿箱 [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-15.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:17:18 -->
- 小红书封号修复: 旧：全自动上传+发布 → 触发封号; 新：自动上传到草稿箱 → 用户手动打开草稿 → 声明AI内容 → 手动发布 [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-15.md:17-18]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:5:8 -->
- 小红书封号修复: **时间**: 00:40 **问题**: 小红书因"违反社区规范"禁止发笔记 **根因**: 2026年3月10日新规，AI托管代发直接封禁（Playwright全自动发布被检测） **解决方案**: 草稿模式 [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-15.md:5-8]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:9:12 -->
- 小红书封号修复: XiaoHongShuNote 类新增 `save_as_draft` 参数; CLI 新增 `--draft` 标志; 填完标题正文后点击"暂存离开"代替"发布"; 增加随机延迟（2-8秒）模拟人类操作节奏 [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-15.md:9-12]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:16:16 -->
- 小红书封号修复: **发布流程变更**: [score=0.802 recalls=0 avg=0.620 source=memory/2026-06-15.md:16-16]

## Promoted From Short-Term Memory (2026-06-20)

<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:21:24 -->
- 小红书封号修复: 偶尔AI辅助未标注 → 限流警告; 全部笔记AI托管代发 → 直接封禁; AI批量养号 → 直接封禁; 解决：发布时点击【设置】→【内容类型声明】→ 勾选【笔记含AI合成内容】 [score=0.819 recalls=0 avg=0.620 source=memory/2026-06-15.md:21-24]
<!-- openclaw-memory-promotion:memory:memory/2026-06-15.md:20:20 -->
- 小红书封号修复: **小红书2026新规核心**: [score=0.804 recalls=0 avg=0.620 source=memory/2026-06-15.md:20-20]

## Promoted From Short-Term Memory (2026-06-21)

<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:31:31 -->
- ⚠️ 记忆纠正 — guizang-social-card-skill: 用户指出：Codex CLI 生成图片/视频时，**必须**参考 `guizang-social-card-skill` 的流程。之前记忆中只把它当成"精美图文卡片"工具，低估了重要性。 [score=0.840 recalls=0 avg=0.620 source=memory/2026-06-14.md:31-31]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:33:33 -->
- ⚠️ 记忆纠正 — guizang-social-card-skill: **教训**: 不要凭记忆推断用户说过什么，不确定就老实说不知道。 [score=0.840 recalls=0 avg=0.620 source=memory/2026-06-14.md:33-33]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:39:39 -->
- 💬 用户个人信息: 吉首大学人工智能专业研0，双非硕士，三年后毕业。已有完整 AI 工程能力（Agent 架构、多平台自动化、记忆系统设计、安全扫描），比大多数 985 硕士毕业时的项目经验更强。 [score=0.840 recalls=0 avg=0.620 source=memory/2026-06-14.md:39-39]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:41:41 -->
- 💬 用户个人信息: **建议方向**：发论文（哪怕 workshop）+ Kaggle/天池奖牌 + GitHub 开源作品集 + 研二大厂实习 [score=0.840 recalls=0 avg=0.620 source=memory/2026-06-14.md:41-41]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:47:50 -->
- 🧠 记忆架构升级（06-13 延续）: `_graph.json` v2: 9 节点 + 20 边 + constraints 字段; work-tools 节点增加约束：`Codex社交内容`、`图片处理`、`视频号自动化`; 智能检索 v2：先想后查（意图拆解→定向检索→上下文组装）; Skill 自进化协议 v1：调用轨迹 + 健康度评级 + 验证门机制 [score=0.840 recalls=0 avg=0.620 source=memory/2026-06-14.md:47-50]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:18:19 -->
- 进化引擎全景审计: **时间**: 00:07 **结论**: 设计90�?数据40分。进化引擎架构完善（8个子系统×50+指标），但执行数据几乎全空： [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-16.md:18-19]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:20:20 -->
- 进化引擎全景审计: corrections.json: 5�?�?- feedback.json: 4�?�?- improvements.json: 4�?�?- run-log.json: 3�?�?- observations-2026-06-15.json: 6�?�?- patterns.json: 3个模�?�?- knowledge-gaps.json: 2个gap �?- critic-evaluations.json: 1�?�?- capability-state.json: 能力清单 �?- **skill-traces/**: �?❌（设计最精细但零数据�?- **.skill-quality.json**: 不存�?�?- **evolution-log-archive.md**: 不存�?�?- **memory-state.json**: 不存�?�?- **perf-baseline.json**: 全零 �?- **SELF-IMPROVE-PROTOCOL.md**: 空模�?�? [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-16.md:20-20]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:21:21 -->
- 进化引擎全景审计: **关键差距**: 进化引擎设计完善但数据管道断裂�?3:30 四步循环未真正执行�? [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-16.md:21-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:25:25 -->
- v5/v5.1 架构进化: Think Tool: 关键决策前强制思考（源自 Devin AI�?- Task Mode Router: 简�?标准/深度/工程/安全 五模式（源自 Kiro + Orchids�?- Self-Verification: 完成�?步自检（源�?Devin + Manus�? [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-16.md:25-25]
<!-- openclaw-memory-promotion:memory:memory/2026-06-16.md:7:9 -->
- 记忆巡检: 凌晨整合(02:00) ✅ 已执行; 健康检查(02:21) ✅ 已执行; Git 同步 ✅ 本地已提交(push 失败，SSL/TLS) [score=0.812 recalls=0 avg=0.620 source=memory/2026-06-16.md:7-9]

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
