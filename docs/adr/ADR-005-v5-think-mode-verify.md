# ADR-005: v5 进化 — Think Tool + Mode Router + Self-Verification

## 日期
2026-06-15

## 状态
已实施

## 背景
分析了 GitHub 仓库 `x1xhlol/system-prompts-and-models-of-ai-tools` 中 20+ AI 工具的 System Prompt，提炼出可复用的设计模式。

## 决策
在现有 v4 架构基础上，引入三个来自顶级 AI Agent 的设计模式：

### 1. Think Tool（源自 Devin AI）
- 关键决策前强制思考步骤
- 5 个强制场景 + 5 个建议场景
- 思考内容用户不可见

### 2. Task Mode Router（源自 Kiro + Orchids）
- 5 种任务模式：💬简单 / ⚡标准 / 🔬深度 / 🏗️工程 / 🛡️安全
- 自动分类，匹配对应策略
- 不确定时默认 ⚡标准

### 3. Self-Verification（源自 Devin + Manus）
- 报告完成前 5 点检查清单
- 不满足不报告完成

### 4. Coding Best Practices（源自 Devin）
- 不加注释、先看现有风格、假设库不存在
- 新组件先看已有组件、写最少代码

## 影响
- AGENTS.md: 新增 v5 章节
- AGENTS-DETAILS.md: 新增详细规则
- RULES.md: 新增编码规范
- agent.yaml: 版本 1.0.0 → 1.1.0

## 快照
`.snapshots/v5-20260615-144933/`
