#!/usr/bin/env python3
"""Generate edge-tts audio for agent-video subtitle lines"""
import subprocess, json, os

output_dir = r"C:\Users\ZhouXuan\.openclaw\workspace\remotion-agent-video\output"
subtitle_lines = [
    (0, 3, "2026年，AI Agent 岗位爆发"),
    (3, 6, "私企 vs 国企，怎么选？"),
    (6, 9.33, "私企重项目，国企重学历"),
    (9.33, 12, "技术栈和薪资模型完全不同"),
    (12, 15.33, "薪资对比：私企天花板更高"),
    (15.33, 18, "但国企公积金加保险，实际差距只有20%到30%"),
    (18, 21.33, "私企：本科够用，项目经历大于学历"),
    (21.33, 24, "国企：硕博起步，证书加考试加政审"),
    (24, 27.33, "私企 Agent 岗位增长 215%"),
    (27.33, 30, "国企从零起步，2026春招爆发"),
    (30, 33.33, "最佳入场窗口：2026年底前"),
    (33.33, 36, "Python + LangChain + MCP = 你的优势"),
]

voice = "zh-CN-YunyangNeural"

segments = []
for i, (start, end, text) in enumerate(subtitle_lines):
    seg_file = os.path.join(output_dir, f"seg_{i:02d}.mp3")
    duration = end - start
    # Add a bit of buffer so speech isn't cut off
    cmd = [
        "edge-tts", "--voice", voice, "--text", text,
        "--write-media", seg_file,
        "--rate", "+6%",
    ]
    print(f"[{i+1}/{len(subtitle_lines)}] {text}")
    subprocess.run(cmd, capture_output=True)
    segments.append((seg_file, duration, start))

print("All segments generated.")

# Generate silence padding
silence_path = os.path.join(output_dir, "silence.mp3")
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
    "-t", "0.5", silence_path
], capture_output=True)
print("Silence generated.")

# Build concat filter
with open(os.path.join(output_dir, "segments.txt"), "w", encoding="utf-8") as f:
    for seg_file, _, _ in segments:
        f.write(f"file '{seg_file}'\n")

concat_path = os.path.join(output_dir, "full_audio.mp3")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", os.path.join(output_dir, "segments.txt"),
    "-c:a", "libmp3lame", "-ar", "44100",
    concat_path
], capture_output=True)
print(f"Concatenated: {concat_path}")

# Mux with video
for video_name, output_name in [
    ("agent-v4.mp4", "agent-v4-final.mp4"),
    ("agent-v4-xhs.mp4", "agent-v4-xhs-final.mp4"),
]:
    video_path = os.path.join(output_dir, video_name)
    out_path = os.path.join(output_dir, output_name)
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", concat_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        out_path
    ], capture_output=True)
    print(f"Muxed: {out_path}")

print("Done!")
