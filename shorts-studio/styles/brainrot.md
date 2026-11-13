# Type: brainrot — recurring character stories

Taken from the fruit "World Hanging Championship" format, made with the story-remix workflow
(break down a viral video → rewrite it with our own characters → scene prompts → image-to-video).

## Story formula
- One simple stake everyone gets in a second (a contest, a dare, a bet, a $1,000,000 prize).
- Recurring original cast from styles/brainrot-cast.md, so viewers come back for the characters.
- Beat pattern: setup + stakes (0-5s) → crowd/side-character reactions (cutaways) → escalation by
  time skips ("3 hours later", "next day", arena empty, janitor sweeping) → twist payoff
  (the "winner" was asleep, the prize was a coupon, etc.) → button joke.
- Short dialogue lines, 3-8 words, one speaker per shot.

## Remix workflow (from the tutorial video)
1. Chris drops a reference (link or notes) into ideas/refs/<slug>.md.
2. idea-scout breaks it down: story beats, character roles, why it hooks. Structure only.
3. It rewrites 3 versions with our cast and picks the one most likely to go viral, saying why.
4. The scriptwriter turns the pick into scenes and sets the visual route (below).
5. The animator makes the shots for that route and drops them into footage/<slug>/.

Never copy the reference's characters, dialogue, or jokes word for word.
No real brand logos (car badges etc.) or real people's faces. Both risk takedowns and demonetization.

## Visual route
The script says `route: code` or `route: ai` under its `type:` line. Default is `code`.

### route: code — code-built cartoon (free)
Taken from the "3D cartoon animations with just code" format (Three.js channels like IFOLOGY).
- Simple stylized 3D cartoon look: chunky low-poly characters, big heads, dot or oval eyes,
  flat colors, soft shadows, simple sets (bank, office, arena, street, train station).
- Each character is a reusable model in footage/_cast/<name>.js, built once from its cast entry,
  so it looks identical in every episode. New sets go in footage/_sets/.
- Acting comes from code: walk cycles, head turns, arm gestures, mouth flaps timed to the voice
  lines, blinks, and camera cuts (wide, close-up, over-the-shoulder, push-in).
- Costs $0 per clip. It renders on Chris's computer.

### route: ai — AI image → video (credits)
- Pixar-like 3D look, same lighting and palette every episode. The animator writes
  prompts/<slug>.json (image prompt per scene in 9:16, then an image-to-video prompt with dialogue
  and camera move), pasting character descriptions word for word from the cast file.
- Costs credits (Kling, Higgsfield, etc.). Ask Chris before spending any, and say how many clips
  and roughly what it will cost. Free tiers first.

## Human angle
- Chris picks the story and jokes and voices at least one character or the narrator
  (or a TTS voice cloned from his own recordings).

## Captions
- One word at a time, big bold white text with a black outline, center of the frame.
