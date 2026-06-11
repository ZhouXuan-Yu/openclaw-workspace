# Git 进化基础设施

> Git 不只是版本控制，它是进化历史的记录者和分析者
> 每一次 commit 都是一次进化的快照

## Git 在进化架构中的角色

```
┌─────────────────────────────────────────────┐
│  Git = 进化历史数据库                        │
│                                             │
│  commit = 进化快照（比 .snapshots/ 更权威）  │
│  diff = 进化差异（精确到行）                 │
│  log = 进化时间线                            │
│  branch = 进化实验分支                       │
│  revert = 进化回滚                           │
│  blame = 进化溯源（谁改的、为什么改）        │
└─────────────────────────────────────────────┘
```

## 与 3 循环的集成

### 觉知循环使用 Git

| 操作 | 命令 | 用途 |
|------|------|------|
| 分析进化趋势 | `git log --oneline --since="7 days"` | 识别近期进化模式 |
| 检查异常提交 | `git diff HEAD~3` | 发现意料之外的修改 |
| 进化频率统计 | `git shortlog -sn` | 哪些文件进化最频繁 |
| 安全审计 | `git log --all --diff-filter=A -- "*.exe"` | 检查是否有可疑文件被添加 |

### 执行-验证循环使用 Git

| 操作 | 命令 | 用途 |
|------|------|------|
| 修改前快照 | `git stash` 或直接 commit | 保存当前状态 |
| 修改后验证 | `git diff` | 精确查看改了什么 |
| 回滚 | `git revert HEAD` 或 `git checkout` | 恢复到之前状态 |
| 实验分支 | `git checkout -b experiment/xxx` | 安全地尝试新方案 |

### 记忆整合循环使用 Git

| 操作 | 命令 | 用途 |
|------|------|------|
| 整合前后对比 | `git diff` | 验证整合没有丢失信息 |
| 进化日志 | `git log --grep="FIX\|DERIVED\|CAPTURED"` | 追踪进化历史 |
| 质量趋势 | `git log --stat` | 文件大小变化趋势 |

## Git 提交规范

### Commit Message 格式

```
<type>(<scope>): <description>

[optional body]
```

### Type 分类

| Type | 含义 | 循环归属 |
|------|------|---------|
| `feat` | 新功能/新 Skill | 执行-验证 |
| `fix` | 修复 Bug/Skill | 记忆整合（FIX 进化） |
| `refactor` | 架构调整 | 觉知（架构进化） |
| `docs` | 文档/记忆更新 | 记忆整合 |
| `perf` | 性能优化 | 执行-验证 |
| `security` | 安全加固 | 觉知 |
| `evolution` | 自进化触发 | 记忆整合 |
| `meta` | 元进化（规则本身的进化） | 记忆整合 |
| `snapshot` | 版本化快照 | 记忆整合 |

### 自动标签

每次 commit 时自动分析：
- 如果 message 包含 "FIX" → 标记为 `#skill-fix`
- 如果 message 包含 "DERIVED" → 标记为 `#skill-derived`
- 如果 message 包含 "CAPTURED" → 标记为 `#skill-captured`
- 如果 diff 涉及 `skills/` 目录 → 标记为 `#skill-change`
- 如果 diff 涉及 `agents/` 目录 → 标记为 `#architecture-change`

## Git 进化分析（觉知循环专用）

### 每周进化报告

```powershell
# 统计本周进化次数
git log --oneline --since="7 days" | Measure-Object

# 按类型统计
git log --since="7 days" --pretty=format:"%s" | 
    Select-String -Pattern "^(feat|fix|refactor|evolution|meta)" |
    Group-Object | Sort-Object Count -Descending

# 最常修改的文件
git log --since="7 days" --name-only --pretty=format: |
    Where-Object { $_ -ne "" } | Group-Object | 
    Sort-Object Count -Descending | Select-Object -First 10

# 进化热点（哪些 Skill 最活跃）
git log --since="30 days" -- "skills/*/SKILL.md" --pretty=format:"%s"
```

### 进化趋势可视化

```
进化频率:
  Week 1: ████████ 8 commits
  Week 2: ████████████ 12 commits
  Week 3: ██████ 6 commits
  
进化类型:
  FIX:      ████████ 40%
  CAPTURED: ██████ 30%
  DERIVED:  ████ 20%
  META:     ██ 10%
```

## Git Hooks（可选增强）

| Hook | 触发 | 操作 |
|------|------|------|
| pre-commit | 提交前 | 检查 MEMORY.md 行数 <200 |
| post-commit | 提交后 | 更新 memory-state.json |
| pre-push | 推送前 | 运行快速测试 |

## 安全边界

- 不修改 `.git/config`（仓库配置）
- 不修改 `.git/hooks`（除非用户明确要求）
- 不 force push（除非用户明确要求）
- 不删除远程分支（除非用户明确要求）
- 所有破坏性操作（reset --hard, clean -fd）需用户确认
