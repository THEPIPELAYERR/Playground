# Review: mash-finale-chicken

Rules: docs/review-memory.md. Max 3 rounds, then escalate to Chris.

## Round 1
Packet: sheet.jpg, cuts.jpg, frames/, audio.txt

Automatic flags:
- 5 frozen stretch(es) over 1.5s, check for a stuck shot

| Rule | Result (PASS/FAIL/N/A) | What I saw |
|---|---|---|
| R1: Walk cycles must read correctly: the planted leg stays straight, the k | | |
| R2: Real-world scale: vehicles, doors, and furniture are sized against the | | |
| R3: Music matches the stakes and builds: a pulse or heartbeat under the ho | | |
| R4: Voices must sound human. Robotic TTS (flite, espeak, old system voices | | |
| R5: Captions follow the real voice timing (Whisper word timestamps), not e | | |
| R6: Copy a reference's format, never its characters or lines. | | |
| R7: Fixed layout: hook header at top for the whole video, 16:9 clip center | | |
| R8: Hosts and voices are our own: no TV or cartoon characters as hosts, an | | |

Fixes sent:
- Frozen stretches on static cards (hospital, armistice, Klinger, BJ). Fix: slow push-in on every scene.

Result: FAIL

## Round 2
Packet: sheet.jpg, cuts.jpg, frames/, audio.txt

Automatic flags:
- none

| Rule | Result (PASS/FAIL/N/A) | What I saw |
|---|---|---|
| R1: Walk cycles must read correctly: the planted leg stays straight, the k | | |
| R2: Real-world scale: vehicles, doors, and furniture are sized against the | | |
| R3: Music matches the stakes and builds: a pulse or heartbeat under the ho | | |
| R4: Voices must sound human. Robotic TTS (flite, espeak, old system voices | | |
| R5: Captions follow the real voice timing (Whisper word timestamps), not e | | |
| R6: Copy a reference's format, never its characters or lines. | | |
| R7: Fixed layout: hook header at top for the whole video, 16:9 clip center | | |
| R8: Hosts and voices are our own: no TV or cartoon characters as hosts, an | | |

Fixes sent:
- "CHICKEN." clipped at the right edge by the push-in. Fix: smaller title.

Result: FAIL

## Round 3
Packet: sheet.jpg, cuts.jpg, frames/, audio.txt

Automatic flags:
- none

| Rule | Result (PASS/FAIL/N/A) | What I saw |
|---|---|---|
| R1: Walk cycles must read correctly: the planted leg stays straight, the k | N/A | no walking characters |
| R2: Real-world scale: vehicles, doors, and furniture are sized against the | N/A | no characters next to props |
| R3: Music matches the stakes and builds: a pulse or heartbeat under the ho | PASS | heartbeat under the hook and the secret, impact on every cut, pads build, riser into the stones payoff; sections rise from -13.7 to -11.8 dB toward the end |
| R4: Voices must sound human. Robotic TTS (flite, espeak, old system voices | PASS | Chris's own recording (New Recording 8), best take of each line |
| R5: Captions follow the real voice timing (Whisper word timestamps), not e | PASS | word timestamps from Parakeet TDT (sherpa-onnx) on the source audio; spot-checked 'chicken.' in the word scene and 'Hawkeye' in quiet: captions land on the word |
| R6: Copy a reference's format, never its characters or lines. | N/A | no reference video |
| R7: Fixed layout: hook header at top for the whole video, 16:9 clip center | N/A | horror only |
| R8: Hosts and voices are our own: no TV or cartoon characters as hosts, an | PASS | no host; voice is Chris's own |

Fixes sent:
- none

Result: PASS
