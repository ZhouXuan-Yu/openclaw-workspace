# 长任务独立执行循环 (Task Loop) v4.0

借鉴 SCALE Engine + Addy Osmani Long-Running Agents + Ralph Loop + Oracle Agent Loop + Anthropic Brain/Hands/Session + Fast.io Checkpointing 的融合设计。

## 参考来源
- Addy Osmani, "Long-running Agents" (2026): 三墙理论、Ralph Loop、Brain/Hands/Session 解耦
- Oracle, "What Is the AI Agent Loop": 五阶段循环 (Perceive→Reason→Plan→Act→Observe)、token 成本 4-15x
- Anthropic, "Effective harnesses for long-running agents": 初始化器/编码器分离、test ratchet
- Anthropic, "Scaling Managed Agents": Session as append-only event log
- Fast.io, "AI Agent Checkpointing": Step/Milestone/Human-in-Loop 三种 checkpoint 模式、原子写入、幂等恢复
- Virtido, "Agentic Workflow Patterns 2026": HITL checkpoint、零信任安全
- Matt Pocock, "Workflow for AI Coding": Tracer bullet slicing、Grill→PRD→Slice→TDD Loop

## 核心概念

Agent 收到长任务后，按 5 阶段循环自主执行：

```
           ┌──────────────────────────────────────┐
           │         OBSERVE (反馈注入)            │
           ▼                                      │
[PERCEIVE] → [REASON] → [PLAN/SLICE] → [ACT] → [OBSERVE] → [VERIFY] → [REPORT]
    ↑         (ALIGN)                                                       │
    └──────────────────────────────────────────────────────────────────── 下一轮
```

### 三堵墙（Addy Osmani 理论 — v4.0 新增）

每个长任务 Agent 必然撞上的三堵墙，必须工程化解决：
1. **有限上下文 (Finite Context)**：1M token 窗口也会满，context rot 更早到来 → 解法：状态外置、每次迭代读盘、靠文件系统而非模型记忆
2. **无持久状态 (No Persistent State)**：新 session 从空白开始 → 解法：Session as Event Log、checkpoint 文件
3. **无自我验证 (No Self-Verification)**：模型对自己工作评分偏乐观 → 解法：Test Ratchet、分离生成与评估

### Token 成本认知（Oracle 数据 — v4.0 新增）
- 单 Agent 消耗 ~4x 标准聊天 token
- 多 Agent 系统消耗可达 15x
- 必须记录每次 Loop 的 token 消耗用于成本追踪

## 循环步骤

### 1. PERCEIVE — 感知输入 + 状态恢复

- 解析用户输入，提取：任务目标 / 约束条件 / 交付标准
- **v4.0 新增**: 先读 checkpoint 文件——上次有中断吗？如果有，恢复状态入上下文
- 先读文件系统状态（"我现在在哪？有什么？"）再推理
- 写入 `memory/heartbeat-state.json`: `{active: true, task, startedAt, phase: "perceive"}`

### 2. REASON + ALIGN — 推理方案 + 对齐用户

对齐触发条件：
- 涉及 3+ 步骤
- 有多种可行方案
- 用户未明确禁止

**v4.0 新增 — Tracer Bullet 设计 (Matt Pocock 方法)**
复杂任务的对齐不仅仅是"你要A还是B"，而是：
1. 先做最薄的一条端到端切片（Tracer Bullet），贯穿整个流程
2. 验证工具链、数据源、输出格式都可行
3. 再基于验证结果做剩下的完整切片

对齐格式：给推荐方案 + 理由 + 风险 + 替代方案对比

### 3. PLAN/SLICE — 切片规划

将任务拆为可独立验证的切片：
- 每个切片 ≤ 15 分钟工作量
- **v4.0 收紧**: 每个切片 ≤ 3 个工具调用，且 **≤ 1 次 write 操作**。一次 write 超 2000 字 = 必须拆
- 每个切片有明确的验收标准
- 每个切片有回滚路径
- 切片列表写入 `memory/task-plan.json`

**v4.0 新增 — 依赖建模**：
- 标记每个切片的依赖关系（切片3依赖切片2的输出）
- 无依赖的切片标记 `parallel: true`，可同时执行
- 关键路径标记 `critical: true`（失败=整个任务死）

**铁律**：
- 一次只做一个切片
- 每个切片后必须能编译/测试/验证
- 不做顺手清理
- v4.0 新增: **不做乐观预判**——不要假设"下一个切片会很简单"而把评估推迟

### 4. ACT — 执行

执行当前切片：
- **v4.0 强化**: 执行前3步强制前置检查：
  1. `enable cron task-heartbeat`
  2. 读取上次 checkpoint（如果有）
  3. 确认当前切片依赖已满足
- 执行中：遵守增量实现 5 条铁律
- 遇到阻力：惰性检测器自动拦截
- 失败时：分析原因 → 换策略 → 继续（不停止整个循环）

**v4.0 新增 — Test Ratchet (Anthropic 机制)**：
- 每次修改代码时，新增的测试不允许删除或跳过已有测试
- 验证通过 = 至少 1 个新测试 + 0 个跳过/删除
- 这防止 Agent "让测试通过"的经典自欺行为

### 5. OBSERVE — 观察结果（v4.0 新增独立阶段）

**这是 v4.0 最关键的改进**。之前 OBSERVE 隐含在 EXECUTE 里，从未被显式执行。

- 上个 ACT 的实际结果是什么？
- 结果和预期一致吗？不一致是因为什么？
- 这个结果是否改变了我对剩余切片的假设？
- 是否需要调整切片计划？

OBSERVE 输出写入 `memory/task-observations.jsonl`（append-only，格式见下面 Session Event Log）

### 6. VERIFY — 验证

每个切片完成后必须验证：
- test / lint / build 至少一项通过
- 与实际需求对比（"做的是用户要的吗？"）
- 如果失败：分析原因，修复后重试 ≤ 3 次，超过则询问用户

**验证铁律（v3.1 保留 + v4.0 强化）**：
- ❌ 禁止用开放式提问（"数据够了吗？"） → 用户不会替你做QA
- ✅ 必须提供可量化证据：数量/覆盖率/对比值
- ✅ 必须标记缺口：明确说"X维度缺失"而非模糊的"可能不够"
- ✅ 必须给出决策建议："建议继续/建议回补" — 由用户选择
- ✅ 必须报告覆盖率：数据源数/维度数/置信度，即使缺口为 0 也要报
- **v4.0 新增**: 必须报告 token 消耗（本次切片用了多少 token）
- 格式：覆盖 X 个数据源 / Y 个维度（Z%），缺口在 W，置信度 [高/中/低]，token: T，建议 [继续/回补]

### 7. REPORT — 汇报

每个切片完成后向用户汇报：
```
✅ [切片名] 完成
📎 证据: [结果]
📊 覆盖率: X/Y (Z%) | token: T
⚠️ 风险: [如有]
🔜 下一步: [下一切片]
```

循环回到 PLAN/SLICE 执行下一切片。

### 全部切片完成后：

```
🎉 任务全部完成
📊 统计:
├── 切片数: X
├── 工具调用: N
├── token 估算: T
├── 验证: ✅ verify items
└── 产出: [产出文件列表]
```

关闭心跳: `write memory/heartbeat-state.json {active: false}` + `disable cron task-heartbeat`

## 检查点 (Checkpoint) — v4.0 大幅增强

### 三种 Checkpoint 模式（Fast.io 分类）

| 模式 | 触发条件 | 保存内容 | 适用场景 |
|------|---------|---------|---------|
| **Step Checkpoint** | 每完成一个切片 | 切片输出文件路径 + 剩余切片列表 | 默认 |
| **Milestone Checkpoint** | 完成关键切片（标记 critical 的） | 完整状态快照 | 高风险任务 |
| **Human-in-Loop Checkpoint** | 要请求用户确认/审批前 | 已完成工作 + 待确认事项 | 外部输出前 |

### Checkpoint 写入协议

```json
{
  "task": "任务名",
  "version": 1,
  "created_at": "ISO-8601",
  "completed_slices": ["切片1", "切片2"],
  "remaining_slices": ["切片3", "切片4"],
  "slice_outputs": { "切片1": "output/file1.md", "切片2": "output/file2.md" },
  "known_gaps": ["缺口描述"],
  "token_estimate": 12000,
  "last_action": "write: output/file2.md",
  "resume_from": "切片3的第一个工具调用"
}
```

### Checkpoint 安全规则
- **原子写入**：先写临时文件 `.checkpoint.tmp`，再 rename 到 `task-checkpoint.json`。防止中途崩溃导致文件损坏
- **幂等恢复**：恢复时，已完成的工具调用不重复执行。Agent 检查 last_action，跳过已完成步骤
- **保留策略**：保留最近 5 个 checkpoint + 所有 Milestone checkpoint
- **验证**：checkpoint 写入后立即读回验证 JSON 可解析

### Checkpoint 强制规则
- 切片 3/6/9... 完成后必须写 checkpoint，不写不许进下一片
- 中断恢复时：先读 checkpoint，汇报"上次中断于切片X，已完成Y/Z"再继续
- v4.0 新增: Milestone checkpoint 后必须 verify 文件完整性

## Session Event Log（v4.0 新增 — Anthropic 方案）

借鉴 Anthropic Managed Agents 的 Session as Event Log 设计。

每步执行追加一条事件到 `memory/task-events.jsonl`:
```json
{"ts":"ISO-8601","phase":"act|observe|verify","action":"工具名","input":"..."}
```

为什么要做：
- Brain crash 后可以从 Event Log 重建状态
- 复盘时能看到"Agent 当时看到了什么，做了怎样的决策"
- 脱离模型的上下文窗口，Session 永远可追溯

## 安全机制

### 自动暂停条件
- 同一操作连续失败 ≥3 次 → 暂停整条任务，询问用户
- 文件修改超过预期范围 → 暂停，确认
- 用户干预/新消息 → 立即响应，保存当前进度
- **v4.0 新增**: Token 消耗超过预期 200% → 暂停，询问是否继续

### 用户随时可中断
- 用户说"停"/"等一下"/"先做X" → 保存 checkpoint，立即中断
- 中断后可从最近的 checkpoint 恢复

## 与现有系统的集成

| 组件 | 集成方式 |
|------|---------|
| task-heartbeat | 执行时 enable，完成时 disable |
| 惰性检测器 | 执行层自动拦截 |
| grill-me | 复杂任务对齐阶段使用 |
| RULES.md | 全程遵守硬约束 |
| MEMORY.md | 完成后写入每日日志 |
| task-events.jsonl | v4.0 新增: 每步追加事件 |
| task-observations.jsonl | v4.0 新增: OBSERVE 阶段输出 |

## 切片设计原则

- **粒度控制**: 每个切片 ≤ 3 个工具调用，且 ≤ 1 次 write 操作。超过 2000 字的 write = 必须拆
- **独立性**: 每个切片应可独立验证，不依赖后续切片内容
- **并行优先**: 如果两个切片无依赖，标记 parallel，同时执行
- **动态调整**: 切片 N 的发现应在切片 N+1 中体现
- **产出明确**: 每个切片必须有可见产出，不能是"了解了XXX"这种无形物
- **v4.0 新增**: Tracer Bullet 优先——复杂任务先做贯穿全流程的最薄切片验证可行性

## 心跳强制规则

- 切片执行前: 必须 enable cron task-heartbeat
- 全部切片完成后: 必须 disable cron task-heartbeat
- 中途暂停: disable，恢复时重新 enable
- 上一次 Task Loop 的心跳未关闭 = 先关再开新任务

## 复盘

每次 Task Loop 完成后，自动生成复盘：

```
🔁 Task Loop 复盘 v4.0
✅ 做对的:
   - [具体哪些环节正确执行]
❌ 做错的:
   - [具体哪些环节错误/遗漏]
🪟 三堵墙检查:
   - 有限上下文: [是否遇到了context rot?]
   - 持久状态: [checkpoint 是否正确写入?]
   - 自我验证: [是否按test ratchet规则验证?]
🔧 改进项:
   - [下次要改什么]
📝 协议更新:
   - [如果有需要修改task-loop.md的地方]
```

复盘结果写入 `memory/task-loop-retrospectives/YYYY-MM-DD-任务名.md`

## 使用方式

用户说以下任一触发词即启动长任务循环:
- "做一下XX" (多步骤任务)
- "帮我完成XX" (复杂任务)
- "全流程XX" (端到端任务)
- 或 Agent 判断任务需要 3+ 步骤时主动进入此模式

Agent 以 `⏳ [任务名] 开始执行，X 步切片` 开头，按循环执行。
