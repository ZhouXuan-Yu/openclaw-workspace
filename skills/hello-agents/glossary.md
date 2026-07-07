# Glossary

**A2A (Agent-to-Agent Protocol)** — Google 提出的智能体间点对点协作协议，每个 Agent 既是服务提供者也是消费者 (Ch10)

**Agent Loop** — 感知→思考(规划+工具选择)→行动→观察的闭环 (Ch01)

**Agentic RL** — 将 LLM 作为可学习策略嵌入多步决策循环，通过 RL 优化长期任务表现 (Ch11)

**ANP (Agent Network Protocol)** — 概念性去中心化服务发现协议，用于大规模 Agent 网络 (Ch10)

**注意力预算 (Attention Budget)** — 每个 token 可分配的注意力有限，上下文越长注意力越分散 (Ch09)

**BFCL (Berkeley Function Calling Leaderboard)** — 工具调用精度的标准化评估基准，含 1120+ 样本 (Ch12)

**Coze (扣子)** — 字节跳动的零代码 Agent 构建平台，强插件生态和发布渠道 (Ch05)

**上下文腐蚀 (Context Rot)** — 上下文窗口增长后模型准确回忆信息的能力下降 (Ch09)

**上下文工程 (Context Engineering)** — 在 LLM 有限上下文窗口中策划最优信息集合的方法论 (Ch09)

**Dify** — 开源 LLM 应用开发平台，支持 RAG Pipeline 和 Agent 工作流 (Ch05)

**ELIZA** — Weizenbaum (1966) 的模式匹配聊天机器人，通过关键词规则制造共情假象 (Ch02)

**专家系统 (Expert System)** — 知识库+推理机的符号主义 AI 应用，MYCIN 为其代表 (Ch02)

**GAIA (General AI Assistants)** — Meta+HuggingFace 的通用 AI 助手评估基准 (Ch12)

**GRPO (Group Relative Policy Optimization)** — 群组相对策略优化，高效的无批评模型 RL 算法 (Ch11)

**GSSC 流水线** — Gather-Select-Structure-Compress 上下文构建四步法 (Ch09)

**HelloAgents 框架** — Datawhale 社区的自建教学 Agent 框架，"万物皆为工具"理念 (Ch07)

**JIT 上下文 (Just-in-time Context)** — 维护轻量化引用而非数据本身，运行时动态加载 (Ch09)

**知识获取瓶颈 (Knowledge Acquisition Bottleneck)** — 手工编码知识不可规模化的根本问题 (Ch02)

**LangGraph** — LangChain 生态的 Agent 执行流建模为状态图，天然支持循环 (Ch06)

**LLM Judge** — 用 LLM 作为评估器评估输出质量的方法 (Ch12)

**马尔可夫假设 (Markov Assumption)** — 词出现概率只与前面有限 n 个词有关 (Ch03)

**MCP (Model Context Protocol)** — Anthropic 提出的智能体与工具标准化通信协议 (Ch10)

**MDP (马尔可夫决策过程)** — 状态/行动/转移/奖励/折扣五元组，RL 的形式化基础 (Ch11)

**MVTS (最小可行工具集)** — 精心甄选的最小工具集合，提升 Agent 长期稳定性 (Ch09)

**MYCIN** — 斯坦福 1970s 开发的血液感染诊断专家系统，引入置信因子 (Ch02)

**n8n** — 开源工作流自动化工具，数百个预置节点连接 SaaS/数据库/API (Ch05)

**N-gram 模型** — 基于马尔可夫假设的统计语言模型，受数据稀疏性限制 (Ch03)

**PBRFT** — Preference-Based RL Fine-Tuning，单轮对话质量优化的传统方法 (Ch11)

**PEAS 模型** — Performance/Environment/Actuators/Sensors 任务环境四要素 (Ch01)

**物理符号系统假说 (PSSH)** — Newell & Simon (1976) 智能=符号计算与处理 (Ch02)

**Plan-and-Solve** — Lei Wang et al. 2023 提出的先规划后执行的两阶段范式 (Ch04)

**PPO (Proximal Policy Optimization)** — 经典 RLHF 算法 (Ch11)

**预训练 (Pretraining)** — 因果语言建模，在海量文本上预测下一个 token (Ch11)

**ReAct** — Yao et al. 2022 的 Reasoning+Acting 结合范式，Thought-Action-Observation 循环 (Ch04)

**Reflection** — 通过自我批判和修正优化输出质量的智能体范式 (Ch04)

**RLHF** — 人工标注偏好数据+PPO 的强化学习微调方法 (Ch11)

**RLAIF** — 用 GPT-4 等 AI 替代人类标注偏好数据，降低标注成本 (Ch11)

**SFT (监督微调)** — (prompt, completion) 对训练，学习指令遵循和对话格式 (Ch11)

**SHRDLU** — Winograd 1968-1970 "积木世界"综合智能体，感知-思考-行动闭环先驱 (Ch02)

**符号主义 (Symbolicism)** — 智能源于符号操作和逻辑规则的传统 AI 范式 (Ch01/Ch02)

**温度 (Temperature)** — LLM 输出的随机性控制参数，ReAct 通常设为 0 (Ch04)

**Transformer** — Vaswani et al. 2017 完全基于自注意力的架构，现代 LLM 的基础 (Ch03)

**词嵌入 (Word Embedding)** — 将离散符号映射到连续向量空间的语义表示 (Ch03)

**自注意力 (Self-Attention)** — 序列中每个 token 与所有 token 建立关联的机制 (Ch03)
