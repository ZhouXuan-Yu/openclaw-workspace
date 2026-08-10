# OpenClaw 版本更新评估报告

- **检查时间**: 2026-07-20 10:17 (CST)
- **当前版本**: 2026.6.10 (aa69b12)
- **最新稳定版**: 2026.7.1-2
- **版本差**: 1 个次要版本
- **上次评估未决**: 无（首次评估）

---

## 变更概要（来自 release notes 及社区讨论）

### 主要变更

| 领域 | 变更内容 | 风险评估 |
|------|----------|----------|
| **记忆系统** | release notes 有 "Memory and conversations" 章节，但无架构级 breaking change 信号（无 SQLite schema 迁移、无 embedding 模型切换的公告） | 🟢 低 |
| **Workspace 布局** | 未提及 workspace 文件布局变更 | 🟢 低 |
| **Hooks 系统** | 未提及 hooks 变更 | 🟢 低 |
| **Cron 任务** | 修复了会话/代理相关稳定性问题，cron 接口无 breaking change | 🟢 低 |
| **Config Schema** | 未提及 openclaw.json 废弃/新增字段 | 🟢 低 |
| **Channel 插件** | Telegram/Slack/Discord/WhatsApp 均有更新，但微信/飞书/企微未在 release highlight 中提及 | 🟡 中（微信通道需关注） |
| **Skill Workshop** | GitHub 提及 PR #93773 "scope Skill Workshop proposals to selected agent" — 功能增强非破坏性 | 🟢 低 |
| **工具系统** | 工具系统无 breaking change 信号 | 🟢 低 |
| **Codex/编码代理** | 有显著改进（BTW routing、harness 更新），但本地未启用 Codex | 🟢 低 |
| **Gateway/稳定性** | 会话续传、崩溃恢复、重连改进 | 🟢 正面 |

### 已知修复（来自 GitHub PR 追踪）
- 会话/代理 compact retries 修复
- Subagent completion announce 修复
- Gateway 空 transcript 修复
- 会话锁 release 修复
- macOS/RPC 适配修复

### Breaking Changes
根据社区帖子（2 天前发布）和 release notes — **无明确 breaking changes 公告**。

---

## 本地影响评估

| 组件 | 本地状态 | 影响 |
|------|----------|------|
| `memory/evolution/` | 自进化引擎 v4/v5 | 记忆系统无 schema 变更 ⬜ |
| `hooks/hooks.yaml` | Hook 增强配置 | hooks 系统不变 ⬜ |
| `cron 任务` | memory-*, security-check, daily-social | cron 接口兼容 ⬜ |
| `workflows/` | 自定义工作流 | 无相关变更 ⬜ |
| `微信通道` | OpenClaw 微信集成 | 未明确更新，需关注 ⬜ |
| `.snapshots/` | SOUL.md/AGENTS.md 快照 | 无影响 ⬜ |
| `openclaw.json` | 调用了 `openclaw config` 可行 | 无 schema 变更 ⬜ |

---

## 升级建议

**🟢 建议：立刻升级**

理由：
1. 版本差仅 1 个次要版本（6.10 → 7.1），非 major 版本
2. 无 breaking changes 公告
3. 包含多项目标稳定性修复（会话续传、崩溃恢复、重连）
4. 社区已发布 2 天，无负面反馈报告
5. 升级命令：`npm update -g openclaw`

**注意**：升级后仍需验证记忆检索、cron 任务、微信通道功能正常。建议升级后进行一次 `openclaw gateway restart` 触发全链路自检。

---

## 复查 2026-08-03 16:36

- **当前版本**: 仍 2026.6.10 (aa69b12)（上次评估后未执行升级，用户未回应）
- **latest stable**: 仍 2026.7.1-2（无新增稳定版）
- **预发布**: 2026.7.2-beta.x 系列在推进（beta.5 / 2026-07-28），含 supervisor external 模式、`openclaw onboard`、clickclack 通道等，但**未稳定**
- **结论**: 上次评估（7-20，建议立刻升级）仍待决。本次无新信息改变结论，升级建议维持不变。
- **状态标记**: ⚠️ 上次评估未决（建议升但用户未执行）

---

## 复查 2026-08-10 11:28

- **当前版本**: 仍 2026.6.10 (aa69b12)
- **latest stable**: 仍 2026.7.1-2（含 2026.7.1-2 热修复：npm 插件更新兼容 singleton-array metadata，官方插件可安装性）
- **上次评估未决**: 是（7-20 / 8-03 两次建议升但用户均未执行）
- **新信号（社区 7-13 发布后反馈）**:
  - ⚠️ **早期用户报告 autoupdate 与 cron 回归** — 官方与社区均建议：生产环境**分阶段(staged)升级**、**先备份 openclaw.json**、若 Node 迁移卡住则重跑 web installer。
  - 🔴 **Breaking changes 确认**：新安装默认 messaging-only 工具 profile；**ACP dispatch 默认开启**；**plugin HTTP handler 注册改为显式 route API**。
  - Node 版本被提升 → 旧版自动更新器可能失效，需重跑 web installer 完成迁移。
  - 变更规模：3,063 contributions / 532 contributors（大版本，含 Control UI 重写、原生移动端大改、GPT-5.6 / Muse Spark 1.1 / Tencent Hy3 路由、Codex delegation 加重）。
  - 预发布 2026.7.2-beta.x 仍在推进，但 8-04 的 beta.1 显示 extended-stable 加固方向（SQLite checkpoints、Feishu outbound 修复等）。

### 更新后的风险评估（2026-08-10）

| 领域 | v2026.6.10 → v2026.7.1 变更 | 风险 |
|------|-------------------------------|------|
| **记忆系统** | 无 schema/embedding/SQLite 迁移公告；6.11 起有 SQLite checkpoints 加固（正面） | 🟢 低 |
| **Workspace 布局** | 无布局变更信号 | 🟢 低 |
| **Hooks 系统** | 未提及 hooks 变更 | 🟢 低 |
| **Cron 任务** | ⚠️ **早期用户报告 cron 回归** | 🔴 高风险（本地依赖 6 个 cron） |
| **Config Schema** | **新增默认 messaging-only 工具 profile；ACP dispatch 默认开** — 可能改变工具权限模型 | 🟡 中 |
| **Channel 插件** | 微信/飞书/企微未在 highlight；6.11 有 Feishu outbound 修复；本地微信通道未明确更新 | 🟡 中 |
| **Skill Workshop** | 无破坏性变更 | 🟢 低 |
| **工具系统** | **plugin HTTP handler 改显式 route API**（若本地装了 HTTP handler 插件需适配）；工具默认 profile 变更 | 🟡 中 |
| **Node 运行时** | **Node 版本提升** — 需重跑 web installer，且旧 autoupdater 失效 | 🟡 中 |

### 本地具体影响
- `memory/evolution/`、`hooks/hooks.yaml`、`workflows/`：无直接 schema 破坏 ⬜
- **cron 6 个任务**（memory-*/security-check/daily-social）：⚠️ 需在升级后逐个验证触发；已有回归报告
- **工具/权限模型**：确认本地 `openclaw.json` 是否受影响（messaging-only profile / ACP dispatch 默认开可能收窄工具权限）
- **微信通道**：升级后必须全链路自检
- **升级动作**：因 Node 提升，升级方式非简单 `npm update -g`，需重跑 web installer + 备份 openclaw.json

### 升级建议（2026-08-10 更新）

**🟡 建议：等几天看反馈（暂缓）**

理由：
1. 与上次“立刻升级”相反 — 新增了 **early-adopter 报告的 cron/autoupdate 回归** 与 **plugin HTTP handler breaking change**，本地重度依赖 cron，风险上升。
2. 变更规模大（532 贡献者 / Control UI 重写），当前仍处社区反馈期。
3. 升级路径复杂化（Node 提升需重跑 web installer + 备份），不宜无准备执行。
4. 可关注 **2026.7.2-beta/extended-stable**（8-04 已显加固方向）转稳定后，作为更稳的升级目标。

**若坚持升**：先 `cp openclaw.json openclaw.json.bak` → 重跑 web installer → `openclaw doctor` 自检 → 逐个验证 cron 与微信通道 → 若无异常再启用。

- **状态标记**: ⚠️ 上次评估未决 + 本次因回归报告下调为**暂缓**（从“立即升”改为“等反馈”）
