# 第15章 构建赛博小镇

## Core Idea
将智能体与 Godot 游戏引擎结合，构建 2D 像素风 AI 小镇。NPC 拥有真正智能：自然语言对话、互动记忆、好感度变化。

## Frameworks Introduced
- **Godot 4.5 游戏引擎**: 游戏渲染
- **Qdrant 向量数据库**: 记忆检索
- **SQLite**: 数据持久化

## Key Concepts
- **智能 NPC 对话** — 自然语言，非对话树
- **NPC 记忆系统** — 短期/长期记忆，记住互动
- **好感度系统** — 陌生→熟悉→友好→亲密
- **SimpleAgent 实例** — 每个 NPC 独立记忆和人格
- **2D 像素风格** — Datawhale 办公室场景

## Mental Models
1. **"活着的 NPC"**: NPC = LLM + 独立记忆 + 个性设定
2. **"好感度温度计"**: 对话→记忆→好感度→对话策略

## Anti-patterns
- NPC 共享 LLM 实例(人格模糊)
- 忽略记忆 TTL
- 只重对话不重 UI 反馈

## Code Examples
```
class NPC:
    def __init__(self, name, role_prompt, llm):
        self.agent = SimpleAgent(name=name, llm=llm, system_prompt=role_prompt)
        self.relationship = RelationshipManager()
        self.memory = MemoryTool()
        self.agent.add_tool(self.memory)

    def chat(self, player_msg):
        self.relationship.update(player_msg)
        context = self.memory.retrieve(player_msg)
        response = self.agent.run(player_msg, context=context)
        self.memory.save(player_msg, response)
        return response
```

## Worked Example
**与 NPC 小红对话**: 首次"你好"→NPC 回复自我介绍→第二次"记得我吗"→记忆检索→NPC 记得上次对话→多次友好互动后好感度提升→回复更热情。

## Key Takeaways
1. Godot+FastAPI+HelloAgents 三件套构建 AI 游戏
2. 独立 SimpleAgent 保证人格一致
3. 好感度系统让对话有"人情味"
4. 记忆是 NPC"活着"的关键

## Connects To
- Ch07: SimpleAgent 核心
- Ch08: 记忆系统支撑
