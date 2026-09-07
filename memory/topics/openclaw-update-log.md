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

---

## 复查 2026-08-28 10:38

- **当前版本**: 仍 2026.6.10 (aa69b12)
- **latest stable**: 仍 2026.7.1-2（自 8-10 复查以来无新稳定版发布）
- **预发布**: 2026.7.2-beta.x 继续推进（未稳定），仍可作为后续更稳升级目标
- **上次评估未决**: 是（7-20 / 8-03 / 8-10 三次评估均未执行升级，用户未回应）
- **本次变化**: 无新稳定版本、无新 breaking change/回归报告信号 → 结论与风险评估维持 8-10 不变。
- **状态标记**: ⚠️ 持续未决 + 维持**暂缓**（等 7.2 稳定或社区反馈趋稳后再升）

---

## 复查 2026-08-31 11:05

- **当前版本**: 仍 2026.6.10 (aa69b12)
- **latest stable**: **2026.8.1**（新稳定版，beta.2 发布于 8-15，现正式 stable）
- **版本差**: 6.10 → 8.1（跨越两个 release-line，含 7.x 全部 breaking changes）
- **上次评估未决**: 是（7-20 / 8-03 / 8-10 / 8-28 四次评估均未执行升级，用户未回应）

### 2026.8.1 主要变更（新增，相对上次复查）

| 领域 | 变更 | 风险 |
|------|------|------|
| **记忆系统** | 🔴 大改：fast active-memory recall、personal installs 默认 cross-conversation recall、Claude Code/Codex/Hermes 引导导入、Memory 设置页 (#108043/#110597/#108977/#114037)；Active Memory 落地（lowercase `memory.md` 已废弃，2026.4.10 起） | 🔴 高（记忆检索行为变化 + memory.md 演进，本地 MEMORY.md 需确认） |
| **Workspace 布局** | 🟡 HEARTBEAT.md 移入 SQLite-backed monitor scratch（revision-safe cron scratch，需用 Doctor 而非手工迁移） | 🟡 中（本地 HEARTBEAT.md/workspace 布局相关） |
| **Cron 任务** | 🔴 大改：auto-disable repeated failures、DST fold/时区历史 on-time scheduling、zoned cron times、cron-backed heartbeat monitors、heartbeat↔task 转换、`/loop`、per-job dynamic cadence、gated script payloads | 🔴 高（本地依赖 6 个 cron，行为与去重/失败语义变化） |
| **Skill Workshop** | 🟡 skill/system 持续演进（release 层面有迭代；注意 SKILL.md version 头要求） | 🟡 中 |
| **Config Schema** | 🔴 结转 7.x breaking：messaging-only 工具 profile 默认、ACP dispatch 默认开、plugin HTTP handler 改显式 route API | 🟡 中–高 |
| **工具系统** | 🟡 plugin HTTP handler route API | 🟡 中 |
| **安全** | 🟢 Secret egress host binding、release validation 加固、SQLite snapshot backup/restore、reliability 加固 (#99067/#100910/#102125/#109590/#112406) | 🟢 正面 |
| **Channel** | 微信/飞书/企微未在 highlight；7.x 有 Feishu outbound 修复 | 🟡 中（本地微信通道需自检） |
| **文档明确升级要点** | 备份 SOUL.md/MEMORY.md/USER.md/config；升级后重启 gateway，逐个验证 cron jobs 是否静默失活（社区高频踩坑） | — |

### 本地具体影响
- `memory/evolution/`、MEMORY.md：Active Memory 演进 + cross-conversation recall 新行为 — 升级后需验证记忆检索结果与原有 MEMORY.md 兼容。
- `cron 6 个任务`：auto-disable 失败重试 + DST 语义变化 — 升级后必须逐个验证触发；已有 7.x 社区回归报告。
- `HEARTBEAT.md`：若升级，用 `openclaw doctor` 处理迁移，勿手工搬。
- 工具 profile / ACP dispatch：需核对本地 `openclaw.json` 是否受影响（可能收窄工具权限）。
- 升级方式：Node 版本提升（7.x 起），非简单 `npm update -g`，需重跑 web installer + 备份。

### 升级建议（2026-08-31 更新）

**🟡 建议：等几天看反馈（暂缓，维持）**

理由：
1. 版本跨度大（6.10 → 8.1），叠加 7.x breaking changes（工具 profile/ACP/plugin route）+ 8.1 记忆与 cron 大改，本地重度依赖 cron 与记忆系统，一次性跨越风险最高。
2. 2026.8.1 为全新 stable，社区反馈期刚开始；建议观察 2 周。
3. 升级路径复杂（Node 提升需 web installer + 备份 + Doctor 迁移 HEARTBEAT.md），不宜无准备执行。
4. 记忆系统 Active Memory 演进需先确认 lowercase memory.md 情况、并核对 MEMORY.md 兼容性。

**若坚持升**：备份 SOUL/MEMORY/USER/config → 重跑 web installer → `openclaw doctor` → 逐个验证 cron（重点查静默失活）与记忆检索 → 全链路自检微信通道 → 无异常再启用。

- **状态标记**: 🔴 持续未决（累计 5 次评估）+ 因版本跨度大维持**暂缓**；同时记录 2026.8.1 需重点自检 cron/记忆两项。

---

## 复查 2026-09-07 16:38

- **当前版本**: 仍 2026.6.10 (aa69b12)
- **latest stable**: **2026.9.2**（新发布，2026-09-05 出版）
- **版本差**: 6.10 → 9.2（跨越 7.x/8.x/9.x 三条 release-line，含全部累计 breaking changes；为历史最大跨度）
- **上次评估未决**: 是（7-20 / 8-03 / 8-10 / 8-28 / 8-31 五次评估均未执行升级，用户持续未回应）

### 2026.8.x → 2026.9.2 新增主要变更

| 领域 | 变更 | 风险 |
|------|------|------|
| **记忆系统** | 8.x-9.x 延续 **Database-first（SQLite）重构**：per-agent `openclaw-agent.sqlite` 承载 sessions/transcripts/memory indexes/embedding；daily memory 跨 session 连续性、rotated-session 上下文保留、减少重复 search/index 工作；新增磁盘占用可视化 | 🔴 高（记忆检索/embedding/SQLite schema 全面重写 + doctor 迁移） |
| **Cron 任务** | **state 迁移到 SQLite**：`cron_jobs` 从 75 列精简到 15 列、subagent_runs 59→6 列（schema 12→13，canonical JSON 重排）；旧 `~/.openclaw/cron/jobs.json`/`jobs-state.json`/`jobs-quarantine.json`/`runs/*.jsonl` 需 `openclaw doctor --fix` 导入并归档 `.migrated`；`cron.store` 已退役；repeated-failures auto-disable；失败/交付/DST 语义强化 | 🔴 高（本地 6 个 cron，迁移必须走 doctor，禁手工搬） |
| **HEARTBEAT.md** | 已移入 SQLite-backed monitor scratch（revision-safe），需用 Doctor 迁移 | 🟡 中（本地 HEARTBEAT.md 逻辑相关） |
| **工具/权限** | 结转 7.x breaking：messaging-only profile 默认、ACP dispatch 默认开、plugin HTTP handler 改显式 route；9.2 新增 `tools.sessions.visibility` 由 `agent`→`all`、`tools.agentToAgent.enabled` `false`→`true` **为默认省略值**（未显式设置将放开跨 agent 会话访问——需核对本地 openclaw.json） | 🟡 中–高 |
| **可靠性** | Gateway restart 恢复、config watcher handoff、worker recovery、SQLite snapshot backup/restore 加固 | 🟢 正面 |
| **Channel** | 微信/飞书/企微未在 highlight；历史有 Feishu outbound 修复 | 🟡 中（本地微信通道需自检） |
| **Skill Workshop** | 延续演进，无破坏性暴雷 | 🟢 低–🟡 中 |

### 🔴 关键风险信号（2026.9.2 为全新 release）
- 2026-09-05 刚发布，**fresh release**，社区仍在反馈期。
- 第三方升级追踪（clawstat.us）点名 **56 个 issue 指向 2026.9.2 本版**，含**无 staged-fix 的数据丢失/数据搁浅级 critical bug**（doctor --session-sqlite import 丢 codex provider 消息、llama.cpp embedding ubatch 回归、reply-run 期间消息被丢等）。即便其具体主张需谨慎对待，**“back up before you update”“等几天下场只会更硬”**的大方向与多次社区踩坑一致。

### 本地具体影响（相对本地 6.10）
- **cron**（memory-*/security-check/daily-social + task-heartbeat）：升级后必须跑 `openclaw doctor --fix` 迁移到 SQLite；auto-disable 失败语义改变 → 逐个验证是否触发、有无静默失活。
- **记忆系统**：本地 `MEMORY.md`/`memory/*.md`/`memory/evolution/` 将面对 Active Memory + SQLite index + embedding + cross-conversation recall 新行为；升级后需核对检索结果与记忆完整性，先备份 memory/。
- **HEARTBEAT.md / workspace 布局**：SQLite-backed，需 Doctor 迁移，勿手工搬。
- **工具/权限**：需核对本地 `openclaw.json` 是否显式设置了 `tools.sessions.visibility` / `tools.agentToAgent.enabled` —— 若留空，升级后跨 agent 权限自动放开。
- **升级路径**：Node 版本早已提升（7.x 起非 `npm update -g`），需重跑 web installer + 备份 config/SOUL/MEMORY/USER。

### 升级建议（2026-09-07 更新）

**🔴 建议：当前不推荐升级（维持暂缓，且因 fresh-release 数据风险进一步下调）**

理由：
1. 版本跨度达**历史最大**（6.10 → 9.2），一次性叠加深记忆 SQLite 重构 + cron state 迁移 + 工具权限默认放开等多项 breaking。
2. **2026.9.2 为全新 release（3 天）**，社区已报告指向本版的数据丢失类 critical bug 与无 staged-fix 状态 —— 我方累计 5 次评估全未执行，无历史包袱催着立刻跳坑。
3. 升级需 Doctor 迁移 cron/HEARTBEAT + 重跑 web installer + 全量备份 + 逐项自检，动作复杂、风险集中在数据层。
4. cron 与记忆是本地运行核心（近 10 个定时任务 + 全记忆体系），任何静默失活/检索回归代价高。

**建议路线**：继续驻留 6.10 稳定运行 → 关注 2026.9.2 后续 hotfix / 9.2.x patch 是否平息数据类 bug → 待社区反馈趋稳后，选一个中间稳定版（如 8.x/9.x 成熟 patch）做**一次性大跳迁移**，迁移前完整备份并预留自检窗口。

**若坚持升**：1) `openclaw.json` + SOUL/MEMORY/USER + `memory/` 全备份 → 2) 重跑 web installer（勿用 `npm update -g`）→ 3) `openclaw doctor --fix` 迁 cron/HEARTBEAT/记忆 → 4) 核对 openclaw.json 工具 visibility 字段 → 5) 逐个验证 cron 触发（查静默失活）与记忆检索 → 6) 全链路自检微信通道 → 7) 留观数天确认无数据异常再常态化。

- **状态标记**: 🔴 持续未决（累计 **6 次**评估）+ 因跨度大 & 2026.9.2 fresh-release 数据风险，维持**不推荐升级（暂缓）**。记录重点自检项：cron Doctor 迁移、记忆 SQLite、工具 visibility 默认放开、微信通道。
