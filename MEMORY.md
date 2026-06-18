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

## Promoted From Short-Term Memory (2026-06-18)

<!-- openclaw-memory-promotion:memory:memory/2026-06-12.md:13:15 -->
- 测试结果: MP4: 62 KB（1080x1920，H.264）; GIF: 316 KB; **渲染时间**：约 3 分钟 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-12.md:13-15]
<!-- openclaw-memory-promotion:memory:memory/2026-06-12.md:18:20 -->
- Skill 创建: 创建 `skills/hyperframes-video/SKILL.md`; 文档化完整工作流程：HTML 组合 → 逐帧截取 → 合成视频; 集成到社交自动化流水线 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-12.md:18-20]
<!-- openclaw-memory-promotion:memory:memory/2026-06-12.md:23:26 -->
- 技术发现: imageio-ffmpeg 可以替代系统 FFmpeg; 宽度需为 16 的倍数（1080→1088）避免警告; GSAP timeline 通过 `time()` 方法精确控制帧; 首次运行需下载 Chrome（~101MB） [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-12.md:23-26]
<!-- openclaw-memory-promotion:memory:memory/2026-06-12.md:30:33 -->
- 平台登录状态汇总: | 平台 | 状态 | 发布测试 | |------|------|---------| | 小红书 | ✅ | ✅ 图文发布成功 | | 快手 | ✅ | ✅ 图文发布成功（定时） | [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-12.md:30-33]
<!-- openclaw-memory-promotion:memory:memory/2026-06-12.md:5:5 -->
- 23:52 — HyperFrames 视频生成测试: 用户要求测试 Codex + HyperFrames 生成短视频，并固化为 Skill。 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-12.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-12.md:8:11 -->
- 测试结果: HyperFrames CLI v0.6.94 已安装; FFmpeg 安装失败（choco 权限问题，GitHub 下载超时）; **解决方案**：Playwright 逐帧截取 + imageio 合成; 生成 150 帧（15s @ 10fps） [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-12.md:8-11]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13-audit.md:10:13 -->
- 模块 1：内容质量 ✅: [x] 内容基于真实经历（记忆系统确实搭建了，测试确实跑了）; [x] 技术细节准确（4层架构、26项测试）; [x] 无错误归因; [x] 文字简洁 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-13-audit.md:10-13]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13-audit.md:14:14 -->
- 模块 1：内容质量 ✅: ⚠️ 小红书格式需确认（无Markdown） [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-13-audit.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13-audit.md:17:20 -->
- 模块 2：人设一致性 ✅: [x] 符合"Agent工程开发者"定位; [x] 体现"从零到一"学习过程; [x] 保持技术深度+实战风格; [x] 无卖课感、鸡汤感 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-13-audit.md:17-20]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13-audit.md:24:27 -->
- 模块 3：平台策略 ✅: [x] 小红书已发布（图文）; [x] 抖音已发布（图文）; [x] 快手定时发布; ⚠️ B站视频待制作 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-13-audit.md:24-27]

## Promoted From Short-Term Memory (2026-06-18)

<!-- openclaw-memory-promotion:memory:memory/2026-06-13.md:10:13 -->
- 完整链路（最终版）: Q0: 内容深化（YouNavi） ├── 研究主题 → research_full → 报告 → 提取核心观点 ├── 会议录音 → audio_transcribe → 文字 → 整理 └── 知识积累 → memory/notes → 引用 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-13.md:10-13]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13.md:15:18 -->
- 完整链路（最终版）: Q1-Q3: 内容生产 ├── 路径A 图文 → Codex + guizang + Playwright → PNG ├── 路径B 视频 → edge-tts + HyperFrames → MP4 ├── 路径C 文章 → Markdown → wechatsync → 多平台 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-13.md:15-18]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13.md:21:23 -->
- 完整链路（最终版）: Q4: 内审 → 发布 ├── 视频/图文 → sau CLI → 小红书/抖音/快手/B站 └── 文章 → wechatsync CLI → 知乎/CSDN/掘金/公众号 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-13.md:21-23]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13.md:28:31 -->
- 工具链最终全景: | 层级 | 工具 | 用途 | |------|------|------| | 研究层 | YouNavi CLI | 深度研究·音频转写·知识管理 | | 生产层 | Codex CLI | AI 生成 HTML/代码 | [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-13.md:28-31]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13.md:5:5 -->
- 02:45 — 社交自动化决策树 v2（加入 YouNavi）: 用户指出 YouNavi CLI 应融入链路。已更新决策树，加入 Q0 内容深化环节。 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-13.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:5:5 -->
- 🔧 视频号上传修复（重要）: **根因**：视频号助手检测到自动化浏览器（patchright headless），访问 `/platform/post/create` 会被 302 重定向到 `/platform`（dashboard）。dashboard 上没有 `input[type="file"]`，所以 `page.set_input_files('input[type="file"]', ...)` 永远超时。 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-14.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:7:7 -->
- 🔧 视频号上传修复（重要）: **修复方案**：`open_upload_page` 方法增加重定向检测——如果 URL 不含 `/post/create`，自动点击「发表视频」按钮进入上传表单。 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-14.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-06-14.md:9:9 -->
- 🔧 视频号上传修复（重要）: **修复文件**：`tools/social-auto-upload/uploader/tencent_uploader/main.py` 第 498-509 行 [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-14.md:9-9]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13-audit.md:21:21 -->
- 模块 2：人设一致性 ✅: [x] 原创内容 [score=0.819 recalls=0 avg=0.620 source=memory/2026-06-13-audit.md:21-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-13.md:19:19 -->
- 完整链路（最终版）: └── 路径D 混合 → A+B+C [score=0.809 recalls=0 avg=0.620 source=memory/2026-06-13.md:19-19]
