import subprocess, os

output_dir = r"C:\Users\ZhouXuan\.openclaw\workspace\remotion-agent-video\output"
ffmpeg = r"C:\tools\ffmpeg\bin\ffmpeg.exe"

# Build one continuous audio track with precise adelay
# each seg_NN.wav is placed at its start time (ms)
delays = [0, 3190, 5990, 8720, 11740, 14660, 20300, 23800, 27680, 31350, 34590, 37560]

labels = []
filter_parts = []
for i, ms in enumerate(delays):
    labels.append(f"[{i}]")
    filter_parts.append(f"[{i}:a]adelay={ms}|{ms}[d{i}]")

mix_inputs = "".join(f"[d{i}]" for i in range(12))
filter_parts.append(f"{mix_inputs}amix=12:normalize=0[out]")
fc = ";".join(filter_parts)

cmd = [ffmpeg, "-y"]
for i in range(12):
    cmd += ["-i", os.path.join(output_dir, f"seg_{i:02d}.wav")]
cmd += ["-filter_complex", fc, "-map", "[out]", "-ac", "1", os.path.join(output_dir, "narration.wav")]

r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr[-500:])
else:
    print("OK: narration.wav")
