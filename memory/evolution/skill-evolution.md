# Skill 自进化协议 v1

**版本**: 1.0
**日期**: 2026-06-14
**核心理念**: 每次 Skill 调用都是一次训练机会，Skill 应随使用自我优化
**灵感来源**: 鲁班工坊的验料→过尺→验证门方法论

---

## 1. 设计哲学

### 为什么 Skill 需要自进化？

当前的 Skill 生命周期是**静态的**：
```
创建 → 发布 → 永远不变（除非人工修改）
```

问题是：
- 用户纠正了 Skill 的输出，下次还会犯同样的错
- 某个步骤经常失败，但 Skill 不知道
- 新的工具/方法出现了，Skill 还在用旧的
- 使用场景变化了，Skill 的适用边界没更新

### 自进化的 Skill 生命周期

```
创建 → 使用 → 观察 → 分析 → 提案 → 验证 → 固化
  ↑                    │
  └────────────────────┘
       每次调用都喂数据
```

---

## 2. 调用轨迹（每次 Skill 使用自动记录）

### 2.1 记录什么

每次调用一个 Skill，记录到 `evolution/skill-traces/{skill-name}.jsonl`：

```json
{
  "ts": "2026-06-14T00:30:00+08:00",
  "skill": "luban",
  "trigger": "用户请求打磨 Skill",
  "steps": [
    {"step": "验料", "status": "ok", "duration_ms": 2000},
    {"step": "访行", "status": "failed", "duration_ms": 30000, "error": "web_search timeout"},
    {"step": "过尺", "status": "ok", "duration_ms": 5000}
  ],
  "outcome": "partial",
  "user_corrections": ["不要用 web_search，用 gh api"],
  "output_quality": "B",
  "notes": "访行阶段工具选择有问题"
}
```

### 2.2 质量评级

每次调用的输出质量（由反思 cron 或用户反馈判定）：

| 等级 | 含义 | 触发条件 |
|------|------|---------|
| A | 完美，无需修改 | 用户无纠正，直接使用 |
| B | 可用，小修 | 用户小幅度修改/补充 |
| C | 需要重写 | 用户大幅修改或重来 |
| D | 完全不对 | 用户放弃，换方案 |
| F | 工具/步骤失败 | 调用报错，无法完成 |

### 2.3 追踪文件管理

- 每个 Skill 一个 `.jsonl` 文件，追加写入
- 单文件上限 200 条，超出淘汰最旧的
- 保留最近 30 天的轨迹
- 脱敏：不存原始用户输入，只存触发词和摘要

---

## 3. 分析层（23:30 反思时执行）

### 3.1 Skill 健康度计算

对每个被调用过的 Skill，计算：

```
健康度 = (A×4 + B×3 + C×1 + D×0 + F×-1) / 总调用次数
```

| 健康度 | 状态 | 动作 |
|--------|------|------|
| ≥ 3.5 | 🟢 健康 | 无动作 |
| 2.5 - 3.5 | 🟡 亚健康 | 生成改进提案 |
| < 2.5 | 🔴 病态 | 标记为待修复，优先级 P0 |

### 3.2 失败模式识别

从轨迹中自动识别：

| 模式 | 检测条件 | 输出 |
|------|---------|------|
| 步骤瓶颈 | 某步骤失败率 > 30% | 标记该步骤为瓶颈 |
| 工具不匹配 | 同一步骤连续失败 ≥2 次 | 建议替换工具 |
| 用户纠正集中 | 同一纠正出现 ≥2 次 | 生成针对性改进 |
| 耗时异常 | 某步骤耗时 > 其他步骤 3 倍 | 建议优化或拆分 |
| 输出偏差 | 连续 ≥2 次评级 ≤ C | 标记输出质量问题 |

### 3.3 改进提案生成

当分析发现问题时，生成改进提案写入 `evolution/skill-improvements.json`：

```json
{
  "id": "imp-001",
  "skill": "luban",
  "detected_at": "2026-06-14T23:30:00+08:00",
  "issue": "访行步骤的 web_search 经常超时",
  "evidence": {
    "total_calls": 5,
    "step_failures": {"访行": 3},
    "user_corrections": ["用 gh api 代替 web_search"]
  },
  "proposal": "将访行步骤的默认工具从 web_search 改为 gh api + curl",
  "confidence": 0.7,
  "status": "proposed",
  "validated_count": 0
}
```

---

## 4. 自进化触发条件

### 4.1 三种进化模式（借鉴鲁班 + 原有引擎）

| 模式 | 触发条件 | 借鉴鲁班 | 动作 |
|------|---------|---------|------|
| **FIX** | failure ≥ 2 或健康度 < 2.5 | 验料→过尺 | 修复 SKILL.md 中的步骤 |
| **DERIVED** | 用户纠正同一问题 ≥ 2 次 | 慢刨→验证门 | 创建增强版 Skill |
| **CAPTURED** | 成功任务无 Skill 匹配 | **验料（新增）** | 先验料再捕获 |

### 4.2 CAPTURED 增加验料环节（借鉴鲁班）

**原有流程**：成功 → 无匹配 Skill → 直接创建

**新流程**：成功 → 无匹配 Skill → **验料** → 值得才创建

验料四问（简化版，用于 CAPTURED 决策）：

1. **真实问题**：这个任务会被重复执行吗？（≥3 次/月才值得）
2. **独特角度**：现有 Skill 真的覆盖不了吗？（检查是否可扩展现有 Skill）
3. **安装理由**：固化后能减少多少人工干预？（节省 >5 分钟/次才值得）
4. **可验证性**：成功标准能明确定义吗？（有明确的输入→输出映射）

**验料结论**：
- 4 问全通过 → 创建新 Skill
- 2-3 问通过 → 考虑扩展现有 Skill
- ≤1 问通过 → 不创建，仅记录到 patterns

### 4.3 FIX 增加验证门（借鉴鲁班慢刨）

**原有流程**：failure ≥ 2 → 直接修改 SKILL.md

**新流程**：failure ≥ 2 → **冻结原版** → 生成候选修改 → **验证门** → 通过才写入

验证门条件：
1. 修改后的步骤在 dry_run 中不报错
2. 不引入新的依赖或私有路径
3. 不让 SKILL.md 变得更长但更难用
4. 修改范围小（单步骤），不重构整个 Skill

### 4.4 DERIVED 增加活体检查（借鉴鲁班过尺）

**原有流程**：用户纠正 ≥ 2 → 创建增强版

**新流程**：用户纠正 ≥ 2 → 生成增强版 → **用真实数据回放** → 确认改进有效

---

## 5. 自进化执行流程

### 5.1 每次调用时（实时）

```
1. 读取 Skill 的 SKILL.md
2. 执行 Skill 步骤
3. 记录每个步骤的状态、耗时
4. 记录用户纠正（如果有）
5. 写入 skill-traces/{skill-name}.jsonl
6. 更新 .skill-quality.json 的调用计数
```

### 5.2 每日反思时（23:30）

```
1. 读取今日所有 skill-traces/*.jsonl
2. 计算每个 Skill 的健康度
3. 识别失败模式
4. 生成改进提案（写入 skill-improvements.json）
5. 检查 CAPTURED 候选（成功但无匹配的任务）
6. 对 CAPTURED 候选执行验料
7. 更新 .skill-quality.json
```

### 5.3 改进固化时（需验证通过）

```
1. 读取 skill-improvements.json 中 status=proposed 的提案
2. 检查 confidence ≥ 0.7 且 validated_count ≥ 1
3. 生成候选修改（冻结原版）
4. 通过验证门 → 写入 SKILL.md
5. 记录到 evolution-log.md
6. 更新 skill-improvements.json 的 status 为 validated
```

---

## 6. 数据结构

### 6.1 skill-traces/{skill-name}.jsonl

每行一条调用记录（JSON），格式见 §2.1。

### 6.2 skill-improvements.json

```json
{
  "version": 1,
  "maxEntries": 30,
  "improvements": [
    {
      "id": "string",
      "skill": "string",
      "detected_at": "ISO-8601",
      "issue": "string",
      "evidence": {
        "total_calls": "number",
        "step_failures": {"step_name": "count"},
        "user_corrections": ["string"],
        "avg_quality": "number"
      },
      "proposal": "string",
      "confidence": 0.0-1.0,
      "status": "proposed|validated|rejected|applied",
      "validated_count": "number",
      "applied_at": "ISO-8601|null"
    }
  ]
}
```

### 6.3 .skill-quality.json 升级

在原有 `success/failure` 基础上，增加：

```json
{
  "skill-name": {
    "success": 1,
    "failure": 0,
    "lastUsed": "ISO-8601",
    "health_score": 3.5,
    "total_calls": 10,
    "quality_distribution": {"A": 5, "B": 3, "C": 1, "D": 0, "F": 1},
    "top_issues": ["web_search timeout in step X"],
    "improvements_applied": 0,
    "notes": "string"
  }
}
```

---

## 7. 与现有系统的集成

| 系统 | 集成方式 |
|------|---------|
| 进化引擎 (23:30) | 新增步骤：分析 skill-traces → 生成改进提案 |
| memory-consolidation (02:00) | 整合 skill-improvements 到 topics/work-tools.md |
| memory-health-sync (02:15) | 检查 skill-traces 文件大小、清理过期 |
| memory-patrol (09:00) | 验证昨日改进提案是否生效 |
| Skill Workshop | FIX/DERIVED 通过验证门后，通过 Workshop 固化 |
| 鲁班 Skill | 当 Skill 需要大幅改造时，触发鲁班流程 |

---

## 8. 安全边界

- **不自动修改 SKILL.md**：所有改进必须通过验证门 + 用户确认
- **轨迹脱敏**：不存原始用户输入，只存摘要和元数据
- **大小限制**：单个 trace 文件 ≤ 200 条，improvements.json ≤ 30 条
- **不扩权**：改进不能给 Skill 增加新的权限或外部调用
- **回滚**：每次修改 SKILL.md 前快照，保留最近 3 个版本

---

## 9. 冷启动

当前已有的 Skill 如何开始自进化：

1. 为每个已有 Skill 创建空的 `skill-traces/{skill-name}.jsonl`
2. 从 `.skill-quality.json` 迁移现有 success/failure 数据
3. 首次调用时自动开始记录轨迹
4. 积累 ≥5 次调用后，首次健康度评估
5. 积累 ≥10 次调用后，开始生成改进提案
