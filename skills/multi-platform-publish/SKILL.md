---
name: "multi-platform-publish"
description: "一键将内容发布到多个平台（social-auto-upload + Wechatsync）"
---

# 多平台一键发布 Skill

## 触发条件
用户说"发布到各平台"、"把这篇文章发出去"、"一键发布"

## 工作流程

### 输入
- 内容目录（如 `memory/content/2026-06-12-ai-agent/`）
- 或单个文件路径
- 目标平台（可选，默认全部已登录平台）
- 发布模式：draft（草稿）| publish（立即发布）| schedule（定时发布）

### 步骤

1. **检查登录状态**
   ```
   sau douyin check --account creator
   sau xiaohongshu check --account creator
   sau kuaishou check --account creator
   sau bilibili check --account creator
   ```
   只发布已登录的平台，跳过未登录的。

2. **读取内容**
   - 读取各平台适配的内容文件
   - 提取标题、正文、标签、配图

3. **生成配图**（如有 image-prompts.md）
   - 调用 image_generate 生成各平台封面
   - 保存到内容目录

4. **逐平台发布**
   
   **视频/图文平台（social-auto-upload CLI）**：
   ```bash
   # 小红书图文
   sau xiaohongshu upload-note --account creator --images <图片> --title "标题" --note "正文"
   
   # 抖音图文
   sau douyin upload-note --account creator --images <图片> --title "标题" --note "正文"
   
   # 快手图文
   sau kuaishou upload-note --account creator --images <图片> --title "标题" --note "正文"
   
   # B站视频
   sau bilibili upload-video --account creator --file <视频> --title "标题"
   ```

   **文章平台（Wechatsync）**：
   - 知乎、CSDN、掘金、公众号等通过 Wechatsync 推草稿箱

5. **生成发布报告**
   ```
   发布报告 - 2026-06-12
   ├── ✅ 小红书 - 已发布
   ├── ✅ 抖音 - 已发布
   ├── ⚠️ 快手 - 未登录，已跳过
   ├── ✅ 知乎 - 草稿箱
   ├── ✅ CSDN - 草稿箱
   └── ✅ 掘金 - 草稿箱
   ```

### 输出
- 发布报告写入内容目录 `publish-report.md`
- 截图各平台发布结果（screenshot.ps1）
- 发送汇总到微信

## 定时发布
- 配合 cron 实现定时发布
- 用户说"明天早上9点发" → 创建 cron job
- 到时间自动执行发布流程

## 依赖
- social-auto-upload CLI（视频/图文平台）
- Wechatsync（文章平台）
- screenshot.ps1（截图验证）
- image_generate（配图）

## 安全规则
- 默认 draft 模式，不默认直接发布
- 发布前必须用户确认
- 外部操作（发布）必须问
