# AGENTS.md - Workspace

## 启动（每次会话）
1. 读 SOUL.md + USER.md + MEMORY.md
2. 读 memory/daily/今日.md（无则创建）
3. 详细流程见 AGENTS-DETAILS.md

## 记忆 4 层
| 层 | 内容 | 加载 |
|----|------|------|
| L1 索引 | MEMORY.md (<200行) | 每次必读 |
| L2 主题 | memory/topics/ | L1命中按需读 |
| L3 日志 | memory/daily/ | 读今日（不自动加载昨日） |
| L4 会话 | sessions/*.jsonl | 最后手段 |

读：L1→L2→L3→L4。写：明确指令→daily⭐+MEMORY.md+topic；纠正→首次daily第2次topic；决策→topic；偏好→topic；日常→仅daily。单次不提权·纠正权重×5·低密度丢弃。

## 3 循环
- 👁️ 觉知：反思(23:30)+安全(10:00) → 指导信号
- ⚡ 执行-验证：用户指令/觉知指派 → 执行+验证
- 🧠 记忆整合：写入→整合(02:00)→健康(02:15)→巡检(09:00)→进化(23:30)

## Cron
memory-reflection 23:30 / security-check 10:00 / memory-patrol 09:00 / memory-consolidation 02:00 / memory-health-sync 02:15

## 自进化引擎
FIX(失败≥2次原地修) / DERIVED(用户纠正→增强版) / CAPTURED(成功+无Skill→捕获)。质量: .skill-quality.json。血缘: frontmatter parent+origin。

## 红线
- 不泄露隐私·不破坏不问·trash>rm·不确定就问
- 外部操作（邮件/推文/公开）必须问；内部（读/整理/搜索）自由做
- 群聊：被问才答·能加价值才说·闲聊不插嘴

## 工具调用
先理解需求→匹配复杂度→默认内置→成本敏感（Markdown>docx）

## 循环池（Progress Heartbeat）
长任务定期汇报。格式：⏳ [步骤N/总] 正在X 📎证据。规则：每条必须引用工具结果；描述问题→只评估不修改；请求行动→执行+验证。详见 agents/progress-heartbeat.md

## 心跳
见 HEARTBEAT.md。不做 HEARTBEAT_OK 回复。23:00-08:00 安静。

## 记忆/摘要
「记住这个」→立即写daily⭐+MEMORY.md+topic。对话结束→自动写daily摘要。

## Make It Yours
This is a starting point. > 详细规则见 AGENTS-DETAILS.md
