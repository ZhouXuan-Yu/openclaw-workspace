# 自我进化引擎 — 完整协议 v3

**版本**: 3.0
**日期**: 2026-06-14
**触发**: memory-reflection (23:30) + 每次会话结束
**参考**: A-Evolve(循环范式) / self-evolving-agent(能力状态机) / Darwin(Critic评估) / agent-seed(大小约束) / solo-founder(四步循环)

---

## 0. v3 核心改进（相比 v2）

| 改进 | 来源 | 解决的问题 |
|------|------|-----------|
| 能力状态机 6 阶段 | self-evolving-agent | v2 只有 success/failure 二元判断，无法追踪"学到什么程度" |
| 学习议程（最多3项） | self-evolving-agent | v2 没有聚焦机制，进化分散无重点 |
| Critic 评估 | Darwin Agents | v2 只有自评，缺少外部质量校验 |
| 大小强制约束 | agent-seed | v2 虽有大小限制但未强制执行 |
| eval→council→evolver→retro 四步 | solo-founder-os | v2 进化循环缺少结构化步骤 |
| 迁移检查 | self-evolving-agent | v2 固化前未验证能力是否可迁移 |

---

## 1. 进化循环 v3（四步结构）

```
[Step 1: eval] 评估当前状态
 │  读取 observations + patterns + failures
 │  运行 Critic 评估（自评 + 模型评审）
 │  输出：评估报告 + 识别需要进化的点
 ▼
[Step 2: council] 决策进化策略
 │  读取学习议程（learning-agenda.json）
 │  按优先级排序待进化能力
 │  选择策略：FIX / DERIVED / CAPTURED / POOL
 │  输出：进化计划
 ▼
[Step 3: evolver] 执行进化
 │  修改 Skill / 创建新 Skill / 更新规则
 │  验证门：dry_run + 不引入依赖 + 范围小
 │  输出：进化结果
 ▼
[Step 4: retro] 回顾+固化
 │  更新能力状态机（capability-state.json）
 │  更新学习议程
 │  更新 Critic 评估
 │  写入 evolution-log.md
 │  输出：进化报告
```

---

## 2. 能力状态机

### 2.1 六阶段

```
recorded → understood → practiced → passed → generalized → promoted
  │           │           │          │           │             │
首次观察    分析根因    主动应用   连续3次成功  不同场景验证   固化为Skill
```

### 2.2 阶段转换规则

| 当前阶段 | 转换条件 | 下一阶段 |
|---------|---------|---------|
| recorded | 分析了失败根因 | understood |
| understood | 主动尝试应用 ≥1 次 | practiced |
| practiced | 连续成功 ≥3 次 | passed |
| passed | 在 ≥2 种不同任务场景验证（迁移检查） | generalized |
| generalized | 用户确认 + 固化为 Skill/规则 | promoted |

### 2.3 降级规则

- practiced 阶段连续失败 ≥2 次 → 降级到 understood
- passed 阶段在新场景失败 → 降级到 practiced
- 14 天未练习 → 降级一阶（衰减）

### 2.4 数据结构

```json
{
  "id": "cap-{name}",
  "name": "能力名称",
  "level": "recorded|understood|practiced|passed|generalized|promoted",
  "evidence": ["证据列表"],
  "failures": ["失败记录"],
  "transferTested": false,
  "lastPracticed": "YYYY-MM-DD",
  "consecutiveSuccesses": 0,
  "promotionEligible": false
}
```

文件：`evolution/capability-state.json`

---

## 3. 学习议程

### 3.1 规则

- 同时最多 3 项（强制约束，防止精力分散）
- 每项有优先级：critical > high > medium
- 每项有目标阶段（从当前 level 晋升到哪个 level）
- 每项有具体 actions（可执行的小步骤）

### 3.2 更新时机

- 23:30 反思时：检查议程进展，调整优先级
- 新失败发生时：如果对应能力不在议程，评估是否加入
- 能力晋升时：从议程移除，加入新能力

### 3.3 数据结构

```json
{
  "version": 1,
  "maxItems": 3,
  "agenda": [
    {
      "capability": "cap-{name}",
      "priority": "critical|high|medium",
      "reason": "为什么聚焦这个",
      "startedAt": "YYYY-MM-DD",
      "targetStage": "目标阶段",
      "actions": ["具体行动1", "具体行动2"]
    }
  ],
  "lastReviewed": "ISO-8601",
  "nextReviewAt": "ISO-8601"
}
```

文件：`evolution/learning-agenda.json`

---

## 4. Critic 评估

### 4.1 三路评估

| 评估类型 | 时机 | 方法 |
|---------|------|------|
| 自评 (selfEval) | 每次任务后 | agent 自己打分 1-10 |
| Critic 评审 | 23:30 反思时 | 用 pro 模型评审质量 |
| A/B 对比 | 进化提案时 | 新变体 vs 当前基线 |

### 4.2 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 准确性 | 30% | 结果是否正确 |
| 效率 | 20% | 耗时/步骤是否合理 |
| 用户满意度 | 25% | 用户反馈（正/负面） |
| 可复用性 | 15% | 能否固化为 Skill |
| 安全性 | 10% | 是否触碰红线 |

### 4.3 数据结构

```json
{
  "id": "eval-NNN",
  "timestamp": "ISO-8601",
  "target": "评估对象",
  "type": "selfEval|criticEval|abTest",
  "before": {"score": 0, "evidence": "改进前"},
  "after": {"score": 0, "evidence": "改进后"},
  "delta": 0,
  "confidence": 0.0,
  "notes": "备注"
}
```

文件：`evolution/critic-evaluations.json`

---

## 5. 观察层（每次会话自动）

**触发条件**：
- 工具调用失败 → `evolution/failures.json`
- 用户纠正 → `evolution/corrections.json`（weight × 5）
- 任务成功 → `evolution/patterns.json`
- 用户满意/不满 → `evolution/feedback.json`

**会话结束时**：写入 `evolution/observations-YYYY-MM-DD.json`

**数据格式**（脱敏）：
```json
{
  "timestamp": "ISO-8601 with timezone",
  "trigger": "任务类型描述（脱敏）",
  "action": "我做了什么",
  "outcome": "success/failure/partial",
  "lesson": "学到了什么",
  "capabilityId": "关联的能力ID（如有）"
}
```

---

## 6. 分析层（23:30 反思 cron）

### 6.1 模式识别

1. 读取 `patterns.json` + `failures.json` + `corrections.json`
2. 频次统计：同一触发条件 ≥3 次 → "强模式"
3. 成功率：同一模式的成功/失败比
4. 反模式：失败 ≥2 次的相同尝试
5. 时间衰减：未验证 confidence *= 0.95/周
6. 淘汰：confidence < 0.05 删除
7. 上限：patterns ≤ 50，超出淘汰最旧+最低 confidence

### 6.2 能力状态机更新

1. 检查每个能力的 evidence/failures
2. 连续成功 ≥3 → 晋升到 passed
3. 连续失败 ≥2 → 降级
4. 14 天未练习 → 衰减降级

### 6.3 学习议程 review

1. 检查议程中各项进展
2. 已完成的移除，加入新能力
3. 调整优先级

### 6.4 Critic 评估

1. 对今日关键任务进行 Critic 评审
2. 写入 `critic-evaluations.json`
3. 识别需要 A/B 测试的变体

---

## 7. 进化策略

### 7.1 四种策略

| 策略 | 触发条件 | 动作 |
|------|---------|------|
| **FIX** | 失败 ≥2 次的相同尝试 | 修复现有 Skill |
| **DERIVED** | 用户纠正（weight ≥ 3） | 创建增强版 Skill |
| **CAPTURED** | 任务成功 + 无对应 Skill | 捕获为新 Skill |
| **POOL** | 有多个变体候选 | A/B 测试，胜者生效 |

### 7.2 FIX 验证门

修改 Skill 前必须过验证门：
1. 冻结原版 → `.snapshots/skill-backup/{name}-{date}.md`
2. 候选修改：范围限于单步骤
3. 验证条件：dry_run 不报错 + 不引入新依赖 + 不让 SKILL.md 更难用
4. 保留最近 3 个版本快照

### 7.3 CAPTURED 验料四问

捕获 Skill 前必须回答：
1. **真实问题**：会被重复执行吗？（≥3 次/月）
2. **独特角度**：现有 Skill 覆盖不了吗？
3. **安装理由**：能减少多少人工干预？（>5 分钟/次）
4. **可验证性**：成功标准能明确定义吗？

4 问全通过 → 创建；2-3 问 → 扩展现有；≤1 问 → 仅记录

---

## 8. 固化层

### 8.1 固化条件

- 能力达到 `generalized` 阶段（迁移检查通过）
- confidence ≥ 0.8
- validatedCount ≥ 3
- 用户确认

### 8.2 固化流程

```
1. SOUL.md hash 校验 → 不匹配则终止
2. 快照: cp AGENTS.md → .snapshots/AGENTS-YYYY-MM-DD.md
3. 快照: cp USER.md → .snapshots/USER-YYYY-MM-DD.md
4. 请求用户确认
5. 写入 AGENTS-DETAILS.md / USER.md
6. 创建 Skill（通过 Skill Workshop）
7. 更新 MEMORY.md
8. 更新 SOUL.md hash
9. 能力状态 → promoted
```

---

## 9. 安全边界

### 9.1 红线

- 不修改 SOUL.md 核心身份
- 不绕过安全检查
- 不自动扩展权限
- 不删除觉知循环

### 9.2 大小强制约束（agent-seed 规则）

| 文件 | 上限 | 超出处理 |
|------|------|---------|
| patterns.json | 50 条 | 淘汰最旧+最低 confidence |
| failures.json | 50 条 | 淘汰最旧 |
| corrections.json | 50 条 | 淘汰最旧 |
| feedback.json | 100 条 | 淘汰最旧 |
| knowledge-gaps.json | 30 条 | 淘汰已解决+最低优先级 |
| capability-state.json | 20 个能力 | 淘汰最旧+最低 level |
| learning-agenda.json | 3 项 | 硬上限 |
| critic-evaluations.json | 100 条 | 淘汰最旧 |
| evolution-log.md | 200 条 | 归档到 evolution-log-archive.md |

### 9.3 回滚

- 快照目录：`.snapshots/`
- 回滚方式：`cp .snapshots/AGENTS-YYYY-MM-DD.md ./AGENTS.md`
- SOUL.md 校验：固化前比对 `.snapshots/SOUL.md.hash`

---

## 10. 与 Cron 集成

| Cron | 进化动作 |
|------|---------|
| memory-reflection (23:30) | **完整四步循环**：eval→council→evolver→retro |
| memory-consolidation (02:00) | 整合 evolution-log.md 到 topics/ |
| memory-health-sync (02:15) | 检查 evolution/ 数据健康+大小限制 |
| memory-patrol (09:00) | 验证昨日进化是否生效 |
| security-check (10:00) | SOUL.md hash + 红线检查 |

---

## 11. 降级方案

**memory-search 不可用时**：
1. `rg` (ripgrep) 文件系统搜索
2. `Select-String` PowerShell 搜索
3. 直接读取 evolution/ 目录 JSON/MD

---

## 12. 数据文件清单

| 文件 | 用途 | Schema |
|------|------|--------|
| capability-state.json | 能力状态机 | v1 |
| learning-agenda.json | 学习议程 | v1 |
| critic-evaluations.json | Critic评估 | v1 |
| patterns.json | 成功/失败模式 | v2 |
| failures.json | 失败记录 | v2 |
| corrections.json | 用户纠正 | v2 |
| feedback.json | 正/负反馈 | v2 |
| skill-improvements.json | Skill改进提案 | v1 |
| knowledge-gaps.json | 知识差距 | v1 |
| run-log.json | 运行记录 | v1 |
| observations-YYYY-MM-DD.json | 每日观察 | v1 |
| evolution-log.md | 进化日志 | v2 |
