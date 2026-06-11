# Errors

Command failures and integration errors.

---

## [ERR-20260611-001] search-memory.ps1

**Logged**: 2026-06-11T11:00:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
search-memory.ps1 UTF-8 无 BOM 导致中文崩溃

### Error
```
无法处理中文字符，返回乱码或空结果
```

### Context
- 操作：搜索包含中文关键词的记忆文件
- 环境：Windows PowerShell，默认编码非 UTF-8
- 根因：脚本文件 UTF-8 无 BOM，PowerShell 无法正确识别

### Suggested Fix
添加 UTF-8 BOM 头或使用英文 key

### Resolution
- **Resolved**: 2026-06-11T15:20:00+08:00
- **Notes**: v6 重写，英文 key 避免编码问题 + UTF-8 BOM

### Metadata
- Reproducible: yes
- Related Files: search-memory.ps1
- See Also: ERR-20260611-002

---

## [ERR-20260611-002] search-memory.ps1

**Logged**: 2026-06-11T22:00:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
空查询和不存在关键词返回虚假结果

### Error
```
空查询返回所有文件，不存在的关键词返回不相关结果
```

### Context
- 操作：search-memory.ps1 "" 或 search-memory.ps1 "不存在的词"
- 根因：缺少空查询防护和结果验证

### Suggested Fix
添加空查询检查 + 结果相关性验证

### Resolution
- **Resolved**: 2026-06-11T22:13:00+08:00
- **Notes**: 大规模测试修复

### Metadata
- Reproducible: yes
- Related Files: search-memory.ps1
- See Also: ERR-20260611-001

---

## [ERR-20260611-003] memory-state.json

**Logged**: 2026-06-11T22:00:00+08:00
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
memory-state.json 所有 cron 时间戳为 null

### Error
```json
{
  "consolidation": null,
  "health_sync": null,
  "patrol": null,
  "reflection": null
}
```

### Context
- 操作：检查 memory-state.json 运行状态
- 根因：cron 执行后未写入时间戳，自检逻辑从未真正执行

### Suggested Fix
cron 输出增加验证步骤，确保时间戳写入

### Resolution
- **Resolved**: 2026-06-11T22:13:00+08:00
- **Notes**: 修复时间戳写入逻辑

### Metadata
- Reproducible: yes
- Related Files: memory/memory-state.json
