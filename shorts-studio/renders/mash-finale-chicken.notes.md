# Render notes: mash-finale-chicken

- Length 69.2s, 1080x1920, 30 fps, -14 LUFS, peak -0.8 dBFS.
- Type: tech-explainer look (cards + word-by-word captions), no host. Single story, not a list.
- Voice: Chris's own recording. Each line was read twice; the clearer take was kept.
  Line 7 only has one take, and "Hawkeye tells" comes out a little fast.
- Captions: word timestamps from Parakeet TDT (sherpa-onnx) on the source audio, text from the script.
- Music: original, synthesized in code (heartbeat, pads, hits on cuts, riser into the stones). No licensed audio.
- Visuals: original shapes drawn in code with Python/PIL (HyperFrames wasn't available in the cloud session).
  No footage, stills, logos or likenesses from the show.
- Build files: footage/mash-finale-chicken/build/ (cut.py, render.py, music.py, timeline.json).
- Debug loop: 3 rounds, PASS (round 1 frozen shots → push-in; round 2 clipped title → smaller).
