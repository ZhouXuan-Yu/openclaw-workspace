# Cron 执行日志 & 离线补偿系统

## 日志文件
`memory/cron-log.md` — 每日 cron 任务执行记录

## 工作流程

### 在线时（正常运行）
1. 每个 cron 任务执行后更新 `cron-log.md`，标记状态
2. 状态: `OK` / `ERROR` / `PENDING`

### 离线恢复时（你上线后）
1. `bootstrap hook` 触发 `tools/cron-recovery.ps1`
2. 扫描今日 PENDING 任务 → 报告遗漏
3. 标记无法补偿的 PENDING → `SKIPPED (offline)`
4. 下次 cron 调度时间自动重试

### 查看方式
1. SQLPage: `http://localhost:8080/cron-log.sql` — 实时日志
2. 本地: `memory/cron-log.md` — 原始文件
3. Dashboard HTML: 自动包含 cron 状态

## 每日刷新策略
- Dashboard HTML: 每次对话结束自动刷新
- SQLPage 数据: 每天最多重启一次（首次 cron 触发时）
- 不必要时不触发容器重启，避免中断使用
