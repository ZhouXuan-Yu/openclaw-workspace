# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260611-001] best_practice

**Logged**: 2026-06-11T23:30:00+08:00
**Priority**: high
**Status**: promoted
**Area**: infra

### Summary
记忆工具本身也需要边界测试

### Details
search-memory.ps1 是记忆体系的基础设施，但首日上线就出 3 轮 bug（UTF-8 → 编码 → 空查询 → 虚假结果）。

### Suggested Action
写完工具先跑边界测试，别等用户踩坑

### Metadata
- Source: conversation
- Related Files: search-memory.ps1
- Tags: testing, memory, robustness
- Pattern-Key: test_before_ship
- Recurrence-Count: 3
- First-Seen: 2026-06-11
- Last-Seen: 2026-06-11

### Resolution
- **Resolved**: 2026-06-11T22:13:00+08:00
- **Notes**: v6 重写，英文 key + UTF-8 BOM + 空查询防护

---

## [LRN-20260611-002] best_practice

**Logged**: 2026-06-11T23:30:00+08:00
**Priority**: high
**Status**: promoted
**Area**: config

### Summary
核心文件 token 密度是隐性成本

### Details
AGENTS.md 膨胀到 470 行后才被发现，token 密度失控。

### Suggested Action
定期检查核心文件行数，<200 行是硬约束

### Metadata
- Source: user_feedback
- Related Files: AGENTS.md
- Tags: token-budget, file-size
- Pattern-Key: enforce_file_size
- Recurrence-Count: 1
- First-Seen: 2026-06-11

### Resolution
- **Resolved**: 2026-06-11T15:20:00+08:00
- **Notes**: AGENTS.md 瘦身 57% → 200 行

---

## [LRN-20260611-003] correction

**Logged**: 2026-06-11T23:30:00+08:00
**Priority**: medium
**Status**: promoted
**Area**: infra

### Summary
先测试已有功能，再推进新功能

### Details
用户纠正「先打牢基础，做测试看边界」→ 从建设转向验证的节奏纠正。Phase 2-4 一天内全部完成验证，但底层工具反复出问题。

### Suggested Action
先测试后建设，不要赶工

### Metadata
- Source: user_feedback
- Tags: workflow, pacing
- Pattern-Key: test_before_build
- Recurrence-Count: 1
- First-Seen: 2026-06-11

### Resolution
- **Resolved**: 2026-06-11T22:13:00+08:00
- **Notes**: 大规模测试 + 修复 6 个缺陷

---

## [LRN-20260611-004] insight

**Logged**: 2026-06-11T13:30:00+08:00
**Priority**: medium
**Status**: promoted
**Area**: config

### Summary
Markdown + grep 战胜向量数据库

### Details
所有世界级方案（Claude Code / Codex / Hermes / claude-mem）都用 markdown 文件 + grep 做主力记忆，没有用向量数据库。

### Suggested Action
保持 markdown 为主，向量为辅

### Metadata
- Source: conversation
- Tags: architecture, memory
- Related Files: 03_记忆系统进化.md

---

## [LRN-20260611-005] insight

**Logged**: 2026-06-11T13:30:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
几层不是关键，三条机制才是

### Details
网上 4 层分类法是认知科学 CoALA 框架，描述「记忆长什么样」，不解决「怎么用」。真正让 agent 越用越智能的是：写入判断树 + 搜索扩展 + 老化淘汰。

### Suggested Action
关注机制设计，不要纠结层数

### Metadata
- Source: conversation
- Tags: architecture, memory, design-philosophy
