#!/usr/bin/env bash
# Debug loop, step 1: build a review packet for a render so it can be looked at before Chris sees it.
#   tools/debug-loop.sh renders/<slug>.mp4
# Writes renders/<slug>.review/:
#   sheet.jpg      16 frames spread evenly over the video (4x4)
#   cuts.jpg       a frame just after each scene cut (up to 12)
#   frames/        full-size frames at each cut + the busiest moments, for close-ups
#   audio.txt      loudness (LUFS), true peak, loudness per section, silent gaps
#   flags.txt      automatic problems found (empty = none)
#   review.md      checklist: one line per active rule in docs/review-memory.md, to fill in
# Exit 0 = packet built (read flags.txt and review.md), 1 = could not run.
set -u
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 1
f="${1:-}"
[ -f "$f" ] || { echo "usage: tools/debug-loop.sh renders/<slug>.mp4" >&2; exit 1; }
command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null || { echo "debug-loop: needs FFmpeg (see Setup in CLAUDE.md)" >&2; exit 1; }

slug=$(basename "$f" .mp4)
out="renders/$slug.review"
mkdir -p "$out/frames"
rm -f "$out"/frames/*.jpg "$out/flags.txt"
touch "$out/flags.txt"
flag() { echo "- $*" >> "$out/flags.txt"; }

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
size=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$f")
fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$f")

# 1) Even contact sheet
ffmpeg -v error -y -i "$f" -vf "fps=16/$dur,scale=270:-1,tile=4x4" -frames:v 1 "$out/sheet.jpg"

# 2) Scene cuts: timestamps, then one full-size frame 0.2s after each
# Hard cuts (scene change) plus fade-through-black cuts (end of a short black stretch), merged.
hard=$(ffmpeg -v info -i "$f" -vf "select='gt(scene,0.25)',showinfo" -an -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*' | cut -d: -f2)
fades=$(ffmpeg -v info -i "$f" -vf "blackdetect=d=0.03:pix_th=0.10" -an -f null - 2>&1 \
  | grep -o 'black_end:[0-9.]*' | cut -d: -f2)
cuts=$(printf '%s\n%s\n' "$hard" "$fades" | grep . | sort -n \
  | awk 'NR==1||$1-last>0.5{print; last=$1}' | awk -v d="$dur" '$1>0.3 && $1<d-0.3' | head -12)
n=0
for t in $cuts; do
  n=$((n+1))
  ts=$(awk -v t="$t" -v d="$dur" 'BEGIN{x=t+0.2; if(x>d-0.05)x=t; printf "%.2f", x}')
  ffmpeg -v error -y -ss "$ts" -i "$f" -frames:v 1 -q:v 3 "$out/frames/cut-$(printf %02d $n)-${ts}s.jpg"
done
if [ "$n" -gt 0 ]; then
  ffmpeg -v error -y -pattern_type glob -i "$out/frames/cut-*.jpg" -vf "scale=270:-1,tile=6x$(( (n+5)/6 )):padding=4" -frames:v 1 "$out/cuts.jpg"
fi
# Mid-scene frames (where characters are mid-action, e.g. mid-stride), at 1/3 and 2/3 of each scene
prev=0
for t in $cuts $dur; do
  for frac in 0.33 0.66; do
    ts=$(awk -v a="$prev" -v b="$t" -v k="$frac" 'BEGIN{printf "%.2f", a+(b-a)*k}')
    ffmpeg -v error -y -ss "$ts" -i "$f" -frames:v 1 -q:v 3 "$out/frames/mid-${ts}s.jpg"
  done
  prev=$t
done

# 3) Audio: overall loudness + per-section + silent gaps
{
  echo "file: $f"; echo "length: ${dur}s  size: $size  fps: $fps"; echo
  if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$f" | grep -q .; then
    ffmpeg -v info -i "$f" -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary:/,$p' | grep -E 'I:|Peak:|LRA:' | sed 's/^ *//'
    echo; echo "loudness per section (mean dB):"
    secs=8; step=$(awk -v d="$dur" -v s=$secs 'BEGIN{printf "%.3f", d/s}')
    for i in $(seq 0 $((secs-1))); do
      st=$(awk -v i=$i -v s="$step" 'BEGIN{printf "%.2f", i*s}')
      mv=$(ffmpeg -v info -ss "$st" -t "$step" -i "$f" -af volumedetect -vn -f null - 2>&1 | grep -o 'mean_volume: [-0-9.]*' | awk '{print $2}')
      echo "  ${st}s: ${mv} dB"
    done
    echo; echo "silent gaps over 1.2s:"
    ffmpeg -v info -i "$f" -af silencedetect=noise=-45dB:d=1.2 -f null - 2>&1 | grep -o 'silence_start: [0-9.]*\|silence_duration: [0-9.]*' | paste - - || true
  else
    echo "NO AUDIO TRACK"
  fi
} > "$out/audio.txt"

# 4) Automatic flags
[ "$size" != "1080x1920" ] && flag "size is $size, must be 1080x1920"
grep -q "NO AUDIO" "$out/audio.txt" && flag "no audio track"
I=$(grep -m1 -o 'I: *[-0-9.]*' "$out/audio.txt" | grep -o '[-0-9.]*$')
P=$(grep -m1 -o 'Peak: *[-0-9.]*' "$out/audio.txt" | grep -o '[-0-9.]*$')
[ -n "${I:-}" ] && awk -v i="$I" 'BEGIN{exit !(i < -20 || i > -9)}' && flag "loudness ${I} LUFS, aim for -16 to -12 (Shorts)"
[ -n "${P:-}" ] && awk -v p="$P" 'BEGIN{exit !(p > -0.5)}' && flag "true peak ${P} dBFS, risk of clipping (keep under -1)"
grep -q 'silence_start' "$out/audio.txt" && flag "dead air: silent gap over 1.2s (see audio.txt), fine only if it's a deliberate beat"
[ "$n" -eq 0 ] && awk -v d="$dur" 'BEGIN{exit !(d > 8)}' && flag "no scene cuts detected in ${dur}s, check the pacing"
# Black or frozen frames
bl=$(ffmpeg -v info -i "$f" -vf "blackdetect=d=0.6:pix_th=0.08" -an -f null - 2>&1 | grep -c black_start)
[ "$bl" -gt 0 ] && flag "$bl black stretch(es) over 0.6s, fine only for deliberate fades or horror beats"
fr=$(ffmpeg -v info -i "$f" -vf "freezedetect=n=0.002:d=1.5" -an -f null - 2>&1 | grep -c freeze_start)
[ "$fr" -gt 0 ] && flag "$fr frozen stretch(es) over 1.5s, check for a stuck shot"

# 5) Checklist from review memory (only active rules)
round=1
if [ -f "$out/review.md" ]; then
  round=$(( $(grep -c '^## Round' "$out/review.md") + 1 ))
else
  printf '# Review: %s\n\nRules: docs/review-memory.md. Max 3 rounds, then escalate to Chris.\n' "$slug" > "$out/review.md"
fi
{
  echo; echo "## Round $round"
  echo "Packet: sheet.jpg, cuts.jpg, frames/, audio.txt"
  echo; echo "Automatic flags:"; if [ -s "$out/flags.txt" ]; then cat "$out/flags.txt"; else echo "- none"; fi
  echo; echo "| Rule | Result (PASS/FAIL/N/A) | What I saw |"; echo "|---|---|---|"
  if [ -f docs/review-memory.md ]; then
    grep -E '^\| R[0-9]+ ' docs/review-memory.md | grep '| active |' | awk -F'|' '{gsub(/^ +| +$/,"",$2); gsub(/^ +| +$/,"",$4); print "| " $2 ": " substr($4,1,70) " | | |"}'
  fi
  echo; echo "Fixes sent:"; echo; echo "Result: OPEN"
} >> "$out/review.md"

echo "debug-loop: round $round packet in $out/ ($(wc -l < "$out/flags.txt") automatic flag(s))."
[ -s "$out/flags.txt" ] && cat "$out/flags.txt"
exit 0
