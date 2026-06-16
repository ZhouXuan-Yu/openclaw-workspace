---
name: hyperframes-video
description: 用 HyperFrames + edge-tts 生成带配音的短视频（MP4），用于社交平台发布。支持文档→TTS→HTML+GSAP动画→渲染视频。
version: 2.0.0
author: GGOB
tags: [video, hyperframes, tts, social-automation, content-creation]
parent: multi-platform-publish
---

# HyperFrames 视频生成 Skill v2

## 概述

**文档内容 → TTS 配音 → HyperFrames 动画 → MP4 视频（带声音）**

核心链路：edge-tts 生成音频 → HTML+GSAP 组合 → `npx hyperframes render` → MP4

## 前置条件

| 依赖 | 用途 | 安装 |
|------|------|------|
| edge-tts | 微软 TTS 语音合成 | `pip install edge-tts` |
| FFmpeg | 视频编码 | `C:\tools\ffmpeg\bin` (已安装) |
| HyperFrames CLI | 渲染引擎 | `npx hyperframes` |
| GSAP | 动画引擎 | CDN 引入 |

## 完整工作流程

### Step 1: 文档内容 → TTS 音频

```python
import edge_tts
import asyncio

async def generate_tts(text, output_path, voice="zh-CN-YunxiNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

# 用法
asyncio.run(generate_tts(
    "用了半年ChatGPT，每次开新对话都要重新解释自己是谁。",
    "tts-output.mp3"
))
```

**可用中文语音**：
- `zh-CN-YunxiNeural` — 男声（推荐）
- `zh-CN-XiaoxiaoNeural` — 女声
- `zh-CN-YunjianNeural` — 男声（沉稳）

### Step 2: 创建 HyperFrames HTML

关键：`<audio>` 元素必须直接写 `src` 属性，不能用 `<source>` 子元素：

```html
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700;900&display=swap');
  body { width: 1080px; height: 1920px; }
</style>
</head>
<body>
  <div data-composition-id="root" data-width="1080" data-height="1920" 
       data-start="0" data-duration="15">
    
    <!-- 场景 -->
    <div id="scene1" class="clip" data-start="0" data-duration="5" data-track-index="0">
      <!-- 内容 -->
    </div>
    
    <!-- 音频（必须直接写 src） -->
    <audio id="tts" src="tts-output.mp3" 
           data-start="0" data-duration="15" 
           data-track-index="2" data-volume="1"></audio>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    // 动画...
    window.__timelines["root"] = tl;
  </script>
</body>
</html>
```

### Step 3: 渲染视频

```powershell
$env:PATH = "C:\tools\ffmpeg\bin;$env:PATH"
cd <项目目录>
npx hyperframes render --output output.mp4
```

## 重要规则

### 音频格式
- `<audio>` 必须直接写 `src` 属性
- 不能用 `<source>` 子元素（HyperFrames 不识别）
- 支持格式：MP3, WAV, OGG

### 字体
- 用 Google Fonts 的 `@import` 引入（HyperFrames 自动缓存）
- 系统字体（如 Microsoft YaHei）不支持，会被替换
- 推荐：`Noto Sans SC`（中文），`Inter`（英文）

### GSAP 动画
- 所有 timeline 必须 `{ paused: true }`
- 注册到 `window.__timelines`
- 场景间必须有过渡（不用 jump cut）
- 最后场景才允许 fade out

## 与社交自动化集成

```
用户需求 → Codex 生成 HTML → edge-tts 生成音频 → HyperFrames 渲染 → 多平台发布
```

**平台适配**：
| 平台 | 尺寸 | 时长 | 格式 |
|------|------|------|------|
| 抖音 | 1080x1920 | 15-60s | MP4 |
| B站 | 1920x1080 | 不限 | MP4 |
| 小红书 | 1080x1440 | 不限 | MP4 |

## 快速命令

```powershell
# 1. 生成 TTS
python -c "import edge_tts, asyncio; asyncio.run(edge_tts.Communicate('文本内容', 'zh-CN-YunxiNeural').save('tts.mp3'))"

# 2. 渲染视频
$env:PATH = "C:\tools\ffmpeg\bin;$env:PATH"
npx hyperframes render --output video.mp4
```

## 故障排除

| 问题 | 解决 |
|------|------|
| FFmpeg not found | `$env:PATH = "C:\tools\ffmpeg\bin;$env:PATH"` |
| 音频不播放 | 检查 `<audio>` 是否直接写 `src` 属性 |
| 字体不对 | 用 `Noto Sans SC`，不要用系统字体 |
| 渲染慢 | 正常，15s 视频约 1-2 分钟 |

## 性能数据

| 视频时长 | 渲染时间 | 文件大小 |
|----------|----------|----------|
| 15s @ 30fps | ~2 分钟 | 1.1-1.3 MB |
| 30s @ 30fps | ~4 分钟 | ~2.5 MB |
| 60s @ 30fps | ~8 分钟 | ~5 MB |
