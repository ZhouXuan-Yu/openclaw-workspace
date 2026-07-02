# QA Checklist

Run this before final delivery.

## Dimensions

- Rednote images are `1080 x 1440`.
- WeChat 21:9 cover is `2100 x 900`.
- WeChat 1:1 cover is `1080 x 1080`.
- WeChat pair preview exists in the same HTML when WeChat covers are requested.
- File names are stable and ordered.

## Text

- No text overflows or touches the edge.
- No content collides with `.foot` / `.issue-strip`. If body copy or a closing line is overlapping the page footer, the footer is probably `position: absolute` while content above grew. Switch to flex `margin-top: auto` (see Anti-pattern C in `style-system.md`).
- Cover title is readable on a phone at thumbnail size.
- Body text is not smaller than it needs to be.
- Chinese line breaks are intentional.
- Important product names, English terms, and code snippets are spelled correctly.
- Captions match the source text; no invented facts.

## Layout

- Each page has one clear focal point.
- Pages do not all use the same structure.
- Lower empty space is either intentional or fixed.
- Images and screenshots align to the grid.
- Screenshot pages give the screenshot enough area.
- 1:1 WeChat cover uses a simplified short title and is composed separately, not blindly cropped.

### 4-band Density Check (3:4 only — run after render)

Open the rendered PNG. Mentally divide it into 4 horizontal bands of 360px each (0-25%, 25-50%, 50-75%, 75-100%). For each band, classify as:

- **Filled** — contains text, image, data, or rule.
- **Justified empty** — empty for a stated reason: hero-image breathing (M01/M16), single-sentence statement (M04/M13), leading/trailing margin (top 8% / bottom 8%).
- **Under-filled** — empty with no reason. **Any single under-filled band > 15% canvas height (>216px) is a fail.**

A poster passes when:

1. Total Filled + Justified empty ≥ 100%.
2. Filled bands cover ≥ 75% canvas height (≥ 1080px of 1440px).
3. No two adjacent bands are both "justified empty" — that creates a >25% void mid-poster.

If failing: don't shrink the canvas, don't add decorative blobs. Either expand copy (more ledger items, longer paragraphs, supporting evidence row, marginalia column) or switch recipe (M07 → M04 for genuinely-short content; M03 → M11 to add a marginal column; thin ledger → M08 Tall Ledger with bigger rows).

## Style

- Package uses one visual system.
- Swiss identity test passes for every Swiss poster (see `style-system.md` "Style Identity Test"). In particular: every display title >=72px uses a typed class with weight <=300; no serif font is loaded; only one accent color is used. A bold 90px headline is not Swiss.
- Editorial identity test passes for every Editorial poster: at least one atmosphere layer beyond a flat fill (paper grain / ink wash / WebGL); serif display family on the title; at least one of large photo well, serif pull quote, marginalia column, or true ledger structure. A flat paper with serif title + mono pills everywhere is Swiss-in-disguise.
- Swiss uses one accent color only.
- Magazine style uses restrained paper/ink tones.
- No random SVG blobs, ovals, drops, circles, stickers, or decorative gradients.
- No nested cards.
- No excessive rounded corners.

## Images

- Supplied images are not distorted.
- Faces, hardware, product UI, and key text are not accidentally cropped.
- Screenshots remain readable.
- Generated images do not contain unwanted text, logos, page numbers, or poster borders.
- Photo crops feel intentional.
- For any image fetched from the web (Pexels / Unsplash / Flickr CC / Wallhaven / direct search): the source URL is recorded in `assets/SOURCES.md`, and the user has been asked whether to add an in-image attribution caption. The user's answer is honored. Flickr CC attribution preserves the author name when the user opts in.

## Text-On-Image (when applicable)

Run these only for posters where text touches a photo (full-bleed cover, large image well, generated overlay). See `references/image-overlay.md`.

- Image area ≥60% of canvas → the photo passes the quiet-zone + light tests; no-mask composition was tried first; any tint is localized, image-toned, and only used if the thumbnail check fails.
- Subject map is documented as an HTML comment next to the hero block (face / focal feature location + safe zones).
- No display title (≥72 px) overlaps a face, hand, or key product feature.
- `object-position` was chosen from the subject-location table, not left at default for face shots.
- Thumbnail test: downscale the rendered PNG to 360 px wide and confirm the title is still legible without strain.

## Final Response

- Include the output path.
- Show the main cover inline when useful.
- Mention verification performed.
- Mention any limitations, such as low-resolution source assets.

## Data Density Checks (D1-D7)

Run these for every data-heavy Swiss poster (S13/S14/S15 or any poster with `.num-mega`, `.h-bar`, `.compare-matrix`, `.kpi-insight`). Append to the standard checklist above.

### D1 — SO WHAT present?

Every data poster has at least one `.kpi-insight`, `.compare-conclusion`, or explicit takeaway sentence. No orphan numbers.

### D2 — ≥3 typographic layers?

Count distinct type roles. A poster with only `.num-mega` + `.t-cat` has 2 layers — add a body/insight/conclusion layer.

### D3 — No chartjunk?

- No gridlines, axis ticks, or data labels on bars (`.h-bar-val` is the label).
- No unnecessary borders around data cells.
- No decorative backgrounds behind numbers.
- Every pixel serves data or readability.

### D4 — Data source explicit?

- Real data: source noted in design brief or page comment.
- Hypothetical/demo: marked as "illustrative" in metadata.
- Never present fabricated data as real.

### D5 — 360px readable?

Squint-test each `.num-mega`, `.h-bar`, `.num-xl`, `.compare-change`. If any data-carrying element disappears at phone width (~360px), increase contrast or weight.

### D6 — ≥75% canvas filled?

Run the 4-band density check above. Content must cover ≥3 bands with no single under-filled band >216px.

### D7 — Spacing not crowded?

Check each `--kpi-gap`/`--bar-gap`/grid gap. If two adjacent KPI blocks blur together, increase `--kpi-gap` by 8px. If H-Bar rows look like a solid block, increase `--bar-gap` by 4px.

Any FAIL → fix the page plan before final delivery.
