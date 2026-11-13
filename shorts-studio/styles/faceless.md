# Type: faceless — "What if…" simulations

Taken from the whatif.sim format: one "What if X for N seconds?" question, answered with a
code-built 3D simulation, real numbers, and a big payoff shot.

## Series formula
- Title/hook on screen: "What if <everyday thing> disappeared / doubled / stopped for <N> seconds?"
  (e.g. all rubber, friction, the Moon's gravity, every phone signal).
- First 2s: the most dramatic frame of the sim, with the question as big text.
- Beats (about 6-10, 3-6s each): setup scene → the change happens → 3-5 consequences, each with one
  sourced number on screen (e.g. "352 cars", "1.2 s to stop") → payoff shot → loop back to the question.
- Ending: a one-line answer plus "What should I break next?" to pull comment ideas.

## Visuals
- Built in code by the `animator` (Three.js scene rendered headless, or Remotion), rendered on Chris's
  machine. No AI video generation needed, so no credits.
- Look: one consistent world (low-poly city / voxel style), same camera language every episode,
  a top-left counter for the key number, a step label strip at the top.
- Optional mascot duo (an original character + a box buddy) who react between beats. Must be our own
  designs, never copied from the reference page.

## Facts
- Every number on screen needs a source listed in the script's `## Sources` section. If a number is an
  estimate or a simplification, the on-screen text says "≈" or "est.".

## Human angle
- Chris picks the question, approves the facts, and does the voiceover (or a TTS voice cloned from
  his own recordings). Each episode needs at least one line of his own take ("honestly the scariest
  part is…").

## Captions
- Word-by-word, bold, centered, with key numbers highlighted.
