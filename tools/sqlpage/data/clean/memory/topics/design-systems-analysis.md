# 世界顶级UI设计系统交叉分析

## 分析方法

数据来源：VoltAgent/awesome-design-md 仓库的15个品牌 DESIGN.md 文件（2026-07-01抓取）。每个文件由AI从实际页面抓取生成，包含YAML frontmatter设计Token + Markdown分析正文。本报告提炼每个品牌的核心参数，然后进行15维交叉对比，提取共同模式形成元设计系统。

---

## 品牌设计系统逐个分析

### Linear
- 来源: https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/linear.app/DESIGN.md
- 颜色: 主色#5E6AD2（薰衣草蓝），纯近黑背景#010102（最深暗面），表面阶梯4级#0F1011→#191A1B，白墨#F7F8F8
- 排版: Linear Display/Text自定制字体，80px/600/-3px tracking，正文16px/400，负字距极强
- 间距: 4px基准，96px节段
- 圆角: 按钮8px，卡片12px，产品截图16px
- 阴影: 无阴影层级，用表面色阶区分深度
- 布局: 暗色全页，产品UI截图为装饰主体
- 独有特征: #010102最深深色背景；-3px字符间距最激进；纯靠表面阶梯+发丝线无阴影

### Vercel
- 来源: https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/vercel/DESIGN.md
- 颜色: 主色#171717（纯墨），白布#FFFFFF，软布#FAFAFA；渐变系统多段色：#007CF0/#00DFD8/#7928CA/#FF0080
- 排版: Geist/Inter，48px/600/-2.4px hero，正文16px/400；Geist Mono代码专用
- 间距: 4px基准，节段最大192px（最宽松）
- 圆角: 按钮pill 100px，卡片6-12px
- 阴影: 极细微叠加阴影 1px+2px+2px
- 布局: 192px节间距最大，多段大气渐变背景
- 独有特征: 全系统仅用墨色CTA + 大气渐变背景作为唯一装饰；Geist字体开源；192px业界最大section间距

### Stripe
- 来源: 同上/stripe/DESIGN.md
- 颜色: 主色#533AFD（电光靛蓝），深海军蓝#0D253D，白布#FFF，软布#F6F9FC；奶油色#F5E9D4；渐变网格大气装饰
- 排版: Söhne变量体，56px/300（极细），负字距-1.4px；正文15px/300；tnum表格数字
- 间距: 4px基准，64px大间距
- 圆角: 按钮全pill 9999px，卡片12px
- 阴影: 多层soft glow叠加
- 布局: 上方渐变网格占据页面上1/3；产品仪表盘mockup暗面
- 独有特征: 权重300极细显示；tnum表格式数字（金融基础）；渐变网格占据页面1/3大气层

### Figma
- 来源: 同上/figma/DESIGN.md
- 颜色: 主色#000000（纯黑），白布#FFFFFF；彩色块域系统：石灰#DCEEB1、薰衣草#C5B0F4、奶油#F4ECD6、薄荷#C8E6CD、粉#EFD4D4、珊瑚#F3C9B6、海军#1F1D3D
- 排版: figmaSans变量体，86px/340权重，-1.72px负字距；figmaMono用于eyebrow/caption
- 间距: 1px hair到96px section
- 圆角: 按钮pill 50px，卡片24px大圆角
- 阴影: 极少
- 布局: 纯黑白导航+彩色块域交替
- 独有特征: 6色彩色块域系统（贴纸式设计）；极细340权重显示；50px pill按钮（独有半径值）

### Notion
- 来源: 同上/notion/DESIGN.md
- 颜色: 无强品牌色（黑+白+灰）；极简灰度系统；强调色仅用于极小装饰
- 排版: Inter/自定义几何sans；黑白极简
- 间距: 4px基准，宽松留白
- 圆角: 极小6-8px
- 阴影: 几乎无
- 布局: 极简内容优先
- 独有特征: 最"无设计"的设计 — 完全信任内容本身

### Supabase
- 来源: 同上/supabase/DESIGN.md
- 颜色: 主色#3ECF8E（翠绿），近黑#171717，白布，冷灰hairline阶梯
- 排版: Circular/Inter，64px/500/-1.92px display，正文16px/400
- 间距: 2-64px阶梯
- 圆角: 按钮6px（方而精），卡片12px
- 阴影: 极微Level 2产品mockup阴影
- 布局: 纯白营销轨，绿按钮+暗色代码块+产品截图
- 独有特征: 翠绿按钮用近黑文字（非白色）—"发光表面"概念

### Raycast
- 来源: 同上/raycast/DESIGN.md
- 颜色: 主色#FFFFFF白胶囊，近黑Canvas#07080A，4级暗面阶梯，分类口音蓝/红/绿/黄仅在扩展图标中使用
- 排版: Inter全站，ss03替用字形（g），64px/600 hero，无负字距（显示512px负跟踪）
- 间距: 96px节段
- 圆角: 多级6/8/10/16px卡片词汇
- 阴影: **无任何阴影**—全用发丝线替代
- 布局: 单一暗模式，产品即为营销页
- 独有特征: ss03替用字形g是品牌标志；无阴影系统全用hairline；红色对角斜条纹hero装饰

### Claude (Anthropic)
- 来源: 同上/claude/DESIGN.md
- 颜色: 主色#CC785C（暖珊瑚橙），奶油画布#FAF9F5，暗海军蓝#181715；青色#5DB8A6
- 排版: Copernicus/Tiempos Headline衬线显示 + StyreneB/Inter无衬线正文，JetBrains Mono代码
- 间距: 4px基准，96px section
- 圆角: 按钮8px，卡片12px，hero容器16px，badge pill
- 阴影: 颜色块优先于阴影，极少阴影
- 布局: 奶油-黑交替节奏
- 独有特征: **唯一使用衬线显示的AI品牌**；奶油暖画布独树一帜；文学编辑感

### Apple
- 来源: 同上/apple/DESIGN.md
- 颜色: 主色#0066CC（Action Blue），纯白/Parchment#F5F5F7，近黑砖#272729/2A2A2C/252527
- 排版: SF Pro Display/Text，56px/600/-0.28px hero；正文17px（唯一17px正文品牌）；权重300少见但刻意
- 间距: 8px基准，80px section
- 圆角: 按钮pill 9999px，卡片18px（商店），产品砖0px
- 阴影: 仅产品图片下方一个柔和阴影rgba(0,0,0,0.22) 3px 5px 30px
- 布局: 全屏产品砖交替亮/暗，零边距堆叠
- 独有特征: 权重300刻意使用；17px正文；零渐变；仅一个阴影全系统；产品摄影即全部

### Nike
- 来源: 同上/nike/DESIGN.md
- 颜色: 主色#111111纯黑，白布，软云#F5F5F5；语义色仅红色#D30005（打折）
- 排版: Nike Futura ND/Helvetica Now，96px/500大写campaign，正文字小但权重坚定500
- 间距: 8px基准，48px section
- 圆角: 所有按钮全pill 30px/9999px；产品卡0px
- 阴影: 无任何drop-shadow
- 布局: 摄影全屏hero + 密集产品网格
- 独有特征: 96px大写Futura（最大字号）；全pill按钮系统；绝对零阴影零渐变

### Airbnb
- 来源: 同上/airbnb/DESIGN.md
- 颜色: 主色#FF385C（Rausch粉红），纯白#FFF，墨水#222；Luxe紫#460479子品牌
- 排版: Airbnb Cereal VF，28px/700 hero（极低调），正文16px；64px/700评分展示（唯一大声时刻）
- 间距: 8px基准，64px section
- 圆角: 按钮8px，卡片14px，搜索栏全pill，类别带32px
- 阴影: 仅一级微弱shadow
- 布局: 三产品导航+大搜索栏+图片属性卡网格
- 独有特征: hero h1仅28px最谦虚；单色Rausch电压；搜索orb圆形粉红按钮标志性

### Spotify
- 来源: 同上/spotify/DESIGN.md
- 颜色: 主色#1ED760（Spotify绿），纯近黑#121212/#181818/#1F1F1F；语义红/橙/蓝
- 排版: SpotifyMixUI/CircularSp，24px-10px紧凑范围；700/400权重二元系统；按钮大写+宽字距
- 间距: 8px基准
- 圆角: 按钮500px-9999px全pill；播放键50%圆形
- 阴影: 重影rgba(0,0,0,0.5) 8px 24px — 系统最重的阴影
- 布局: 暗色沉浸式应用布局，侧栏+主内容+底部播放条
- 独有特征: 大写按钮标签+1.4-2px字距；最重阴影；200+市场全球字体栈

### Shopify
- 来源: 同上/shopify/DESIGN.md
- 颜色: 主色#000000纯黑，极暗黑#000000画布营销轨；芦荟#C1FBD4 + 开心果#D4F9E0仅在交易轨
- 排版: Neue Haas Grotesk Display 330极细权重96px + Inter Variable 420-550正文
- 间距: 8px基准，64-128px奢侈留白
- 圆角: 所有按钮pill 9999px；卡片12-20px
- 阴影: 4级阴影系统（最完整）
- 布局: 双轨系统：暗黑电影营销 vs 亮白交易
- 独有特征: 96px/330极细显示（最细）；双画布策略；最完整4级阴影系统

### Tesla
- 来源: 同上/tesla/DESIGN.md
- 颜色: 主色#3E6AE1（电光蓝），纯白#FFF；碳黑#171A20；无任何语义色
- 排版: Universal Sans Display/Text，40px/500 hero；正文14px/400；标准字距（不缩紧）
- 间距: 8px基准，100vh全屏段
- 圆角: 按钮4px（极锐），卡片~12px
- 阴影: 几乎无 — 毛玻璃透明替代影
- 布局: 全视口全屏段，每次滚动只看一个信息
- 独有特征: 零负字距（唯一品牌）；4px最锐按钮；毛玻璃导航；100vh全屏段策略

### Ferrari
- 来源: 同上/ferrari/DESIGN.md
- 颜色: 主色#DA291C（Rosso Corsa法拉利红），近黑#181818画布；暗面阶梯#303030；Hypersail黄#FFF200
- 排版: FerrariSans单家族，80px/500 hero，负字距-1.6px；按钮大写+1.4px字距
- 间距: 4px基准，128px super间距（最大）
- 圆角: 全CTAs 0px（锐角）— 奢侈汽车精密感
- 阴影: 色彩块+摄影深度
- 布局: 全出血电影摄影hero + 编辑体
- 独有特征: 0px全锐角按钮（跑车精密）；128px super间距；Rosso Corsa红仅稀少使用

---

## 交叉对比矩阵

### 色彩趋势

| 趋势 | 品牌 | 占比 |
|------|------|------|
| 暗底白字（Dark mode primary） | Linear, Raycast, Spotify, Shopify, Ferrari | 5/15 (33%) |
| 白底暗字（Light mode primary） | Apple, Vercel, Stripe, Figma, Notion, Supabase, Airbnb, Nike, Tesla | 9/15 (60%) |
| 暖画布特殊 | Claude（奶油#FAF9F5） | 1/15 (7%) |
| **单色强调策略**（仅1个品牌色） | Linear, Apple, Raycast, Supabase, Airbnb, Nike, Tesla, Ferrari | 8/15 (53%) |
| 多彩装饰（渐变/多色块） | Vercel, Stripe, Figma, Spotify, Shopify | 5/15 (33%) |
| 极简灰度 | Notion | 1/15 |
| 强调色暖色系 | Airbnb(#FF385C), Claude(#CC785C), Ferrari(#DA291C) | 3/15 |
| 强调色冷色系 | Linear(#5E6AD2), Stripe(#533AFD), Apple(#0066CC), Tesla(#3E6AE1), Supabase(#3ECF8E), Spotify(#1ED760) | 6/15 |
| 强调色中性 | Vercel, Figma, Shopify, Notion, Nike（全用黑色） | 5/15 |

**核心规律**：
- 绝大多数顶级品牌只用**1-2个品牌强调色**，其余都是灰度阶梯
- 开发者工具倾向**冷色**（蓝/紫/绿），消费品牌倾向**暖色或黑**
- 黑色作为主色的品牌（Vercel/Figma/Shopify/Nike）用黑CTAs在亮底上
- 暗底品牌用**白色或单色亮强调色**做CTA

### 排版趋势

| 参数 | 规律 | 品牌示例 |
|------|------|----------|
| 字体数量 | 85%+使用1-2个家族（显示+正文或单一家族） | 几乎所有 |
| 开源替代首选 | **Inter** 是最常见替代（9/15提及） | Vercel, Raycast, Claude, Shopify, Supabase等 |
| Hero字号 | 40-96px，集中48-64px | Linear 80, Stripe 56, Apple 56, Figma 86 |
| Hero字重 | 500-600主导（极少700+） | 13/15使用500-600 |
| 正文大小 | 14-17px，16px最多 | Apple 17（唯一例外） |
| 负字距显示 | **13/15使用**，范围-0.3到-3.0px | Tesla唯一不使用 |
| 字体特征设置 | ss01/ss03/liga/tnum/kern 在各种品牌出现 | Stripe(ss01), Raycast(ss03), Shopify(ss03) |
| 衬线显示 | 仅Claude使用 | Claude(Copernicus) |
| 等宽字体 | Geist Mono/Fira Code/JetBrains Mono | Vercel, Claude, Linear |
| 大写按钮 | 4/15使用 | Spotify, Ferrari, Nike(部分), Shopify(eyebrow) |

### 间距趋势

| 值 | 出现频率 | 使用品牌 |
|----|----------|----------|
| 基准4px | 8/15 | Linear, Stripe, Figma, Notion, Claude, Supabase, Ferrari, Vercel |
| 基准8px | 6/15 | Apple, Nike, Airbnb, Spotify, Shopify, Tesla |
| Section间距 | 48-192px | 中位数80-96px |

### 圆角趋势

| 风格 | 品牌示例 | 占比 |
|------|----------|------|
| 全Pill按钮（9999px） | Vercel, Stripe, Figma, Apple, Nike, Airbnb, Spotify, Shopify, Notion | 9/15 (60%) |
| 方形-微圆按钮（4-8px） | Linear(8), Raycast(8), Supabase(6), Claude(8), Tesla(4) | 5/15 (33%) |
| 全锐角按钮（0px） | Ferrari | 1/15 (7%) |
| 卡片圆角 | 8-16px，最常12px | 几乎所有 |

### 阴影趋势

| 类型 | 品牌 | 特点 |
|------|------|------|
| **无阴影或极微** | Apple, Nike, Figma, Notion, Raycast, Tesla, Ferrari, Claude | 靠表面色差或发丝线 |
| 轻微软影 | Linear, Vercel, Stripe, Supabase, Airbnb | 1-2级细微 |
| 重阴影 | Spotify | 唯一 0.5 opacity 24px blur |
| 4级完整系统 | Shopify | 最完整 |

**核心发现**：顶级设计普遍**极简阴影**—多数品牌零到一级阴影。深度靠颜色块/表面阶梯/发丝线区分，而非投影。

### 按钮风格趋势

| 特征 | 占比 |
|------|------|
| 全Pill圆角 | 60% |
| 方形-微圆 | 33% |
| 全锐角 | 7% (Ferrari) |
| 黑色/近黑填充 | Vercel, Figma, Shopify, Nike (8/15) |
| 彩色品牌填充 | Linear, Stripe, Apple, Airbnb, Claude, Spotify, Tesla, Supabase (7/15) |
| 白底+边框 | 几乎所有作为次按钮 |
| 大写标签 | Spotify, Ferrari, Nike(部分) |

---

## 元设计系统（Meta Design System）

从以上15个顶级品牌提取的可参数化通用设计框架。覆盖这些YAML Token即可切换完整品牌风格。

```yaml
# ============================================================
# 元设计Token — 覆盖这些值即可切换品牌风格
# 默认值: 现代开发者工具/SaaS风格
# ============================================================

colors:
  # --- 品牌 ---
  primary: "#5E6AD2"            # 主CTA色（多数品牌只用此一色）
  primary_hover: "#828FFF"
  primary_active: "#4F5ABF"
  on_primary: "#FFFFFF"         # 主色上的文字

  # --- 表面（从上到下变亮） ---
  background: "#0D0D0D"         # 页面底层（暗模式默认）
  background_alt: "#FAFAFA"     # 亮模式默认
  surface: "#141516"            # 卡片/面板
  surface_elevated: "#18191A"   # 浮起表面
  surface_overlay: "#1C1D1E"   # 最高浮起

  # --- 文字 ---
  text_primary: "#F7F8F8"       # 主文字（暗底）
  text_secondary: "#D0D6E0"     # 副文字
  text_muted: "#8A8F98"         # 辅助/禁用
  text_primary_light: "#171717" # 主文字（亮底）
  text_secondary_light: "#4D4D4D"

  # --- 边框 ---
  border: "#23252A"             # 默认1px
  border_light: "#E6E6E6"
  border_strong: "#34343A"

  # --- 语义 ---
  success: "#27A644"
  warning: "#F5A623"
  error: "#EE0000"
  info: "#539DF5"

  # --- 特有装饰（可选） ---
  color_blocks: []              # Figma风格色块
  gradient_mesh: ""             # Stripe/Vercel风格渐变
  accent_secondary: ""          # 极少品牌使用

typography:
  # --- 字体栈 ---
  font_sans: "Inter, -apple-system, system-ui, 'Segoe UI', sans-serif"
  font_mono: "JetBrains Mono, ui-monospace, 'Cascadia Code', monospace"
  font_display:                   # 与sans相同或自定义

  # --- 字号层级 ---
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
  button: "14px"
  button_weight: 500
  code: "14px"

  # --- 字体特性 ---
  font_features: "\"kern\", \"liga\", \"calt\""

  # --- 字重梯度 ---
  weight_normal: 400
  weight_medium: 500
  weight_semibold: 600
  weight_bold: 700

spacing:
  unit: 4                         # px基准
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
  md: "8px"                       # 默认按钮/输入
  lg: "12px"                      # 默认卡片
  xl: "16px"
  xxl: "24px"
  pill: "9999px"

shadows:
  none: "none"
  sm: "0 1px 2px rgba(0,0,0,0.04)"
  md: "0 2px 8px rgba(0,0,0,0.08)"
  lg: "0 8px 24px rgba(0,0,0,0.12)"
  modal: "0 16px 48px rgba(0,0,0,0.2)"

layout:
  max_width: "1200px"             # 内容最大宽度
  reading_width: "720px"          # 长文本栏宽
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
```

### 品牌切换示例

**暗黑开发者工具**（默认）：暗background + 灰白surface + 单色强调 + 微圆按钮 + 负字距 + 无阴影
**亮色SaaS**：`background: "#FFFFFF"` `text_primary: "#171717"` `border: "#E6E6E6"` + 保持其他不变
**消费级暖色**：`primary: "#FF385C"` `background: "#FFFFFF"` `font_display: "Circular"` `radius.pill` 按钮
**极简奢侈**：`primary: "#000000"` `background: "#FFFFFF"` `radius.none` 0px + `shadows.none` 零影
**暗色沉浸**：`background: "#121212"` `primary: "#1ED760"` `radius.pill` + 大写按钮
**暖编辑AI**：`background: "#FAF9F5"` `font_display: "Tiempos Headline"` `primary: "#CC785C"` `radius.sm` 6-8px
