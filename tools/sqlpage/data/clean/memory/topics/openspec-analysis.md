# OpenSpec 源码架构分析 【已归档】

**归档日期**: 2026-07-21
**原因**: 30天无强化，已从活跃记忆索引移除
**分析日期**: 2026-06-12
**版本**: v1.3.1 (commit a3f7b2c)
**仓库**: github.com/Fission-AI/OpenSpec

---

## 1. 项目概览

OpenSpec 是一个 **Spec-Driven Development (SDD)** 框架，为 AI 编码助手提供规格管理层。
- **语言**: TypeScript (Node.js 20.19+)
- **包管理**: pnpm + changesets
- **测试**: Vitest
- **验证**: Zod schema
- **Stars**: 54k+ | **License**: MIT

## 2. 目录结构

```
OpenSpec/
├── src/
│   ├── cli/              # CLI 入口 (index.ts)
│   ├── commands/         # 命令实现
│   │   ├── workflow/     # 工作流命令 (propose/apply/archive等)
│   │   └── workspace/    # 工作区命令 (setup/link/open等)
│   ├── core/             # 核心逻辑
│   │   ├── artifact-graph/   # 🔑 工件依赖图 (DAG)
│   │   ├── change-metadata/  # 变更元数据
│   │   ├── collections/      # 集合管理 (initiatives)
│   │   ├── command-generation/ # 🔑 命令生成 (30+ AI工具适配器)
│   │   ├── completions/      # Shell补全
│   │   ├── context-store/    # 🔑 上下文存储
│   │   ├── parsers/          # Markdown/Delta解析器
│   │   ├── schemas/          # Zod schema定义
│   │   ├── templates/        # 工作流模板
│   │   ├── validation/       # 🔑 多级验证器
│   │   └── workspace/        # 工作区管理
│   ├── prompts/          # 交互式提示
│   ├── telemetry/        # 遥测
│   ├── ui/               # 终端UI
│   └── utils/            # 工具函数
├── schemas/              # 内置schema定义
│   ├── spec-driven/      # 默认工作流
│   └── workspace-planning/ # 跨区工作流
├── openspec/             # 自举: OpenSpec自身的spec
│   ├── specs/            # 源规格
│   └── changes/          # 变更+归档
└── docs/                 # 文档
```

## 3. 核心架构模式

### 3.1 工件依赖图 (ArtifactGraph)

**文件**: `src/core/artifact-graph/graph.ts`

用 **DAG (有向无环图)** 管理工件依赖，核心算法：

```typescript
class ArtifactGraph {
  // Kahn's algorithm 拓扑排序
  getBuildOrder(): string[]
  // 获取就绪工件 (所有依赖已完成)
  getNextArtifacts(completed: CompletedSet): string[]
  // 检查是否全部完成
  isComplete(completed: CompletedSet): boolean
  // 获取阻塞工件及其未满足依赖
  getBlocked(completed: CompletedSet): BlockedArtifacts
}
```

**Schema 定义** (YAML):
```yaml
name: spec-driven
artifacts:
  - id: proposal
    generates: proposal.md
    requires: []
  - id: specs
    generates: "specs/**/*.md"
    requires: [proposal]
  - id: design
    generates: design.md
    requires: [proposal]
  - id: tasks
    generates: tasks.md
    requires: [specs, design]
apply:
  requires: [tasks]
  tracks: tasks.md
```

**关键设计**:
- Zod schema 验证 YAML 结构
- 拓扑排序确定构建顺序
- 依赖是"使能器"而非"门控"——可跳过不需要的工件
- 完成状态通过文件系统检测（文件是否存在）

### 3.2 Delta Spec (增量规格)

**文件**: `src/core/parsers/requirement-blocks.ts`

**核心思想**: 描述"变化什么"而非重述整个规格。四种操作：

| 操作 | 含义 | 归档时效果 |
|------|------|-----------|
| `## ADDED Requirements` | 新行为 | 追加到主规格 |
| `## MODIFIED Requirements` | 变更行为 | 替换现有需求 |
| `## REMOVED Requirements` | 废弃行为 | 从主规格删除 |
| `## RENAMED Requirements` | 重命名 | 更新名称 |

**格式规范**:
```markdown
## ADDED Requirements

### Requirement: Two-Factor Auth
The system MUST support TOTP-based 2FA.

#### Scenario: 2FA enrollment
- GIVEN a user without 2FA
- WHEN the user enables 2FA
- THEN a QR code is displayed
```

**关键规则**:
- 每个需求必须有 SHALL/MUST
- 每个需求必须至少一个 Scenario
- Scenario 必须用 `####` (4个#)
- 归档时 delta 合并到 source of truth

### 3.3 Schema 系统

**文件**: `src/core/artifact-graph/schema.ts`, `src/core/artifact-graph/resolver.ts`

Schema 解析顺序：
1. 项目级 `openspec/schemas/` (版本控制)
2. 用户级 `~/.local/share/openspec/schemas/` (跨项目共享)
3. 内置 schemas

Schema 支持 fork：
```bash
openspec schema fork spec-driven my-workflow
```

### 3.4 命令生成 (Adapter 模式)

**文件**: `src/core/command-generation/`

**30+ AI 工具适配器**：
```
amazon-q, antigravity, auggie, bob, claude, cline, codex,
continue, costrict, crush, cursor, factory, gemini,
github-copilot, iflow, junie, kilocode, kiro, lingma,
opencode, pi, qoder, qwen, roocode, windsurf...
```

每个适配器实现 `ToolCommandAdapter` 接口：
```typescript
interface ToolCommandAdapter {
  getFilePath(commandId: string): string;
  formatFile(content: CommandContent): string;
}
```

### 3.5 上下文存储 (Context Store)

**文件**: `src/core/context-store/foundation.ts`

- **Registry**: 全局注册表，管理多个 context store
- **Metadata**: 每个 store 的元数据 (version, id)
- **Backend**: 目前仅 Git backend
- **Lock**: 文件锁机制防并发写入
- **原子写入**: tmpfile + rename 模式

### 3.6 工作区协调 (Workspace)

**文件**: `src/core/workspace/foundation.ts`

多仓库协调的"本地视图"模型：
```
workspace     = 私有本地视图
context store = 持久共享上下文容器
initiative    = 上下文 store 中的协调上下文
link          = 仓库/文件夹的稳定名称
change        = 一个计划中的工作单元
```

### 3.7 验证管线

**文件**: `src/core/validation/validator.ts`

三级验证：
1. **Spec 验证**: 结构、Purpose 长度、需求格式
2. **Change 验证**: Delta 描述长度、需求存在性
3. **Delta Spec 验证**: SHALL/MUST、Scenario、跨段冲突

### 3.8 归档流程

**文件**: `src/core/archive.ts`

```
归档前:
openspec/specs/auth/spec.md ←──┐
openspec/changes/add-2fa/     │ merge
  ├── proposal.md              │
  ├── design.md                │
  ├── tasks.md                 │
  └── specs/auth/spec.md ──────┘

归档后:
openspec/specs/auth/spec.md (已合并2FA)
openspec/changes/archive/2025-01-24-add-2fa/ (完整保留)
```

## 4. 设计亮点

| 亮点 | 说明 |
|------|------|
| **Brownfield-first** | Delta spec 优先修改现有系统 |
| **Fluid, not rigid** | 无严格阶段门控，工件可按需创建 |
| **Self-contained changes** | 每个变更自包含一个文件夹 |
| **Schema 可定制** | Fork/创建自定义工作流 |
| **Source of truth** | specs/ 是行为真相源 |
| **验证前置** | 归档前强制验证 |
| **适配器模式** | 30+ AI 工具统一接口 |
| **原子操作** | 文件锁+原子写入防损坏 |

## 5. 不足/风险

| 问题 | 说明 |
|------|------|
| **400 open issues** | 社区活跃但问题多 |
| **全局安装** | `npm install -g` 对多项目不友好 |
| **仅 Node.js** | 不支持 Python/Rust 等生态 |
| **Git-only context store** | 后端单一 |
| **TypeScript 耦合** | 核心逻辑与 TS 生态深度绑定 |
| **新项目** | <1年历史，API 可能变化 |
