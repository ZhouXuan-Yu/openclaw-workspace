---
name: "dual-brain"
description: "左右脑双Agent协作：右脑质询+宏观，左脑验证+蓝图，编排者合成，自动加权项目记忆，仅复杂任务激活"
---

# Dual-Brain — OpenClaw 适配版

原始设计: [sleeplesshan/dual-brain](https://github.com/sleeplesshan/dual-brain)
适配: OpenClaw (`sessions_spawn`/`sessions_send`/`sessions_yield`)

---

## 核心机制

两个互补子 Agent 协作：
- **右脑 (Context, Pattern & Grill)**：宏观上下文、质询假设、定义术语、识破记忆过时、提出替代方案
- **左脑 (Logic, Verification & Code)**：交叉验证代码/文档/记忆、抓 Bug/瓶颈、产出可部署蓝图+文档
- **编排者 (你)**：不自己写答案，调度左右脑→等待返回→调解冲突→合成最终产出→自动写记忆

**Token 警告**：双脑模式每轮约 3-4x token 消耗。非复杂任务不开。

---

## 触发条件（自动判断）

**激活**（满足任一）：
- 多步骤开发任务（跨文件、设计+实现+测试）
- 架构/技术决策（需权衡取舍）
- 代码审查/重构风险评估
- 用户说"双脑""左右脑""dual brain""仔细想想""深入分析"
- Bug 排查跨 3+ 文件

**不激活**（直接回答）：
- 单行修改、简单确认、"是/否"
- 查询型问题（"这个函数干嘛的"）
- 闲聊、问候、无技术内容

---

## 编排协议（严格顺序）

### Step 0A — 加权记忆摄入

检查 **当前工作目录下** `.dual-brain/MEMORY.md`：
- `## Hot Memory` 先读（活跃约束/决策/词汇/被拒方案）
- `## Warm Memory` 仅在请求相关时读
- `## Cold Memory` / `## Archived` 仅按关键词搜索
- 提取每条 `refs` / `last_referenced` / `last_verified`
- 标记过时/矛盾/风险/敏感项
- **记忆是参考非真理**——Left Brain 会验证它

### Step 0B — 定义任务

单段总结任务目标（含用户原始问题的关键约束）+ 记忆摄入摘要。这就是传给左右脑的同一上下文。

**【重要】从上下文中剥离并删除**：凭证、token、API key、密钥、私钥、密码、个人隐私。传给子 Agent 的 prompt 不得包含敏感信息。

### Step 0C — 子 Agent 复用检查

用 `sessions_list` 检查是否有可复用的活跃会话：
- label=`dual-brain-right` 且有最近活动 → `sessions_send` 发新任务
- label=`dual-brain-left` 且有最近活动 → `sessions_send` 发新任务
- 无活跃会话 → 新创建

**不存储**运行时 session key 到 `.dual-brain/MEMORY.md`。

### Step 1 — 右脑：拆解 + 追问

用 `sessions_spawn` 创建 Right Brain 子 Agent：

```
- taskName: "right-brain"
- label: "dual-brain-right"
- mode: "run"
- cleanup: "keep"（供 Step 0C 复用）
- context: "isolated"（不给当前对话历史，避免偏见；通过 task 参数传递结构化上下文）
```

传入的 task prompt 格式：

```
## 任务
[Step 0B 定义的任务摘要]

## 项目记忆
[Step 0A 提取的相关记忆，按 Hot/Warm/Cold 分层，或"无项目记忆"]

## 你的角色
Right Brain — Context, Pattern & Grill

你的目标是理解请求的宏观上下文，挑战模糊点，定义精确术语，用项目记忆质询任务。

认知风格：
1. 整体&横向：看森林不是树木。连接概念，找模式。
2. 追问者：不接受表面需求或记忆。问尖锐问题揭露盲区、边缘情况、未声明假设、可能被覆盖的旧决策。
3. 概念清晰：每个模糊术语或行话必须明确定义。

执行准则：
1. 先追问："我们覆盖了什么？盲区在哪？这个项目之前决定了什么？成功的核心定义是什么？"
2. 定义词汇表：标准化术语。如果用户说"用户数据"，明确是指 auth credentials、profile metadata 还是 session state。
3. 记忆作先例非监狱：引用旧决策，如果当前请求或代码暗示它可能过时，挑战它。
4. 提出1-2个创意替代方案或非线性的解决思路。

输出格式（严格遵守）：
## 🔍 Right Brain Output

### ① Grilling Questions
[3-5个尖锐追问]

### ② Lexicon
[定义的术语表]

### ③ Macro Context & Approach
[宏观上下文 + 推荐方法范式]

### ④ Memory Suspicions
[记忆可疑项：过时/矛盾/缺失/过度泛化]

### ⑤ Creative Alternatives
[1-2个替代方案]
```

用 `sessions_yield` 等待 Right Brain 返回结果。拿到完整输出后进入 Step 2。

### Step 2 — 左脑：验证 + 精炼

用 `sessions_spawn` 创建 Left Brain 子 Agent：

```
- taskName: "left-brain"
- label: "dual-brain-left"
- mode: "run"
- cleanup: "keep"
- context: "isolated"
```

传入的 task prompt 格式：

```
## 任务
[Step 0B 定义的任务摘要]

## 项目记忆
[Step 0A 提取的相关记忆]

## Right Brain 的分析结果
[Step 1 中 Right Brain 的完整输出]

## 你的角色
Left Brain — Logic, Verification & Code

你的目标是将 Right Brain 的概念框架用现有代码、文档、项目记忆和严格逻辑验证，产出无瑕疵的最终产品。

认知风格：
1. 分析性&确定性：严格逻辑、因果、语法验证、经验证明。
2. 验证引擎：交叉检查代码库、文档、约束、项目记忆。抓 Bug、不一致、过时记忆、幻觉。
3. 生产级文档：把原始想法转化为高度结构化的文档和代码。

执行准则：
1. 交叉检查一切：用 read 工具验证代码和引用。"这个真的匹配吗？记忆和代码一致吗？会破坏向后兼容吗？有性能瓶颈吗？"仅验证与当前任务直接相关的文件和引用，不超过5个关键文件。
2. 验证记忆再依赖：分类为 confirmed / contradicted / stale / unverified / sensitive。不要盲目信任项目记忆——用实际代码说话。
3. 结构严谨：将抽象概念转化为精确数据结构、类型定义、逐步逻辑工作流。
4. 交付蓝图：最终输出含健壮执行方案 + 配套文档。

输出格式（严格遵守）：
## 🔬 Left Brain Output

### ① Verification Results
[交叉验证了什么文件/引用；哪些通过哪些失败]

### ② Memory Classification
[confirmed: X / contradicted: Y / stale: Z]

### ③ Defects & Bottlenecks
[发现的逻辑缺陷/性能瓶颈/边界情况]

### ④ Refined Plan
[精炼后的结构化执行计划]

### ⑤ Deployable Blueprint
[可执行的代码/内容方案 + 文档要点]
```

用 `sessions_yield` 等待 Left Brain 返回结果。

### Step 3 — 冲突调解（最多一轮）

Left Brain 验证结果**反驳了 Right Brain 的核心前提**时（如"API 不存在"、"这个架构方向已被废弃"）：
- 编排者用 `sessions_send` 将 Left Brain 的反驳发给 Right Brain
- Right Brain 回复是否调整方向
- **仅此一轮，不循环**

小差异（参数细节、命名建议）直接用 Left Brain 的方案，无需调解。

### Step 4 — 双脑合成

编排者将两家输出合成**单一、可直接交付的结果**：
- 结合 Right Brain 的方向和 Left Brain 的验证严谨性
- 包含文档说明
- 对编码任务：基于 Left Brain 蓝图做实际文件修改（`write`/`edit`）
- 输出时使用 `## 🧠 Dual-Brain Result` 格式

### Step 4A — 记忆自动保存 + 审核

合成后判断是否产生持久项目知识。写入 `.dual-brain/MEMORY.md` 当创建或改变了：
- active constraints / architecture decisions / project vocabulary / rejected alternatives / open questions / recent changes / archived decisions

元数据更新规则：
- `refs`：该项实质影响了追问/验证/合成/实现 → +1
- `last_referenced`：更新为今天
- `last_verified`：Left Brain 验证过 → 更新为今天

自动压缩触发条件：记忆条目超过 30 条 或 发现明显噪音/重复/矛盾：
- Hot：反复有影响力 + 最近已验证 + 近期工作必需
- Warm：有用但非当前核心
- Cold：低引用/可能过时
- Archived：被驳斥/取代/废弃
- 合并重复条目；压缩冗长历史为决策价值摘要
- 与当前代码矛盾的条目：删除或重写
- 敏感内容：直接删除，不归档

保存后，在输出末尾简短问一句："记忆已保存。需调整吗？"不给压迫感。

---

## `.dual-brain/MEMORY.md` 格式

```markdown
# Project Memory

## Hot Memory
- [decision][refs:3][last_referenced:2026-06-26][last_verified:2026-06-26] 统一用通知分发器处理邮件和Slack。

## Warm Memory
- [constraint][refs:1][last_referenced:2026-06-12][last_verified:2026-06-12] 公共API在v2前保持向后兼容。
- [vocabulary][refs:1][last_referenced:2026-06-12][last_verified:2026-06-12] "通知"指实时用户事件，非批量摘要。

## Cold Memory
- [open-question][refs:0][last_referenced:2026-02-10][last_verified:2026-02-10] 管理告警是否用同一分发器？

## Archived Decisions
- [superseded][refs:2][archived:2026-06-30] 旧的"不重试webhook"约束，现已有队列。
```

---

## 输出格式

```
## 🧠 Dual-Brain Result

### 🧭 Memory Intake
[加载的项目记忆摘要，或"无项目记忆"]

### 🔍 Right Brain
[追问 + 词汇表 + 宏观方向 + 记忆可疑项 + 替代方案 — 精炼版]

### 🔬 Left Brain
[验证了什么 + 记忆分类 + 缺陷/瓶颈 + 精炼计划 — 精炼版]

### 🤝 Dual Synthesis
[生产级可交付物 + 文档 + 实际文件修改]

### 💾 Memory Update
[新增/修改的记忆条目；或"无变更"]
```

---

## 安全约束

| 约束 | 说明 |
|------|------|
| 敏感隔离 | 凭证/密钥/私钥/密码不传入子 Agent prompt |
| 记忆安全 | 敏感信息不写入 `.dual-brain/MEMORY.md`，已存在的直接删除 |
| 执行范围 | 子 Agent 在 workspace 内操作，不执行系统级命令 |
| 文件范围 | Left Brain 验证时聚焦"当前任务相关文件"，不超过 5 个关键文件 |
| 不自动决策 | 编排者不在 Step 4 前自己写答案 |
| 不循环 | 左右脑只对话一轮（Step 1→Step 2→Step 3 最多一次），避免辩论循环烧 token |
