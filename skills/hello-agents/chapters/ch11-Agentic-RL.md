# 第11章 Agentic-RL

## Core Idea
Agentic RL 将 LLM 作为可学习策略嵌入智能体的决策循环，通过强化学习优化多步任务表现。

## Frameworks Introduced
- **PBRFT** — Preference-Based RL Fine-Tuning，单步质量优化
- **PPO (Proximal Policy Optimization)** — 经典 RLHF 算法
- **GRPO (Group Relative Policy Optimization)** — 高效策略优化
- **RLAIF** — 用 AI 替代人类标注偏好数据

## Key Concepts
- **预训练** — 因果语言建模，预测下一个 token
- **监督微调 (SFT)** — 学习指令遵循和对话格式
- **奖励建模 (RM)** — 学习人类偏好，给更好回答更高分
- **RLHF** — 人工标注 + PPO
- **MDP 五元组** — 状态/行动/转移/奖励/折扣
- **Agentic RL 序列决策** — 多步交互，每步可获反馈
- **KL 散度约束** — 防止模型偏离太远

## Mental Models
1. **PBRFT = 考试评分**: 一次问答定好坏
2. **Agentic RL = 游戏通关**: 多步每步反馈
3. **SFT→RM→RLHF = 师从→助教→实战**

## Anti-patterns
- 单步奖励优化多步任务
- 忽略 KL 散度约束
- 只依赖人工标注(RLHF)，成本高

## Code Examples
```
# PBRFT: 单步奖励
reward = reward_model(question, answer)

# Agentic RL: 多步累积奖励
total_reward = 0
for step in agent_trajectory:
    total_reward += intermediate_reward(step.state, step.action)
```

## Worked Example
**数学求解智能体训练**: 问题"Janet has 16 eggs, eats 3, bakes with 4, sells rest at $2 each"
1. 生成多个候选推理路径
2. 奖励模型判断路径正确性
3. GRPO 基于群组内相对表现更新策略
4. 迭代后学会正确推理模式

## Key Takeaways
1. Agentic RL 将 LLM 嵌入多步决策循环
2. SFT 学格式，RL 学探索更优解
3. RLAIF 大幅降低标注成本
4. MDP 是数学基础
5. 多步中间奖励比单步终局奖励更有效

## Connects To
- Ch02: RL 的演进历史
- Ch12: 评估验证训练效果
