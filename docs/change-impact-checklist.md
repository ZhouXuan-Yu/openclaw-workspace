# 变更影响清单

当修改 OpenClaw 核心组件时，必须同步检查以下文件：

## 修改 Skill 时
1. `skills/<name>/SKILL.md` — 核心指令
2. `CONTEXT.md` — 术语表（如果引入新术语）
3. `MEMORY.md` — 主题索引（如果是新 Skill）
4. `memory/topics/work-tools.md` — 工具使用记录

## 修改 Memory 架构时
1. `AGENTS.md` — 记忆4层规则
2. `CONTEXT.md` — 术语表
3. `docs/adr/` — 新增 ADR 记录决策
4. `memory/evolution/EVOLUTION-PROTOCOL.md` — 进化协议

## 修改 Evolution 引擎时
1. `memory/evolution/EVOLUTION-PROTOCOL.md` — 协议文档
2. `memory/evolution/patterns.json` — 模式库
3. `memory/evolution/failures.json` — 失败记录
4. `AGENTS.md` — 自进化引擎章节
5. `docs/adr/` — 新增 ADR 记录决策

## 修改发布流程时
1. `TOOLS.md` — 工具使用指南
2. `memory/topics/work-tools.md` — 工具记录
3. `memory/daily/` — 当日日志
4. 相关 Skill 的 SKILL.md

## 修改安全规则时
1. `SOUL.md` — 安全红线
2. `AGENTS.md` — 红线章节
3. `RULES.md` — 硬约束
