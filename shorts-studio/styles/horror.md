# Type: horror — anime horror story Shorts

Based on the anime horror format Chris shared (a creepy carnival-clown villain who finds a lost girl,
returns her to her mom, then threatens the mom). Copy the **format**, never the characters: the
reference's villain and dialogue belong to another creator. Our villains and victims live in
styles/horror-cast.md.

## Story formula (15-40 seconds)
1. **Innocent setup (0-3s):** someone vulnerable in an ordinary place (a lost kid on a busy street,
   a night-shift guard on rounds, a babysitter alone).
2. **The villain appears (3-8s):** close-up, too-wide smile, one line that is friendly on the surface
   and wrong underneath.
3. **Misdirect (8-20s):** the villain seems to help. The viewer expects the worst; it doesn't come yet.
4. **Reveal (20-30s):** the help was the setup. The villain turns on the person who should have
   been paying attention.
5. **Button line (last 2-3s):** one short threat or twist the comments will quote.

Dialogue lines are 2-8 words, one speaker per shot. Lines sound spoken, not written.

## Layout (fixed, every episode)
- 1080x1920 black frame.
- **Hook header** at the top (y ≈ 230-560): 2-3 lines, white, sentence case, bold sans, ending in
  one emoji. It stays on screen the whole video. It is the comment bait, e.g.
  "If you leave your kid alone at night, [villain] might keep them 😨".
- **Clip window** in the middle: the 16:9 anime clip scaled to 1080x608, centered (y ≈ 610-1218).
- **Captions** under the clip (y ≈ 1300-1500): ALL CAPS, heavy bold white, black outline,
  word by word, the current word fully opaque and the next one fading in.
  Never cover the clip or the bottom 300px (platform UI).

## Visuals (AI, needs credits)
- Anime look: clean cel shading, cinematic city lighting, shallow depth of field.
  Same palette and lighting every episode.
- Every shot moves: slow push-ins on the villain, handheld drift on the victim, a fast whip-pan or
  motion blur between locations.
- Character descriptions are pasted word for word from styles/horror-cast.md into every prompt,
  so the villain looks identical in every shot and episode.
- The animator writes prompts/<slug>.json and stops for Chris's OK before any credits are spent.
- No gore. Fear comes from the smile, the line delivery, and the music, not from injuries.
  Keeps the channel advertiser-friendly.

## Sound
- Voice acting, not narration: each character has a voice (Chris voices at least one, or a voice
  cloned from his recordings with VoiceStudio, see docs/toolbox.md). Robotic TTS (flite, espeak, old system voices) is never acceptable.
  See docs/review-memory.md.
- Under the villain: a music-box or detuned carnival loop, then a low drone. Silence for half a
  second right before the button line, then a hit.

## Captions
Word by word, timed from Whisper word timestamps on the final voice track, never guessed.
