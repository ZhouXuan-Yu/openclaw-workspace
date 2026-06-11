# 工具发现 — Tool Discovery

> 不只是使用固定工具集，能自动发现和集成新工具
> 对应 OpenSpace 的"工具生态进化"

## 当前工具清单

| 类别 | 工具 | 来源 |
|------|------|------|
| 文件 | read, write, edit, apply_patch | OpenClaw 内置 |
| 执行 | exec, process | OpenClaw 内置 |
| 搜索 | web_search, web_fetch | OpenClaw 内置 |
| 记忆 | memory_search, memory_get | OpenClaw 内置 |
| 调度 | cron | OpenClaw 内置 |
| 会话 | sessions_spawn, sessions_send | OpenClaw 内置 |
| 媒体 | image, image_generate, video_generate | OpenClaw 内置 |
| 状态 | session_status, subagents | OpenClaw 内置 |

## 发现机制

### 1. 被动发现（用户引入）
- 用户安装新 Skill → 自动注册到工具清单
- 用户说"帮我找一个XX工具" → 搜索 ClawHub

### 2. 主动发现（系统探索）
- 任务失败时检查是否有更好的工具
- 定期扫描 ClawHub 热门 Skill
- 检查 npm/pip 包管理器中的相关工具

### 3. 经验驱动（从执行中学习）
- 记录每次工具调用的成功/失败
- 识别工具使用的模式
- 推荐更优工具

## 工具质量追踪

```json
{
  "tool_name": {
    "calls": 0,
    "success": 0,
    "failure": 0,
    "avg_latency_ms": 0,
    "last_used": "ISO-8601",
    "last_error": "string",
    "alternatives": ["tool1", "tool2"]
  }
}
```

## 集成流程

```
发现新工具
    ↓
评估：是否比现有工具更好？
    ├── 不是 → 忽略
    └── 是 → 安装 → 测试 → 集成
        ↓
    记录到工具清单
    更新 SKILL.md（如果需要）
```

## 安全边界

- 不安装未经验证的第三方包
- 不修改系统级工具
- 新工具需要通过沙箱测试
- 用户有权拒绝任何工具安装
