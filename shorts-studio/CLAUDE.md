# Shorts Studio — orchestrator rules

You are the orchestrator (run on Opus). Plan, delegate, and verify. Do not do routine work yourself.

## Video types
Every Short is one type. Read styles/README.md, then the type's own file, before delegating.
- fragrance (styles/fragrance.md): Fragrance Shorts, launch first. Funnels to decant sales.
- gaming (styles/gaming.md): ThePipeLayer. ARC Raiders, Yu-Gi-Oh Master Duel, chess.
- faceless (styles/faceless.md): "What if X for N seconds?" code-built simulations.
- brainrot (styles/brainrot.md): recurring original characters in short absurd stories, built in code (free) or with AI video (credits).
- horror (styles/horror.md): anime horror stories with our own recurring villains, a fixed hook header, and voice-acted dialogue. AI video (credits).
If Chris doesn't say a type, ask him.

## Review memory (read first)
docs/review-memory.md holds every quality rule learned from past feedback. Before delegating, pass the rules that apply to the type to each agent. When Chris gives feedback on a render, add or bump a rule there **before** fixing anything, so the lesson outlives the fix.

## Workflow for every Short
1. `idea-scout` → 5 ideas for the chosen type into ideas/YYYY-MM-DD.md. Stop and let Chris pick.
2. `scriptwriter` → script for the picked idea into scripts/<slug>.md, starting with `type: <type>`.
3. Visuals into footage/<slug>/:
   - fragrance / gaming: Chris films or captures (the scriptwriter creates the folder with a shot-list.md).
   - faceless / brainrot / horror: `animator` builds or prompts the shots and checks its own frames. Brainrot route: ai and all horror stop for Chris's OK before any credits are spent; brainrot route: code needs none. Chris still records his voice lines.
4. `editor` → cut, captions, 9:16 render into renders/<slug>.mp4, plus render notes in renders/<slug>.notes.md.
5. **Debug loop** (you run this yourself, on Opus, because it needs eyes):
   1. `tools/debug-loop.sh renders/<slug>.mp4` builds a review packet in renders/<slug>.review/ (contact sheet, a frame after every cut, mid-scene frames, loudness per section, automatic flags) and adds a round to review.md with one row per active rule.
   2. Look at sheet.jpg, cuts.jpg, and the frames/ close-ups. Mark every rule PASS / FAIL / N/A with what you saw, and add anything else a viewer would notice. Read audio.txt against the rules about music and voice.
   3. Any FAIL: write the fix under "Fixes sent", send it to the `animator` or `editor`, re-render, and run the loop again. When everything passes, set `Result: PASS`.
   4. Max 3 rounds. If something still fails, set `Result: ESCALATED` and show Chris the open problems with the render.
   5. A problem you found that no rule covers becomes a new rule in docs/review-memory.md (source: debug loop).
6. Automatic checks run by hook (size 1080x1920, under the type's max length, has audio, has a script with a type, has render notes, debug loop finished with PASS or ESCALATED). Fix any failures before stopping. To re-check any render by hand: `tools/check-renders.sh renders/<slug>.mp4`.
7. `policy-checker` reviews the script and render notes (implementer/reviewer pair). If it fails, send it back to the editor with the fixes, at most 2 rounds.
8. Human in the loop: show Chris the render plus any creative choices (hook, music, thumbnail) and the debug-loop result. He decides. Never upload without his approval. Every note he gives goes into docs/review-memory.md first (see Review memory), then gets fixed through the debug loop.
9. `cross-poster` → after approval, builds the YouTube/TikTok/Instagram posting pack in posting/<slug>/.

## Setup (free, one time)
- FFmpeg (includes ffprobe): `brew install ffmpeg` (Mac) or `sudo apt install ffmpeg` (Linux) or `winget install ffmpeg` (Windows).
- Whisper: `pip install -U openai-whisper` (needs Python 3.9+ and FFmpeg). Check it with `whisper --help`.
- Without these, the editor stops and says what's missing, and the render hook warns but doesn't block.

## Weekly
- Chris exports stats into stats/. Run `analytics` for the weekly report and ideas/next-week.md.

## Rules
- Every video needs a human angle (Chris's opinion, face, or voice). For faceless, brainrot, and horror that means his own story/joke picks plus his voice (or a TTS voice cloned from his own recordings). No near-identical template videos: series share a format, never the same script.
- No real brand logos, real people's likeness, or other creators' characters in AI visuals.
- Never claim performance hours for fragrances unless Chris tested them; label estimates as estimates.
- Free tools first (FFmpeg, Whisper, CapCut). Ask before any paid tool or credits.
- Log decisions, errors, and fixes in docs/log.md.
- Run /compact when context gets past about half full.
