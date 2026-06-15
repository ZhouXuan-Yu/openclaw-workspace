# 重要决策记录

> 最后更新：2026-06-16

---

## 决策日志

| 日期 | 决策 | 理由 | 影响范围 |
|------|------|------|---------|
| 2026-06-11 | 记忆架构采用 4 层 + 文件系统方案 | 零外部依赖，Windows 兼容，未来可升级 | 全局记忆体系 |
| 2026-06-11 | MEMORY.md 只做索引，内容放 topic 文件 | 瘦身 <200 行，按需加载 | 启动 token |
| 2026-06-11 | 记忆架构 v3：三条核心机制（写入/检索/老化） | 别纠结几层，机制才是关键 | 记忆质量 |
| 2026-06-11 | 记忆架构 v4：对标世界级方案 | 两阶段管道+反射+Git同步 | 全面升级 |
| 2026-06-15 | v5 架构进化：Think Tool + Task Mode Router + Self-Verify | 借鉴 Devin/Kiro/Orchids/System Prompt 仓库 | AGENTS.md/RULES.md/agent.yaml |
| 2026-06-15 | Agent Skills 增量实现 + 对抗性审查 | 借鉴 Addy Osmani agent-skills，与现有体系互补 | RULES.md |
| 2026-06-14 | Skill 自进化协议 v1 | 借鉴鲁班方法论，FIX/DERIVED/CAPTURED 三模式 + 调用轨迹 | evolution/skill-evolution.md |
| 2026-06-14 | 小红书草稿模式 | AI 托管检测封禁，改为 save_as_draft 人工发布 | social-auto-upload CLI |

---

> 🛡️ 重大决策记录在此，日常小决策只写 daily 日志
