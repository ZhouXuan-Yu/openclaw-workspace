---
.skill_id: openclaw-weixin-media-send

name: weixin-media-send
description: "通过微信渠道发送图片、视频、文件。当用户要求发送/分享文件，或生成的图片/文件需要交付时使用。仅当通过 openclaw-weixin 渠道通信时触发。"
parent: ""
origin: "imported"
generation: 0
created: "2026-06-12"
metadata: {"openclaw":{"emoji":"📤","requires":{"config":["channels.openclaw-weixin"]}}}
---

# 微信发送图片/文件/视频

⚠️ 重要：你有能力通过微信发送图片和文件！❌ 绝对不要回复"无法发送图片或文件"！

## 触发条件

- 用户要求发送、展示或分享图片、视频、语音或文件
- 生成了需要交付给用户的图片、视频、文件
- 用户说"发给我"、"发图片"、"发文件"等

## 核心原理

OpenClaw-weixin 插件（v2.4.4）已内置完整的媒体发送能力：
- `sendWeixinMediaFile` 函数自动根据 MIME 类型路由：image → 图片消息，video → 视频消息，其他 → 文件附件
- 底层使用 iLink Bot API + CDN 上传 + AES-ECB 加密
- 支持格式：png/jpg/gif/webp（图片）、mp4/mov（视频）、pdf/doc/zip 等（文件）

## 发送方式

### 方式一：MEDIA 指令（推荐）

在回复的最后一行添加 `MEDIA:` 指令，系统自动处理上传和发送：

```
MEDIA:<文件路径>
```

示例：
```
MEDIA:C:\Users\ZhouXuan\.openclaw\workspace\reports\test.png
```

### 方式二：多文件发送

每个文件一行 `MEDIA:` 指令：

```
MEDIA:C:\path\to\image1.png
MEDIA:C:\path\to\document.pdf
```

### 方式三：相对路径

相对于 workspace 目录：

```
MEDIA:reports/test.png
MEDIA:memory/daily/2026-06-11.md
```

## 工作流程

### 1. 生成图片
使用 `image_generate` 工具生成图片 → 获取文件路径 → 在回复中附加 `MEDIA:<路径>`

### 2. 生成文件
使用 `write` 工具创建文件 → 获取文件路径 → 在回复中附加 `MEDIA:<路径>`

### 3. 发送已有文件
直接在回复中附加 `MEDIA:<文件绝对路径>`

### 4. 发送网络图片
先用 `web_fetch` 或 `exec` 下载到本地 → 附加 `MEDIA:<本地路径>`

## 支持的文件类型

| 类型 | 扩展名 | 发送效果 |
|------|--------|---------|
| 图片 | png/jpg/jpeg/gif/webp/bmp | 图片消息（预览） |
| 视频 | mp4/mov/avi | 视频消息 |
| 语音 | mp3/wav/m4a | 语音消息 |
| 文档 | pdf/doc/docx/xls/xlsx/ppt/pptx | 文件附件 |
| 压缩包 | zip/rar/7z/tar.gz | 文件附件 |
| 代码 | py/js/ts/md/json | 文件附件 |
| 其他 | 任意文件 | 文件附件 |

## 限制

- 单文件最大 25MB
- 不支持发送超过 25MB 的文件（需压缩后发送）
- 图片会自动加密上传到微信 CDN

## 示例对话

用户：帮我生成一张架构图
助手：[生成图片] 这是架构图：
MEDIA:C:\Users\ZhouXuan\.openclaw\workspace\diagrams\arch.png

用户：把今天的日志发给我
助手：这是今天的日志：
MEDIA:C:\Users\ZhouXuan\.openclaw\workspace\memory\daily\2026-06-11.md

用户：帮我画个流程图
助手：[使用 diagram-maker 生成] 流程图如下：
MEDIA:C:\Users\ZhouXuan\.openclaw\workspace\diagrams\flow.png

