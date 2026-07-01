#!/usr/bin/env python3
"""Fixed: generate edge-tts audio and mux with video using filter_complex for timing"""
import subprocess, os

output_dir = r"C:\Users\ZhouXuan\.openclaw\workspace\remotion-agent-video\output"
ffmpeg = r"C:\tools\ffmpeg\bin\ffmpeg.exe"

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

# Step 1: generate individual WAV segments
print("=== Generating TTS segments ===")
segments = []
for i, (start, end, text) in enumerate(subtitle_lines):
    seg_file = os.path.join(output_dir, f"seg_{i:02d}.wav")
    print(f"[{i+1}/12] {start:.1f}s-{end:.1f}s: {text}")
    subprocess.run([
        "edge-tts", "--voice", voice, "--text", text,
        "--write-media", seg_file, "--rate", "+4%",
    ], capture_output=True)
    segments.append((seg_file, start, end - start))

# Step 2: build ffmpeg filter_complex with atrim + adelay per segment
print("\n=== Building audio timeline ===")
filter_parts = []
for i, (seg_file, start, dur) in enumerate(segments):
    label = f"s{i}"
    # Trim each segment to its natural duration (edge-tts output), then delay to start time
    filter_parts.append(
        f"[{i}:a]atrim=0:{dur},adelay={int(start*1000)}|{int(start*1000)},apad=pad_dur=36[pad{i}]"
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
    print(f"\n=== Muxing: {video_name} -> {output_name} ===")
    
    cmd = [ffmpeg, "-y"]
    # Add video input
    cmd += ["-i", video_path]
    # Add all audio segment inputs
    for seg_file, _, _ in segments:
        cmd += ["-i", seg_file]
    # filter + map
    cmd += [
        "-filter_complex", filter_complex,
        "-map", "0:v:0",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-ar", "44100", "-b:a", "128k",
        "-shortest",
        out_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("STDERR:", result.stderr[-500:])
    else:
        print(f"OK: {out_path}")

print("\n=== Done ===")
