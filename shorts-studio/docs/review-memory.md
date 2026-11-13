---
tags: [shorts-studio, review-memory]
---
# Review memory

Every note Chris (or the debug loop) has ever made about a render, turned into a rule, so the same
mistake never ships twice. This file is the channel's long-term memory for quality. It's plain
Markdown, so it opens in the Obsidian vault as-is.

## How it's used
- **Before working:** scriptwriter, animator, and editor read the rules that apply to their type
  (`applies to`) and follow them.
- **In the debug loop:** every active rule is checked against the review packet
  (tools/debug-loop.sh) and marked PASS / FAIL / N/A in renders/<slug>.review/review.md.
- **After Chris's feedback:** the orchestrator adds a rule right away, before fixing anything:
  next free ID, what went wrong in Chris's words, the rule, and how to check it. A note that
  repeats an existing rule raises its `hits` count instead of adding a duplicate.
- Rules are never deleted. If one stops applying, set `status: retired` and say why.

## Active rules

| ID | Applies to | Rule | How to check it | Source | Hits | Status |
|---|---|---|---|---|---|---|
| R1 | all animated | Walk cycles must read correctly: the planted leg stays straight, the knee bends only while the foot swings forward, and toes point the way the character walks. | Close-up frames mid-stride and after any turn. Feet never trail behind the knee like a kick. | Chris, walking test 2026-11-13: "his feet are backward in some scenes" | 1 | active |
| R2 | all animated | Real-world scale: vehicles, doors, and furniture are sized against the characters. A car is about 1.5x a person's height and 4x their width; anything closer to the camera looks bigger, never smaller. | Frames where a character and a prop share the shot. | Chris, walking test 2026-11-13: "the cars are smaller than him" | 1 | active |
| R3 | all | Music matches the stakes and builds: a pulse or heartbeat under the hook, then layers added each beat, an impact on every cut, and a peak right before the payoff. No flat loops. | debug-loop audio sections: loudness rises toward the payoff; an impact at each scene cut. | Chris, walking test 2026-11-13: "make the music a little more high stakes" | 1 | active |
| R4 | all with voice | Voices must sound human. Robotic TTS (flite, espeak, old system voices) never ships. Use Chris's own recordings, a voice cloned from them, or a natural AI voice he approves. | Note the voice source in render notes; FAIL if it's a robotic engine. | Chris, walking test 2026-11-13: "less 80s robotic" | 1 | active |
| R5 | all with captions | Captions follow the real voice timing (Whisper word timestamps), not evenly spaced guesses. | Spot-check 3 words per scene: caption lands within 0.15s of the spoken word. | Debug loop, walking test 2026-11-13 | 1 | active |
| R6 | horror, brainrot | Copy a reference's format, never its characters or lines. | Compare the cast and dialogue with the reference in ideas/refs/. | Chris's horror reference 2026-11-13 (another creator's villain) | 1 | active |
| R7 | horror | Fixed layout: hook header at top for the whole video, 16:9 clip centered, ALL CAPS word-by-word captions under the clip, bottom 300px kept clear. | Contact sheet: header present in every frame; captions never overlap the clip. | Chris's horror reference 2026-11-13 | 1 | active |

## Retired rules
_(none yet)_
