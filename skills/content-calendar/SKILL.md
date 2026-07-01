---
name: "content-calendar"
description: "内容日历管理：规划主题、定时提醒、跟踪发布状态"
---

# 内容日历 Skill

## 触发条件
- 用户说"安排本周内容"、"下周发什么"、"内容日历"
- 用户说"每天发一篇关于XXX"

## 工作流程

### 1. 内容规划
读取 `memory/content/calendar.json`，包含：
```json
{
  "version": 1,
  "plan": [
    {
      "date": "2026-06-13",
      "topic": "AI Agent 入门",
      "platforms": ["xiaohongshu", "csdn", "zhihu"],
      "status": "planned",
      "contentDir": null,
      "publishReport": null
    }
  ],
  "themes": {
    "weekly": "AI 工具使用技巧",
    "daily": ["周一: 入门", "周二: 进阶", "周三: 实战"]
  }
}
```

### 2. 自动生成内容
- 按日历主题调用 multi-platform-content skill
- 提前一天生成内容
- 写入 `memory/content/<日期>-<主题>/`

### 3. 定时提醒
- 每天早上 9:00 提醒今日发布计划
- cron: `0 9 * * *`
- 提醒格式：
  ```
  📅 今日发布计划
  ├── 09:30 小红书 - AI Agent 入门
  ├── 12:00 公众号 - AI Agent 深度解析
  └── 18:00 CSDN - AI Agent 实战教程
  ```

### 4. 状态跟踪
- planned → generated → published
- 记录每篇内容的发布状态
- 生成周报/月报

### 5. 内容规划建议
根据分析给出建议：
- 最佳发布时间
- 热门话题趋势
- 各平台内容频率建议

## 输出文件
```
memory/content/
├── calendar.json           # 内容日历
├── 2026-06-13-ai-agent/   # 每日内容
├── 2026-06-14-prompt-eng/
└── weekly-report.md        # 周报
```

## 依赖
- multi-platform-content skill
- multi-platform-publish skill
- cron（定时提醒）
- web_search（趋势分析）
