# OpenClaw System Dashboard

## 入口
- **交互式面板**: http://localhost:8080 (SQLPage，搜索/浏览/过滤/分页)
- **快速总览**: tools/dashboard.html (静态 HTML，每次对话自动刷新)

## 页面功能

| 页面 | URL | 功能 |
|------|-----|------|
| 首页 | /index.sql | 概览卡片 + 能力进度条 + 快速搜索 + 最近文件 |
| 文件浏览器 | /file-browser.sql | 导航所有核心文件 + 点击即读 Markdown 原文 |
| 记忆搜索 | /content-search.sql | 关键词全文搜索 + 分页 + 结果计数 |
| 进化引擎 | /evolution-stats.sql | 能力进度条 + 信任注册表 + 进化文件索引 |
| Cron 面板 | /cron-dashboard.sql | 14 个任务状态 + 记忆健康度 |

## 自动维护
每次对话结束时 teardown hook 自动：
1. 刷新 `dashboard.html`（实时数据采集）
2. 重启 SQLPage 容器（同步最新记忆数据库）

你不需要做任何操作，打开浏览器即可看到最新状态。
