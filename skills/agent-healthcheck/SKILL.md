---
name: agent-healthcheck
description: |
  Agent 系统健康检查 + 质量验收。两层检查：系统层（环境/工具链/安全/Cron/架构）+ Agent 层（效率/成本/韧性/可观测/可插拔/可追溯）。每次运行自动记录结果、追踪趋势、对比历史、生成改进提案。借鉴鲁班自举机制，越用越准。
  触发词：测试、验收、健康检查、healthcheck、体检、系统检查、agent检查
version: 1.0.0
author: GGOB
tags: [testing, validation, healthcheck, agent-quality, self-improvement]
triggers: [测试, 验收, 健康检查, healthcheck, 体检, 系统检查, agent检查]
---

# Agent Healthcheck — 系统健康检查 + Agent 质量验收

## 概述

两层检查，一次跑完，出一份报告：
- **系统层**：基础设施健不健康（环境、工具链、平台、Cron、安全、架构）
- **Agent 层**：Agent 本身聪不聪明（效率、成本、韧性、可观测、可插拔、可追溯）

每次运行自动记录结果到 `memory/evolution/healthcheck/`，支持趋势追踪和改进提案。

## 自举机制（越用越好用）

借鉴鲁班五步，每次检查后自动优化下次检查：

### 1. 结果追踪（每次运行）
每次检查写入 `memory/evolution/healthcheck/{date}-{seq}.json`。

### 2. 趋势分析（对比历史）
读取最近 5 次检查结果，识别：
- **持续失败**：同一检查项连续 ≥3 次失败 → 标记为 P0 待修复
- **新退化**：上次通过这次失败 → 标记为回归问题
- **改善趋势**：上次失败这次通过 → 标记为已修复

### 3. 检查项自进化（自举核心）
- **新发现**：本次检查发现了之前没覆盖的问题 → 生成"新增检查项"提案
- **误报**：用户说"这个不是问题" → 标记为误报，下次跳过或降权
- **阈值调整**：同一指标多次触发但用户不关心 → 自动调整阈值
- **检查优化**：某检查项耗时过长但从未发现问题 → 生成"简化检查"提案

改进提案写入 `memory/evolution/healthcheck/improvements.json`，下次运行时自动加载。

### 4. 验证门（借鉴鲁班慢刨）
新增或修改检查项前：
1. 冻结当前检查清单
2. 候选检查项必须满足：有过真实问题记录 / 误报率 < 20% / 执行时间 < 30s
3. 通过验证门才写入正式检查清单

---

## 执行方式

运行检查脚本：
```powershell
python temp/healthcheck.py
```

或通过触发词触发：`测试`、`验收`、`健康检查`、`体检`

## 检查维度

### 系统层（50 分）

| 维度 | 分值 | 检查内容 |
|------|------|---------|
| 基础环境 | 10 | Node.js, Python, uv, Git, FFmpeg |
| 工具链 | 10 | sau, Wechatsync, SkillSpector, YouNavi, HyperFrames |
| 平台登录 | 10 | 5 个平台的 cookie 状态 |
| Cron 健康度 | 10 | 启用状态、连续失败、最近运行、模型可达 |
| 安全扫描 | 5 | 杀毒软件、监听端口、Git 授权、凭据安全 |
| 架构完整性 | 5 | MEMORY/SOUL/AGENTS/graph/daily |

### Agent 层（50 分）

| 维度 | 分值 | 检查内容 |
|------|------|---------|
| 效率 | 8 | 冗余调用、无效重试、检索命中率 |
| 成本 | 8 | Token 消耗、子 Agent 成本、模型选择 |
| 韧性 | 9 | 级联失败、Fallback 链、错误恢复 |
| 可观测 | 9 | daily 日志、skill-traces、错误记录 |
| 可插拔 | 8 | 集成路径、接口标准化、无硬编码 |
| 可追溯 | 8 | 决策记录、修正记录、结论引用 |

## 输出格式

```markdown
# 🏥 Agent 健康检查报告 — {date} {time}

## 总分: {total}/100 ({grade})

| 层级 | 得分 | 等级 |
|------|------|------|
| 系统层 | {system_score}/50 | {system_grade} |
| Agent 层 | {agent_score}/50 | {agent_grade} |

## 🟢 通过项
## 🔴 失败项
## ⚠️ 警告项
## 📈 趋势分析
## 🔧 改进提案
```

## 等级标准

| 等级 | 分数 | 含义 |
|------|------|------|
| A | ≥ 90% | 健康 |
| B | 75-89% | 良好 |
| C | 60-74% | 亚健康 |
| D | < 60% | 病态 |

## 自举数据文件

```
memory/evolution/healthcheck/
├── {date}-{seq}.json        # 每次检查结果
├── improvements.json         # 改进提案
├── false-positives.json      # 误报记录
└── thresholds.json           # 动态阈值
```

## 已知误报（首次运行后修正）

- Windows Defender：系统安装了 McAfee，Defender 按设计禁用 → 跳过
- 监听端口：全部为标准服务（RPC/SMB/VMware/PostgreSQL/Ollama/HanaAgent/Steam）→ 阈值调整为 >80 才告警
- skill-traces 空目录：新系统预期行为 → 首次运行不扣分

## 与进化引擎集成

检查结果自动反馈到进化引擎：
- 系统层失败 → 可能触发 FIX（修复工具/Cron）
- Agent 层失败 → 可能触发 DERIVED（改进工作流）
- 新发现的问题类型 → 可能触发 CAPTURED（新增检查项）
