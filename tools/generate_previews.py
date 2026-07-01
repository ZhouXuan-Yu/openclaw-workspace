#!/usr/bin/env python3
"""Batch generate preview.html from DESIGN.md YAML front matter — v2 robust."""
import yaml
import re
import os
from pathlib import Path

TEMPLATES_DIR = Path(r"E:\Obsidian仓库\ZhouXuan私人领域\顶级UI设计\templates")

def parse_design_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Extract between first --- and second ---
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    front = parts[1].strip()
    try:
        return yaml.safe_load(front)
    except yaml.YAMLError:
        # Fix common issues: quoted values with colons, problematic chars
        front = re.sub(r'(description|note|summary):\s*"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)"',
                       r'\1: "..."', front)
        try:
            return yaml.safe_load(front)
        except:
            return None

def extract_tokens(data):
    tk = {}
    c = data.get('colors', {}) if data else {}
    # Find primary — try many possible key names
    primary_keys = ['primary', 'accent', 'brand-primary', 'brandColor', 'accent-color']
    for k in primary_keys:
        if k in c and c[k]:
            tk['primary'] = str(c[k]).strip('"\'')
            break
    if 'primary' not in tk:
        tk['primary'] = '#333333'

    bg_keys = ['canvas', 'background', 'page-bg', 'bg', 'background-color']
    for k in bg_keys:
        if k in c and c[k]:
            tk['bg'] = str(c[k]).strip('"\'')
            break
    if 'bg' not in tk:
        tk['bg'] = '#FFFFFF'

    surface_keys = ['surface-1', 'surface_1', 'surface', 'card-bg', 'bg-elevated', 'surface-primary']
    for k in surface_keys:
        if k in c and c[k]:
            tk['surface'] = str(c[k]).strip('"\'')
            break
    if 'surface' not in tk:
        tk['surface'] = _is_dark(tk['bg']) and '#1A1A1A' or '#F5F5F5'

    surface2_keys = ['surface-2', 'surface_2', 'surface-elevated', 'bg-overlay', 'surface-secondary']
    for k in surface2_keys:
        if k in c and c[k]:
            tk['surface2'] = str(c[k]).strip('"\'')
            break
    if 'surface2' not in tk:
        tk['surface2'] = _is_dark(tk['bg']) and '#222222' or '#EEEEEE'

    text_keys = ['ink', 'text-primary', 'body', 'text', 'text-color']
    for k in text_keys:
        if k in c and c[k]:
            tk['text'] = str(c[k]).strip('"\'')
            break
    if 'text' not in tk:
        tk['text'] = _is_dark(tk['bg']) and '#F5F5F5' or '#1A1A1A'

    text2_keys = ['ink-muted', 'ink-secondary', 'text-secondary', 'text-muted', 'secondary-text']
    for k in text2_keys:
        if k in c and c[k]:
            tk['text_secondary'] = str(c[k]).strip('"\'')
            break
    if 'text_secondary' not in tk:
        tk['text_secondary'] = _is_dark(tk['bg']) and '#888888' or '#666666'

    text3_keys = ['ink-subtle', 'ink-tertiary', 'text-tertiary', 'text-subtle']
    for k in text3_keys:
        if k in c and c[k]:
            tk['text_subtle'] = str(c[k]).strip('"\'')
            break
    if 'text_subtle' not in tk:
        tk['text_subtle'] = '#999999'

    border_keys = ['hairline', 'border', 'divider', 'border-color']
    for k in border_keys:
        if k in c and c[k]:
            tk['border'] = str(c[k]).strip('"\'')
            break
    if 'border' not in tk:
        tk['border'] = _is_dark(tk['bg']) and '#333333' or '#E0E0E0'

    border_strong_keys = ['hairline-strong', 'border-strong', 'hairline_strong']
    for k in border_strong_keys:
        if k in c and c[k]:
            tk['border_strong'] = str(c[k]).strip('"\'')
            break
    if 'border_strong' not in tk:
        tk['border_strong'] = _is_dark(tk['bg']) and '#555555' or '#CCCCCC'

    on_primary_keys = ['on-primary', 'on_primary']
    for k in on_primary_keys:
        if k in c and c[k]:
            tk['on_primary'] = str(c[k]).strip('"\'')
            break
    if 'on_primary' not in tk:
        tk['on_primary'] = '#FFFFFF'

    success_keys = ['success', 'semantic-success', 'green']
    for k in success_keys:
        if k in c and c[k]:
            tk['success'] = str(c[k]).strip('"\'')
            break
    if 'success' not in tk:
        tk['success'] = '#27A644'

    error_keys = ['error', 'semantic-error', 'red', 'danger']
    for k in error_keys:
        if k in c and c[k]:
            tk['error'] = str(c[k]).strip('"\'')
            break
    if 'error' not in tk:
        tk['error'] = '#EE0000'

    warning_keys = ['warning', 'yellow']
    for k in warning_keys:
        if k in c and c[k]:
            tk['warning'] = str(c[k]).strip('"\'')
            break
    if 'warning' not in tk:
        tk['warning'] = '#F5A623'

    # Typography
    t = data.get('typography', {}) if data else {}
    tk['font_display'] = _find_font(t, ['display-xl', 'display-lg', 'display-md', 'hero-display', 'display', 'h1', 'heading-xl', 'headline'])
    tk['font_body'] = _find_font(t, ['body', 'body-md', 'body-lg', 'text', 'paragraph'])
    tk['h1_size'] = _find_size(t, ['display-xl', 'display-lg', 'hero-display', 'display', 'h1'])
    tk['h2_size'] = _find_size(t, ['display-md', 'display-sm', 'heading-xl', 'h2'])
    tk['h3_size'] = _find_size(t, ['headline', 'heading-lg', 'h3'])
    tk['body_size'] = _find_size(t, ['body', 'body-md', 'body-lg', 'text', 'paragraph'])

    return tk

def _find_font(typography, keys):
    for k in keys:
        v = typography.get(k, {})
        if isinstance(v, dict) and v.get('fontFamily'):
            return str(v['fontFamily']).strip('"\'')
    return "Inter, -apple-system, sans-serif"

def _find_size(typography, keys):
    for k in keys:
        v = typography.get(k, {})
        if isinstance(v, dict) and v.get('fontSize'):
            return str(v['fontSize']).strip('"\'')
    return '16px'

def _is_dark(hex_color):
    hex_color = hex_color.lstrip('#').strip('"\'')
    try:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return (r * 0.299 + g * 0.587 + b * 0.114) < 128
    except:
        return False

def _rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#').strip('"\'')
    try:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f'rgba({r},{g},{b},{alpha})'
    except:
        return f'rgba(0,0,0,{alpha})'

def _swatch(name, hex_color):
    return f'''<div class="swatch">
      <div class="swatch-color" style="background:{hex_color}"></div>
      <div class="swatch-info">
        <div class="swatch-name">{name}</div>
        <div class="swatch-hex">{hex_color}</div>
      </div>
    </div>'''

def generate_preview_html(brand, tk):
    is_dark_bg = _is_dark(tk['bg'])
    mood = 'Dark Theme' if is_dark_bg else 'Light Theme'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{brand} · Design Preview</title>
<style>
  :root {{
    --p: {tk['primary']};
    --bg: {tk['bg']};
    --surface: {tk['surface']};
    --surface2: {tk['surface2']};
    --text: {tk['text']};
    --text2: {tk['text_secondary']};
    --text3: {tk['text_subtle']};
    --border: {tk['border']};
    --borderS: {tk['border_strong']};
    --on-p: {tk['on_primary']};
    --success: {tk['success']};
    --error: {tk['error']};
    --warning: {tk['warning']};
    --font-display: {tk['font_display']};
    --font-body: {tk['font_body']};
  }}

  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: var(--font-body);
    background: var(--bg);
    color: var(--text);
    font-size: 16px;
    line-height: 1.6;
    padding: 40px;
    min-height: 100vh;
  }}

  .container {{ max-width: 1100px; margin: 0 auto; }}
  .header {{ margin-bottom: 40px; text-align: center; }}
  .header .brand {{ font-family: var(--font-display); font-size: 40px; font-weight: 700; color: var(--p); }}
  .header .mood {{ color: var(--text2); font-size: 14px; margin-top: 4px; }}

  .section {{ margin-bottom: 48px; }}
  .section-title {{ font-family: var(--font-display); font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: var(--text3); margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }}

  /* Color Swatches */
  .swatches {{ display: flex; flex-wrap: wrap; gap: 12px; }}
  .swatch {{ width: 130px; border-radius: 8px; overflow: hidden; border: 1px solid var(--border); }}
  .swatch-color {{ height: 70px; }}
  .swatch-info {{ padding: 10px 12px; background: var(--surface); }}
  .swatch-name {{ font-size: 11px; font-weight: 600; }}
  .swatch-hex {{ font-size: 12px; font-family: "JetBrains Mono", Consolas, monospace; margin-top: 2px; color: var(--text2); }}

  /* Typography */
  .type-row {{ margin-bottom: 20px; padding: 18px; background: var(--surface); border-radius: 8px; }}
  .type-label {{ font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--text3); letter-spacing: 1px; margin-bottom: 6px; }}
  .type-meta {{ font-size: 12px; color: var(--text2); margin-top: 8px; font-family: var(--font-body); }}

  /* Buttons */
  .btn-row {{ display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }}
  .btn {{ padding: 10px 22px; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; border: none; font-family: var(--font-body); }}
  .btn-primary {{ background: var(--p); color: var(--on-p); }}
  .btn-secondary {{ background: var(--surface); color: var(--text); border: 1px solid var(--border); }}
  .btn-ghost {{ background: transparent; color: var(--text); border: 1px solid var(--border); }}

  /* Card */
  .card-grid {{ display: grid; grid-template-columns: repeat(auto-fill,minmax(300px,1fr)); gap: 16px; }}
  .card {{
    padding: 24px;
    background: var(--surface);
    border-radius: 12px;
    border: 1px solid var(--border);
  }}
  .card-title {{ font-family: var(--font-display); font-size: 18px; font-weight: 600; margin-bottom: 8px; }}
  .card-text {{ color: var(--text2); font-size: 14px; }}

  /* Input */
  .input-row {{ display: flex; gap: 12px; flex-wrap: wrap; }}
  .input {{
    padding: 10px 14px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 14px;
    font-family: var(--font-body);
    background: var(--surface);
    color: var(--text);
    outline: none;
    min-width: 240px;
  }}
  .input:focus {{ border-color: var(--p); box-shadow: 0 0 0 3px {_rgba(tk['primary'], 0.15)}; }}

  footer {{ text-align: center; color: var(--text3); font-size: 12px; margin-top: 60px; padding-top: 24px; border-top: 1px solid var(--border); }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <div class="brand">{brand}</div>
    <div class="mood">Design System Preview · {mood}</div>
  </div>

  <div class="section">
    <div class="section-title">🎨 色彩系统</div>
    <div class="swatches">
      {_swatch("Primary", tk['primary'])}
      {_swatch("Background", tk['bg'])}
      {_swatch("Surface", tk['surface'])}
      {_swatch("Surface ↑", tk['surface2'])}
      {_swatch("Text Primary", tk['text'])}
      {_swatch("Text Secondary", tk['text_secondary'])}
      {_swatch("Border", tk['border'])}
      {_swatch("Success", tk['success'])}
      {_swatch("Error", tk['error'])}
    </div>
  </div>

  <div class="section">
    <div class="section-title">🔤 排版层级</div>
    <div class="type-row">
      <div class="type-label">Display / H1</div>
      <div style="font-family:var(--font-display);font-size:{tk['h1_size']};font-weight:600;line-height:1.08">The quick brown fox</div>
      <div class="type-meta">{tk['h1_size']} · 600 · {tk['font_display']}</div>
    </div>
    <div class="type-row">
      <div class="type-label">Heading / H2</div>
      <div style="font-family:var(--font-display);font-size:{tk['h2_size']};font-weight:600;line-height:1.18">Design is intelligence</div>
      <div class="type-meta">{tk['h2_size']} · 600</div>
    </div>
    <div class="type-row">
      <div class="type-label">Subheading / H3</div>
      <div style="font-family:var(--font-display);font-size:{tk['h3_size']};font-weight:500;line-height:1.28">Every great design begins with a story</div>
      <div class="type-meta">{tk['h3_size']} · 500</div>
    </div>
    <div class="type-row">
      <div class="type-label">Body Text</div>
      <div style="font-size:{tk['body_size']};color:var(--text2)">A design system is a collection of reusable components, guided by clear standards, that can be assembled together to build any number of applications.</div>
      <div class="type-meta">{tk['body_size']} · {tk['font_body']}</div>
    </div>
    <div class="type-row">
      <div class="type-label">Small / Caption</div>
      <div style="font-size:12px;color:var(--text3)">The small print — metadata, timestamps, secondary information</div>
      <div class="type-meta">12px · muted</div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">🔘 按钮系统</div>
    <div class="btn-row">
      <button class="btn btn-primary">Primary Action</button>
      <button class="btn btn-secondary">Secondary</button>
      <button class="btn btn-ghost">Ghost</button>
      <button class="btn" style="background:var(--success);color:#fff">Success</button>
      <button class="btn" style="background:var(--error);color:#fff">Danger</button>
    </div>
  </div>

  <div class="section">
    <div class="section-title">🃏 卡片 / 面板</div>
    <div class="card-grid">
      <div class="card">
        <div class="card-title">Project Dashboard</div>
        <div class="card-text">A summary card with key metrics. Uses surface + border tokens from the {brand} design system.</div>
        <div style="margin-top:16px;display:flex;gap:8px;">
          <button class="btn btn-primary" style="font-size:12px;padding:6px 14px">View</button>
          <button class="btn btn-ghost" style="font-size:12px;padding:6px 14px">Close</button>
        </div>
      </div>
      <div class="card" style="background:var(--surface2);">
        <div class="card-title">Elevated Panel</div>
        <div class="card-text">Elevated surface level for layered content or modals.</div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-title">📝 输入框</div>
    <div class="input-row">
      <input class="input" type="text" placeholder="Default state…">
      <input class="input" type="email" value="user@example.com" placeholder="email@example.com">
      <input class="input" type="text" placeholder="Focused" style="border-color:var(--p);box-shadow:0 0 0 3px {_rgba(tk['primary'], 0.15)};">
    </div>
  </div>

  <footer>
    {brand} Design Preview · Tokens from DESIGN.md · © original brand
  </footer>
</div>
</body>
</html>'''
    return html


def main():
    brands = sorted([d.name for d in TEMPLATES_DIR.iterdir()
                     if d.is_dir() and (d / 'DESIGN.md').exists()])

    success = 0
    for brand in brands:
        md_path = TEMPLATES_DIR / brand / 'DESIGN.md'
        try:
            data = parse_design_md(md_path)
            if not data:
                print(f"  ⚠ {brand}: No YAML front matter")
                continue

            tk = extract_tokens(data)
            html = generate_preview_html(brand, tk)

            out_path = TEMPLATES_DIR / brand / 'preview.html'
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)

            print(f"  ✓ {brand} ({len(html)} bytes)")
            success += 1

        except Exception as e:
            import traceback
            print(f"  ✗ {brand}: {e}")
            traceback.print_exc()

    print(f"\nDone. {success}/{len(brands)} previews generated.")


if __name__ == '__main__':
    main()
