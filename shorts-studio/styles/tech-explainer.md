# Type: tech-explainer — ranked tech lists with an original host

Based on a "Top 10 GitHub repos" video Chris shared: a cartoon host narrates a countdown over clean
editorial cards. Copy the format. The reference's host is a TV cartoon character with an imitated
voice; never use any existing character or a copy of a real person's voice (review memory R8).

## Format
- **Topic:** a ranked list Chris actually uses or has tried: GitHub repos (start with his own
  stars, see docs/toolbox.md), AI tools, free apps, Linux commands, home-server tools.
- **Length:** 45-180 seconds. Short lists (3-5 items) for 45-60s, a top 10 up to 180s.
  YouTube Shorts allows up to 3 minutes; TikTok allows longer.
- **Per item (about 12-18s):** rank number + name → what it's for, in one plain sentence → one
  proof card (stars, a key feature, a short list of what's inside) → why it's worth using.
- **Hook (0-3s):** the promise, e.g. "10 GitHub repos that teach you more than a degree".
- **Ending:** all items on one screen plus a one-line takeaway (the reference used
  "Don't just star them. Use them.", so write our own).
- Chris's own take on at least two items ("I use this for…"), so it isn't a template list.

## Look (built in code with HyperFrames, free)
- 1080x1920. Warm off-white paper background, dark ink, one accent color.
  The HyperFrames `claude` or `monochrome` preset is a close fit.
- Top bar on every frame: series label on the left (e.g. "GITHUB REPOS · TOP 10") and progress
  dots 1-N on the right, the current item filled.
- Item intro: a huge serif rank number, the name next to it, and owner/repo in mono under it.
- Cards: soft rounded panels with small mono labels ("ABOUT THIS REPOSITORY", "WHAT'S INSIDE"),
  simple bar charts for stars, checklists, category grids, code-terminal panels for commands.
  Each card animates in (fade + small rise), and lists fill in line by line with the voice.
- Captions: serif, word by word, at the bottom (y ≈ 1500-1640), the current word darker and
  underlined. Keep the bottom 280px clear.
- The host stands in the lower left, about 40% of the frame height, overlapping the cards a little.

## Host (original, recurring)
- One recurring mascot host for the series, designed once and added to the table below before
  the first episode. Built as a 2D or 3D character in code (HyperFrames + Three.js or SVG), with
  idle sway, blinks, mouth flaps timed to the voice, and a pointing gesture on each new item.
- Voice: Chris's own voice or his VoiceStudio clone (docs/toolbox.md). No celebrity or
  cartoon-character voice copies.

| Host name | Look (shapes, colors, outfit) | Personality | Voice |
|---|---|---|---|
| _(design before episode 1)_ | | | |

## Accuracy
- Every number on screen (stars, counts, prices) comes from the source checked the day the script
  is written, listed in the script's Sources section, and rounded honestly ("nearly 400K").
- Star counts change: say "as of <month year>" in the render notes.
- Describe repos from their own README, not from memory.
