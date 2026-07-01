# 自举进化协议 — 内容发布系统

**目标**: 每运行 N 次自动优化，越用越好用。

---

## 核心指标

| 指标 | 初始基线 | 目标 | 优化手段 |
|------|---------|------|---------|
| 发布耗时 | 10min | 5min | 并行发布、缓存登录态 |
| Token 消耗 | ~8000/run | ~4000/run | 压缩 prompt、复用模板 |
| 成功率 | 80% | 95% | 失败重试、跳过不可用平台 |
| 内容质量 | 人工审核 | 自动校验 | 规则校验、A/B 测试 |

---

## 进化循环

```
运行 → 记录 → 分析(每5次) → 提炼规则 → 应用 → 验证
  │       │         │            │          │       │
  每次    metrics   cron触发    优化prompt  下次运行  确认提升
```

### 1. 每次运行记录

```json
{
  "runId": "run-001",
  "timestamp": "ISO-8601",
  "task": "content-generation | publishing",
  "tokensUsed": 0,
  "timeSeconds": 0,
  "platforms": {
    "xiaohongshu": {"status": "ok|fail|skip", "error": null},
    "douyin": {"status": "ok|fail|skip", "error": null}
  },
  "optimizationsApplied": []
}
```

### 2. 每 5 次运行触发优化分析

分析维度：
- **Token 消耗趋势**: 上升 → 压缩 prompt
- **失败模式**: 同一平台连续失败 → 标记为不可用，自动跳过
- **耗时瓶颈**: 哪个步骤最慢 → 优化该步骤
- **缓存命中率**: 低 → 增加缓存

### 3. 优化动作

| 优化类型 | 触发条件 | 动作 |
|---------|---------|------|
| Prompt 压缩 | Token > 6000 | 去除冗余指令，合并重复要求 |
| 平台跳过 | 连续 3 次失败 | 标记为 unavailable，跳过 |
| 并行发布 | 串行耗时 > 60s | 无依赖平台并行执行 |
| 模板缓存 | 相同主题重复生成 | 复用已生成内容 |
| 错误预检 | 同类错误出现 2 次 | 发布前预检该错误 |
| 链路精简 | 步骤数 > 10 | 合并可省略步骤 |

### 4. 固化条件

- 优化后连续 3 次成功率提升 → 固化到 Skill
- Token 消耗降低 > 20% → 固化到 Skill
- 耗时降低 > 30% → 固化到 Skill

---

## 自动化规则

### Rule 1: Token 预算控制
```yaml
max_tokens_per_run: 8000
warning_threshold: 6000
action_on_exceed: "compress_prompt"
```

### Rule 2: 平台健康检查
```yaml
check_before_publish: true
skip_unhealthy: true
health_check_command: "sau <platform> check --account creator"
```

### Rule 3: 失败重试
```yaml
max_retries: 2
retry_delay_seconds: 5
backoff: exponential
```

### Rule 4: 内容缓存
```yaml
cache_generated_content: true
cache_ttl_hours: 24
reuse_on_same_topic: true
```

### Rule 5: 并行执行
```yaml
parallel_platforms: true
max_concurrent: 3
timeout_per_platform: 60
```

---

## 进化日志

每次优化记录到 `evolution/evolution-log.md`：

```markdown
### YYYY-MM-DD HH:MM 优化事件

**类型**: SKILL_OPTIMIZED
**触发**: 第 N 次运行分析
**问题**: [具体问题]
**优化**: [具体动作]
**效果**: [量化提升]
**状态**: proposed → validated → 固化
```

---

## 经济性约束

**Token 经济**:
- 内容生成: 目标 ≤ 4000 tokens/次
- 发布执行: 目标 ≤ 1000 tokens/次
- 优化分析: 目标 ≤ 2000 tokens/次（每 5 次触发）

**时间经济**:
- 内容生成: 目标 ≤ 3 分钟
- 发布执行: 目标 ≤ 2 分钟（并行）
- 端到端: 目标 ≤ 5 分钟

**降级策略**:
- Token 超预算 → 降级到模板化生成
- 平台不可用 → 降级到可用平台子集
- 网络超时 → 降级到本地操作
