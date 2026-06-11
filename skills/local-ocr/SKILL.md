---
.skill_id: openclaw-local-ocr

name: local-ocr
description: "本地 OCR 图片文字识别。当收到图片、截图、文档照片需要提取文字时使用。使用 EasyOCR 本地模型，不依赖云端 API。"
parent: ""
origin: "captured"
generation: 1
created: "2026-06-12"
metadata: {"openclaw":{"emoji":"🔍","requires":{"python":["easyocr"]}}}
---

# 本地 OCR 图片文字识别

## 触发条件
- 用户发送图片/截图/文档照片
- 需要从图片中提取文字内容
- 用户说"看看这张图"、"识别一下"等

## 使用方式

```bash
python C:\Users\ZhouXuan\.openclaw\workspace\scripts\ocr.py <图片路径>
```

### 参数
- 默认输出纯文字（置信度 >0.5 的行）
- `--json` 输出 JSON 格式（含坐标和置信度）

## 工作流程

1. 收到图片 → 保存到本地临时文件
2. 调用 OCR 脚本识别文字
3. 分析识别结果，回复用户

## 支持的语言
- 中文简体 ✅
- 英文 ✅
- 其他语言需额外下载模型

## 限制
- CPU 运行（无 GPU），识别速度较慢（~5-10秒/图）
- 复杂排版可能识别不准
- 手写体识别效果一般
- 图片需清晰，分辨率过低会影响效果

## 模型信息
- EasyOCR 1.7.2
- 检测模型: craft_mlt_25k (~100MB)
- 识别模型: chinese_sim + english (~100MB)
- 模型路径: ~/.EasyOCR/model/
