# Feature Requests

Capabilities requested by the user.

---

## [FEAT-20260611-001] semantic_search

**Logged**: 2026-06-11T13:30:00+08:00
**Priority**: high
**Status**: pending
**Area**: infra

### Requested Capability
语义搜索：搜索「之前讨论过的部署方案」能返回 docker/podman 相关内容

### User Context
当前 grep 精确匹配 + 同义词表无法处理语义相似但词不同的查询

### Complexity Estimate
medium

### Suggested Implementation
- nomic-embed-text 本地嵌入模型
- SQLite + sqlite-vss 向量存储
- grep 为主，向量为辅（双保险）

### Metadata
- Frequency: recurring
- Related Features: search-memory.ps1, 记忆系统进化 阶段A

---

## [FEAT-20260611-002] experience_memory

**Logged**: 2026-06-11T13:30:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Requested Capability
经验记忆：记录「怎么做更好」而非仅「知道什么」

### User Context
当前只记事实，不记经验。遇到类似场景时无法引用过去的教训。

### Complexity Estimate
medium

### Suggested Implementation
- 新增 memory/topics/experience.md
- 反射管道输出自动写入
- 格式：[场景] → [做法] → [结果] → [教训]

### Metadata
- Frequency: first_time
- Related Features: 反射管道, 记忆系统进化 阶段B

---

## [FEAT-20260611-003] task_reminder

**Logged**: 2026-06-11T14:19:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Requested Capability
未完成任务到期前提醒 + 长时间未联系人物提醒

### User Context
Phase 2 主动智能的子任务，当前只有日历提醒

### Complexity Estimate
simple

### Suggested Implementation
- 从 daily 日志提取未完成待办
- 到期前通过心跳提醒
- 人物联系频率追踪

### Metadata
- Frequency: first_time
- Related Features: HEARTBEAT.md, Phase 2 主动智能
