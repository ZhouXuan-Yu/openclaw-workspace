---
name: daily-report
description: 每日工作汇报自动生成
triggers:
  - "汇报"
  - "日报"
  - "工作汇报"
  - "daily report"
---

# 每日工作汇报 Skill

## 功能
1. 每天 17:30 cron 提醒用户填写今日完成
2. 汇总：今日完成 + 进行中 + 问题 + 明日计划
3. 生成标准化汇报文档
4. 发送到指定渠道

## 使用方式

### 方式一：主动触发
用户说"写汇报" → 收集今日信息 → 生成汇报

### 方式二：Cron 自动触发
17:30 提醒 → 用户补充 → 生成汇报

## 汇报模板

```markdown
# 工作汇报 — {date} ({weekday})

## 今日完成
- {completed_items}

## 进行中
- {in_progress_items}

## 遇到的问题
- {issues}

## 明日计划
- {tomorrow_plan}

## 数据指标
| 指标 | 数值 | 变化 |
|------|------|------|
| {metrics}
```

## 数据收集来源
1. memory/daily/{today}.md — 今日对话记录
2. memory/evolution/run-log.json — 任务执行记录
3. memory/evolution/publish-metrics.json — 发布数据
4. 用户主动补充
