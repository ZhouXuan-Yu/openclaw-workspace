# Density Gate

Mandatory quality gate executed between Step 4 (Plan Pages) and Step 5 (Build and Render) in SKILL.md. The gate forces a deliberate composition check before any HTML is written.

## Gate Position in Workflow

```
Step 4: Plan Pages → Density Gate (4a) → Step 4.5: Copy Seed Template → Step 5: Build
```

If the density gate fails, **stop and redesign the page plan**. Do not proceed to template copy and render.

## Phase 1 — Plan Audit (before writing HTML)

After the internal page plan is written and before `Step 4.5: Copy The Seed Template`, fill this template for every poster in the set:

```text
[DENSITY GATE] Poster: xhs-NN / Recipe: SXX
  Info zones:  [count, e.g. 3: kicker + title + data-grid]
  Hero:sidebar ratio: [e.g. none / 35:65 / full-bleed]
  Chart plan:  [none / S09 KPI Tower / S10 H-Bar / S14 H-Bar / S15 Matrix]
  Component hierarchy: [list: .num-mega → .t-meta → .kpi-insight → .compare-cell ...]
  SO WHAT:     [one sentence — what this page proves]
```

### Plan-Audit Gate Rules

| Field | Requirement |
|-------|-------------|
| Info zones | Must be ≥2. Single-zone posters (one giant number, nothing else) are M04/M13 territory — not data-density. |
| SO WHAT | Must be a claim, not a description. "Shows revenue is up" fails. "Revenue grew 12% driven by new-user retention — the acquisition channel is working" passes. |
| Chart plan | If `none` and the page claims to be data-driven: add a component or rename the page as a narrative page (S01/S03/S05). A data page with no data component is a contradiction. |
| Component hierarchy | Must list ≥3 distinct typographic layers (e.g. `.num-mega` + `.t-meta` + `.kpi-insight`). Single-layer data pages read as unfinished infographics. |

## Phase 2 — Pre-Render Checklist (7 items)

Before opening the HTML file, answer these 7 questions for each data-heavy poster:

| # | Check | Pass criteria |
|---|-------|---------------|
| 1 | **SO WHAT present?** | Every data poster has at least one `.kpi-insight`, `.compare-conclusion`, or explicit takeaway sentence. No orphan numbers. |
| 2 | **≥3 typographic layers?** | Count distinct type roles on the poster. A poster with only `.num-mega` + `.t-cat` has 2 layers — add a body/insight/conclusion layer. |
| 3 | **No chartjunk?** | No gridlines, no axis ticks, no data labels on bars (the `.h-bar-val` already is the label), no unnecessary borders around data cells, no decorative backgrounds behind numbers. Every pixel serves data or readability. |
| 4 | **Data source explicit?** | Real data: source noted in the design brief or page comment. Hypothetical/demo: marked as "illustrative" in metadata. Never present fabricated data as real. |
| 5 | **360px readable?** | Squint-test each `.num-mega`, `.h-bar`, `.num-xl`, `.compare-change`. If any data-carrying element disappears at phone width, increase contrast or weight. |
| 6 | **≥75% canvas filled?** | Run the 4-band density check from `qa-checklist.md`. Content must cover ≥3 bands with no single under-filled band >216px. |
| 7 | **Spacing not crowded?** | Check each `--kpi-gap`/`--bar-gap`/grid gap: is every data cluster visually separable? If two adjacent KPI blocks blur together, increase `--kpi-gap` by 8px. If H-Bar rows look like a solid block, increase `--bar-gap` by 4px. |

Any FAIL → fix the page plan before rendering.

## Data-Ink Ratio (qualitative)

Tufte's data-ink ratio: "erase non-data-ink, within reason." We apply this as a qualitative sniff test, not a pixel calculation.

### Check

For each data poster, ask: **"Does every pixel on this canvas serve data communication?"**

Pixels that serve data:
- Numbers, labels, bars, cell fills encoding values, conclusions, source citations.
- Hairline rules that separate data clusters.
- Typographic hierarchy that guides reading order.

Pixels that do not serve data:
- Decorative dots, abstract rings, cross-mats behind KPI numbers.
- Gradient fades on bars (`.h-bar` is flat accent — that's the spec).
- Card backgrounds with no data content (empty `.compare-cell`).
- "Empty row" spacers thicker than 16px between data clusters.

### Anti-Patterns

| Pattern | Detection | Fix |
|---------|-----------|-----|
| **Bar chart with gridlines** | Visible vertical/horizontal lines inside `.h-bar-track` | Remove. The track is already grey-1, the bar is accent — that's the only visual axis needed. |
| **KPI number on accent background with no So What** | `.num-mega` inside `.card-accent`, nothing below | Add `.kpi-insight` in accent-on colour below the unit. |
| **Matrix cell with number but no delta** | `.compare-cell` with `.num-xl` and conclusion, missing `.compare-change` | The delta is the comparison. Without it, it's just a stat card — use S12 Matrix Fill instead. |
| **Duplicate data labels** | Both `.h-bar-val` (number) and a second label inside the bar | `.h-bar-val` is the only label. The bar carries no text. |
| **3 KPI blocks in a tower with identical `--kpi-gap` but different content lengths** | Visual rhythm broken by unequal text wrap | Equalize: either all blocks have 1-line insights, or all have 2-line. Mixed lengths create a "missing content" illusion. |
| **Bar chart with no baseline** | 5+ bars all at 60-90%, no reference | Add one `.h-bar-baseline` at the median or at a meaningful threshold (50%, target, industry avg). |

## Integration with Existing QA

After render, the standard QA checklist (`qa-checklist.md`) already covers the 4-band density check. The Density Gate adds the pre-render audit — catching structural problems before pixels exist. Together they form:

```
Plan Audit (density-gate.md) → Build → Render → 4-Band Check (qa-checklist.md) → Deliver
```

### Quick Reference for Build Step

When building a Swiss data page, open the HTML and confirm before `<style>` closure:

```text
□ .kpi-insight defined (if using KPI Tower)
□ .h-bar-group carries --bar-gap token
□ .compare-matrix has exactly 4 or 6 cells
□ .change-up / .change-down / .change-flat classes used (not inline colour)
□ No empty cells in matrix
□ Baseline line present on ≥5-row bar charts
```

If any checkbox fails, the gate is not cleared — go back to plan phase.
