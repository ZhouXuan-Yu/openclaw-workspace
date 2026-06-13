# 自我进化引擎 — 完整协议 v2

**版本**: 2.0
**日期**: 2026-06-12
**触发**: memory-reflection (23:30) + 每次会话结束
**修复**: v2 修复了 19 个漏洞/缺陷

---

## 1. 进化循环

```
观察 → 分析 → 提炼 → 验证 → 用户确认 → 固化
  │       │       │       │       │         │
每次会话  23:30   自动    下次    必须      快照+hash
自动记录  反思    提取    测试    用户审批   安全写入
```

### 1.1 观察层（每次会话自动）

**触发条件**：
- 工具调用失败 → 记录到 `evolution/failures.json`
- 用户纠正 → 记录到 `evolution/corrections.json`
- 任务成功 → 记录到 `evolution/patterns.json`
- 用户满意/不满 → 记录到 `evolution/feedback.json`

**数据格式**（脱敏，不存原始用户输入）：
```json
{
  "timestamp": "ISO-8601 with timezone",
  "trigger": "任务类型描述（脱敏）",
  "action": "我做了什么",
  "outcome": "success/failure/partial",
  "lesson": "学到了什么（如果有）"
}
```

**会话结束时**：写入 `evolution/observations-YYYY-MM-DD.json`

### 1.2 分析层（23:30 反思 cron）

**模式识别算法**：
1. 读取 `evolution/patterns.json` + `evolution/failures.json`
2. 统计频次：同一触发条件出现 ≥3 次 → 标记为"强模式"
3. 统计成功率：同一模式的成功/失败比
4. 识别反模式：失败 ≥2 次的相同尝试
5. **时间衰减**：未被验证的模式 confidence *= 0.95/周
6. **淘汰**：confidence < 0.05 的模式自动删除
7. **上限**：patterns 总数 ≤ 50，超出淘汰最旧+最低 confidence

**输出**：
- 更新 `patterns.json` 的 confidence 字段
- 新发现的模式添加到 patterns
- 反模式添加到 antiPatterns

### 1.3 提炼层（自动）

**从模式中提取规则**：

| 模式类型 | 提取规则 | 写入位置 |
|---------|---------|---------|
| 成功工具链 | "遇到X时，先Y再Z" | AGENTS-DETAILS.md |
| 失败教训 | "不要在X时做Y" | AGENTS-DETAILS.md 红线 |
| 用户偏好 | "用户喜欢X风格" | USER.md / topics/preferences.md |
| 技术决策 | "选X因为Y" | topics/decisions.md |
| Skill 候选 | "这个流程值得固化" | evolution/skill-candidates.md |
| **Topic 关联** | "X和Y经常一起被检索" | **topics/_graph.json** |

**关联学习规则**：
- 同一会话中连续检索 ≥2 个 topic 才找到答案 → 记录关联候选
- 关联候选出现 ≥3 次 → 自动写入 `_graph.json` 的 connections
- 用户明确说"这个跟XX有关" → 直接写入（高置信度）

### 1.4 验证层（下次会话）

**验证流程**：
1. 提炼的规则标记为 `status: "proposed"`
2. 下次遇到相同触发条件时，尝试应用规则
3. 成功 → `status: "validated"`，confidence +0.1，validatedCount +1
4. 失败 → `status: "rejected"` 或重新分析

### 1.5 固化层（需用户确认）

**固化条件**：confidence ≥ 0.8 且 validatedCount ≥ 3 次
**固化流程**（严格顺序）：

```
1. 生成 SOUL.md hash → 与 .snapshots/SOUL.md.hash 比对
   └─ 不匹配 → 终止，报告异常
2. 快照: cp AGENTS.md → .snapshots/AGENTS-YYYY-MM-DD.md
3. 快照: cp USER.md → .snapshots/USER-YYYY-MM-DD.md
4. 请求用户确认: "准备固化规则 [X]，修改 AGENTS.md/USER.md，确认？"
   └─ 用户拒绝 → 终止
5. 写入 AGENTS-DETAILS.md（行为规则）/ USER.md（偏好）
6. 创建 Skill（流程固化）
7. 更新 MEMORY.md（知识）
8. 更新 SOUL.md hash（如 SOUL.md 被合法修改）
```

---

## 2. 失败分析协议

### 2.1 失败分类

| 类型 | 代码 | 处理 |
|------|------|------|
| 工具调用失败 | TOOL_FAIL | 重试→换方案→记录 |
| 用户纠正 | USER_CORRECT | 立即学习→记录 |
| 理解偏差 | MISUNDERSTAND | 澄清→记录触发词 |
| 超时/性能 | TIMEOUT | 优化路径→记录 |
| 安全拦截 | SAFETY_BLOCK | 检查红线→不绕过 |

### 2.2 失败响应

```json
{
  "id": "fail-NNN",
  "timestamp": "ISO-8601 with timezone",
  "type": "TOOL_FAIL|USER_CORRECT|MISUNDERSTAND|TIMEOUT|SAFETY_BLOCK",
  "trigger": "脱敏的任务描述",
  "attempt": "尝试了什么",
  "result": "失败结果",
  "rootCause": "根因分析",
  "fix": "修正方案",
  "status": "proposed → validated",
  "occurrences": 1,
  "parentEventId": "触发此失败的事件ID（如有）"
}
```

### 2.3 FIX 验证门（借鉴鲁班慢刨）

当 failure ≥ 2 准备修复 Skill 时，必须过验证门：

1. **冻结原版**：修改前备份当前 SKILL.md 到 `.snapshots/skill-backup/{skill-name}-{date}.md`
2. **候选修改**：生成修改方案，范围限于单步骤，不重构整个 Skill
3. **验证条件**（全部满足才写入）：
   - 修改后的步骤 dry_run 不报错
   - 不引入新的外部依赖或私有路径
   - 不让 SKILL.md 变得更长但更难用
   - 修改范围小（单步骤/单工具替换）
4. **保留回滚**：最近 3 个版本的快照保留

详见 `memory/evolution/skill-evolution.md`

---

## 3. 成功捕获协议（借鉴鲁班验料）

### 3.1 Skill 候选识别（增加验料环节）

**触发条件**：
- 任务成功完成
- 涉及 ≥3 个工具调用
- 流程可复用（不是一次性任务）

**验料四问**（鲁班方法论，捕获前必须回答）：
1. **真实问题**：这个任务会被重复执行吗？（≥3 次/月才值得）
2. **独特角度**：现有 Skill 覆盖不了吗？（检查是否可扩展现有 Skill）
3. **安装理由**：固化后能减少多少人工干预？（>5 分钟/次才值得）
4. **可验证性**：成功标准能明确定义吗？

**验料结论**：
- 4 问全通过 → 创建新 Skill
- 2-3 问通过 → 考虑扩展现有 Skill
- ≤1 问通过 → 不创建，仅记录到 patterns

**捕获流程**：
1. 验料通过后，记录完整工具链到 `evolution/skill-candidates.md`
2. 标记为 `status: "candidate"`
3. 下次类似任务时验证
4. 验证 ≥2 次 → 创建正式 Skill（通过 Skill Workshop）

### 3.2 工具链优化

**记录格式**：
```markdown
## 工具链: [任务类型]
**触发**: [什么时候用]
**步骤**:
1. [工具A] → [输出]
2. [工具B] → [输出]
3. [工具C] → [输出]
**耗时**: ~Xs
**成功率**: X%
**替代方案**: [如果失败的备选]
```

---

## 4. 知识差距检测

### 4.1 检测方法

**每次会话自动检测**：
1. 用户问了我不知道的 → 记录到 `evolution/knowledge-gaps.json`
2. 搜索无结果 → 记录搜索词
3. 工具调用失败因为参数不懂 → 记录工具+场景

### 4.2 差距分类

| 类型 | 优先级 | 处理 |
|------|--------|------|
| 高频询问 | P0 | 立即学习/创建 Skill |
| 技术知识 | P1 | 搜索→整理→写入 topics/ |
| 工具用法 | P2 | 读文档→记录到 work-tools.md |
| 领域知识 | P3 | 按需学习 |

---

## 5. 进化指标

### 5.1 核心指标

| 指标 | 计算方式 | 目标 |
|------|---------|------|
| 任务成功率 | success / total | >90% |
| 记忆准确率 | relevantHits / retrievals | >80% |
| 响应简洁率 | concise / (concise+verbose) | >70% |
| 工具一次成功率 | singleShot / total | >85% |
| 模式验证率 | validated / proposed | >60% |

### 5.2 进化速度

**计算**：每周新增 validated 模式数
**目标**：≥2 个/周（初期），≥1 个/周（成熟期）

---

## 6. 安全边界

### 6.1 进化红线（技术强制）

**绝不进化**：
- 不修改 SOUL.md 核心身份 → **强制: 固化前校验 SOUL.md hash**
- 不绕过安全检查
- 不自动扩展权限
- 不删除觉知循环

**需要确认**（强制用户审批）：
- 修改 AGENTS.md 行为规则 → **强制: 快照 + 用户确认**
- 修改 USER.md 用户画像 → **强制: 快照 + 用户确认**
- 创建新 Skill

**自由进化**：
- 更新 evolution/ 数据文件
- 更新 memory/daily/ 日志
- 更新 memory/topics/ 知识
- 更新 .skill-quality.json

### 6.2 并发保护

**写入前**：创建 `.lock` 文件（含 PID + 时间戳）
**写入时**：原子写入（tmpfile + rename）
**写入后**：删除 `.lock`
**锁超时**：30 秒自动释放（防死锁）

### 6.3 回滚机制

**快照目录**: `.snapshots/`
**快照时机**: 每次修改 AGENTS.md / USER.md 前（强制第一步）
**回滚方式**: `cp .snapshots/AGENTS-YYYY-MM-DD.md ./AGENTS.md`
**SOUL.md 校验**: 固化前比对 `.snapshots/SOUL.md.hash`

### 6.4 隐私保护

**记录时脱敏**：
- trigger 字段：只记录任务类型，不存原始用户输入
- 不记录文件路径中的用户名
- 不记录 API key / token / 密码

### 6.5 大小限制

| 文件 | 上限 | 超出处理 |
|------|------|---------|
| patterns.json | 50 条 | 淘汰最旧+最低 confidence |
| failures.json | 50 条 | 淘汰最旧 |
| knowledge-gaps.json | 30 条 | 淘汰已解决+最低优先级 |
| feedback.json | 100 条 | 淘汰最旧 |
| corrections.json | 50 条 | 淘汰最旧 |
| evolution-log.md | 200 条 | 归档旧条目到 evolution-log-archive.md |

---

## 7. 进化日志格式

每次进化写入 `evolution/evolution-log.md`：

```markdown
### YYYY-MM-DD HH:MM+TZ 进化事件

**类型**: [PATTERN_LEARNED / FAILURE_ANALYZED / SKILL_CAPTURED / KNOWLEDGE_GAP / RULE固化]
**触发**: [什么事件触发了这次进化]
**内容**: [具体学到了什么]
**动作**: [写入了哪个文件/创建了什么]
**状态**: proposed / validated / 固化
**因果**: parent=[父事件ID] / root=[根因事件ID]
```

**时间格式**: 统一使用 ISO-8601 with timezone (如 `2026-06-12T16:00:00+08:00`)

---

## 8. 与现有系统的集成

| 系统 | 集成方式 |
|------|---------|
| memory-consolidation (02:00) | **第一步**读取 evolution/evolution-log.md；整合到 topics/ |
| memory-reflection (23:30) | 运行模式识别+提炼+时间衰减+淘汰 + **Skill 健康度分析** |
| memory-health-sync (02:15) | 检查 evolution/ 数据健康+大小限制 + 清理过期 traces |
| memory-patrol (09:00) | 验证昨日进化是否生效 |
| security-check (10:00) | 检查进化是否触碰红线+SOUL.md hash |
| Skill Workshop | FIX/DERIVED 通过验证门后固化 |
| **Skill 自进化** | **详见 skill-evolution.md；每次调用记录轨迹，23:30 分析生成改进提案** |

### 8.1 降级方案

**memory-search 不可用时**：
1. 使用 `rg` (ripgrep) 文件系统搜索
2. 使用 `Select-String` PowerShell 搜索
3. 搜索 evolution/ 目录下的 JSON/MD 文件

---

## 9. 进化引擎启动清单

每次会话开始时（与 AGENTS.md 启动流程并行）：

1. ✅ 检查 .snapshots/ 目录存在性（不存在则创建）
2. ✅ 读 `evolution/patterns.json` — 加载已知模式（空文件跳过）
3. ✅ 读 `evolution/performance.json` — 加载性能指标（空文件跳过）
4. ✅ 检查 `evolution/knowledge-gaps.json` — 待填补的差距
5. ✅ 本次会话中：观察→记录→（不自动进化，留给 23:30）

**冷启动优化**：文件大小为 0 或仅含空数组时跳过加载。

会话结束时：
1. ✅ 写入本次会话的观察到 `evolution/observations-YYYY-MM-DD.json`（脱敏）
2. ✅ 如果有重大发现，立即写入 `evolution/patterns.json`（遵守大小限制）

23:30 反思时：
1. ✅ 读取今日所有 observations
2. ✅ 运行模式识别（频次统计+成功率）
3. ✅ 时间衰减：未验证模式 confidence *= 0.95/周
4. ✅ 淘汰：confidence < 0.05 的模式删除
5. ✅ 提炼规则
6. ✅ 写入 evolution-log.md（含因果链）
7. ✅ 更新 patterns.json / failures.json（遵守大小限制）
8. ✅ 标记 skill-candidates

---

## 10. 数据文件 Schema

### patterns.json v2
```json
{
  "version": 2,
  "maxEntries": 50,
  "lastUpdated": "ISO-8601 with timezone",
  "patterns": [
    {
      "id": "string",
      "type": "success|failure",
      "category": "toolchain|decision|preference|safety",
      "trigger": "string (脱敏)",
      "pattern": "string",
      "confidence": 0.0-1.0,
      "validatedCount": "number",
      "observedCount": "number",
      "lastObserved": "YYYY-MM-DD",
      "lastValidated": "YYYY-MM-DD",
      "expiresAt": "YYYY-MM-DD",
      "notes": "string"
    }
  ],
  "antiPatterns": [
    {
      "id": "string",
      "category": "string",
      "trigger": "string",
      "pattern": "string",
      "fix": "string",
      "confidence": 0.0-1.0,
      "observedCount": "number",
      "lastObserved": "YYYY-MM-DD"
    }
  ],
  "decayConfig": {
    "enabled": true,
    "decayRate": 0.95,
    "decayIntervalDays": 7,
    "minConfidence": 0.1,
    "purgeBelowConfidence": 0.05
  }
}
```

### failures.json v2
```json
{
  "version": 2,
  "maxEntries": 50,
  "failures": [
    {
      "id": "string",
      "timestamp": "ISO-8601 with timezone",
      "type": "TOOL_FAIL|USER_CORRECT|MISUNDERSTAND|TIMEOUT|SAFETY_BLOCK",
      "trigger": "string (脱敏)",
      "attempt": "string",
      "result": "string",
      "rootCause": "string",
      "fix": "string",
      "status": "proposed|validated",
      "occurrences": "number",
      "parentEventId": "string|null"
    }
  ]
}
```
