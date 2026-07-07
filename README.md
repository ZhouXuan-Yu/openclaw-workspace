# OpenClaw Workspace · ZhouXuan

> 皇家卫士 GGOB 🛡️ — 自主智能体工作区

基于 [OpenClaw](https://github.com/openclaw/openclaw) 构建的 AI Agent 工作区，承载自进化引擎、多平台社交自动化、记忆系统与日常任务。

## 架构

```
├── AGENTS.md             行为规则与启动协议
├── SOUL.md               身份定义与安全红线
├── MEMORY.md             长时记忆索引
├── RULES.md              硬约束
├── agent.yaml            Agent 清单
│
├── memory/               记忆系统
│   ├── daily/            每日日志
│   ├── topics/           主题知识库
│   └── evolution/        自进化引擎
│
├── skills/               可调用技能
├── workflows/            工作流 YAML
├── hooks/                生命周期钩子
├── knowledge/            知识索引
├── tools/                工具集
│   ├── social-auto-upload/   多平台发布
│   ├── SkillSpector/         安全扫描
│   └── ...
└── docs/                 文档与架构决策
```

## 核心能力

- **自进化引擎** — 失败自修复 (FIX)、用户纠正衍生 (DERIVED)、成功模式捕获 (CAPTURED)
- **多平台发布** — 抖音/快手/B站/视频号/小红书 自动化发布
- **社交内容生产** — AI 视频生成 + 设计 + 配音 + 多平台分发全链路
- **记忆系统** — 4 层记忆架构（索引→主题→日志→会话）
- **主动智能** — 定时巡检、安全扫描、记忆整合、日常复盘

## 日常维护

每日自动：记忆整合 (02:00) → 健康同步 (02:15) → 巡检 (09:00) → 安全扫描 (10:00) → 复盘 (23:30)

## 状态

[//]: # (自动生成 — 最后更新见 commit 记录)

---

*ZhouXuan 个人工作区 · 未经授权请勿使用*
