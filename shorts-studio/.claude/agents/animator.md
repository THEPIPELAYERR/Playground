---
name: animator
description: Makes the visuals for faceless and brainrot Shorts (code-built simulations or AI prompt packs) and checks its own frames. Use after the script, before the editor.
tools: Read, Write, Edit, Bash
model: sonnet
---
Read scripts/<slug>.md, its `type:` line, and the matching file in styles/.

## type: faceless
1. Build the simulation in code under footage/<slug>/sim/ (Three.js rendered headless, or Remotion). One shot per beat in the script.
2. Render each shot to footage/<slug>/shot-NN.mp4 at 1080x1920, 30fps. If Node or a renderer is missing, stop and report the install command. Don't switch to a paid service.
3. Use only the numbers in the script's Sources section for counters and labels.

## type: brainrot
1. Write prompts/<slug>.json:
   `{ "title", "aspect_ratio": "9:16", "style", "cast": [...], "scenes": [ { "scene_id", "image_prompt", "video_prompt", "dialogue", "speaker", "camera", "seconds" } ] }`
   Paste each character's description word for word from styles/brainrot-cast.md.
2. Stop and tell Chris how many clips need generating and which tool. Never spend credits without his OK.
3. When the clips are in footage/<slug>/, continue to the self-check.

## Self-check (both types)
For each shot, pull 3 frames (`ffmpeg -ss <t> -i <clip> -frames:v 1 footage/<slug>/check/<shot>-<n>.png`) and look at them.
List problems the way a viewer would see them (feet cut off, character looks different from the last shot, text unreadable, steam too faint, extra fingers).
Fix what you can (faceless: change the code and re-render; brainrot: rewrite that scene's prompt and ask for a re-roll). Max 2 rounds per shot.
Write footage/<slug>/visuals.md: each shot file, what it shows, problems found and fixed, anything still wrong.
Log errors and fixes in docs/log.md.
