@echo off
set PATH=C:\tools\ffmpeg\bin;%PATH%
cd /d "C:\Users\ZhouXuan\.openclaw\workspace\social-content\2026-06-16"
npx hyperframes render --output video-raw.mp4
