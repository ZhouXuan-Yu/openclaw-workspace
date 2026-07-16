# 工具使用发现

> 最后更新:2026-07-16

---

## 架构组件（v3, 2026-06-25）

| 组件 | 位置 | 用途 |
|------|------|------|
| 惰性检测器 | `hooks/laziness-detectors.yaml` | 7 种实时检测: brute_retry / idle_tool / busy_loop / premature_done / blame_shift / passive_wait / same_file_edit |
| 长任务循环 | `hooks/task-loop.md` | RECEIVE→ALIGN→SLICE→EXECUTE→VERIFY→REPORT，自动切片+检查点+汇报 |
| hooks 配置 v3 | `hooks/hooks.yaml` | 集成惰性检测器 + task_loop 配置段 |
| RuleMaturity | `RULES.md` | shadow→proposed→enforced 三阶段渐进式规则演进 |

---

## OpenClaw 工具

| 工具 | 发现 | 日期 |
|------|------|------|
| session-logs skill | rg + jq 搜 JSONL,支持时间范围过滤 | 2026-06-11 |
| memory_search | 语义搜索 memory/*.md,但不能搜 sessions | 2026-06-11 |
| memory_get | 按路径+行号读文件,有 corpus 参数 | 2026-06-11 |
| search-memory.ps1 | 全文 grep,精确匹配,跨 memory/ + Obsidian vault | 2026-06-11 |

## 外部工具

| 工具 | 发现 | 日期 |
|------|------|------|
| Obsidian | 个人知识库,Vault 在 E:\Obsidian仓库\ZhouXuan私人领域 | 2026-06-11 |
| EasyOCR | 本地 OCR,不依赖云端 API | 2026-06-11 |
| SkillSpector | NVIDIA Skill 安全扫描器 | 2026-06-12 |
| social-auto-upload | 多平台发布 CLI | 2026-06-12 |
| Wechatsync | 文章同步工具 | 2026-06-12 |
| cover-gen.py | 本地配图生成(Pillow) | 2026-06-12 |
| tracker.py | 发布数据追踪 | 2026-06-12 |
| YouNavi CLI | 对话分析/深度研究/音频转写 | 2026-06-12 |
| Agent Reach | 全网搜索+多平台内容采集（Skill: agent-reach） | 2026-07-16 |
| Codex CLI | AI生图（有独立API凭证，OpenAI gpt-5.5） | 2026-07-16 |

---

## ⚠️ GitHub 每日推送规则（2026-07-07 用户指令）

**规则**: 每次修改工作区文件后必须立即 git push，不攒批。优先级最高。

```powershell
cd C:\Users\ZhouXuan\.openclaw\workspace
git add -A
git commit -m "类型: 描述"
git push
```

**新增 cron 任务**:
| 任务 | 时间 | 功能 |
|------|------|------|
| github-trends-daily | 每日 16:00 | GitHub 趋势推送 → WeChat |
| github-trends-weekly | 周日 16:30 | 周度趋势报告 → Obsidian + WeChat 摘要 |

---

## ⚠️ 图片处理工作流(必须记住)

**收到图片时,必须走这条链路,不要依赖云端 API:**

```
收到图片 → 保存本地 → EasyOCR 提取文字 → 模型推理分析 → 回复用户
```

**为什么不用云端 API:**
- OpenAI API 额度用尽(429 错误)
- Claude API 无图片权限(403 错误)
- 本地 OCR 无限制,更可靠

**OCR 命令:**
```bash
python C:\Users\ZhouXuan\.openclaw\workspace\scripts\ocr.py <图片路径>
```

**工作流步骤:**
1. 保存图片到本地临时文件
2. 调用 OCR 脚本识别文字
3. 结合上下文分析识别结果
4. 回复用户

**适用场景:**
- 截图识别
- 文档照片
- 图片中的文字提取
- 界面截图分析

---

## ⚠️ 小红书/快手内容格式(必须记住)

**发布到小红书/快手时,禁止使用 Markdown 格式:**

❌ 错误写法:
- `---`(分隔线)
- `## 标题`
- `**加粗**`
- `*列表*`

✅ 正确写法:
- 短句分段(每段 1-2 行)
- emoji 开头增加视觉吸引力
- 空行分隔不同段落
- 口语化,像朋友聊天
- 数字用 1️⃣2️⃣3️⃣

**原因:** 小红书/快手文本框不支持 Markdown,格式符会被当成普通文本显示。

---

## ⚠️ 小红书防封 — 草稿模式（2026-06-14）

**问题**：小红书检测到 AI 托管代发，触发封禁（2026年3月新规）
**方案**：`save_as_draft` 草稿模式 — 自动上传素材，人工手动发布+声明 AI 内容

```powershell
sau xiaohongshu upload-note --account creator --images img1.png --title "标题" --note "正文" --draft
```

**规则**：
- 小红书默认用 `--draft`，不用自动发布
- 其他平台（抖音/B站/快手/视频号）仍可自动发布
- 草稿箱手动发布时需声明 AI 内容

---

## ⚠️ guizang-social-card-skill（核心链路）

**地位**：内容生产的核心 Skill，不是可选工具。

**正确链路**：
- 图文：Codex → **guizang-social-card** → Playwright → PNG
- 视频：Codex → **guizang-social-card** → HyperFrames → MP4

**教训**：不要凭记忆推断用户说过什么，不确定就老实说不知道。

---

## 社交内容生产完整链路（2026-07-16 v5 — 自进化版本）

**新增环节**：Q2.5 ComfyUI 精修（可选，使用 skills/comfyui-skill/SKILL.md）

**前置检查（每次必做）**：
1. 读 memory/topics/work-tools.md（本文）
2. 读 skills/guizang-social-card/SKILL.md
3. 读 skills/hyperframes-video/SKILL.md
4. 如果使用 Agent Reach：读 ~/.agents/skills/agent-reach/SKILL.md
   **Windows 特殊处理**: PowerShell 下 `curl` 是别名，必须用 `curl.exe`；
   Python Scripts 目录在 `$env:USERPROFILE\AppData\Roaming\Python\Python314\Scripts`
5. 如果使用 ComfyUI：读 skills/comfyui-skill/SKILL.md，先检查 server status
6. memory_search 确认历史教训
7. **健康检查**: 加载 `memory/evolution/pipeline-health.json`（自进化路由表）

**完整流程**：
```
Q0: 内容来源（双通道）
├── Track A: Agent Reach 社会监听（热点/舆情/大众讨论）
│   ├── Skill: agent-reach（~/.agents/skills/agent-reach/SKILL.md）
│   ├── 用法: 先 `agent-reach doctor --json` 检查可用后端
│   ├── 场景: 小红书搜话题、推特看讨论、B站找评测、Reddit看海外反应
│   ├── 产出: 互联网实时讨论/热度/大众情绪
│   ├── 参考: references/social.md（小红书/推特/B站/V2EX/Reddit）
│   └── 参考: references/search.md（Exa 网页搜索）
├── Track B: YouNavi 深度研究（行业/竞品/专业洞察）
│   ├── 用法: yn.research_full("主题")
│   └── 产出: 结构化深度报告
├── 交叉验证: Track A 完成 → 搜一遍互联网确认选题新颖性
└── 选题提案: 双通道结果汇总 → 你定选题 → 进入Q1

Q1: 图片素材生成（必须步骤）
├── 工具: Codex CLI（首选，有独立API凭证）或 ComfyUI（备选本地）或 image_generate（最后手段）
│   ├── 首选: codex exec "只用image_generate生成一张[描述]" → 从 ~/.codex/generated_images/ 取图
│   │   └── Codex CLI 的 OpenAI 额度独立于当前模型，通常可用
│   ├── 备选: ComfyDesktop已运行 → comfyui-skill --json run <id>
│   ├── 兜底: Swiss纯排版（无配图，靠文字+几何元素）
│   └── 注意: image_generate（OpenAI API）余额不足时不可用；Pexels/Unsplash 网络可能403
├── Swiss模式: 产品渲染/UI截图/keyshot风格 → AI生成
├── Editorial模式: Pexels/Unsplash/Flickr CC → web找图
├── 输出: 每张卡片的 hero image → assets/
└── 记录: assets/SOURCES.md 记录图片来源

Q2: 卡片设计
├── Skill: guizang-social-card
├── 风格: Swiss International (ikb 蓝)
├── 模板: assets/template-swiss-card.html
├── 渲染: Playwright → PNG (图文) / HyperFrames → MP4 (视频)
└── 输出: 1080x1920 竖版

Q2.5: ComfyUI 精修（v4 新增，可选）
├── 用途: 对Q2输出的图片/视频做画质增强、风格迁移、细节优化
├── 前提: ComfyDesktop已本地运行
├── 检查: comfyui-skill --json server status
├── 生图: comfyui-skill --json list → submit + status → 获取增强后的图片
├── 补充说明: 如果ComfyDesktop未运行则跳过此环节，使用Q2原图
└── 注意: 首次使用需先 cd skills/comfyui-skill && 配置config.json

Q3: TTS 配音
├── 工具: edge-tts
├── 语音: zh-CN-YunxiNeural (男声)
└── 输出: MP3

Q4: 字幕
├── 方案: 文稿 → 按句分割 → 算时间戳 → SRT
├── 样式: FontSize=10, 黑字+半透明浅灰底条, MarginV=80
├── 烧录: FFmpeg subtitles + force_style
└── 决策: 白底卡片用黑字（不是白字，白底上看不见）

Q5: 视频合成
├── 路径A: HyperFrames 动画 → npx hyperframes render → MP4
├── 路径B: 静态帧拼接 → FFmpeg concat → MP4
├── 合并: FFmpeg -i video -i audio -vf subtitles → final.mp4
└── 注意: GSAP 不能在 clip 元素上设 visibility（HyperFrames 限制）

Q6: 发布
├── 工具: sau CLI (.venv/Scripts/python.exe sau_cli.py)
├── 小红书: --draft 草稿模式（AI声明）
├── 抖音/快手/B站: 自动发布
├── 公众号/知乎/掘金: Wechatsync
├── 发布前: sau <platform> check 验证登录状态
└── 发布后 → Q7

Q7: 发布后追踪（Agent Reach）
├── 工具: Agent Reach 监测各平台发文后的讨论/反馈
├── 场景:
│   ├── 小红书/推特/B站 搜相关关键词 → 看讨论趋势
│   ├── Reddit 搜海外反应
│   └── Exa 网页搜索覆盖全网的转发/引用
├── 产出: 反馈简报 → 写回 daily log
└── 参考: Q0 Track A 的引用方式，复用 agent-reach

### Q7 自进化闭环（v5 新增）
├── 记录: 每次执行结果 → tool成功/失败 → 写入 pipeline-health.json
├── 读取: 每次 Q0 开始前→读 pipeline-health.json→跳过已知失败的后端
├── 学习: 连续 3 次失败→标记后端为 bad→自动切换主后端
├── 恢复: 连续 3 次成功→提升该后端优先级
└── 告警: 某平台所有后端都 bad→主动提醒用户

### 自进化路由表文件

位置: `memory/evolution/pipeline-health.json`

```json
{
  "platforms": {
    "bilibili": {
      "backends": [
        {
          "name": "B站搜索API",
          "status": "fail",
          "last_ok": null,
          "last_fail": "2026-07-16T14:20:00",
          "fail_reason": "CDN拦截，空响应",
          "fail_count": 3
        },
        {
          "name": "bili-cli",
          "status": "ok",
          "last_ok": "2026-07-16T14:25:00",
          "last_fail": null,
          "fail_count": 0
        }
      ],
      "active_backend": "bili-cli",
      "learned_at": "2026-07-16T14:25:00"
    }
  },
  "version": 1
}
```
```

### 自进化健康管理脚本

位置: `scripts/pipeline-health.py`

```powershell
# 查看当前链路健康状态
python scripts/pipeline-health.py status

# 重新测试所有平台并自动更新路由
python scripts/pipeline-health.py learn

# 完整报告
python scripts/pipeline-health.py report
```

**每次使用链路前必做**：
1. 读 `memory/evolution/pipeline-health.json` — 看哪些后端已知失败
2. 如果有新增的失败或恢复 → 跑 `python scripts/pipeline-health.py learn`
3. 开始 Q0 双通道调研

**HyperFrames 注意事项**：
- GSAP 不能在 clip 元素上设 visibility/display（用 CSS opacity:0 代替）
- Google Fonts 需本地化（@font-face + .woff2），否则离线渲染失败
- Noto Sans SC 需要 @font-face 声明
- 入口文件必须是 index.html

**sau CLI 路径**：
```powershell
$py = "tools/social-auto-upload/.venv/Scripts/python.exe"
$sau = "tools/social-auto-upload/sau_cli.py"
& $py $sau <command>
```

**决策树位置**: `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\社交自动化决策树.md`

---

## YouNavi CLI（必须记住路径）

**固定调用路径：**
```powershell
$cli = "D:\YouNavi\resources\backend\agent-cli.exe"
& $cli <command>
```

**推荐用法：Python 桥梁（解决 GBK 编码问题）**
```python
import sys
sys.path.insert(0, r"C:\Users\ZhouXuan\.openclaw\workspace\tools")
from younavi_bridge import YouNavi
yn = YouNavi()

# 深度研究
r = yn.research_full("主题")  # 完整流程：启动→等待→报告
r = yn.research_plan_only("主题")  # 仅生成计划
r = yn.research_start("主题")  # 异步启动

# 会议同步
r = yn.sync_meetings()  # 同步所有渠道（腾讯会议/飞书妙记/钉钉闪记/Plaud）

# 音频转写
r = yn.audio_transcribe("音频.mp3")

# 记忆/笔记/任务
r = yn.memory_list()
yn.memory_append("全局记忆文件.txt", "新内容")
yn.notes_create("标题", "内容")
r = yn.task_list()

# 每日简报
r = yn.daily_briefing()
```

**核心命令：**
| 命令 | 功能 |
|------|------|
| `research_full("主题")` | 深度研究（完整流程） |
| `research_plan_only("主题")` | 生成研究计划 |
| `research_start("主题")` | 启动异步研究 |
| `audio_transcribe(文件)` | 音频转文字 |
| `sync_meetings()` | 同步所有会议渠道 |
| `channel_sync(渠道)` | 同步指定渠道 |
| `memory_list/get/update/append` | 记忆管理 |
| `notes_list/show/create` | 笔记管理 |
| `task_list/show/report/cancel` | 任务管理 |
| `daily_briefing()` | 每日简报 |

**支持的会议渠道：**
| 渠道 | 说明 |
|------|------|
| `tencent_meeting` | 腾讯会议 |
| `feishu_miaoji` | 飞书妙记 |
| `dingding_shanji` | 钉钉闪记 |
| `plaud` | Plaud |
| `plaudcn` | Plaud CN |

**注意事项：**
- 首次调用自动启动后台服务（Agent Manager + API Server），需等 5-10 秒
- 遇到“服务启动超时”先 `serve start`
- 数据目录: `C:\Users\ZhouXuan\navi-ai\`
- 生成产物: `C:\Users\ZhouXuan\navi-ai\generated_artifacts\`
- OpenClaw Skill: `skills/younavi-integration/SKILL.md`
- 详细文档: `E:\Obsidian仓库\ZhouXuan私人领域\开发项目\YouNavi-CLI使用手册.md`

**已知限制：**
- `channel sync --all` 在 JSON 模式下不可用（需手动在客户端触发）
- `research start` 只生成计划，`research execute` 才执行研究
- 服务启动超时（agent_manager + api_server 启动后 30s 内未就绪），需先启动 YouNavi.exe 主应用
- GBK 编码问题可通过 Python bridge 绕过
- ⚠️ 2026-06-27起持续不稳定（至07-01连续5天失败）：CLI 服务频繁启动超时，agent_manager/api_server 无日志写入，可能依赖/端口/配置问题。Fallback: SQLite 直读数据库 + web_search/web_fetch 替代

**Cron 自动化：**
| 任务 | 时间 | 功能 |
|------|------|------|
| younavi-meeting-sync | 09:00/18:00 | 同步会议渠道并生成摘要 |
| younavi-weekly-research | 周一 10:00 | 每周深度研究 |

---

## ⚠️ 视频号上传踩坑（必须记住）

**问题**：`sau tencent upload-video` 报 `Locator.set_input_files: Timeout 30000ms exceeded`

**根因**：视频号助手检测到自动化浏览器后，`/platform/post/create` 会被重定向到 dashboard (`/platform`)，页面上根本没有 `input[type="file"]`。

**排查方法**：
- Playwright locator 超时 ≠ 元素不可见，**先检查 page.url 是否是预期地址**
- SPA 页面的 URL 重定向是常见反自动化手段

**修复**：`open_upload_page` 增加重定向检测，被重定向时自动点击「发表视频」按钮

**教训**：
1. locator 找不到元素 → 先检查 URL，再检查 DOM
2. headless/headed 模式下页面行为可能不同
3. 视频号等平台会检测自动化浏览器并重定向

---

> 🛡️ 工具使用中的坑、技巧、最佳实践记录在此
