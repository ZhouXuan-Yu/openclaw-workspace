# 版本化自修改 — Versioned Self-Modification

> 任何自我修改前，先快照，可回滚
> 安全第一：改错了能恢复

## 原则

1. **修改前快照** — 任何文件修改前，先保存到 `.snapshots/`
2. **版本号递增** — 每次修改递增版本号
3. **可回滚** — 任何时候可以恢复到任意历史版本
4. **修改日志** — 记录每次修改的原因和差异

## 快照目录结构

```
.snapshots/
├── agents/
│   ├── awareness-loop.v1.md
│   ├── awareness-loop.v2.md
│   └── ...
├── skills/
│   ├── evolution-engine.v1.md
│   └── ...
├── AGENTS.v1.md
├── AGENTS.v2.md
├── SOUL.v1.md
├── MEMORY.v1.md
└── changelog.json
```

## 修改流程

```
需要修改文件
    ↓
1. 检查 .snapshots/ 是否有该文件的快照
2. 如果没有 → 创建初始快照 (v1)
3. 如果有 → 获取最新版本号
4. 创建新快照 (vN+1)
5. 执行修改
6. 记录到 changelog.json
7. 验证修改（读取确认）
```

## Changelog 格式

```json
{
  "entries": [
    {
      "timestamp": "2026-06-12T03:00:00+08:00",
      "file": "agents/awareness-loop.md",
      "version": 2,
      "reason": "添加元进化规则",
      "diff_summary": "新增## 元进化章节",
      "trigger": "manual",
      "status": "applied"
    }
  ]
}
```

## 回滚流程

```
需要回滚
    ↓
1. 确认目标文件和版本号
2. 从 .snapshots/ 读取目标版本
3. 覆盖当前文件
4. 记录回滚操作到 changelog.json
5. 验证回滚
```

## 安全边界

| 操作 | 是否允许快照 |
|------|------------|
| 修改 AGENTS.md | ✅ 必须快照 |
| 修改 SOUL.md | ✅ 必须快照 |
| 修改 MEMORY.md | ✅ 必须快照 |
| 修改 Skill 文件 | ✅ 必须快照 |
| 修改 memory-state.json | ❌ 不快照（频繁更新） |
| 修改 daily 日志 | ❌ 不快照（追加写入） |
| 修改 topic 文件 | ⚠️ 重大修改时快照 |
