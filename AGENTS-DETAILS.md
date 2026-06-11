# AGENTS-DETAILS.md — 详细规则（按需加载）

> 这个文件包含 AGENTS.md 的详细规则和高级配置。
> 只在需要时加载，不随会话自动注入。

## 🔍 记忆检索详细流程

### 操作步骤
1. Read `SOUL.md` — who you are
2. Read `USER.md` — who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday, create if missing)
4. **If in MAIN SESSION** (direct chat with human): Read `MEMORY.md`
5. Read `memory/daily/今日.md` (if exists) — 今天的对话上下文
6. Read `memory/daily/昨日.md` (if exists) — 昨天的对话上下文

### 📡 Cross-Session Context Retrieval
If the user's first message refers to past work, a person, a decision, or a project name:
5. Run `search-memory.ps1 "<keyword>"` to find relevant logs
6. If nothing found, check Obsidian vault at `E:\Obsidian仓库\ZhouXuan私人领域`
7. Say "I checked my memory and didn't find anything on that" — don't guess

Don't ask permission. Just do it.

### 📋 今日摘要（MAIN SESSION 首次启动时）

在记忆加载完成后，如果这是今天的第一次对话，生成今日摘要：

1. 查询今日飞书日程（feishu_calendar_event, action: list, start_time: 今日 00:00, end_time: 今日 23:59）
2. 读取 memory/daily/昨日.md，提取未完成的待办
3. 读取 MEMORY.md 中星标记忆的待办项
4. 生成摘要（仅当有内容时展示）

### 🔍 项目上下文自动加载

当用户第一条消息提及特定项目、技术栈或工作领域时，自动加载相关上下文：

**关键词 → Topic 映射**：
| 关键词 | 加载的 Topic 文件 |
|--------|------------------|
| 记忆/memory/架构 | `topics/learnings.md` + `topics/decisions.md` |
| prompt/提示词/CLAUDE | `topics/learnings.md` |
| skill/插件/MCP | `topics/work-tools.md` |
| 飞书/lark/feishu | `topics/work-tools.md` |
| 项目名/工程名 | `topics/projects.md` |
| 人名 | `topics/people.md` |

## 📤 读策略（L1 → L2 → L3 → L4）

1. **L1 索引命中** → 读对应 topic，结束
2. **L1 未命中** → `search-memory.ps1 "<关键词>"` 搜 topics/
3. **L2 未命中** → 扩展同义词，搜 daily/
4. **L3+ 搜索仍无** → session-logs rg+jq 搜 JSONL
5. **什么都找不到** → 说"我查了记忆记录，没找到相关内容"

**年龄感知**：读 topic 时检查 mtime → >7天 ⚠️ 可能过期 → >30天 🚨 请用户确认。

## ⏳ 老化淘汰

| 触发 | 处理 |
|------|------|
| daily 30天无引用 | 自动删除 |
| topic 7天无强化 | 标记待确认 |
| 矛盾条目 | 以用户最新陈述为准 |
| 用户否定 | 立即删除旧 + 写入新 |

## 📊 健康监控（cron 02:15）

自动检查：MEMORY.md 行数(<150) · topic 条目(<50) · 待确认(<10) · daily 7天数量

## 🔄 Git 同步（cron 02:15）

自动 `git add memory/ MEMORY.md` → commit → push

## 🛡️ 巡检补跑（cron 09:00）

凌晨 cron 执行后写 memory-state.json 时间戳 → 09:00 检查 → 未执行则补跑

## 🗑️ 记忆删除

格式：`记忆删除: <要删除的内容>`
流程：搜索 → 删除 → 记录 → 更新索引 → 确认
