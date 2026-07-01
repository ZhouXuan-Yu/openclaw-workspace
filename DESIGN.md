---
name: Meta Design System
version: 2.0
description: 从15个世界顶级品牌提炼的参数化通用设计系统 — 覆盖YAML Token即可切换品牌风格。默认值倾向现代开发者工具/SaaS。
design_tokens_version: 2
source_brands:
  - Linear
  - Vercel
  - Stripe
  - Figma
  - Notion
  - Supabase
  - Raycast
  - Claude (Anthropic)
  - Apple
  - Nike
  - Airbnb
  - Spotify
  - Shopify
  - Tesla
  - Ferrari

# ═══════════════════════════════════════════
#  Token 层 — 覆盖这些值即可切换品牌
# ═══════════════════════════════════════════
colors:
  primary: "#5E6AD2"
  primary_hover: "#828FFF"
  primary_active: "#4F5ABF"
  on_primary: "#FFFFFF"

  background: "#0D0D0D"
  background_alt: "#FAFAFA"
  surface: "#141516"
  surface_elevated: "#18191A"
  surface_overlay: "#1E1F20"

  text_primary: "#F7F8F8"
  text_secondary: "#D0D6E0"
  text_muted: "#8A8F98"
  text_primary_light: "#171717"
  text_secondary_light: "#4D4D4D"

  border: "#23252A"
  border_light: "#E6E6E6"
  border_strong: "#34343A"

  success: "#27A644"
  warning: "#F5A623"
  error: "#EE0000"
  info: "#539DF5"

  color_blocks: []
  gradient_mesh: ""
  accent_secondary: ""

typography:
  font_sans: "Inter, -apple-system, system-ui, 'Segoe UI', sans-serif"
  font_mono: "JetBrains Mono, ui-monospace, 'Cascadia Code', monospace"

  h1_size: "56px"
  h1_weight: 600
  h1_line_height: 1.05
  h1_letter_spacing: "-1.8px"

  h2_size: "36px"
  h2_weight: 600
  h2_line_height: 1.15
  h2_letter_spacing: "-0.5px"

  h3_size: "24px"
  h3_weight: 600
  h3_line_height: 1.25
  h3_letter_spacing: "-0.3px"

  h4_size: "20px"
  h4_weight: 500
  h4_line_height: 1.3
  h4_letter_spacing: "0"

  body_size: "16px"
  body_weight: 400
  body_line_height: 1.5
  body_letter_spacing: "-0.05px"

  body_small: "14px"
  caption: "12px"
  code: "14px"

  button_size: "14px"
  button_weight: 500

  font_features: "\"kern\", \"liga\", \"calt\""

  weight_normal: 400
  weight_medium: 500
  weight_semibold: 600
  weight_bold: 700

spacing:
  unit: 4
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  xxl: "32px"
  xxxl: "48px"
  section: "96px"
  container_padding: "24px"

radius:
  none: "0px"
  xs: "4px"
  sm: "6px"
  md: "8px"
  lg: "12px"
  xl: "16px"
  xxl: "24px"
  pill: "9999px"
  full: "9999px"

shadows:
  none: "none"
  sm: "0 1px 2px rgba(0,0,0,0.04)"
  md: "0 2px 8px rgba(0,0,0,0.08)"
  lg: "0 8px 24px rgba(0,0,0,0.12)"
  modal: "0 16px 48px rgba(0,0,0,0.2)"

layout:
  max_width: "1200px"
  reading_width: "720px"
  grid_columns: 12
  gutter: "24px"

  breakpoints:
    mobile: 640
    tablet: 1024
    desktop: 1440

motion:
  duration_fast: "150ms"
  duration_normal: "250ms"
  duration_slow: "350ms"
  ease_default: "cubic-bezier(0.4, 0, 0.2, 1)"
---

# 元设计系统 — Meta Design System v2.0

## 概述

本系统提炼自Linear, Vercel, Stripe, Figma, Notion, Supabase, Raycast, Claude, Apple, Nike, Airbnb, Spotify, Shopify, Tesla, Ferrari 共15个世界顶级品牌的设计DNA，提取它们的**共同优秀实践**形成一个可参数化、可切换的通用设计系统。修改顶部YAML Token即可在暗黑开发者工具、亮色SaaS、消费级暖色、极简奢侈、沉浸式暗色、暖编辑AI 六种风格之间自由切换。

**设计哲学**：
1. **少即是多** — 15个品牌中8个仅用1个品牌强调色，其余全灰度
2. **字体即声音** — 显示/正文双字体策略，负字距为现代品牌标志
3. **微圆即现代** — 60%顶级品牌用全Pill按钮；开发者工具用6-8px微圆
4. **影不如面** — 多数品牌用表面色阶替代阴影，仅Shopify/Spotify例外
5. **产品即装饰** — Linear, Supabase, Raycast以产品截图为页面装饰主元素

---

## 1. 视觉主题与氛围

### 默认：暗黑开发者工具风格

- **暗画布** (`colors.background` #0D0D0D)：近黑背景，让代码/产品截图发光
- **四阶表面阶梯**：canvas → surface → surface_elevated → surface_overlay，用色调微差替代阴影
- **单色强调** (`colors.primary`)：唯一颜色事件，仅用于主CTA按钮、焦点环、品牌标记
- **负字距显示**：h1-h3 使用 -0.3到-1.8px 负字距，现代"紧张感"
- **发丝线边框**：所有卡片用1px `colors.border`，无投影
- **4px基准间距**：所有间距基于4px系统

### 切换模式

通过修改顶部YAML `colors`, `typography`, `radius`, `shadows` 四个键组可快速切换六种风格：

| 模式 | 关键Token变更 |
|------|--------------|
| **暗黑开发者工具**（默认） | background:#0D0D0D, primary:蓝紫系, radius 6-8px, 负字距 |
| **亮色SaaS** | background:#FFFFFF, text_primary:#171717, 逆polarity |
| **消费级暖色** | primary:#FF385C, pill按钮, 圆形搜索, Airbnb Cereal字体 |
| **极简奢侈** | primary:#000000, radius:0px, 零阴影, 全出血摄影 |
| **沉浸式暗色** | background:#121212, primary:#1ED760, 大写按钮, 重阴影 |
| **暖编辑AI** | background:#FAF9F5, font_display:衬线, primary:暖珊瑚, 奶油表面 |

---

## 2. 色彩系统

### 2.1 品牌强调色

**唯一品牌色原则**：15个品牌中53%仅使用1个品牌色。主色应仅用于：
- 主CTA按钮填充
- 焦点环/选中状态
- 品牌文字标记
- 内联链接

*反模式*：装饰性使用品牌色、渐变背景、色块装饰

### 2.2 表面阶梯

```
canvas (页面底层)        #0D0D0D
  └─ surface (卡片)      #141516
       └─ elevated (浮起) #18191A
            └─ overlay (模态) #1E1F20
```

**4级足够**。每级差约 #040404-#030303。不需要更多。

### 2.3 灰阶文字

```
text_primary (标题+正文)    #F7F8F8
text_secondary (副标)       #D0D6E0
text_muted (禁用/脚注)      #8A8F98
```

文字必须永远不是纯白 (#FFF) 或纯黑 (#000)。始终有色调微差。

### 2.4 语义色

```
success: #27A644  (仅状态指示/成功标记)
warning: #F5A623  (警告)
error:   #EE0000  (错误/验证失败)
info:    #539DF5  (信息/提示)
```

语义色**绝不在营销铬中使用**。仅在功能型界面出现。

### 2.5 亮模式逆极

当使用亮模式时：
```
background → #FFFFFF
surface    → #FAFAFA 或 #F5F5F5
text_primary → #171717
border     → #E6E6E6
```

---

## 3. 排版系统

### 3.1 字体栈

**显示 → 正文 → 等宽** 三栈策略：

```css
--font-sans: Inter, -apple-system, system-ui, 'Segoe UI', sans-serif;
--font-mono: JetBrains Mono, ui-monospace, 'Cascadia Code', monospace;
```

**Inter** 是所有15个品牌分析中最常推荐的免费替代字体（9/15提及）。Geist Sans（Vercel开源）是第二选择。

### 3.2 层次

| 级别 | Token | 用途 | 字号 | 字重 | 行高 | 字距 |
|------|-------|------|------|------|------|------|
| H1 | hero | 页面主标题 | 56px | 600 | 1.05 | -1.8px |
| H2 | section | 节标题 | 36px | 600 | 1.15 | -0.5px |
| H3 | sub-section | 子节标题 | 24px | 600 | 1.25 | -0.3px |
| H4 | card-title | 卡片标题 | 20px | 500 | 1.3 | 0 |
| Body | body | 正文 | 16px | 400 | 1.5 | -0.05px |
| Body-sm | small | 辅助文字 | 14px | 400 | 1.5 | 0 |
| Caption | caption | 标注 | 12px | 400 | 1.4 | 0 |
| Button | button | 按钮 | 14px | 500 | 1.2 | 0 |
| Code | code | 代码 | 14px | 400 | 1.5 | 0 |

### 3.3 核心原则

1. **显示用负字距**：H1-H3必须带负letter-spacing（-0.3到-1.8px）—— 这是现代品牌区别于传统设计的核心标志
2. **一个字重梯度**：400/500/600/700四阶。600用于显示，500用于按钮/标签，400用于正文
3. **正文16px**：正文绝不用14px（15/15品牌中仅Tesla和Spotify例外）
4. **代码14px**：等宽字体始终14px
5. **不用大写**：按钮标签默认小写/sentence-case；仅在选择"Spotify/Nike"模式时使用大写
6. **Inter替代**：当无法使用自定义字体时，Inter是最佳开源替代（接近SF Pro, Circular, Söhne的特征比例）

---

## 4. 组件规范

### 4.1 按钮

**主CTA按钮** (button_primary)：
```css
background: var(--color-primary);
color: var(--color-on-primary);
font: var(--typography-button);
border-radius: var(--radius-md);   /* 8px 微圆 — 开发者风格 */
padding: 8px 16px;
border: none;
cursor: pointer;
transition: background var(--motion-fast) var(--motion-ease);
```
- hover: `primary_hover`
- active: `primary_active`
- disabled: opacity 0.5

**次按钮** (button_secondary)：
```css
background: var(--color-surface);
color: var(--color-text-primary);
border-radius: var(--radius-md);
padding: 8px 16px;
border: 1px solid var(--color-border);
```

**幽灵按钮** (button_ghost)：
```css
background: transparent;
color: var(--color-text-primary);
border-radius: var(--radius-md);
padding: 8px 16px;
```

**链接按钮** (button_link)：
```css
background: transparent;
color: var(--color-primary);
padding: 0;
text-decoration: underline;
```

### 4.2 卡片

**默认卡片** (card)：
```css
background: var(--color-surface);
border: 1px solid var(--color-border);
border-radius: var(--radius-lg);   /* 12px */
padding: var(--spacing-xl);        /* 24px */
```

**无边框卡片** (card_borderless) — 当背景色差足够区分时：
```css
background: var(--color-surface);
border-radius: var(--radius-lg);
padding: var(--spacing-xl);
```

**特色卡片** (card_featured) — 深底反转：
```css
background: var(--color-text-primary-light);  /* 近黑 */
color: var(--color-text-primary);             /* 近白 */
border-radius: var(--radius-lg);
```

### 4.3 输入框

```css
background: var(--color-surface);
color: var(--color-text-primary);
border: 1px solid var(--color-border);
border-radius: var(--radius-md);   /* 8px */
padding: 8px 12px;
font: var(--typography-body);
height: 40px;
```
- focus: border变为 `color-primary`，外发光 0 0 0 2px rgba(primary, 0.2)
- placeholder: `color-text-muted`

### 4.4 导航栏

```css
background: var(--color-background);
border-bottom: 1px solid var(--color-border);
height: 56px;
padding: 0 var(--spacing-lg);
display: flex;
align-items: center;
```
- Logo左，主导航中，CTA按钮右
- 粘性定位 sticky top

### 4.5 徽章/标签

```css
/* 填充徽章 */
background: var(--color-primary);
color: var(--color-on-primary);
border-radius: var(--radius-pill);
padding: 2px 8px;
font: var(--typography-caption);

/* 轮廓徽章 */
background: transparent;
color: var(--color-text-secondary);
border: 1px solid var(--color-border);
border-radius: var(--radius-pill);
```

---

## 5. 布局系统

### 5.1 栅格

```
content: max 1200px centered
reading: max 720px  (长文本)
features: 3-up at desktop, 2-up tablet, 1-up mobile
pricing: 4/3/2/1 up 按屏幕
```

### 5.2 间距节奏

```
组件内: 4px/8px/12px/16px (4px阶梯)
卡片间: 24px gutter
节之间: 96px vertical (section token)
页首/页脚: 64px
```

**关键**：96px 是现代SaaS section间距的黄金标准（Linear, Vercel, Stripe, Figma, Raycast, Claude, Notion 全部使用80-96px）。

### 5.3 留白哲学

- **暗底留白用"呼吸密度"** — 96px节间 + 较紧的卡片内边距（24-32px）
- **亮底留白用"内容呼吸"** — 同样96px节间但卡片更大
- 不在组件之间加装饰分隔线。空间本身即分隔
- 每屏一个核心信息（Apple/Tesla哲学），用滚动传递

---

## 6. 阴影与深度

### 6.1 默认：无影系统

现代顶级品牌**极少使用阴影**。深度通过以下实现：
1. 表面色阶差异（#OD0D0D vs #141516 vs #18191A）
2. 1px发丝线边框
3. 颜色块对比（亮底色块vs暗底色块）

### 6.2 可选阴影等级

```css
shadow_sm:   0 1px 2px rgba(0,0,0,0.04);   /* hover微升 */
shadow_md:   0 2px 8px rgba(0,0,0,0.08);   /* 卡片浮起 */
shadow_lg:   0 8px 24px rgba(0,0,0,0.12);   /* 模态/下拉 */
shadow_modal: 0 16px 48px rgba(0,0,0,0.2);  /* 全屏模态 */
```

默认不使用任何阴影。仅当组件需要与背景区分且色差不足以区分时添加shadow_sm。

---

## 7. 设计禁忌

### 不要做的事

| 禁忌 | 原因 | 来源 |
|------|------|------|
| 使用超过2个品牌色 | 15个顶级品牌中53%只用1个 | 全样本 |
| 纯黑(#000)或纯白(#FFF)作背景/文字 | 微小色调差是品质标志 | Linear, Apple, Ferrari等 |
| 正文小于14px | 16px是标准，14px仅Tesla/Spotify用 | 13/15品牌 |
| 按钮无圆角 | 60%品牌用全pill，其余用微圆4-8px | 15/15品牌有圆角 |
| 显示标题用正字距 | 负字距是"现代品牌"标志 | 14/15品牌 |
| 装饰性渐变/辉光 | 品牌渐变仅在特定品牌(Vercel/Stripe)有目的使用 | 多数品牌 |
| 5级以上阴影 | 顶级品牌最多4级，多数0-2级 | 全样本 |
| 忽略4px/8px基准 | 15/15品牌使用明确的间距基准 | 全样本 |
| 按钮和表单输入圆角差异过大 | 保持6-8px一致 | 开发者工具模式 |

### 必须做的事

- 品牌色仅在CTA/焦点/链接使用，不装饰
- 任何交互元素有hover/active/focus三态
- 过渡动画统一150ms-350ms且用标准ease曲线
- 所有文本颜色通过WCAG AA对比度（至少4.5:1正文）

---

## 8. 响应式行为

### 8.1 断点

```css
mobile:  0 - 640px    (单列，堆叠CTA)
tablet:  641 - 1024px (2列，侧栏折叠)
desktop: 1025px+      (完整布局)
wide:    1440px+      (内容居中，增大边距)
```

### 8.2 折叠策略

- 导航：水平 → 汉堡菜单 (mobile)
- CTA对：并排 → 堆叠 (mobile)
- 特性网格：3列 → 2列 → 1列
- 定价卡：4列 → 2列 → 1列
- 页脚：5列 → 2列 → 1列
- 间距：96px → 64px → 48px

---

## 9. AI Agent 提示词指南

### 9.1 快速颜色参考

```
暗底: bg=#0D0D0D, surface=#141516, text=#F7F8F8, border=#23252A
亮底: bg=#FFFFFF,  surface=#FAFAFA, text=#171717, border=#E6E6E6
强调: #5E6AD2 (主CTA/链接/焦点), hover=#828FFF
语义: success=#27A644, error=#EE0000, warning=#F5A623
```

### 9.2 组件生成提示词模板

**生成按钮**：
> "创建一个主按钮：背景#5E6AD2，白色文字#FFFFFF，14px Inter weight 500，8px圆角，padding 8px 16px。hover变#828FFF，active变#4F5ABF。过渡150ms ease-out。"

**生成卡片**：
> "在#141516背景上创建一个卡片：1px边框#23252A，12px圆角，24px内部padding。内容用16px/400 #F7F8F8正文，标题用20px/500。"

**生成页面布局**：
> "创建暗黑主题登录页面：最外层#0D0D0D全宽。顶部56px粘性导航栏带1px底部边框。主区域96px垂直padding。hero h1=56px/600/-1.8px字距。下面一个CTA按钮（主钮+次钮对）。接着3列特性卡片网格，24px间距。"

**生成暗模式页面**：
> "整个页面#0D0D0D基础背景。所有卡片#141516表面，1px边框#23252A。主文字#F7F8F8 16px Inter，副文字#D0D6E0。唯一色彩仅用于CTA按钮和链接。层次感和深度仅通过表面色差和细线边框产生——绝不使用投影。"

### 9.3 品牌快速切换

**开发者工具** → 暗底+微圆+单色+负字距+无影
**亮色SaaS** → 白底+暗字+微圆+单色+无影
**消费应用** → 白底+pink主色+pill按钮+圆形元素+Cereal字体
**极简奢侈** → 白底+全黑+0px锐角+全屏摄影+无影
**沉浸式暗色** → #121212+绿色强调+pill按钮+大写标签+重阴影
**暖编辑AI** → 奶油底#FAF9F5+珊瑚强调+衬线显示+暖墨text+JetBrains代码

### 9.4 迭代指南

1. 先确定画布底色（暗/亮/奶油）
2. 选一个强调色 — 只一个，不多
3. 建表面阶梯 — canvas→surface→elevated→overlay
4. 设字体尺度 — h1从56px开始，正文16px
5. 加负字距到显示层 — 品牌能量从这里来
6. 定按钮形状 — pill(消费) 或 8px微圆(开发工具)
7. 决定阴影策略 — 默认无，需要时才加
8. 用4px/8px间距搭栅格
9. 最后检查：所有非功能色元素是否真需要存在

---

## 附录A：15品牌核心参数速查

| 品牌 | 主色 | 背景 | Hero字号/字重 | 正文 | 按钮圆角 | 阴影 |
|------|------|------|--------------|------|----------|------|
| Linear | #5E6AD2 | #010102 | 80/600 | 16/400 | 8px | 无 |
| Vercel | #171717 | #FFF | 48/600 | 16/400 | Pill | 微 |
| Stripe | #533AFD | #FFF | 56/300 | 15/300 | Pill | 微 |
| Figma | #000 | #FFF | 86/340 | 18/320 | 50px | 无 |
| Notion | 灰度 | #FFF | — | 16/400 | 6-8px | 无 |
| Supabase | #3ECF8E | #FFF | 64/500 | 16/400 | 6px | 微 |
| Raycast | #FFF | #07080A | 64/600 | 16/400 | 8px | 无 |
| Claude | #CC785C | #FAF9F5 | 64/400 | 16/400 | 8px | 无 |
| Apple | #0066CC | #FFF | 56/600 | 17/400 | Pill | 极微 |
| Nike | #111 | #FFF | 96/500 | 16/500 | Pill | 无 |
| Airbnb | #FF385C | #FFF | 28/700 | 16/400 | Pill | 微 |
| Spotify | #1ED760 | #121212 | 24/700 | 16/400 | Pill | 重 |
| Shopify | #000 | #000/#FFF | 96/330 | 16/420 | Pill | 4级 |
| Tesla | #3E6AE1 | #FFF | 40/500 | 14/400 | 4px | 无 |
| Ferrari | #DA291C | #181818 | 80/500 | 14/400 | 0px | 无 |
| **元系统(默认)** | **#5E6AD2** | **#0D0D0D** | **56/600** | **16/400** | **8px** | **无** |

## 附录B：完整品牌切换Cheat Sheet

```yaml
# 模式1: 暗黑开发者工具 (默认)
colors.background: "#0D0D0D"
colors.text_primary: "#F7F8F8"
colors.primary: "#5E6AD2"
radius.md: "8px"            # 按钮微圆
shadows: 不使用
typography.font_sans: "Inter"
typography.h1_letter_spacing: "-1.8px"

# 模式2: 亮色SaaS
colors.background: "#FFFFFF"
colors.text_primary: "#171717"
colors.primary: "#533AFD"
radius.md: "8px"

# 模式3: 消费级暖色
colors.background: "#FFFFFF"
colors.primary: "#FF385C"
radius.pill: "9999px"       # 全局pill按钮
typography.font_sans: "Circular, Inter"

# 模式4: 极简奢侈
colors.background: "#FFFFFF"
colors.primary: "#000000"
radius.none: "0px"          # 全锐角
shadows: 完全禁用

# 模式5: 沉浸式暗色
colors.background: "#121212"
colors.surface: "#181818"
colors.primary: "#1ED760"
radius.pill: "9999px"
shadows.lg: "0 8px 24px rgba(0,0,0,0.5)"

# 模式6: 暖编辑AI
colors.background: "#FAF9F5"
colors.text_primary: "#141413"
colors.primary: "#CC785C"
typography.font_display: "Tiempos Headline, serif"
radius.md: "8px"
```
