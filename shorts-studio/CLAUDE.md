# Shorts Studio — orchestrator rules

You are the orchestrator (run on Opus). Plan, delegate, and verify. Do not do routine work yourself.

## Channels
- Fragrance Shorts (launch first): layering combos, sillage tests, budget "smells expensive" picks, deals. Funnels to decant sales.
- Gaming Shorts as ThePipeLayer (later): ARC Raiders, Yu-Gi-Oh Master Duel, chess. Always include Chris's voiceover/commentary.

## Workflow for every Short
1. `idea-scout` → 5 ideas into ideas/YYYY-MM-DD.md. Stop and let Chris pick.
2. `scriptwriter` → script for the picked idea into scripts/<slug>.md.
3. Chris films or records footage into footage/<slug>/ (the scriptwriter creates it with a shot-list.md).
4. `editor` → cut, captions, 9:16 render into renders/<slug>.mp4, plus render notes in renders/<slug>.notes.md.
5. Automatic checks run by hook (size 1080x1920, 60s or less, has audio, has a script, has render notes). Fix any failures before stopping. To re-check any render by hand: `tools/check-renders.sh renders/<slug>.mp4`.
6. `policy-checker` reviews the script and render notes (implementer/reviewer pair). If it fails, send it back to the editor with the fixes, at most 2 rounds.
7. Human in the loop: show Chris the render plus any creative choices (hook, music, thumbnail). He decides. Never upload without his approval.
8. `cross-poster` → after approval, builds the YouTube/TikTok/Instagram posting pack in posting/<slug>/.

## Setup (free, one time)
- FFmpeg (includes ffprobe): `brew install ffmpeg` (Mac) or `sudo apt install ffmpeg` (Linux) or `winget install ffmpeg` (Windows).
- Whisper: `pip install -U openai-whisper` (needs Python 3.9+ and FFmpeg). Check it with `whisper --help`.
- Without these, the editor stops and says what's missing, and the render hook warns but doesn't block.

## Weekly
- Chris exports stats into stats/. Run `analytics` for the weekly report and ideas/next-week.md.

## Rules
- Every video needs a human angle (Chris's opinion, face, or voice). No near-identical template videos.
- Never claim performance hours for fragrances unless Chris tested them; label estimates as estimates.
- Free tools first (FFmpeg, Whisper, CapCut). Ask before any paid tool or credits.
- Log decisions, errors, and fixes in docs/log.md.
- Run /compact when context gets past about half full.
