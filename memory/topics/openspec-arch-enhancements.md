# OpenSpec 架构启发 → 当前架构增强方案

**日期**: 2026-06-12
**来源**: OpenSpec v1.3.1 源码分析

---

## 可借鉴的核心模式

### 1. ✅ Delta 变更追踪 (已部分实现，可增强)

**OpenSpec 思想**: 用 ADDED/MODIFIED/REMOVED/RENAMED 描述增量变化，而非重述全文。

**当前架构现状**: memory/daily/ 已有日志，memory/topics/ 是持久存储，但缺少结构化的"变更描述"。

**增强方案**: 在 AGENTS-DETAILS.md 的记忆写入流程中，增加 delta 格式：
```markdown
## ADDED 记忆
- 新增 OpenSpec 架构分析到 topics/work-tools.md

## MODIFIED 记忆
- 更新 topics/learnings.md 的 prompt 工程部分
  - 旧: 仅记录基础 prompt 技巧
  - 新: 增加 Spec-Driven Development 模式

## REMOVED 记忆
- 删除过时的 Phase 1 验证记录（已整合到 decisions.md）
```

**适用场景**: memory-consolidation (02:00) 整合日志时使用 delta 格式追踪变化。

### 2. ✅ Schema/模板系统 (已部分实现，可增强)

**OpenSpec 思想**: YAML 定义工件类型+依赖关系，可 fork 自定义。

**当前架构现状**: Skill Workshop 已有 proposal 系统，但缺少显式的依赖图。

**增强方案**: 为复杂任务引入轻量级依赖追踪：
```yaml
# 在 task planning 中使用
artifacts:
  - id: research
    generates: research-notes
    requires: []
  - id: design
    generates: architecture-doc
    requires: [research]
  - id: implementation
    generates: code-changes
    requires: [design]
```

**适用场景**: planning-with-files skill 可加入此模式。

### 3. ✅ Source of Truth + Delta 合并 (已实现)

**OpenSpec 思想**: specs/ 是真相源，changes/ 是提议，归档时合并。

**当前架构现状**: 
- MEMORY.md 是索引（真相源）
- memory/topics/ 是持久存储
- memory/daily/ 是变更日志
- memory-consolidation cron 做合并

**结论**: 当前架构已自然实现了此模式。✅ 无需修改。

### 4. ✅ 验证前置 (可增强)

**OpenSpec 思想**: 归档前强制验证规格格式。

**当前架构现状**: memory-health-sync (02:15) 做健康检查，但验证较弱。

**增强方案**: 在 memory-consolidation 中加入验证步骤：
- 检查 MEMORY.md 行数 < 200
- 检查 topics/ 文件格式一致性
- 检查 daily/ 日志完整性
- 检查无重复条目

### 5. ✅ 适配器模式 (参考价值)

**OpenSpec 思想**: 30+ AI 工具通过统一适配器接口集成。

**当前架构现状**: OpenClaw 已有 channel 适配器（weixin/telegram/signal等）。

**结论**: 当前架构已采用此模式。✅ 无需修改。

### 6. ✅ 工件依赖图 (可轻量引入)

**OpenSpec 思想**: DAG 管理工件依赖，拓扑排序确定执行顺序。

**当前架构现状**: AGENTS.md 的流程是隐式的（读 SOUL → 读 MEMORY → 读 daily）。

**增强方案**: 为复杂多步任务引入显式依赖追踪（不改变日常流程）：
```markdown
# 在复杂任务 planning 中使用
Task Dependency Graph:
  [1. 搜索信息] → [2. 分析内容] → [3. 写入文件]
                  ↘ [4. 生成图表] ↗
```

**适用场景**: 只在 >3 步的复杂任务中使用，日常单步任务不引入。

### 7. ✅ 自包含变更文件夹 (参考价值)

**OpenSpec 思想**: 每个变更自包含一个文件夹（proposal + specs + design + tasks）。

**当前架构现状**: memory/topics/ 按主题组织，daily/ 按日期组织。

**结论**: 当前架构不适合此模式（我们不是代码项目管理工具）。但"自包含"思想可用于：
- 重大决策记录时，附带完整的上下文链
- Skill 创建时，包含完整的示例和参考

---

## 增强优先级

| 优先级 | 增强项 | 工作量 | 收益 |
|--------|--------|--------|------|
| P1 | Delta 变更追踪格式 | 小 | 高 - 记忆整合更清晰 |
| P2 | 验证前置增强 | 中 | 中 - 减少记忆污染 |
| P3 | 轻量依赖图 | 中 | 低 - 仅复杂任务受益 |
| P4 | Schema 模板 | 大 | 低 - 当前 Skill Workshop 已覆盖 |

## 不采纳的模式

| 模式 | 原因 |
|------|------|
| 全局 npm 安装 | 不适合我们的场景 |
| Git-only context store | 我们用文件系统+memory |
| 30+ 工具适配器 | OpenClaw 已有 channel 适配器 |
| YAML schema 定义 | 过重，我们用 Markdown + 文件约定 |
| 工作区协调 | 我们是单机单用户 |

---

## 结论

OpenSpec 的核心价值在于 **Spec-Driven 思想** 和 **Delta 变更追踪**。
我们的架构已自然实现了 Source of Truth + 合并模式。
主要可借鉴的是 **Delta 格式** 和 **验证前置**，工作量小但能提升记忆整合质量。
