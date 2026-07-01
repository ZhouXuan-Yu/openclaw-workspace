---
name: evolution-engine
description: "自进化引擎：基于 OpenSpace 思路，每次任务后自动分析成败，触发 Skill 进化（FIX/DERIVED/CAPTURED）。"
parent: ""
origin: "imported"
generation: 0
created: "2026-06-12"
metadata: {"openclaw":{"emoji":"🧬"}}
---

# Skill Evolution Engine — 自进化引擎

基于 OpenSpace 思路，适配 OpenClaw 文件系统架构。三种进化模式：FIX / DERIVED / CAPTURED。

## 概述

每次任务执行后，自动分析结果，决定是否触发进化：
- **FIX**: 修复出错/过时的 Skill（failure >= 2 触发）
- **DERIVED**: 从现有 Skill 创建增强版（用户纠正触发）
- **CAPTURED**: 从成功执行中捕获可复用模式（成功+无Skill触发）

## 进化触发条件

| 模式 | 触发条件 | 操作 |
|------|---------|------|
| FIX | Skill 执行失败 ≥ 2次 | 原地修复 SKILL.md |
| DERIVED | 用户说"不要这样"/"换个方式" | 创建增强版（带 parent） |
| CAPTURED | 任务成功 + 无现有 Skill 匹配 | 捕获为新 Skill |

## 文件结构

```
skills/
├── evolution-engine/
│   ├── SKILL.md          # 本文件
│   └── .skill_id         # 唯一标识
├── .skill-quality.json   # 全局质量计数器
└── ...
```

## SKILL.md Frontmatter 扩展规范

```yaml
---
name: skill-name
description: "简短描述"
parent: ""           # 父 Skill ID（进化链，空=根节点）
origin: "imported"   # imported | captured | derived | fixed
generation: 0        # 进化代数（FIX/DERIVED 时 +1）
created: "2026-06-12"
---
```

## 质量计数器 (skills/.skill-quality.json)

```json
{
  "version": 1,
  "skills": {
    "skill-name": {
      "success": 0,
      "failure": 0,
      "last_used": "2026-06-12T02:30:00+08:00",
      "last_status": "success",
      "error_types": []
    }
  },
  "evolution_log": []
}
```

## 集成点

| 组件 | 集成方式 |
|------|---------|
| 反射管道 (23:30 cron) | 执行后分析 → 触发进化 |
| 记忆整合 (02:00 cron) | 识别重复模式 → 升级为 Skill |
| AGENTS.md | 反射管道章节已扩展 |
| learnings.md | 失败教训自动写入 |
