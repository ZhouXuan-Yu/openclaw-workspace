"""
Daily Social Content Pipeline
Input: content.json {title, sections: [[title, body]], tts_text}
Output: MP4 video + PDF
"""
import os
import sys
import subprocess
import json
import time
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE, "..")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output-daily")
FFMPEG = r"C:\tools\ffmpeg\bin\ffmpeg.exe"
FFPROBE = r"C:\tools\ffmpeg\bin\ffprobe.exe"

def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "cards"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "video"), exist_ok=True)

def generate_tts(text, output_path, voice="zh-CN-YunxiNeural", retries=3):
    import edge_tts
    import asyncio
    async def _gen():
        import os as _os
        old_http = _os.environ.pop('HTTP_PROXY', None)
        old_https = _os.environ.pop('HTTPS_PROXY', None)
        _os.environ['NO_PROXY'] = '*'
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
        finally:
            if old_http: _os.environ['HTTP_PROXY'] = old_http
            if old_https: _os.environ['HTTPS_PROXY'] = old_https
            _os.environ.pop('NO_PROXY', None)
    for attempt in range(retries):
        try:
            asyncio.run(_gen())
            print(f"TTS OK: {output_path}")
            return
        except Exception as e:
            if attempt < retries - 1:
                wait = (attempt + 1) * 5
                print(f"TTS retry {attempt+1}/{retries} (wait {wait}s)")
                time.sleep(wait)
            else:
                print(f"TTS FAIL: {e}")
                raise

def generate_srt(text, output_path, total_duration):
    sentences = []
    for s in text.replace(".", ".\n").replace("!", "!\n").replace("?", "?\n").replace("\u3002", "\u3002\n").replace("\uff01", "\uff01\n").replace("\uff1f", "\uff1f\n").split("\n"):
        s = s.strip()
        if s:
            sentences.append(s)
    if not sentences:
        sentences = [text]

    def fmt(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int((sec % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    cur = 0.3
    for i, sent in enumerate(sentences):
        dur = max(1.2, min(4.0, len(sent) * 0.15))
        start = cur
        end = start + dur
        if end > total_duration:
            end = total_duration
        lines.append(f"{i+1}")
        lines.append(f"{fmt(start)} --> {fmt(end)}")
        lines.append(sent)
        lines.append("")
        cur = end + 0.08
        if cur >= total_duration:
            break

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"SRT OK: {output_path} ({len(sentences)} lines)")

def generate_cards(title, sections, output_dir, images=None):
    template_path = os.path.join(PROJECT_ROOT, "skills", "guizang-social-card", "assets", "template-swiss-card.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    cards_html = ""
    for i, (ct, cb) in enumerate(sections[:6]):
        img_tag = ""
        if images and i < len(images) and os.path.exists(images[i]):
            img_src = images[i].replace(os.sep, "/")
            img_tag = f'<div class="hero-img"><img src="file:///{img_src}" style="width:100%;object-fit:cover;max-height:500px" /></div>'
        cards_html += f"""
    <section class="poster xhs" data-page="{i+1}">
      <div class="card-header">
        <span class="page-num">{i+1:02d}</span>
        <span class="label">AGENT DAILY</span>
      </div>
      {img_tag}
      <h1 class="title">{ct}</h1>
      <div class="body-text">{cb}</div>
      <div class="footer">
        <span class="tag">#AI Agent</span>
        <span class="date">{datetime.now().strftime('%Y.%m.%d')}</span>
      </div>
    </section>"""

    html = template.replace("<!-- POSTERS_HERE -->", cards_html)
    html_path = os.path.join(output_dir, "cards", "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    render_script = f"""
const {{ chromium }} = require('playwright');
const path = require('path');
(async () => {{
  const browser = await chromium.launch({{ channel: 'msedge', headless: true }});
  const page = await browser.newPage({{ viewport: {{ width: 1080, height: 1440 }} }});
  await page.goto('file:///' + '{html_path.replace(chr(92), '/')}', {{ waitUntil: 'networkidle' }});
  await page.waitForTimeout(3000);
  const posters = await page.$$('.poster');
  for (let i = 0; i < posters.length; i++) {{
    const p = path.join('{output_dir.replace(chr(92), '/')}', 'cards', `card-${{String(i+1).padStart(2,'0')}}.png`);
    await posters[i].screenshot({{ path: p }});
    console.log(`Card ${{i+1}}: ${{p}}`);
  }}
  await browser.close();
  console.log('Done');
}})();
"""
    render_dir = os.path.join(PROJECT_ROOT, "social-card-2026-06-15")
    render_path = os.path.join(render_dir, "render-daily.js")
    with open(render_path, "w", encoding="utf-8") as f:
        f.write(render_script)

    result = subprocess.run(["node", render_path], capture_output=True, text=True, timeout=120, cwd=render_dir)
    if result.returncode == 0:
        print(f"Cards OK: {len(sections[:6])} images")
    else:
        print(f"Cards FAIL: {result.stderr[:200]}")
    return [os.path.join(output_dir, "cards", f"card-{str(i+1).zfill(2)}.png") for i in range(len(sections[:6]))]

def get_duration(path):
    probe = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(probe.stdout.strip()) if probe.stdout.strip() else 40

def generate_video_pdf(title, text, card_paths, tts_path, srt_path, output_video, output_pdf):
    concat_path = os.path.join(OUTPUT_DIR, "video", "concat.txt")
    dur = 8
    with open(concat_path, "w", encoding="utf-8") as f:
        for p in card_paths:
            f.write(f"file '{p.replace(os.sep, '/')}'\n")
            f.write(f"duration {dur}\n")
        f.write(f"file '{card_paths[-1].replace(os.sep, '/')}'\n")

    srt_rel = os.path.relpath(srt_path, PROJECT_ROOT).replace("\\", "/")
    concat_rel = os.path.relpath(concat_path, PROJECT_ROOT).replace("\\", "/")
    tts_rel = os.path.relpath(tts_path, PROJECT_ROOT).replace("\\", "/")
    out_rel = os.path.relpath(output_video, PROJECT_ROOT).replace("\\", "/")
    cmd = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_rel,
        "-i", tts_rel,
        "-vf", f"pad=1080:1920:0:240:black,subtitles={srt_rel}:force_style='FontSize=10,PrimaryColour=&H00000000,BackColour=&H80FFFFFF,BorderStyle=3,MarginV=80,Outline=0,Shadow=0'",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", out_rel
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=PROJECT_ROOT)
    if os.path.exists(output_video):
        sz = os.path.getsize(output_video)
        print(f"Video OK: {output_video} ({sz//1024}KB)")
    else:
        print("Video FAIL")

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas as pdfcanvas
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        c = pdfcanvas.Canvas(output_pdf, pagesize=A4)
        w, h = A4
        c.setFont('STSong-Light', 24)
        c.drawString(2*cm, h - 3*cm, title)
        c.setFont('STSong-Light', 11)
        y = h - 5*cm
        for line in text.split('\n'):
            if y < 3*cm:
                c.showPage()
                y = h - 3*cm
                c.setFont('STSong-Light', 11)
            while len(line) > 40:
                c.drawString(2*cm, y, line[:40])
                line = line[40:]
                y -= 0.5*cm
                if y < 3*cm:
                    c.showPage()
                    y = h - 3*cm
                    c.setFont('STSong-Light', 11)
            c.drawString(2*cm, y, line)
            y -= 0.5*cm
        c.setFont('STSong-Light', 9)
        c.drawString(2*cm, 2*cm, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        c.save()
        print(f"PDF OK: {output_pdf}")
    except Exception as e:
        print(f"PDF FAIL: {e}")

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    else:
        print("Usage: python daily_pipeline.py content.json")
        sys.exit(1)

    title = data.get("title", "Daily Agent")
    sections = data.get("sections", [])
    tts_text = data.get("tts_text", "")
    images = data.get("images", [])

    ensure_dirs()
    today = datetime.now().strftime("%Y-%m-%d")
    tts_path = os.path.join(OUTPUT_DIR, "video", "tts.mp3")
    srt_path = os.path.join(OUTPUT_DIR, "video", "subtitles.srt")
    output_video = os.path.join(OUTPUT_DIR, f"daily-{today}.mp4")
    output_pdf = os.path.join(OUTPUT_DIR, f"daily-{today}.pdf")

    generate_tts(tts_text, tts_path)
    tts_dur = get_duration(tts_path)
    generate_srt(tts_text, srt_path, tts_dur)
    card_paths = generate_cards(title, sections, OUTPUT_DIR, images)
    generate_video_pdf(title, tts_text, card_paths, tts_path, srt_path, output_video, output_pdf)

    print(f"\n=== Done ===")
    print(f"Video: {output_video}")
    print(f"PDF: {output_pdf}")

if __name__ == "__main__":
    main()
