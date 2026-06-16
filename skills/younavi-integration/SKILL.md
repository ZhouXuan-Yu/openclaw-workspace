---
name: younavi-integration
description: YouNavi 深度研究+会议同步+音频转写集成到 OpenClaw
version: 1.0.0
author: GGOB
tags: [younavi, research, meeting, transcribe]
triggers: [深度研究, 会议同步, 音频转写, younavi]
---

# Skill: YouNavi Integration

YouNavi 深度研究 + 会议同步 + 音频转写 集成到 OpenClaw 自动化体系。

## 快速调用

```python
# 在 OpenClaw 中通过 exec 调用
python tools/younavi_bridge.py <command> [args...]
```

## 可用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `auth_me` | 获取当前用户信息 | `python tools/younavi_bridge.py auth_me` |
| `memory_list` | 列出记忆文件 | `python tools/younavi_bridge.py memory_list` |
| `memory_get` | 获取记忆内容 | `python tools/younavi_bridge.py memory_get "全局记忆文件.txt"` |
| `memory_append` | 追加记忆 | `python tools/younavi_bridge.py memory_append "全局记忆文件.txt" "新内容"` |
| `notes_list` | 列出笔记 | `python tools/younavi_bridge.py notes_list` |
| `notes_create` | 创建笔记 | `python tools/younavi_bridge.py notes_create "标题" "内容"` |
| `task_list` | 列出任务 | `python tools/younavi_bridge.py task_list` |
| `task_show` | 任务详情 | `python tools/younavi_bridge.py task_show <task_id>` |
| `task_report` | 任务报告 | `python tools/younavi_bridge.py task_report <task_id>` |
| `file_list` | 列出文件 | `python tools/younavi_bridge.py file_list` |
| `file_upload` | 上传文件 | `python tools/younavi_bridge.py file_upload <path>` |
| `channel_list` | 列出渠道 | `python tools/younavi_bridge.py channel_list` |
| `channel_sync` | 同步渠道 | `python tools/younavi_bridge.py channel_sync tencent_meeting` |
| `channel_sync_all` | 同步所有渠道 | `python tools/younavi_bridge.py channel_sync_all` |
| `audio_transcribe` | 转写音频 | `python tools/younavi_bridge.py audio_transcribe <path>` |
| `llm_show` | 查看LLM设置 | `python tools/younavi_bridge.py llm_show` |
| `llm_models` | 列出可用模型 | `python tools/younavi_bridge.py llm_models` |
| `dir_list` | 列出监控目录 | `python tools/younavi_bridge.py dir_list` |
| `research_plan` | 生成研究计划 | `python tools/younavi_bridge.py research_plan_only "主题"` |
| `research_start` | 启动异步研究 | `python tools/younavi_bridge.py research_start "主题"` |
| `research_report` | 获取研究报告 | `python tools/younavi_bridge.py research_report <task_id>` |
| `research_full` | 完整研究流程 | `python tools/younavi_bridge.py research_full "主题"` |
| `sync_meetings` | 同步所有会议 | `python tools/younavi_bridge.py sync_meetings` |
| `daily_briefing` | 每日简报 | `python tools/younavi_bridge.py daily_briefing` |

## 深度研究工作流

```
用户: "研究一下 XXX"
  ↓
1. research_plan_only("XXX") → 生成研究计划
2. 用户确认计划
3. research_start("XXX") → 启动异步研究
4. task_wait(task_id) → 等待完成
5. task_report(task_id) → 获取报告
6. 写入 Obsidian Vault
```

## 会议同步工作流

```
定时触发 (Cron 每日 09:00/18:00)
  ↓
1. channel_sync_all() → 同步所有渠道
2. task_list() → 获取新任务
3. audio_transcribe(新音频) → 转写新录音
4. memory_append("全局记忆文件.txt", 摘要) → 写入记忆
5. 推送到微信通知用户
```

## 数据流

```
YouNavi 数据目录: C:\Users\ZhouXuan\navi-ai\
├── ZhouXuan_/
│   ├── cognition/    ← 记忆文件
│   ├── notes/        ← 笔记
│   ├── uploads/      ← 上传文件
│   └── meeting_records/ ← 会议记录
└── generated_artifacts/ ← 生成产物（PDF/图片）
```

## 注意事项

1. **编码问题**：CLI 输出含 Unicode 字符，必须用 Python 包装调用
2. **服务自动启动**：默认 `auto_start=True`，CLI 会自动启动后端服务
3. **API 端口**：`127.0.0.1:18429`（每次重启会变，用 CLI 优先）
4. **超时设置**：研究类命令建议 timeout≥120s，音频转写≥300s
5. **产物路径**：`C:\Users\ZhouXuan\navi-ai\generated_artifacts\`
