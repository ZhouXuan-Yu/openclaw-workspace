#!/usr/bin/env python3
"""补全缺失的 DESIGN.md 和 preview.html"""
from pathlib import Path

BASE = Path(r"E:\Obsidian仓库\ZhouXuan私人领域\顶级UI设计\templates")

def _hex_rgb(h):
    h = h.lstrip('#')
    return ','.join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))

def gen_design_md(scene, tk):
    glow = f"rgba({_hex_rgb(tk['primary'])},0.35)"
    return f"""---
version: "2.0"
name: {scene}
description: {tk['desc']}
style: techno-futurist

colors:
  primary: "{tk['primary']}"
  primary_glow: "{glow}"
  background: "{tk['bg']}"
  surface: "{tk['surface']}"
  surface_elevated: "{tk['surface2']}"
  text_primary: "{tk['text']}"
  text_secondary: "{tk['text2']}"
  text_muted: "{tk['text3']}"
  border: "{tk['border']}"
  border_strong: "{tk['borderS']}"
  on_primary: "{tk['on_p']}"
  success: "{tk['success']}"
  error: "{tk['error']}"
  warning: "{tk['warning']}"

typography:
  font_display: "{tk['font_display']}"
  font_body: "{tk['font_body']}"
  font_mono: "JetBrains Mono, ui-monospace, monospace"
  h1_size: "{tk['h1']}"
  h1_weight: 600
  h2_size: "{tk['h2']}"
  h2_weight: 600
  h3_size: "{tk['h3']}"
  h3_weight: 500
  body_size: "{tk['body']}"
  body_weight: 400
  caption_size: "12px"
  button_size: "14px"
  button_weight: 500

material:
  glass_blur: "12px"
  glass_opacity: 0.08
  surface_noise: 0.02

micro_interactions:
  hover_scale: 1.02
  hover_duration: "200ms"
  hover_easing: "cubic-bezier(0.34,1.56,0.64,1)"

accessibility:
  wcag_level: "AA"
  min_contrast_ratio: 4.5

spacing:
  unit: 4
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  section: "80px"

radius:
  sm: "6px"
  md: "10px"
  lg: "16px"
  pill: "9999px"

shadows:
  card: "0 1px 3px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.05)"
  elevated: "0 4px 16px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.08)"
  glow: "0 0 24px {glow}"

layout:
  max_width: "1200px"
  sidebar_width: "260px"

---

## 1. Visual Theme & Atmosphere

Techno-Futurist {scene} — 暗深空背景+霓虹发光强调色+玻璃态材质+Bento Grid 布局。
2026趋势：Dark Mode by Default, Bento Grids, Glassmorphism 2.0, Micro-Delight。

## 2. Color Palette & Roles

主色 {tk['primary']} 带 glow 发光变体 {glow}。暗底9级灰阶系统。

## 3. Typography

Display: {tk['font_display']} | Body: {tk['font_body']} | Mono: JetBrains Mono
层级: h1={tk['h1']}/600 h2={tk['h2']}/600 h3={tk['h3']}/500 body={tk['body']}/400

## 4. Component Stylings

按钮: Primary solid {tk['primary']} + glow, Secondary outline, 全pill圆角
卡片: {tk['surface']} + {tk['border']} + glass_blur
输入: border focus时 {glow} 发光环

## 5. Layout Principles

Bento Grid非对称模块马赛克。桌面复杂墙体，移动端自然堆叠。

## 6. Depth & Elevation

玻璃态材质 (backdrop-filter:blur) + 发丝线边框 + 霓虹glow阴影

## 7. Micro-Interactions

hover弹性缩放(1.02x spring easing), focus ring发光, scroll渐现

## 8. Responsive Behavior

Bento Grid移动端垂直堆叠。侧栏折叠为底部导航。触控目标>=44px。

## 9. Agent Prompt Guide

Build a {scene} UI using this DESIGN.md. Dark background {tk['bg']}, primary {tk['primary']} with glow, glass-morphism cards, Bento Grid, hairline borders, micro-interactions. All values from YAML front matter.
"""

def gen_preview(scene, tk):
    g = f"rgba({_hex_rgb(tk['primary'])},0.35)"
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{scene} · Techno-Futurist</title>
<style>
:root{{
--p:{tk['primary']};--bg:{tk['bg']};--surface:{tk['surface']};--surface2:{tk['surface2']};
--text:{tk['text']};--text2:{tk['text2']};--text3:{tk['text3']};
--border:{tk['border']};--borderS:{tk['borderS']};--on-p:{tk['on_p']};
--success:{tk['success']};--error:{tk['error']};--glow:{g};
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:{tk['font_body']};background:var(--bg);color:var(--text);font-size:{tk['body']};line-height:1.6;padding:40px;min-height:100vh}}
.container{{max-width:1100px;margin:0 auto}}
.header{{text-align:center;margin-bottom:48px}}
.brand{{font-size:36px;font-weight:700;background:linear-gradient(135deg,var(--p),{tk['text2']});-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.mood{{color:var(--text2);font-size:14px;margin-top:6px}}
.section{{margin-bottom:48px}}
.st{{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:var(--text3);margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid var(--border)}}
.swatches{{display:flex;flex-wrap:wrap;gap:10px}}
.sw{{width:120px;border-radius:8px;overflow:hidden;border:1px solid var(--border);transition:transform .2s cubic-bezier(0.34,1.56,0.64,1)}}
.sw:hover{{transform:scale(1.04)}}
.swc{{height:60px}}
.swi{{padding:8px 10px;background:var(--surface)}}
.swn{{font-size:10px;font-weight:600;letter-spacing:.5px}}
.swh{{font-size:11px;font-family:monospace;margin-top:2px;color:var(--text2)}}
.tr{{margin-bottom:16px;padding:18px;background:var(--surface);border-radius:10px;border:1px solid var(--border);transition:all .2s}}
.tr:hover{{border-color:var(--p);box-shadow:0 0 20px var(--glow)}}
.tl{{font-size:10px;font-weight:600;text-transform:uppercase;color:var(--text3);letter-spacing:1px;margin-bottom:6px}}
.tm{{font-size:11px;color:var(--text2);margin-top:6px}}
.br{{display:flex;gap:10px;flex-wrap:wrap}}
.btn{{padding:10px 22px;border-radius:9999px;font-size:14px;font-weight:500;cursor:pointer;border:none;font-family:{tk['font_body']};transition:all .2s cubic-bezier(0.34,1.56,0.64,1)}}
.btn:hover{{transform:scale(1.03)}}
.btn:active{{transform:scale(0.97)}}
.btn-p{{background:var(--p);color:var(--on-p);box-shadow:0 0 20px var(--glow)}}
.btn-p:hover{{box-shadow:0 0 30px var(--glow)}}
.btn-s{{background:var(--surface);color:var(--text);border:1px solid var(--border)}}
.btn-g{{background:transparent;color:var(--text);border:1px solid var(--border)}}
.bento{{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:140px;gap:14px}}
.bi{{background:var(--surface);border-radius:16px;border:1px solid var(--border);padding:22px;display:flex;flex-direction:column;justify-content:center;backdrop-filter:blur(12px);transition:all .2s cubic-bezier(0.34,1.56,0.64,1)}}
.bi:hover{{transform:scale(1.02);border-color:var(--p);box-shadow:0 0 24px var(--glow)}}
.bi2{{grid-column:span 2}}
.bir2{{grid-row:span 2}}
.bt{{font-size:18px;font-weight:600;margin-bottom:4px}}
.bd{{color:var(--text2);font-size:13px}}
.kpi{{display:flex;gap:14px;margin-bottom:20px;flex-wrap:wrap}}
.kc{{flex:1;min-width:180px;background:var(--surface);border-radius:16px;border:1px solid var(--border);padding:22px;backdrop-filter:blur(12px);transition:all .2s cubic-bezier(0.34,1.56,0.64,1)}}
.kc:hover{{transform:scale(1.02);border-color:var(--p)}}
.kl{{font-size:11px;font-weight:500;text-transform:uppercase;color:var(--text3);letter-spacing:1px}}
.kv{{font-size:36px;font-weight:700;margin-top:4px}}
.kup{{color:var(--success);font-size:13px;margin-top:4px}}
.kdn{{color:var(--error);font-size:13px;margin-top:4px}}
.card{{padding:24px;background:var(--surface);border-radius:16px;border:1px solid var(--border);backdrop-filter:blur(12px);transition:all .2s}}
.card:hover{{border-color:var(--p)}}
.ct{{font-size:18px;font-weight:600;margin-bottom:8px}}
.cd{{color:var(--text2);font-size:14px}}
.inp{{padding:10px 14px;border:1px solid var(--border);border-radius:10px;font-size:14px;font-family:{tk['font_body']};background:var(--surface);color:var(--text);outline:none;min-width:220px;transition:all .2s}}
.inp:focus{{border-color:var(--p);box-shadow:0 0 0 3px var(--glow)}}
.ft{{text-align:center;color:var(--text3);font-size:12px;margin-top:60px;padding-top:24px;border-top:1px solid var(--border)}}
</style></head><body>
<div class="container">
<div class="header"><div class="brand">{scene}</div><div class="mood">Techno-Futurist · Dark Mode · Glass + Glow + Bento Grid</div></div>

<div class="section"><div class="st">🎨 Color System</div><div class="swatches">
<div class="sw"><div class="swc" style="background:{tk['primary']}"></div><div class="swi"><div class="swn">Primary</div><div class="swh">{tk['primary']}</div></div></div>
<div class="sw"><div class="swc" style="background:{tk['bg']}"></div><div class="swi"><div class="swn">BG</div><div class="swh">{tk['bg']}</div></div></div>
<div class="sw"><div class="swc" style="background:{tk['surface']}"></div><div class="swi"><div class="swn">Surface</div><div class="swh">{tk['surface']}</div></div></div>
<div class="sw"><div class="swc" style="background:{tk['surface2']}"></div><div class="swi"><div class="swn">Surface↑</div><div class="swh">{tk['surface2']}</div></div></div>
<div class="sw"><div class="swc" style="background:{tk['text']}"></div><div class="swi"><div class="swn">Text</div><div class="swh">{tk['text']}</div></div></div>
<div class="sw"><div class="swc" style="background:{tk['text2']}"></div><div class="swi"><div class="swn">Text 2°</div><div class="swh">{tk['text2']}</div></div></div>
<div class="sw"><div class="swc" style="background:{tk['success']}"></div><div class="swi"><div class="swn">Success</div><div class="swh">{tk['success']}</div></div></div>
<div class="sw"><div class="swc" style="background:{tk['error']}"></div><div class="swi"><div class="swn">Error</div><div class="swh">{tk['error']}</div></div></div>
</div></div>

<div class="section"><div class="st">🔤 Typography</div>
<div class="tr"><div class="tl">Display H1</div><div style="font-size:{tk['h1']};font-weight:600;line-height:1.1">Techno-Futurist</div><div class="tm">{tk['h1']}/600</div></div>
<div class="tr"><div class="tl">Heading H2</div><div style="font-size:{tk['h2']};font-weight:600;line-height:1.2">Dark mode is default</div><div class="tm">{tk['h2']}/600</div></div>
<div class="tr"><div class="tl">Subheading H3</div><div style="font-size:{tk['h3']};font-weight:500;line-height:1.3">Glass meets Bento Grid</div><div class="tm">{tk['h3']}/500</div></div>
<div class="tr"><div class="tl">Body</div><div style="color:var(--text2)">Techno-Futurist design system — dark space, neon glow, glass-morphism, Bento Grid, hairline borders, micro-interactions. Built for enterprise.</div><div class="tm">{tk['body']}</div></div>
</div>

<div class="section"><div class="st">📊 Bento Grid</div>
<div class="bento">
<div class="bi bi2 bir2"><div class="bt">Hero Block</div><div class="bd">Large showcase · 2×2</div></div>
<div class="bi"><div class="bt">Feature A</div><div class="bd">1×1</div></div>
<div class="bi"><div class="bt">Feature B</div><div class="bd">1×1</div></div>
<div class="bi bi2"><div class="bt">Stats Panel</div><div class="bd">2×1 overview</div></div>
<div class="bi"><div class="bt">CTA</div><div class="bd">1×1</div></div>
<div class="bi"><div class="bt">Metric</div><div class="bd">1×1</div></div>
</div></div>

<div class="section"><div class="st">📈 KPI Cards</div><div class="kpi">
<div class="kc"><div class="kl">Revenue</div><div class="kv">¥2.4M</div><div class="kup">↑ 12.5%</div></div>
<div class="kc"><div class="kl">Users</div><div class="kv">18,240</div><div class="kup">↑ 8.2%</div></div>
<div class="kc"><div class="kl">Latency</div><div class="kv">142ms</div><div class="kdn">↓ 5.1%</div></div>
<div class="kc"><div class="kl">Uptime</div><div class="kv">99.97%</div><div class="kup">↑ 0.02%</div></div>
</div></div>

<div class="section"><div class="st">🔘 Buttons</div><div class="br">
<button class="btn btn-p">Primary Glow</button>
<button class="btn btn-s">Secondary</button>
<button class="btn btn-g">Ghost</button>
<button class="btn" style="background:var(--success);color:#fff;box-shadow:0 0 16px rgba(34,197,94,.3)">Success</button>
</div></div>

<div class="section"><div class="st">🃏 Glass Cards</div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px">
<div class="card"><div class="ct">Project Alpha</div><div class="cd">Glass card with blur. Hover for glow.</div><div style="margin-top:14px;display:flex;gap:8px"><button class="btn btn-p" style="font-size:12px;padding:6px 14px">View</button><button class="btn btn-g" style="font-size:12px;padding:6px 14px">Close</button></div></div>
<div class="card" style="background:var(--surface2)"><div class="ct">Elevated</div><div class="cd">Higher surface layer for depth.</div></div>
</div></div>

<div class="ft">{scene} · Techno-Futurist v2.0</div>
</div></body></html>"""

SCENES = {
    "_场景04-企业协作面板": {
        "primary": "#22C55E", "bg": "#0D0D12", "surface": "#16161E",
        "surface2": "#1E1E28", "text": "#F8F8FC", "text2": "#A0A0B0",
        "text3": "#6B6B7B", "border": "#252530", "borderS": "#333345",
        "on_p": "#0D0D12", "success": "#22C55E", "error": "#EF4444", "warning": "#F59E0B",
        "font_display": "Inter, -apple-system, sans-serif",
        "font_body": "Inter, -apple-system, sans-serif",
        "h1": "24px", "h2": "18px", "h3": "15px", "body": "14px",
        "desc": "企业协作面板 — 翠绿+暗底灰阶+多面板+标签页+Bento Grid。对标Notion/Figma/HubSpot"
    },
    "_场景07-Techno品牌官网": {
        "primary": "#7C3AED", "bg": "#08080C", "surface": "#111118",
        "surface2": "#1A1A24", "text": "#F5F3FF", "text2": "#A78BFA",
        "text3": "#7C6FA6", "border": "#1F1A2E", "borderS": "#3D3560",
        "on_p": "#FFFFFF", "success": "#22C55E", "error": "#EF4444", "warning": "#F59E0B",
        "font_display": "Inter, -apple-system, sans-serif",
        "font_body": "Inter, -apple-system, sans-serif",
        "h1": "64px", "h2": "40px", "h3": "26px", "body": "17px",
        "desc": "Techno-Futurist品牌官网 — 霓虹紫+全屏Bento Grid+动态标题+粒子背景+电影滚动。对标Linear/Cursor/Vercel"
    },
    "_场景08-混合品牌官网": {
        "primary": "#4F46E5", "bg": "#0F172A", "surface": "#1E293B",
        "surface2": "#334155", "text": "#F8FAFC", "text2": "#94A3B8",
        "text3": "#64748B", "border": "#334155", "borderS": "#475569",
        "on_p": "#FFFFFF", "success": "#22C55E", "error": "#EF4444", "warning": "#F59E0B",
        "font_display": "Söhne, Inter, -apple-system, sans-serif",
        "font_body": "Inter, -apple-system, sans-serif",
        "h1": "56px", "h2": "36px", "h3": "22px", "body": "16px",
        "desc": "混合品牌官网 — 靛蓝+明暗交替+渐变网格+Glassmorphism+电影滚动。对标Stripe/Coinbase"
    },
}

MISSING_PREVIEW = {
    "_场景03-数据密集分析": {
        "primary": "#06B6D4", "bg": "#0A0A0F", "surface": "#111118",
        "surface2": "#171720", "text": "#F8F8FC", "text2": "#A8A8B8",
        "text3": "#6A6A78", "border": "#1E1E2A", "borderS": "#2A2A3A",
        "on_p": "#0A0A0F", "success": "#22C55E", "error": "#EF4444", "warning": "#F59E0B",
        "font_display": "Inter, -apple-system, sans-serif",
        "font_body": "Inter, -apple-system, sans-serif",
        "h1": "22px", "h2": "16px", "h3": "14px", "body": "13px"
    },
    "_场景06-开发者工具终端": {
        "primary": "#3ECF8E", "bg": "#07080A", "surface": "#0D0F14",
        "surface2": "#15171D", "text": "#EDEEF0", "text2": "#8B8F98",
        "text3": "#5A5E66", "border": "#242728", "borderS": "#333638",
        "on_p": "#07080A", "success": "#3ECF8E", "error": "#FF5470", "warning": "#F5A623",
        "font_display": "Inter, -apple-system, sans-serif",
        "font_body": "Inter, -apple-system, sans-serif",
        "h1": "48px", "h2": "28px", "h3": "18px", "body": "14px"
    },
}

def main():
    for name, tk in SCENES.items():
        d = BASE / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "DESIGN.md").write_text(gen_design_md(name, tk), encoding='utf-8')
        (d / "preview.html").write_text(gen_preview(name, tk), encoding='utf-8')
        print(f"✓ {name} (DESIGN.md + preview.html)")

    for name, tk in MISSING_PREVIEW.items():
        d = BASE / name
        (d / "preview.html").write_text(gen_preview(name, tk), encoding='utf-8')
        print(f"✓ {name} (preview.html)")

    print("\nDone. All 8 scenes complete.")

if __name__ == '__main__':
    main()
