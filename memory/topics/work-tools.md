# 工具使用发现

> 最后更新:2026-06-14

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
