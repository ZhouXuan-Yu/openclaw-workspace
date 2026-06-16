# CONTEXT.md — OpenClaw 项目术语表

统一项目内部语言，避免歧义。

## 核心术语

| 术语 | 定义 | 避免 |
|------|------|------|
| **Skill** | 可复用的行为指令包，由 SKILL.md 定义 | 插件、功能、模块 |
| **Memory** | 持久化记忆，分4层（索引/主题/日志/会话） | 记录、日志、数据 |
| **Evolution** | 自进化引擎，观察→分析→提炼→验证→固化 | 迭代、优化、改进 |
| **Agent** | OpenClaw 运行实例 | 机器人、助手、AI |
| **Heartbeat** | 定时任务（cron），周期性检查 | 心跳、定时器 |
| **Topic** | memory/topics/ 下的主题记忆文件 | 主题、话题 |
| **Daily** | memory/daily/ 下的每日日志 | 日志、日记 |
| **ADR** | Architecture Decision Record，架构决策记录 | 设计文档、方案 |

## 关系

- **Skill** 包含 **SKILL.md** + assets/ + examples/
- **Memory** 包含 **MEMORY.md**（索引） + topics/ + daily/ + evolution/
- **Evolution** 读写 **Memory**，生成/优化 **Skill**
- **Heartbeat** 触发 **Evolution** 循环

## 纠正记录

- "插件" → 统一用 "Skill"
- "日志" → 指 daily/ 下的文件；topics/ 下的是"主题记忆"
- "进化" → 指 evolution 引擎的整体机制；单次改进叫"进化动作"
