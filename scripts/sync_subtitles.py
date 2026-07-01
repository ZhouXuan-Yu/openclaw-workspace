#!/usr/bin/env python3
"""Measure actual TTS duration per segment, regenerate with precise sync"""
import subprocess, os, json

output_dir = r"C:\Users\ZhouXuan\.openclaw\workspace\remotion-agent-video\output"
ffmpeg = r"C:\tools\ffmpeg\bin\ffmpeg.exe"

lines = [
    "2026年，AI Agent 岗位爆发",
    "私企 vs 国企，怎么选？",
    "私企重项目，国企重学历",
    "技术栈和薪资模型完全不同",
    "薪资对比：私企天花板更高",
    "但国企公积金加保险，实际差距只有20%到30%",
    "私企：本科够用，项目经历大于学历",
    "国企：硕博起步，证书加考试加政审",
    "私企 Agent 岗位增长 215%",
    "国企从零起步，2026春招爆发",
    "最佳入场窗口：2026年底前",
    "Python + LangChain + MCP = 你的优势",
]

voice = "zh-CN-YunyangNeural"

# Step 1: Generate and measure each segment
print("=== Measuring TTS durations ===")
segments = []
current_time = 0.0

for i, text in enumerate(lines):
    seg_file = os.path.join(output_dir, f"seg_{i:02d}.wav")
    subprocess.run([
        "edge-tts", "--voice", voice, "--text", text,
        "--write-media", seg_file, "--rate", "+4%",
    ], capture_output=True)
    
    # Get actual duration via ffprobe
    result = subprocess.run(
        [ffmpeg, "-i", seg_file, "-f", "null", "-"],
        capture_output=True, text=True
    )
    import re
    m = re.search(r"time=(\d+):(\d+):([\d.]+)", result.stderr)
    if m:
        actual_dur = int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
    else:
        actual_dur = 3.0  # fallback
    
    start = current_time
    end = current_time + actual_dur
    segments.append({
        "start": start,
        "end": end,
        "text": text,
        "duration": actual_dur,
        "file": seg_file,
    })
    print(f"[{i+1:02d}] {start:.2f}s-{end:.2f}s ({actual_dur:.2f}s): {text}")
    current_time = end

total_dur = current_time
print(f"\nTotal audio duration: {total_dur:.2f}s")

# Step 2: Build subtitle data for index.js
subtitle_js = "const subtitleLines = [\n"
for seg in segments:
    start_frame = int(seg["start"] * 30)
    end_frame = int(seg["end"] * 30)
    subtitle_js += f'  {{ start: {start_frame}, end: {end_frame}, text: "{seg["text"]}" }},\n'
subtitle_js += "];"

# Save for reference
with open(os.path.join(output_dir, "subtitle_data.json"), "w", encoding="utf-8") as f:
    json.dump({"total_duration": total_dur, "segments": segments}, f, ensure_ascii=False, indent=2)

print("\n=== Subtitle data (for index.js) ===")
print(subtitle_js)
print(f"\n=== Total frames needed: {int(total_dur * 30)} ===")

# Step 3: Mux with precise adelay
print("\n=== Muxing audio ===")
filter_parts = []
for i, seg in enumerate(segments):
    filter_parts.append(
        f"[{i}:a]atrim=0:{seg['duration']},adelay={int(seg['start']*1000)}|{int(seg['start']*1000)},apad=pad_dur={total_dur}[pad{i}]"
    )
mix_inputs = "".join(f"[pad{i}]" for i in range(len(segments)))
filter_parts.append(f"{mix_inputs}amix={len(segments)}:dropout_transition=0:normalize=0[aout]")
filter_complex = ";".join(filter_parts)

for video_name, output_name in [
    ("agent-v4.mp4", "agent-v4-final.mp4"),
    ("agent-v4-xhs.mp4", "agent-v4-xhs-final.mp4"),
]:
    video_path = os.path.join(output_dir, video_name)
    out_path = os.path.join(output_dir, output_name)
    cmd = [ffmpeg, "-y"]
    cmd += ["-i", video_path]
    for seg in segments:
        cmd += ["-i", seg["file"]]
    cmd += [
        "-filter_complex", filter_complex,
        "-map", "0:v:0", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-ar", "44100", "-b:a", "128k",
        "-shortest", out_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"OK: {output_name}")
    else:
        print(f"FAIL: {output_name}")
        print(result.stderr[-300:])

print("\n=== Done ===")
