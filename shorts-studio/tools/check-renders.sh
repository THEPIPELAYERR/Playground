#!/usr/bin/env bash
# Automatic checks on renders: 1080x1920, 60s or less, has audio, has a matching script.
# As a Stop hook (no args): checks renders changed in the last 15 minutes.
#   Exit 2 = block and tell Claude what to fix.
# Manually / from cross-poster: tools/check-renders.sh renders/<slug>.mp4 [...]
#   Checks exactly those files, however old they are.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

if ! command -v ffprobe >/dev/null 2>&1; then
  # Exit 1 = non-blocking: the warning is shown, but Claude isn't trapped in a loop.
  echo "check-renders: ffprobe not found, render checks skipped. Install FFmpeg (see Setup in CLAUDE.md)." >&2
  exit 1
fi

fail=0
check() {
  local f="$1" slug dur size audio
  slug=$(basename "$f" .mp4)
  if [ ! -f "$f" ]; then echo "$f: file not found" >&2; fail=1; return; fi
  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null)
  size=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$f" 2>/dev/null)
  audio=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$f" 2>/dev/null)
  if [ -z "$dur" ] || [ -z "$size" ]; then
    echo "$f: ffprobe could not read it (corrupt or unfinished render?)" >&2; fail=1; return
  fi
  [ "$size" != "1080x1920" ] && { echo "$f: size is $size, must be 1080x1920" >&2; fail=1; }
  awk -v d="$dur" 'BEGIN{exit !(d > 60)}' && { echo "$f: ${dur}s long, must be 60s or less" >&2; fail=1; }
  [ -z "$audio" ] && { echo "$f: no audio track" >&2; fail=1; }
  [ ! -f "scripts/$slug.md" ] && { echo "$f: no matching script in scripts/$slug.md" >&2; fail=1; }
  [ ! -f "renders/$slug.notes.md" ] && { echo "$f: no render notes in renders/$slug.notes.md" >&2; fail=1; }
}

if [ $# -gt 0 ]; then
  for f in "$@"; do check "$f"; done
else
  while IFS= read -r -d '' f; do check "$f"; done < <(find renders -name '*.mp4' -mmin -15 -print0 2>/dev/null)
fi

[ $fail -eq 1 ] && exit 2
exit 0
