# 学习沉淀

> 最后更新：2026-06-29

---

## Tool Calling 原则

从 Claude Fable 5 进攻端提炼的 7 条原则：
1. **工具优先级树** — 内部数据 > 搜索 > MCP
2. **复杂度标尺** — 1 次搜索=简单事实，3-5次=中等，5-10次=深度
3. **意图推导** — 从语言模式判断用什么工具
4. **追问艺术** — 一次问一件事，给 2-4 个选项
5. **成本意识** — 最轻量格式优先
6. **"不该用"的规则** — 每个工具都要写不用的情况
7. **"Think before and after"** — 执行工具前后反思

详见：`prompt学习提示词/Claude/Claude_Fable5_进攻端实战技巧.md`

## 架构设计原则

- **先测试后建设**：写完工具先跑边界测试，别等用户踩坑。Phase 2-4 一天赶完但底层工具反复出 bug 的教训
- **Agent 文件 token 密度是硬约束**：<200 行，定期检查，发现膨胀立即瘦身
- **自检不能留空**：cron 任务输出必须有验证步骤，时间戳全 null 是反面教材
- **Markdown + grep > 向量数据库**：Claude Code / Codex / Hermes / claude-mem 全用 markdown 文件，不用向量 DB
- **年龄感知 > 精确检索**：读旧记忆时自动加时间警告比提高检索精度更实用

## 智能检索（先想后查）

- 从"先查后想"升级为"先想后查"：先读 _graph.json → 意图分类 → 定向检索相关 topic
- `_graph.json` 存储 topic 关联图（9节点/20边），支持 keywords + connections 扩展
- `retrieval-strategy.md` 定义三阶段流程：意图拆解→定向检索→上下文组装
- 跨周期推理：连续检索 ≥2 个 topic → 记录关联候选 → 出现 ≥3 次写入 graph
- 降级方案：graph 不可用时按 MEMORY.md 索引顺序遍历
- 来源：借鉴 YouNavi 认知网络机制

## Memory Architecture 关键发现

- agentmemory 4层管道（工作→情景→语义→程序）是 gold standard
- Hermes 双文件分离 + 硬容量上限最实用
- Claude Code /dream 离线整合理念：24h + 5次 session 后触发
- 记忆整合应关注：用户纠正信号、强化模式、失败信号、肯定确认
- 核心过滤：单次事件不提权，多次出现才记忆

详见：`prompt学习提示词/Memory记忆架构/`

## AI Agent 记忆架构 2026 前沿（2026-06-15 深度研究）

完整报告：`E:\Obsidian仓库\ZhouXuan私人领域\开发项目\AI-Agent记忆架构-2026深度研究.md`

### 核心趋势
- **RAG → MaaS**：记忆即服务架构成为主流，记忆与推理解耦
- **记忆治理是核心**：写入-管理-读取闭环 + 冲突处理 + 智能遗忘 + 来源追踪
- **协同记忆**：受控协作记忆框架（私有→草稿→规范→弃用四层），多Agent集体认知
- **效率双轮驱动**：向量量化压缩存储（TurboQuant 6x） + 多信号检索（Mem0 92.5分/LoCoMo）
- **差异化竞争**：LLM推理能力商品化，记忆系统成为Agent核心壁垒

### 关键技术
- **Mem0 2026算法**：单程分层提取 + 多信号检索，查询token从26K降至7K，LoCoMo 92.5分
- **四层协同记忆**：Private → Shared Drafts → Canonical → Deprecated
- **指数衰减遗忘**：检索时引入新近度信号，时间久远记忆权重自然降低
- **向量量化**：Google TurboQuant，向量存储压缩6倍+，不牺牲检索性能

### 未来方向
1. 自管理记忆（Agent学会何时记忆/遗忘）
2. 生成式记忆（从被动回忆到主动推理）
3. 多模态记忆（文本+视觉+音频+空间）
4. 标准化协同记忆协议（Agent互联网）

## Addy Osmani Agent Skills 分析（2026-06-15）

24 个 Skill 覆盖完整开发生命周期（Define→Plan→Build→Verify→Review→Ship）。

最值得学的 5 个：
1. **doubt-driven-development** — 不确定时先验证再实现（≈ Think Tool）
2. **incremental-implementation** — 增量实现 5 条铁律（已写入 RULES.md）
3. **context-engineering** — 上下文窗口管理
4. **spec-driven-development** — 规格先行
5. **Anti-Rationalization 表** — 对抗偷懒（已加入关键 Skill）

与现有体系互补：
- interview-me ≈ grill-me（需求对齐）
- DDD ≈ Think Tool（关键决策前思考）
- using-agent-skills ≈ Task Mode Router（任务模式路由）

完整报告：`E:\Obsidian仓库\ZhouXuan私人领域\开发项目\Addy-Osmani-Agent-Skills深度解析.md`

## AI Agent 工程化全景 2026（2026-06-15 深度研究）

完整报告：`E:\Obsidian仓库\ZhouXuan私人领域\开发项目\AI-Agent工程化2026深度研究报告.md`

### Harness Engineering（驾驭工程）
- **范式转变**：从 Prompt Engineering(2022-2024) → Context Engineering(2025) → Harness Engineering(2026)
- **核心公式**：AI Agent = 大模型 + Harness Engineering
- **四大支柱**：约束与规则 / 反馈与评估回路 / 工作流编排 / 安全与权限
- **关键洞察**：设计精良的 Harness 带来的性能提升 > 升级下一代大模型

### 主流框架对比
| 框架 | 编排模型 | 记忆 | 最佳场景 |
|------|----------|------|----------|
| LangGraph | 图状态机 | 强（持久化） | 企业级复杂工作流 |
| CrewAI | 角色协作 | 轻量 | 快速原型/任务团队 |
| AutoGen | 对话协作 | 中等 | 动态对话系统 |
| Hermes Agent | 闭环学习 | 非常强 | 长期个性化助手 |
| Haystack | 模块化管道 | 强（RAG） | 知识密集型应用 |

### 多智能体协作模式
- **层级式**：主管 Agent 分配 + 专家 Agent 执行（结构化项目）
- **角色式**：预定义角色流转（CrewAI 模式）
- **对话式**：无中心，协商推进（AutoGen 模式）
- **A2A 协议**：Google 提出的 Agent 互操作开放标准

### MCP 协议 2026
- **架构**：彻底无状态，JSON-RPC 2.0，`_meta` 字段传递上下文
- **传输**：STDIO（本地）/ SSE（远程）
- **开发**：FastMCP (Python) 为主流 SDK，Resources(只读) vs Tools(有副作用)
- **生态**：Anthropic Claude + Cursor 已深度集成，云服务商尚未原生支持
- **定位**：开发者工具领域事实标准，通用基础设施愿景仍在发展

### 与我相关
- OpenClaw 的 Skill 架构 = Harness Engineering 的实践（约束+反馈+编排+安全）
- 记忆 4 层架构对标 Hermes Agent 的闭环学习模式
- MCP 工具调用模式可借鉴到 OpenClaw 的工具集成
- 多智能体编排参考 LangGraph 的图状态机或 CrewAI 的角色模式

## AI Agent 2026 下半年趋势（2026-06-29 深度研究）

完整报告：`E:\Obsidian仓库\ZhouXuan私人领域\开发项目\AI-Agent-2026下半年趋势深度研究.md`

### 自进化 Agent 三巨头
- **GenericAgent** (4.3K⭐): 3,300行种子代码→自动生长，5层记忆+技能结晶(skill crystallization)，首次执行贵但后续 6x token 节省
- **Evolver** (4.7K⭐): 基因进化协议(GEP)，结构化进化资产(genes+capsules)，Git-based 回滚+爆炸半径计算
- **MOSS 论文**: Agent 重写自身源码→自动测试验证→部署，Ratchet 论文提供安全门

### 自进化 vs 微调
- 自进化: 协议化离散周期，可审计，确定性，不需要 GPU
- 微调: 连续梯度更新，黑箱权重，随机性，需要 GPU
- 关键: Evolver 进化"Agent 如何行为"，Fine-tuning 改变"模型知道什么"——不同层

### 记忆架构 2026 前沿
- **行业共识**: Memory 是 Agent Stack 最后的真正战场，LLM 推理能力正在商品化
- **Mem0 2026**: LoCoMo 92.5 分，token 从 26K→6,956，多信号并行检索
- **两层架构成标准**: Tier1(RAM/5-10条记忆) + Tier2(存储/按需供给)
- **记忆生命周期**: 提取→更新→删除，ADD-only 初始 + self-check gate 提升 8x yield
- **RAG vs Agent Memory 分离**: 不同检索命名空间，避免冲突
- **Context Window 是 RAM**: BEAM 研究: 偏好遵循率从第5轮73%降至第16轮33%

### 多 Agent 协议生态
- **MCP** (Anthropic): Agent↔工具，2026 强势回归，OAuth/多租户/企业治理首选
- **A2A** (Google): Agent↔Agent，v1 发布，被 Semantic Kernel 等集成
- **ACP/AGUI/A2UI**: 消息/UI 层协议
- **编排模式**: 层级式(主管+专家)/角色式(CrewAI)/对话式(AutoGen)/协议式(A2A)

### Agent 编译
- Compiling Agentic Workflows into LLM Weights: 多步管道→单次推理，成本 $0.50→$0.005 (100x)，延迟 30s→2s
- IdleSpec: 工具等待时投机规划，预测正确率 60-80%，感知延迟减半

### 对 OpenClaw 的行动建议
1. **短期**: 技能结晶 MVP — task 成功后自动检查可提取 pattern
2. **中期**: MOSS 风格工具调用逻辑自优化 + Ratchet 安全门
3. **长期**: A2A 协议集成 + 多 Agent 编排
