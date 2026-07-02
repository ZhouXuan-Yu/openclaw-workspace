# 重要决策记录

> 最后更新：2026-07-02

---

## 决策日志

| 日期 | 决策 | 理由 | 影响范围 |
|------|------|------|---------|
| 2026-06-25 | v3 架构升级：惰性检测器 + 长任务执行循环 | task-heartbeat 反复超时，借鉴 SCALE Engine v0.51.0 Hook 阻断机制 | hooks/laziness-detectors.yaml + hooks/task-loop.md + hooks/hooks.yaml + RULES.md |
| 2026-06-25 | RuleMaturity 三阶段（shadow→proposed→enforced） | 规则渐进式演进，避免一次性写出不成熟的硬约束 | RULES.md 规则段 |
| 2026-06-24 | Trust Scoring v1：5 级 trust 标记 + 纠正/验证/冲突机制 | 借鉴 duMem Bayesian trust，轻量文件方案 | memory/evolution/trust-registry.json + RULES.md |
| 2026-06-24 | 分级 Decay v1：5 tier 差异化衰减替代一刀切 | 借鉴 duMem 分级衰减，decay-scanner.py + cron 集成 | scripts/decay-scanner.py + memory-consolidation cron + RULES.md |
| 2026-06-24 | Semantic Dedup v1：中文关键词指纹去重 | 借鉴 duMem Semantic Dedup，改用中文 2-4 字滑动窗口指纹替代 Jaccard | scripts/dedup-scanner.py + RULES.md |
| 2026-06-11 | 记忆架构采用 4 层 + 文件系统方案 | 零外部依赖，Windows 兼容，未来可升级 | 全局记忆体系 |
| 2026-06-11 | MEMORY.md 只做索引，内容放 topic 文件 | 瘦身 <200 行，按需加载 | 启动 token |
| 2026-06-11 | 记忆架构 v3：三条核心机制（写入/检索/老化） | 别纠结几层，机制才是关键 | 记忆质量 |
| 2026-06-11 | 记忆架构 v4：对标世界级方案 | 两阶段管道+反射+Git同步 | 全面升级 |
| 2026-06-15 | v5 架构进化：Think Tool + Task Mode Router + Self-Verify | 借鉴 Devin/Kiro/Orchids/System Prompt 仓库 | AGENTS.md/RULES.md/agent.yaml |
| 2026-06-15 | Agent Skills 增量实现 + 对抗性审查 | 借鉴 Addy Osmani agent-skills，与现有体系互补 | RULES.md |
| 2026-06-14 | Skill 自进化协议 v1 | 借鉴鲁班方法论，FIX/DERIVED/CAPTURED 三模式 + 调用轨迹 | evolution/skill-evolution.md |
| 2026-06-14 | 小红书草稿模式 | AI 托管检测封禁，改为 save_as_draft 人工发布 | social-auto-upload CLI |
| 2026-07-01 | UI设计系统:Techno-Futurist方向 | 深入Awwwards/CSSDA/Mobbin研究后确定暗底+霓虹+玻璃态+Bento Grid | 顶级UI设计/全部场景 |
| 2026-07-01 | UI方案v1→v2推倒重来 | 用户反馈v1太简陋达不到标准，不犹豫直接重构 | 千亿项目UI方案 |

---

> 🛡️ 重大决策记录在此，日常小决策只写 daily 日志
