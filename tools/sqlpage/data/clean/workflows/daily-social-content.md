# 每日社交内容自动化任务

## 触发时间
每天 23:00（Asia/Shanghai）

## 完整流程

```
10:00 触发
  ↓
[Step 1] 收集内容
  ├── 读 memory/daily/今日.md（昨天做了什么）
  ├── 读 Obsidian 仓库 Agent 相关目录
  │   ├── Agent学习/
  │   ├── 未来agent项目发展思考/
  │   ├── AA每日前沿信息/
  │   └── 每日更新/
  └── 读 Obsidian 教育行业内容
      └── 软件项目开发/教育AI/
  ↓
[Step 2] 生成内容大纲
  ├── 主题: Agent 发展方向 + 教育行业 Agent 落地
  ├── 角度: 个人实践 + 行业观察
  └── 风格: 真实、有观点、不套话
  ↓
[Step 3] 生成配图（必须步骤）
  ├── 工具: image_generate（AI生图）
  ├── 为每张卡片生成 hero image
  ├── 保存到 output-daily/assets/
  └── 风格: 瑞士国际风格，简洁几何蓝色调
  ↓
[Step 4] 视频生产（按 work-tools.md Q0-Q5 流程）
  ├── guizang-social-card Swiss International → HTML（含配图）
  ├── Playwright → PNG
  ├── edge-tts zh-CN-YunxiNeural → MP3
  ├── SRT 字幕 (FontSize=10, MarginV=80)
  ├── HyperFrames 渲染 → MP4
  └── FFmpeg 合成字幕+音频 → final.mp4
  ↓
[Step 5] 生成 PDF
  ├── 标题 + 正文文本
  ├── 关键数据/图表
  └── 视频截图/卡片预览
  ↓
[Step 6] 发送审核
  ├── 视频文件 → 微信
  ├── PDF 文件 → 微信
  └── 等待用户回复"通过"或修改意见
  ↓
[Step 7] 用户审核通过后
  ├── sau CLI 发布视频（抖音/快手/B站/小红书）
  ├── 小红书 --draft 草稿模式
  └── Wechatsync 发布文章（公众号/知乎/掘金）
```

## 审核机制
- 用户回复"通过" → 自动发布
- 用户回复修改意见 → 按意见修改后重新提交
- 超过 2 小时无回复 → 不发布，等下次

## 相关文件
- 卡片模板: skills/guizang-social-card/assets/template-swiss-card.html
- 视频技能: skills/hyperframes-video/SKILL.md
- 发布工具: tools/social-auto-upload/
- 决策树: E:\Obsidian仓库\ZhouXuan私人领域\开发项目\社交自动化决策树.md
