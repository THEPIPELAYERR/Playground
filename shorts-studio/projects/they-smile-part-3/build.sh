#!/usr/bin/env bash
# Rebuilds renders/they-smile-part-3.mp4 from scratch (about 5 minutes).
# Needs: node + playwright (with Chromium), python3 + numpy, ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build
node render.js build/video.mp4            # frames -> silent video, also writes timeline.json
python3 audio.py timeline.json build/audio.wav
ffmpeg -v error -y -i build/video.mp4 -i build/audio.wav -map 0:v -map 1:a \
  -c:v libx264 -preset slow -crf 22 -tune animation -pix_fmt yuv420p -maxrate 6M -bufsize 12M \
  -af "loudnorm=I=-14:TP=-1.5:LRA=14" -ar 48000 -c:a aac -b:a 192k -movflags +faststart -shortest \
  ../../renders/they-smile-part-3.mp4
echo "done: renders/they-smile-part-3.mp4"
