# Data Components

CSS-only data-visualization micro-components for Swiss International social cards. No JS, no Canvas, no external charting libs. Every component encodes data through pure CSS dimensions (`width`, `height`, custom properties) and reads at 360px-wide mobile downscale.

All spacing tokens below assume the Swiss Carbon scale defined in `components.md` and shipped in `template-swiss-card.html`. Tokens not in that scale are defined inline as `--kpi-gap` / `--bar-gap`.

## KPI Tower

Vertical stacked metric blocks. Each block shows one key number, its unit, and a So What insight below. Use when you have 2–4 KPIs that belong together (monthly revenue, DAU, conversion, churn).

### CSS Spec

```css
--kpi-gap: 24px;

.kpi-stack {
  display: flex;
  flex-direction: column;
  gap: var(--kpi-gap);
}

.kpi-block {
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}

.kpi-block > .num-mega {
  /* .num-mega already defined in template: 200px, weight 200, sans */
}

.kpi-block > .t-meta {
  /* .t-meta already defined: 20px, weight 500, mono, uppercase */
  /* Use as unit label: "DAILY ACTIVE USERS", "CONVERSION RATE" */
}

.kpi-insight {
  font-family: var(--sans-zh);
  font-weight: 400;
  font-size: 24px;
  line-height: 1.4;
  color: var(--ink);
  margin: 0;
  /* Positioned directly below the unit */
}
```

### Usage

```html
<div class="kpi-stack">
  <div class="kpi-block">
    <p class="num-mega">132K</p>
    <p class="t-meta">DAILY ACTIVE USERS</p>
    <p class="kpi-insight">环比增长 12%,创近半年新高</p>
  </div>
  <div class="kpi-block">
    <p class="num-mega">3.4×</p>
    <p class="t-meta">TASK COMPLETION</p>
    <p class="kpi-insight">AI 辅助后任务完成速度提高了 3.4 倍</p>
  </div>
</div>
```

### Layout Rules

- 2–4 KPI blocks per tower, stacked vertically.
- `--kpi-gap: 24px` between blocks.
- Each `.kpi-insight` must be a factual, one-sentence So What — not a label definition.
- On `.poster.xhs`: limit to 2–3 blocks; 4 blocks with long insights under-fills the remaining canvas.
- On `.poster.wide`: pair with a right-column chart or matrix. Typical split: KPI tower 35% / chart 65%.
- On `.poster.square`: 2 blocks max.

## H-Bar Chart

Horizontal bar chart for rankings and comparisons. Each bar's width encodes a value via `--w:NN%`. Bars are 4px accent-gradient fill on a neutral track. No gridlines, no borders, no axis ticks — pure data ink.

### CSS Spec

```css
--bar-gap: 8px;

.h-bar-group {
  display: flex;
  flex-direction: column;
  gap: var(--bar-gap);
}

.h-bar-row {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: var(--sp-6);
  padding: var(--sp-3) 0;
}

.h-bar-row > .h-bar-track {
  position: relative;
  height: 4px;
  background: var(--grey-1);
  border-radius: 0;
  width: 100%;
}

.h-bar-row > .h-bar-track > .h-bar {
  position: absolute;
  left: 0;
  top: 0;
  height: 4px;
  border-radius: 2px;
  background: var(--accent);
  width: var(--w, 50%);
  /* Gradient depth: 0-100% maps to accent colour; no gradient banding */
}

.h-bar-row > .h-bar-val {
  font-family: var(--mono);
  font-weight: 500;
  font-size: 22px;
  letter-spacing: .04em;
  color: var(--ink);
  text-align: right;
  min-width: 64px;
}

.h-bar-baseline {
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  border-top: 1px dashed var(--grey-2);
  transform: translateY(-50%);
  pointer-events: none;
}

.h-bar-label {
  font-family: var(--sans-zh);
  font-weight: 400;
  font-size: 24px;
  color: var(--ink);
  grid-column: 1 / -1;
  margin: 0;
}
```

### Usage

```html
<div class="h-bar-group">
  <div class="h-bar-row">
    <p class="h-bar-label">Claude Code</p>
    <div class="h-bar-track">
      <div class="h-bar" style="--w:94%"></div>
    </div>
    <p class="h-bar-val">94%</p>
  </div>
  <div class="h-bar-row">
    <p class="h-bar-label">Cursor</p>
    <div class="h-bar-track">
      <div class="h-bar-baseline" style="--w:50%"></div>
      <div class="h-bar" style="--w:78%"></div>
    </div>
    <p class="h-bar-val">78%</p>
  </div>
  <div class="h-bar-row">
    <p class="h-bar-label">Linear</p>
    <div class="h-bar-track">
      <div class="h-bar-baseline" style="--w:50%"></div>
      <div class="h-bar" style="--w:62%"></div>
    </div>
    <p class="h-bar-val">62%</p>
  </div>
</div>
```

### Layout Rules

- 3–6 rows per chart. Hard max: 6 on 3:4 and 1:1; 10 on 21:9.
- Rows spaced `--bar-gap: 8px` apart (tighter than standard grid gaps — data-dense reading demands compression).
- Baseline line `.h-bar-baseline` is optional. Place at 50% for "below/above target" reading across multiple rows.
- No borders between rows. No gridlines. The bar itself is the only visual cue.
- On `.poster.xhs`: label sits above the track (stacked), not beside it. Template auto-handles this via single-column grid.
- On `.poster.wide`: label + track + value in a 3-column row.
- All values must be real or normalized to a real 100% reference. Never fabricate.

## Comparison Matrix

2×2 to 3×2 grid of cells, each comparing one metric across two context points (before/after, product A/B, this week/last week). Each cell carries a title, a large number, a delta arrow, and a one-line conclusion.

### CSS Spec

```css
.compare-matrix {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-5);
}

.compare-cell {
  background: var(--grey-1);
  padding: var(--sp-5);
  border-radius: 0;
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}

.compare-cell > .compare-title {
  font-family: var(--mono);
  font-size: 18px;
  font-weight: 500;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--grey-3);
  margin: 0;
}

.compare-cell > .num-xl {
  /* .num-xl already defined: 144px, weight 200, sans */
}

.compare-cell > .compare-change {
  font-family: var(--mono);
  font-size: 28px;
  font-weight: 600;
  line-height: 1;
}

.compare-cell > .compare-conclusion {
  font-family: var(--sans-zh);
  font-weight: 400;
  font-size: 22px;
  line-height: 1.4;
  color: var(--ink);
  margin: 0;
}

.change-up   { color: #16a34a; }
.change-up::before   { content: "↑ "; }

.change-down { color: #dc2626; }
.change-down::before { content: "↓ "; }

.change-flat { color: var(--grey-3); }
.change-flat::before { content: "→ "; }
```

### Usage

```html
<div class="compare-matrix">
  <div class="compare-cell">
    <p class="compare-title">01 · Weekly Active</p>
    <p class="num-xl">132K</p>
    <p class="compare-change change-up">+12.4%</p>
    <p class="compare-conclusion">连续五周正增长,新用户留存带动</p>
  </div>
  <div class="compare-cell">
    <p class="compare-title">02 · Task Completion</p>
    <p class="num-xl">68%</p>
    <p class="compare-change change-down">−3.2%</p>
    <p class="compare-conclusion">复杂任务比例上升,简单任务已完成饱和</p>
  </div>
  <div class="compare-cell">
    <p class="compare-title">03 · Avg Session</p>
    <p class="num-xl">24m</p>
    <p class="compare-change change-flat">+0.2%</p>
    <p class="compare-conclusion">基本持平,用户习惯已稳定</p>
  </div>
  <div class="compare-cell">
    <p class="compare-title">04 · Conversion</p>
    <p class="num-xl">8.2%</p>
    <p class="compare-change change-up">+1.8%</p>
    <p class="compare-conclusion">新的引导流程上线后首次突破 8%</p>
  </div>
</div>
```

### Layout Rules

- Grid: 2 columns default, 3 columns on `.poster.wide`.
- Gap: `var(--sp-5)` (16px).
- Each cell: `.compare-title` (mono label) + `.num-xl` (big number) + `.compare-change` with `change-up`/`change-down`/`change-flat` + `.compare-conclusion` (one-line So What).
- Arrow colours: green for ↑, red for ↓, grey for →. These are hard-coded semantic colours, not accent — do not theme them.
- All four components are required per cell. An empty conclusion reads as unfinished.
- Minimum 4 cells (2×2). Maximum 6 cells (3×2) on `.poster.wide`, 4 cells on `.poster.xhs` and `.poster.square`.
- Cells have equal height via grid. Do not mix this with the existing `.card-fill` system — `.compare-cell` is self-contained.
- Every conclusion must be factual. If you only have numbers and no interpretation, add the context row as a `.t-meta` instead of fabricating a conclusion.

## Mobile Readability (@360px)

All three components are designed to survive the 1080→360px downscale:

- `.num-mega` (200px) → ~67px on phone: still readable as a hero stat.
- `.num-xl` (144px) → ~48px on phone: comfortable for comparison grids.
- `.kpi-insight` (24px) → ~8px: **borderline**. Ensure the text colour has sufficient contrast against the background. On ultra-saturated accent backgrounds, bump the font-weight to 500 or add a `.card-fill` backing.
- `.h-bar` (4px) → ~1.3px on phone: visible as a thin line but the bar fill must have ≥0.60 contrast against its track. Test: squint at the 360px render — if the bar disappears, increase the track from `var(--grey-1)` to `var(--grey-2)`.
- `.compare-cell` conclusion (22px) → ~7px: the conclusion line is for web reading, not thumbnail decoding. If this is a cover page (P1), swap the conclusion for a larger `.t-meta` callout. On interior data pages (P3+), 22px is acceptable.

### Phone Adaptation

No JS media queries needed. The existing `.poster.xhs` overrides in the seed template already handle single-column stacking for H-Bar rows. For `.compare-matrix` on `.poster.xhs`, keep 2 columns — pushing to 1 column creates excessive vertical travel and breaks the comparison reading pattern.

### Always Run After Building Data Pages

1. Render the poster at 1080×1440.
2. View at 360px wide (browser zoom 33% or actual phone screenshot).
3. Verify: every number is decodable, every bar is visible, every conclusion is readable without zooming in.
4. If any component fails the squint test: increase contrast, bump font-weight, or simplify the component hierarchy.
