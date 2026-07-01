# 可吸收项目深度分析 — 进化方案

**日期**: 2026-06-15 02:05
**目标**: 从5个高相关项目中提炼设计模式，优化 OpenClaw 自身

---

## 1. mattpocock/skills — Skill 设计模式吸收

### 核心模式

**模式A: `/grill-me` 对齐会话**
- 用户说"grill me" → Agent 追问每一个设计决策的分支
- 一次问一个问题，每个问题提供推荐答案
- 能从代码库获取答案的，直接探索代码库
- **吸收价值**: 当前 OpenClaw 的 Skill 缺少"对齐"环节，直接执行容易偏

**模式B: `/grill-with-docs` 带文档的对齐**
- 在 grill-me 基础上增加：
  - 术语表维护（CONTEXT.md）— 统一项目语言
  - ADR（Architecture Decision Records）— 记录重要决策
  - 模糊语言纠正："你说的'账户'是指 Customer 还是 User？"
  - 代码交叉验证：用户说的和代码实际是否一致
- **吸收价值**: 可在 AGENTS.md 中增加"对齐协议"

**模式C: 架构改进 Skill**
- **深度分析**: 模块的"深度"概念 — 接口小但实现丰富 = 深模块
- **删除测试**: 删除模块后复杂度是消失还是分散？消失=透传模块，分散=有价值的深模块
- **HTML 报告**: 自动化生成架构审查报告（Tailwind CDN + Mermaid 图表）
- **术语一致性**: 所有建议使用 CONTEXT.md 的领域语言
- **吸收价值**: 进化引擎可增加"架构审查"能力

### 具体吸收方案

1. **新建 `grill-me` Skill** — 在 skills/ 下创建：
   ```
   skills/grill-me/SKILL.md
   ```
   - 当用户说"grill me"、"对齐"、"压力测试"时触发
   - 追问设计决策，一次一个问题
   - 能从文件/记忆获取答案的不问用户

2. **CONTEXT.md 术语表** — 在 workspace 根目录创建：
   ```
   CONTEXT.md — 项目术语表
   ```
   - 统一 OpenClaw 内部术语（Skill、Memory、Evolution、Agent 等）
   - 纠正模糊语言

3. **ADR 目录** — 记录重要架构决策：
   ```
   docs/adr/0001-memory-4-layer-architecture.md
   docs/adr/0002-evolution-engine-design.md
   ```

---

## 2. rohitg00/agentmemory — 记忆架构吸收

### 核心模式

**模式D: 三层引擎架构**
- Worker: 执行具体任务的函数
- Function: 通过 `registerFunction` 注册
- Trigger: 通过 `registerTrigger` 注册（HTTP/WebSocket/Cron）
- **关键约束**: 所有操作通过 iii-engine 的 `sdk.trigger()`，不绕过

**模式E: Hook 系统**
- 12 个生命周期钩子：pre-tool-use, pre-compact, session-start, stop, session-end 等
- **Context-injecting hooks**（写 stdout 给 Agent 注入上下文）：pre-tool-use, pre-compact, session-start
- **Telemetry-only hooks**（fire-and-forget）：其余所有
- 关键模式：`try/catch + AbortSignal.timeout(N)` 防挂起
- `setTimeout(() => process.exit(0), 500).unref()` 硫 Node 不阻塞
- **吸收价值**: OpenClaw 已有 hooks/ 目录，但缺少 pre-tool-use 和 pre-compact

**模式F: 混合检索**
- BM25 关键词搜索 + 本地嵌入向量搜索
- 零 LLM 模式下也能语义检索
- **吸收价值**: OpenClaw 的 memory_search 可参考其混合策略

**模式G: 一致性规则（最重要）**
- 添加/删除 MCP 工具时必须同步更新 8 个文件
- 添加 REST 端点时必须同步 3 个文件
- 版本更新时必须同步 6 个文件
- **吸收价值**: 进化引擎的"变更影响分析"可借鉴此模式

### 具体吸收方案

1. **增强 hooks 系统** — 在 `hooks/` 下补充：
   ```
   hooks/pre-tool-use.md — 工具调用前注入上下文
   hooks/pre-compact.md — 压缩前注入关键记忆
   hooks/session-start.md — 会话开始注入今日日志
   ```

2. **记忆检索增强** — 在 evolution 引擎中增加：
   - 关键词搜索 + 语义搜索的混合策略
   - 检索结果排序：相关度 × 时间衰减 × 来源权重

3. **变更影响清单** — 在 evolution 引擎中：
   - 修改 Skill 时自动列出需要同步的文件
   - 修改 Memory 架构时自动检查一致性

---

## 3. anthropics/financial-services — 行业插件组织范式

### 核心模式

**模式H: Agent 插件自包含**
- 每个 Agent 插件自带所有 Skills，安装即用
- 不依赖外部 Skill 库
- **吸收价值**: OpenClaw Skill 应该是自包含的

**模式I: 垂直+水平分离**
- **垂直插件**: 按行业分（金融、医疗、法律）
- **水平插件**: 按功能分（研究、写作、审查）
- **吸收价值**: OpenClaw 的 Skill 可以分为 `domain/` 和 `function/` 两类

**模式J: Managed Agents API**
- 同一套 Skill 既可作为 Cowork 插件，也可通过 API 部署
- **吸收价值**: OpenClaw 的 Skill 应该支持多种调用方式（CLI/Skill/API）

### 具体吸收方案

1. **Skill 分类重构** — 按功能域重新组织：
   ```
   skills/
   ├── domain/          # 垂直领域
   │   ├── content-production/
   │   ├── research/
   │   └── dev-tools/
   └── function/        # 水平功能
       ├── grill-me/
       ├── daily-report/
       └── evolution/
   ```

2. **自包含规则** — 每个 Skill 必须包含：
   - SKILL.md（核心指令）
   - assets/（模板/样式）
   - examples/（few-shot 示例）
   - 不依赖外部路径

---

## 4. CodeGraphContext — 代码知识图谱

### 核心模式

**模式K: 本地代码索引**
- 把代码仓库索引成可查询的"知识图谱"
- Agent 查图谱找调用链，而不是盲目扫文件
- 大幅减少 Token 消耗
- 100% 本地运行，源码不出机器
- **吸收价值**: 可作为 MCP Server 集成

### 具体吸收方案

1. **评估集成** — 未来可考虑将 CGC 作为 MCP Server 集成到 OpenClaw
2. **当前替代**: 利用 memory_search + topics/ 做项目知识索引

---

## 5. MoneyPrinterTurbo — 短视频 pipeline 对比

### 对比分析

| 环节 | MoneyPrinterTurbo | 我们的方案 |
|------|-------------------|-----------|
| 脚本 | LLM 生成 | 手动/guizang |
| 配音 | 多 TTS 引擎 | edge-tts (YunyangNeural) |
| 字幕 | 自动生成 SRT | 文稿+TTS时长分割 |
| 素材 | 全网抓取 | guizang 社交卡片 |
| 合成 | MoviePy | FFmpeg |
| 界面 | Web UI | CLI |

### 吸收价值
- **多 TTS 引擎支持**: 可以支持更多 TTS 方案
- **素材库**: 积累卡片模板，形成素材库
- **Web UI**: 未来可考虑增加 Web 界面

---

## 立即可执行的进化

### Priority 1: grill-me Skill
创建 `skills/grill-me/SKILL.md`，实现设计对齐协议

### Priority 2: CONTEXT.md 术语表
统一 OpenClaw 内部术语

### Priority 3: ADR 目录
记录已有的重要架构决策

### Priority 4: Hook 增强
补充 pre-tool-use / pre-compact / session-start 钩子

### Priority 5: 变更影响清单
在 evolution 引擎中增加一致性检查
