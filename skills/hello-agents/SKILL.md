---
name: hello-agents
description: "Knowledge base from 'Hello-Agents' by Datawhale. Use when building AI Native Agents, implementing ReAct/Reflection patterns, applying MCP/A2A protocols, or training Agentic-RL models."
---

# Hello-Agents Knowledge Base

Knowledge distilled from *Hello-Agents* (Datawhale, 16 chapters), covering AI Native Agent construction from theory to practice.

## Core Frameworks

### Agent Paradigms
- **ReAct (Yao et al. 2022)**: "Think-Act-Observe" loop. Steps output to LLM as growing context. Best for dynamic tasks needing external knowledge. ✅ high interpretability, ❌ prompt fragility, depends on LLM capability.
- **Plan-and-Solve (Lei Wang et al. 2023)**: Two-phase: plan first, execute strictly. For structurally decomposable tasks (math, report writing). Mitigates "derailing" in long chains.
- **Reflection**: Generate → Critique → Revise → Re-critique. Reduces hallucination, higher cost. Use when output quality matters more than speed.
- **Workflow vs Agent**: Workflow = preset rules, deterministic. Agent = autonomous, goal-driven with LLM reasoning. Use Workflow when path is known, Agent when uncertain.

### Architecture (HelloAgents)
- **"Everything is a Tool"**: Memory, RAG, MCP, RL all abstracted as Tool. Eliminates unnecessary layers.
- **GSSC Pipeline**: Gather → Select → Structure → Compress context. Manage LLM's limited attention budget.
- **JIT Context**: Maintain references (paths/URLs) instead of data, load on demand. Prevents context rot.

### Communication Protocols
- **MCP (Model Context Protocol, Anthropic)**: Standardizes Agent↔Tool communication. USB-like: plug and play.
- **A2A (Agent-to-Agent Protocol, Google)**: Peer-to-peer Agent collaboration. Each Agent is both provider and consumer.
- **ANP (Agent Network Protocol)**: Decentralized service discovery for large-scale Agent networks.

### Training (Agentic-RL)
- **Pipeline**: Pretraining (next-token prediction) → SFT (format learning) → Reward Modeling (preference learning) → RLHF/GRPO (strategy optimization).
- **PBRFT vs Agentic-RL**: PBRFT = single-step reward (exam grading). Agentic-RL = multi-step cumulative reward (game level completion).
- **RLAIF**: Use AI (GPT-4) for preference labeling instead of humans. Dramatically reduces annotation cost.

### Evaluation Benchmarks
- **BFCL**: 1120+ function-calling samples. AST matching for precision.
- **GAIA**: 466 real-world problems, 3 levels. Quasi Exact Match scoring.
- **Key metrics**: Accuracy, response time, token usage, error rate, failure recovery.

## Chapter Index

| Ch | Title | Core Content |
|----|-------|-------------|
| 01 | 初识智能体 | Agent definition, PEAS model, symbolic/sub-symbolic/neuro-symbolic, Workflow vs Agent |
| 02 | 智能体发展史 | PSSH, expert systems (MYCIN), ELIZA, SHRDLU, knowledge bottleneck, frame problem |
| 03 | 大语言模型基础 | N-gram → word embedding → RNN/LSTM → Transformer (self-attention) |
| 04 | 经典范式构建 | ReAct, Plan-and-Solve, Reflection — from-scratch code implementation |
| 05 | 低代码平台 | Coze (zero-code), Dify (open-source), n8n (automation) |
| 06 | 框架开发实践 | AutoGen (dialogue-driven), AgentScope, CAMEL (role-playing), LangGraph (state graph) |
| 07 | 构建 Agent 框架 | HelloAgents design: lightweight, tool-centric, progressive learning |
| 08 | 记忆与检索 | Memory types (working/episodic/semantic), RAG pipeline, vector/graph/doc storage |
| 09 | 上下文工程 | Context rot, attention budget, GSSC, JIT context, MVTS |
| 10 | 通信协议 | MCP (tool protocol), A2A (agent protocol), ANP (network protocol) |
| 11 | Agentic-RL | Pretraining → SFT → RM → RLHF/GRPO, MDP formulation, PBRFT vs Agentic-RL |
| 12 | 性能评估 | BFCL, GAIA, ToolBench, AgentBench; AST matching, LLM Judge |
| 13 | 旅行助手 | Multi-Agent (4 specialized agents), MCP + FastAPI + Vue3, map visualization |
| 14 | 深度研究助手 | Planner+Summarizer+Writer Agents, SSE streaming, NoteTool, multi-round search |
| 15 | 赛博小镇 | Godot + FastAPI + HelloAgents, NPC memory + relationship system |
| 16 | 毕业设计 | Project selection, GitHub PR workflow, Co-creation-projects |

## Topic Index

| Topic | Chapters |
|-------|----------|
| Agent definition & paradigms | 01, 04 |
| LLM internals (Transformer) | 03 |
| Evaluation | 12 |
| Frameworks & tools | 05, 06, 07 |
| History & symbol systems | 02 |
| Memory & RAG | 08 |
| Context engineering | 09 |
| Communication protocols | 10 |
| Reinforcement learning | 11 |
| Project architectures | 13, 14, 15 |

## Supporting Files

- `chapters/` — Per-chapter study notes (each 2000-3000 tokens)
- `glossary.md` — Alphabetical term definitions with chapter refs
- `cheatsheet.md` — Decision rules, comparison tables, thresholds
