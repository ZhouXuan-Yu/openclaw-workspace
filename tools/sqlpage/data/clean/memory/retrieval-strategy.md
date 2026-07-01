# 智能检索策略 — "先想后查"

**版本**: 1.0
**日期**: 2026-06-13
**核心理念**: 先规划检索路径，再执行检索，最后组装上下文

---

## 1. 与旧策略的区别

| 维度 | 旧策略（先查后想） | 新策略（先想后查） |
|------|-------------------|-------------------|
| 流程 | 收到问题 → 挨个搜 memory → 拼答案 | 收到问题 → **意图拆解** → **路径规划** → 定向检索 → 推理 → 答案 |
| 检索范围 | 模糊，可能读一堆无关文件 | 精确，基于关联图只读相关 topic |
| 跨周期能力 | 弱，靠关键词碰运气 | 强，沿关联链路自动拉取上下文 |
| Token 效率 | 低，加载大量无关内容 | 高，只加载决策链路上的内容 |

---

## 2. 三阶段流程

### 阶段 1: 意图拆解（Think）

收到用户问题后，**不急着搜索**，先回答三个问题：

```
Q1: 用户在问什么？（意图分类）
    → 事实查询 / 决策回顾 / 项目状态 / 偏好确认 / 技术问题 / 闲聊

Q2: 答案可能在哪些 topic 里？（候选 topic）
    → 查 _graph.json 的 nodes 和 keywords

Q3: 这些 topic 跟哪些其他 topic 有关？（关联扩展）
    → 查 _graph.json 的 connections
```

**输出**: 一个有序的检索计划（最多 3 个 topic + 1 个 daily）

### 阶段 2: 定向检索（Search）

按检索计划**顺序执行**（不是并行加载所有）：

```
优先级 1: 主 topic（最可能包含答案）
优先级 2: 关联 topic（补充上下文）
优先级 3: daily 日志（今日/昨日的实时信息）
优先级 4: memory_search 语义搜索（兜底，当 topic 里找不到时）
```

**关键规则**:
- 读到答案就停，不浪费 token 加载后续 topic
- 如果主 topic 已经回答了问题，跳过关联 topic
- daily 日志只在问题涉及时效信息时加载

### 阶段 3: 上下文组装（Assemble）

将检索到的信息组装成**结构化上下文**：

```
[核心事实] ← 来自主 topic
[相关背景] ← 来自关联 topic
[近期动态] ← 来自 daily 日志
[决策历史] ← 来自 decisions.md（如果是决策类问题）
```

---

## 3. 意图分类 → 检索路径映射

| 意图类型 | 典型问法 | 检索路径 |
|---------|---------|---------|
| 事实查询 | "XX 是什么" "XX 在哪" | 主 topic → memory_search 兜底 |
| 决策回顾 | "上次为什么选了XX" | decisions.md → 关联 project topic → daily |
| 项目状态 | "XX 项目怎么样了" | projects.md → 关联 work-tools → daily |
| 偏好确认 | "我喜欢什么" "上次怎么说的" | preferences.md → daily |
| 技术问题 | "这个工具怎么用" "这个错误怎么回事" | work-tools.md → learnings.md → memory_search |
| 跨周期推理 | "跟上次比有什么变化" "趋势是什么" | 主 topic → daily(多天) → decisions.md |
| 闲聊/问候 | "在吗" "怎么样" | 不检索，直接回复 |

---

## 4. 关联图使用规则

### 4.1 查询关联

```
用户提到 "OpenSpec" 
→ _graph.json keywords 命中 "openspec-analysis"
→ connections: ["projects", "learnings", "openspec-arch-enhancements"]
→ 检索计划: openspec-analysis.md → projects.md → learnings.md
```

### 4.2 关联强度

| 强度 | 含义 | 检索策略 |
|------|------|---------|
| core | 核心 topic，信息密度高 | 优先读取 |
| derived | 从核心 topic 派生 | 按需读取 |
| support | 辅助信息 | 仅在核心 topic 不够时读取 |

### 4.3 动态更新

当新 topic 被创建时：
1. 分析其内容，提取 keywords
2. 找到与现有 topic 的关联（共同关键词 / 引用关系）
3. 更新 _graph.json 的 nodes 和 connections
4. 记录到 evolution-log.md

---

## 5. 跨周期推理协议

### 5.1 什么是跨周期推理

用户问的不是"某个时间点的事实"，而是"随时间变化的趋势/对比"。

**示例**:
- "记忆架构从最初到现在改了几次？"
- "跟上周比，项目进度怎么样？"
- "你学到了哪些之前不知道的东西？"

### 5.2 推理流程

```
1. 确定时间范围（从问题推断）
2. 加载主 topic（获取当前状态）
3. 检索 daily 日志（获取时间线上的变化记录）
4. 检索 decisions.md（获取关键决策点）
5. 组装时间线：起点 → 变化事件 → 当前状态
6. 输出趋势分析
```

### 5.3 时间线组装格式

```
[时间线] 主题: XX
├── T0 (初始状态): ...
├── T1 (事件A): 变化了什么
├── T2 (事件B): 变化了什么
└── 现在: 当前状态
```

---

## 6. 与进化引擎的集成

### 6.1 检索失败 → 知识差距

如果检索计划中所有 topic + memory_search 都没找到答案：
1. 记录到 `evolution/knowledge-gaps.json`
2. 标记差距类型：`MISSING_TOPIC` / `INCOMPLETE_TOPIC` / `SCATTERED_INFO`

### 6.2 检索成功 → 关联强化

如果检索计划命中了答案：
1. 更新 `_graph.json` 中对应 node 的 `lastAccessed` 字段
2. 如果发现新的 topic 关联，追加到 connections

### 6.3 模式发现

如果多次检索同一组 topic 才能找到答案：
1. 这组 topic 之间可能存在未记录的关联
2. 记录到 `evolution/patterns.json` 作为候选关联
3. 23:30 反思时确认并更新 _graph.json

---

## 7. 降级方案

当 `_graph.json` 不可用时：
1. 使用 MEMORY.md 的主题索引表（扁平查找）
2. 使用 memory_search 语义搜索（兜底）
3. 使用 search-memory.ps1 全文 grep（最后手段）

---

## 8. 性能约束

| 约束 | 值 | 原因 |
|------|---|------|
| 单次检索最多读取 topic 数 | 3 | 控制 token 消耗 |
| 检索计划生成时间 | <1s | 纯本地 JSON 读取 |
| 关联图最大节点数 | 50 | 防止图过大导致查询变慢 |
| 关联图最大边数 | 200 | 防止过度连接 |
