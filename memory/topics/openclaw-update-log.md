# OpenClaw 版本更新评估日志

> 只做评估，不自动升级。最新记录在最上方。

---

## 复检 2026-10-19 14:56

- **当前版本**: 2026.6.10 (aa69b12)
- **latest（npm）**: **2026.10.5**
- **上次评估**: 2026-10-12（目标 10.1）→ **用户未回应，评估仍未决（累计第 10 次）**
- **版本差**: 6.10 → 10.5，跨越 7/8/9/10 四条 release line

### 2026.10.5 关键变更（相对 10.1 增量）

| 领域 | 变更 | 风险 |
|------|------|------|
| 更新机制 | `openclaw update` 全平台自愈：pnpm 12、Windows 提权、跨文件系统、卡住的 handoff lease / activation journal 自动收敛；`--no-restart` 诚实报错 | 🟢 正面 |
| Gateway/会话 | 会话/transcript/history 读操作移入 worker 线程，SQLite 每次 turn 负载大减；Gateway 重启后中断的 turn/subagent/deferred task 可续跑；并发写与失败发布不再丢用户输入 | 🟢 正面（对本地长时 cron 会话友好） |
| Hooks（**破坏性**） | Tool approval hooks：普通 hook 不能再改写已 trusted-inline-approved 的工具参数，改写型插件需单独申请批准，否则**调用被阻断**。迁移见 docs/plugins/hooks/tool-policy.md | 🟠 中（本地 hooks/hooks.yaml 需核对） |
| Sessions | 允许 directed send 不附带 transcript 访问权限 | 🟢 低 |
| Channel | 新增 X (Twitter) channel；语音通话能力；微信/飞书/企微未在 highlight | 🟡 中（微信链路自检） |
| 模型 | 模型选择器以 provider 推荐为先；Gemini 4 Argon / 3.8 Flash；支持未发版即列新模型 | 🟢 低 |
| ClawHub | Gateway 内可浏览/搜索 ClawHub 插件与 skill | 🟢 低（与 Skill Workshop 无破坏） |
| 记忆/cron/配置 schema | 本版无新增破坏性条目，**但全部承接 9.x–10.1 的累积**：SQLite 记忆索引重构、Dreaming/Wiki 旧 JSON 不再导入、cron JSON→SQLite state、工具 visibility/agentToAgent 默认放开、`metadata.clawdbot`→`metadata.openclaw` | 🔴 高（累积） |

### 升级路径约束（未变）
官方 docs/install/updating：**早于 2026-07 的安装必须先升 2026.9.5 → `doctor --fix` → 再升 latest**。
本地 6.10（2026-06）在边界内 → 必须走桥接：
`6.10 → 2026.9.5 (+doctor --fix) → 2026.9.7 (+doctor --fix) → 2026.10.5 (+doctor --fix)`

### 本地影响
- **cron 6 任务**：走 Doctor 迁移到 SQLite state，须逐项触发验证（9.6 有社区 cron 全挂报告，10.x 已修部分 cron 与 cleanup 被 update history 写入阻塞的问题）
- **memory/**：升级前全量备份；Dreaming/Wiki 旧格式与 pre-schema-8 会话布局可能需要 2026.9.7 Doctor 完整拷贝恢复，否则拒绝升级
- **hooks/hooks.yaml**：10.5 工具参数改写规则收紧 → 若本地有改写型 hook 会直接 block，需迁移
- **openclaw.json**：核对 `tools.sessions.visibility` / `tools.agentToAgent.enabled`，勿留空
- **微信通道**：升级后全链路自检

### 结论（2026-10-19）

🔴 **仍不推荐直接升级；若升级必须走桥接多阶段。**

理由：
1. 跨度仍为历史最大，破坏性集中在**数据层**（记忆 SQLite 索引、cron state、会话 schema）。
2. 10.5 虽修了大量 Windows 更新阻塞与重启续跑问题（对本地有利），但仍为 10-17 前后发布的 fresh release，未过反馈期。
3. 10.5 新增一条 hooks 破坏性变更，本地 hook 需适配。
4. 本地重度依赖 cron + 全记忆体系，静默失活代价高。
5. 连续 10 次评估用户均未回应，不建议在无人工窗口时动数据层。

**若长官批准升级（需预留 1–2 小时 + 人工在场）：**
1. 备份：`openclaw.json`、SOUL/MEMORY/USER、整个 `memory/`、`hooks/`、workspace git commit
2. `openclaw gateway stop`
3. 装 **2026.9.5** → `openclaw --version` 确认 → `openclaw doctor --fix`（解决 import 冲突再继续）
4. 装 **2026.9.7** → `openclaw doctor --fix`（cron JSON→SQLite、HEARTBEAT、记忆索引）
5. 装 **2026.10.5** → `openclaw doctor --fix`
6. 核对 `openclaw.json` 工具 visibility / agentToAgent；hooks 参数改写策略
7. 逐项触发验证 6 个 cron（查静默失活）+ 记忆检索
8. 微信通道全链路自检
9. 观察 3–5 天再恢复常规节奏

- **状态标记**: 🔴 持续未决（累计 **10 次**评估）

---

## 历史记录（摘要）
- 2026-10-05：latest 2026.9.8 → 首次识别桥接硬约束，不建议升级
- 2026-10-12：latest 2026.10.1 → 维持暂缓；发现 hooks `metadata.clawdbot` 重命名、工具权限默认放开
- 2026-10-19：latest 2026.10.5 → 维持暂缓；新增 tool approval hooks 破坏性变更；更新机制/重启续跑大幅改善
