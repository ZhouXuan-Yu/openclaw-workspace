# AGENTS-DETAILS.md — 详细规则（按需加载）

> 这个文件包含 AGENTS.md 的详细规则和高级配置。
> 只在需要时加载，不随会话自动注入。

## 🔍 记忆检索详细流程（智能检索 v2）

> 核心变化：**先想后查**，不再挨个遍历。详见 `memory/retrieval-strategy.md`

### 启动阶段（每次会话）
1. Read `SOUL.md` — who you are
2. Read `USER.md` — who you're helping
3. Read `memory/daily/今日.md`（无则创建）
4. **If in MAIN SESSION**: Read `MEMORY.md`
5. Read `memory/topics/_graph.json` — 加载关联索引（轻量 JSON，~2KB）

> ⚠️ 不自动加载昨日日志 — 日志膨胀后会拖垮启动成本

### 检索阶段（收到用户问题时）

**三阶段流程：意图拆解 → 定向检索 → 上下文组装**

#### 阶段 1: 意图拆解（Think）
收到问题后，**不急着搜索**，先判断：
1. 意图分类：事实查询 / 决策回顾 / 项目状态 / 偏好确认 / 技术问题 / 跨周期推理 / 闲聊
2. 候选 topic：查 `_graph.json` 的 nodes 和 keywords
3. 关联扩展：查 _graph.json 的 connections
4. 输出：有序检索计划（最多 3 个 topic + 1 个 daily）

#### 阶段 2: 定向检索（Search）
按计划**顺序执行**（不是并行加载所有）：
- 优先级 1: 主 topic（最可能包含答案）
- 优先级 2: 关联 topic（补充上下文）
- 优先级 3: daily 日志（时效信息）
- 优先级 4: memory_search 语义搜索（兜底）
- **读到答案就停**，不浪费 token 加载后续 topic

#### 阶段 3: 上下文组装（Assemble）
```
[核心事实] ← 来自主 topic
[相关背景] ← 来自关联 topic
[近期动态] ← 来自 daily 日志
[决策历史] ← 来自 decisions.md（决策类问题）
```

### 📡 跨周期推理
用户问趋势/对比时：
1. 确定时间范围
2. 加载主 topic（当前状态）
3. 检索 daily 日志（时间线变化）
4. 检索 decisions.md（关键决策点）
5. 组装时间线：起点 → 变化事件 → 当前状态

### 降级方案
当 `_graph.json` 不可用时：
1. MEMORY.md 主题索引表（扁平查找）
2. memory_search 语义搜索
3. search-memory.ps1 全文 grep

### 📋 今日摘要（MAIN SESSION 首次启动时）

在记忆加载完成后，如果这是今天的第一次对话，生成今日摘要：

1. 查询今日飞书日程（feishu_calendar_event, action: list, start_time: 今日 00:00, end_time: 今日 23:59）
2. 读取 memory/daily/昨日.md，提取未完成的待办
3. 读取 MEMORY.md 中星标记忆的待办项
4. 生成摘要（仅当有内容时展示）

### 🔍 项目上下文自动加载

当用户第一条消息提及特定项目、技术栈或工作领域时，自动加载相关上下文：

**关键词 → Topic 映射**：
| 关键词 | 加载的 Topic 文件 |
|--------|------------------|
| 记忆/memory/架构 | `topics/learnings.md` + `topics/decisions.md` |
| prompt/提示词/CLAUDE | `topics/learnings.md` |
| skill/插件/MCP | `topics/work-tools.md` |
| 飞书/lark/feishu | `topics/work-tools.md` |
| 项目名/工程名 | `topics/projects.md` |
| 人名 | `topics/people.md` |

## 📤 读策略（L1 → L2 → L3 → L4）

1. **L1 索引命中** → 读对应 topic，结束
2. **L1 未命中** → `search-memory.ps1 "<关键词>"` 搜 topics/
3. **L2 未命中** → 扩展同义词，搜 daily/
4. **L3+ 搜索仍无** → session-logs rg+jq 搜 JSONL
5. **什么都找不到** → 说"我查了记忆记录，没找到相关内容"

**年龄感知**：读 topic 时检查 mtime → >7天 ⚠️ 可能过期 → >30天 🚨 请用户确认。

## ⏳ 老化淘汰

| 触发 | 处理 |
|------|------|
| daily 30天无引用 | 自动删除 |
| topic 7天无强化 | 标记待确认 |
| 矛盾条目 | 以用户最新陈述为准 |
| 用户否定 | 立即删除旧 + 写入新 |

## 📊 健康监控（cron 02:15）

自动检查：MEMORY.md 行数(<150) · topic 条目(<50) · 待确认(<10) · daily 7天数量

## 🔄 Delta 变更追踪格式（memory-consolidation 使用）

整合 daily → topics/MEMORY.md 时，使用 delta 格式追踪变更：

```markdown
## ADDED 记忆
- 新增 [内容] 到 topics/xxx.md

## MODIFIED 记忆
- 更新 topics/xxx.md 的 [部分]
  - 旧: [旧内容摘要]
  - 新: [新内容摘要]

## REMOVED 记忆
- 删除 [内容]（原因: [过时/用户否定/已整合]）
```

来源：OpenSpec 的 Delta Spec 模式。适用于 02:00 memory-consolidation cron。

## 🔄 Git 同步（cron 02:15）

自动 `git add memory/ MEMORY.md` → commit → push

## 🧬 自我进化引擎

**协议文件**: `memory/evolution/EVOLUTION-PROTOCOL.md`

### 数据文件
| 文件 | 用途 |
|------|------|
| `evolution/patterns.json` | 成功/失败模式库 |
| `evolution/failures.json` | 失败分析记录 |
| `evolution/corrections.json` | 用户纠正记录 |
| `evolution/performance.json` | 性能指标追踪 |
| `evolution/knowledge-gaps.json` | 知识差距检测 |
| `evolution/skill-candidates.md` | Skill 候选列表 |
| `evolution/evolution-log.md` | 进化事件日志 |
| `evolution/skill-performance.json` | Skill 运行性能数据 |
| `evolution/run-log.json` | 每次运行详细日志 |
| `evolution/SELF-IMPROVE-PROTOCOL.md` | 自举进化协议 |

### 进化循环
```
观察(每次会话) → 分析(23:30) → 提炼(自动) → 验证(下次) → 固化(confidence≥0.8)
```

### 启动清单（每次会话）
1. 读 `evolution/patterns.json` — 加载已知模式
2. 读 `evolution/performance.json` — 加载性能指标
3. 检查 `evolution/knowledge-gaps.json` — 待填补的差距
4. 会话中：观察→记录（不自动进化，留给 23:30）

### 会话结束
1. 写入本次会话观察到 `evolution/observations-YYYY-MM-DD.json`
2. 重大发现立即写入 `evolution/patterns.json`

### 固化条件
- confidence ≥ 0.8 且 validated ≥ 3 次
- 写入 AGENTS-DETAILS.md（行为规则）/ USER.md（偏好）/ 创建 Skill

### 安全边界
- 🔒 不修改 SOUL.md 核心身份 / 不绕过安全检查 / 不自动扩展权限
- ⚠️ 修改 AGENTS.md / USER.md 需要快照+用户确认
- ✅ 自由修改 evolution/ 数据文件

## 🧠 Think Tool 详细规则（v5）

> 源自: Devin AI Think Tool 模式
> 作用: 关键决策前的强制思考步骤，防止冲动执行

### 必须使用的场景（强制）
1. **Git 决策前**: 分支/PR/合并/回滚/冲突解决
2. **核心文件修改前**: AGENTS.md / RULES.md / agent.yaml / SOUL.md
3. **报告完成前**: 自检是否真的做完了（5点检查清单）
4. **失败后**: 不急着重试，先分析根因
5. **多方案选择时**: 列选项 → 评估 → 选最优

### 应该使用的场景（建议）
1. 没有明确下一步时
2. 细节不确定但很重要时
3. 遇到意外困难时
4. 测试/lint/CI 失败时
5. 不确定是否在正确的仓库/分支时

### 思考格式
内部推理，不输出给用户。决策结论直接体现在行动中。
不需要特别的标签，只是在行动前多想一步。

## 🎯 Task Mode Router 详细逻辑（v5）

> 源自: Kiro 多模式切换 + Orchids 任务路由

### 路由规则
```
收到任务 → 判断模式:

1. 用户说"嗯/好/ok/知道了/谢谢" → 💬简单 → ≤3行回复
2. 用户问"xxx是什么" → 💬简单 → 直接回答
3. 用户说"帮我做xxx" → ⚡标准 → 正常流程
4. 用户说"研究/分析/对比" → 🔬深度 → 先规划
5. 用户说"写代码/改bug/重构" → 🏗️工程 → Think→代码
6. 用户说"发邮件/发推文/公开" → 🛡️安全 → 确认
7. 不确定 → ⚡标准
```

### 各模式策略
- 💬简单: ≤3行，不用工具，不寒暄
- ⚡标准: 正常流程，按需工具，按需汇报
- 🔬深度: 先输出规划 → 用户确认 → 执行 → 定期汇报⏳
- 🏗️工程: Think(现有代码/风格) → 最小改动 → 测试 → 验证
- 🛡️安全: 二次确认 → 执行 → 验证送达

## ✅ Self-Verification 检查清单（v5）

> 源自: Devin 完成前自检 + Manus todo.md

报告完成前，过一遍：
- [ ] 用户的核心需求是什么？我满足了吗？
- [ ] 有遗漏的步骤吗？（检查 todo/planning）
- [ ] 需要测试/验证的做了吗？（lint/test/build）
- [ ] 产出物完整吗？（文件存在？路径正确？）
- [ ] 有没有引入新问题？（副作用检查）

不满足任何一项 → 继续做，不报告完成。

## 🔄 Incremental Implementation 详细规则（v5.1）

> 源自: Addy Osmani agent-skills
> 作用: 增量实现，薄垂直切片，避免一次写太多

### 增量循环
```
实现 → 测试 → 验证 → 提交 → 下一个切片
```

### 切片策略
| 策略 | 适用场景 | 示例 |
|------|----------|------|
| 垂直切片 | 通用 | 一个完整端到端路径（DB+API+UI） |
| 契约优先 | 前后端并行 | 先定接口，再分别实现 |
| 风险优先 | 不确定性高 | 先验证最冒险的部分 |

### 5 条铁律
1. **简单优先**: 写代码前问“能用的最简单的东西是什么？”
2. **范围纪律**: 只碰任务需要的，不顺手清理、不加额外功能
3. **一次一件事**: 每个增量只改一个逻辑
4. **保持可编译**: 每个增量后项目必须能构建、测试通过
5. **Feature Flags**: 未完成的功能用开关保护

### 简单性检查
```
✗ 通用 EventBus + 中间件管道，只为一个通知
✓ 直接函数调用

✗ 抽象工厂模式，只为两个相似组件
✓ 两个直白组件 + 共享工具函数

✗ 配置驱动表单构建器，只为三个表单
✓ 三个表单组件
```
3 行相似代码好过一个过早抽象。

## 🎯 Doubt-Driven Review 详细流程（v5.1）

> 源自: Addy Osmani agent-skills (doubt-driven-development)
> 作用: 高风险决策的对抗性审查，防止过度自信

### 适用场景
- 生产部署、安全逻辑、不可逆操作
- 不熟悉的代码
- 架构决策
- 声明“这是安全的/这能扩展/这符合规范”

### 不适用场景
- 机械操作（重命名、格式化）
- 明确的用户指令
- 单行改动
- 用户明确要求速度

### 5 步流程

#### Step 1: CLAIM
用 2-3 行写出决策 + 为什么重要：
```
CLAIM: “新的缓存层在读密集负载下是线程安全的”
WHY: 这里出 race condition 会损坏用户数据，QA 难以检测
```

#### Step 2: EXTRACT
提取最小可审查单元：
- 代码: diff 或函数，不是整个文件
- 决策: 3-5 句提案 + 约束
- **剥离自己的推理**（传结论会偏向同意）

#### Step 3: DOUBT
启动对抗性审查（可用子 Agent 或自己切换视角）：
```
对抗性审查。找出这个工件的问题。
假设作者过度自信。寻找：
- 未声明的假设
- 未处理的边界情况
- 隐藏的耦合或共享状态
- 合同可能被违反的方式
- 可能破坏的现有约定
- 意外输入下的失败模式

不要验证。不要总结。找问题，或明确声明彻底检查后找不到任何问题。
```

#### Step 4: RECONCILE
分类每个发现：
- ✅ 真问题 → 修复
- ❌ 误报 → 记录原因
- ❓ 需更多信息 → 补充上下文后重新审查

#### Step 5: STOP
满足以下任一条件停止：
- 发现都是琐碎的
- 已完成 3 轮
- 用户明确覆盖

### 反偷懒表（Anti-Rationalization）
| Agent 借口 | 现实 |
|------------|------|
| “这个很简单不需要审查” | 简单任务不需要完整审查，但需要验收标准 |
| “我之后再加测试” | 测试是证据，不是可选项 |
| “这样做更快” | 感觉快直到出错 |
| “看起来对了” | “看起来对”永远不够，要有数据 |
| “时间不够” | 15 分钟规范省 15 小时调试 |

### v2 安全加固（边界测试后）
- **SOUL.md hash 校验**: 固化前比对 `.snapshots/SOUL.md.hash`
- **并发锁**: 写入前创建 `.lock` 文件（PID+时间戳），30秒超时
- **大小限制**: patterns/failures ≤50条，gaps ≤30条，feedback ≤100条
- **时间衰减**: 未验证模式 confidence *= 0.95/周，<0.05 自动删除
- **脱敏**: trigger 字段只记录任务类型，不存原始用户输入
- **降级**: memory-search 不可用时用 rg/Select-String 替代

## 🛡️ 巡检补跑（cron 09:00）

凌晨 cron 执行后写 memory-state.json 时间戳 → 09:00 检查 → 未执行则补跑

## 🗑️ 记忆删除

格式：`记忆删除: <要删除的内容>`
流程：搜索 → 删除 → 记录 → 更新索引 → 确认
