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

## 主题索引
| 主题 | 位置 |
|------|------|
| 偏好 | `topics/preferences.md` |
| 项目 | `topics/projects.md` |
| 多平台发布 | `tools/social-auto-upload/` (见 topics/work-tools.md) |
| 安全扫描 | `tools/SkillSpector/` (见 topics/work-tools.md) |
| 社交内容设计 | `skills/guizang-social-card/` (Codex CLI 生成图片/视频时必用) |
| 学习 | `topics/learnings.md` |
| 决策 | `topics/decisions.md` |
| 人物 | `topics/people.md` |
| 工具 | `topics/work-tools.md` |
| 沟通 | `topics/communication.md` |
| 进化 | `evolution/EVOLUTION-PROTOCOL.md` |
| 智能检索 | `memory/retrieval-strategy.md` + `topics/_graph.json` |
| OpenSpec 分析 | `topics/openspec-analysis.md` |
| 架构增强 | `topics/openspec-arch-enhancements.md` |
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

## Tag 索引
`#memory-architecture` `#skill-evolution` `#claude-fable5` `#openclaw-skills` `#obsidian-notes` `#openspec` `#opengap` `#security-scan` `#workflows`
