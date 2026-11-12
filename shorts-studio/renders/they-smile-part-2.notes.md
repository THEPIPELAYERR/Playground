# Render notes: they-smile-part-2

- **Length / size:** 51.0 s, 1080x1920, 30 fps, H.264 + AAC 192k, 39 MB. Loudness −15.4 LUFS integrated, true peak ≤ −1.5 dB.
- **Made by:** Claude, from code in `projects/they-smile-part-2/`. To rebuild, run `./build.sh` there (about 15 minutes).

## Clips used, in order
No camera footage and no stock. Every frame is drawn on a canvas by `projects/they-smile-part-2/scene.html`:
1. 0.0–2.8 s: extreme close-up of the grin, with the hook text
2. 2.8–33.0 s: first-person gas-station aisle. Maddie is a silhouette at 8.5 m, then 4.6 m after the 24.5 s blink, then 2.3 m after the 32.2 s blink
3. 33.0–34.3 s: close-up of the grin
4. 34.3–47.0 s: the aisle again; a notification drops at 39.2 s; whip pan to black at 46.3 s
5. 47.0–51.0 s: end card (text)

**Nothing here is anyone else's footage, art or characters.** The notification is a generic banner, not a real app's UI. The 🙂 is the open-source Noto Color Emoji font.

## Human angle
**None yet.** There's no face or voice of Chris in this render. Before it's posted, he needs to whisper the captions as a voiceover (see `scripts/they-smile-part-2.md`).

## Caption text, as burned in
SHE HASN'T STOPPED SMILING / IN 4 MINUTES. · the cooler door was wide open. · her phone was on the floor. i picked it up. · ...maddie? · she's smiling. maddie never smiles like that. · you never look away from them. · they're like dogs. look away, they charge. · so we stare. · my eyes are burning. · she moved. · she's copying my breathing. · don't blink. don't blink. don't— · close enough to hear her humming. · my phone buzzed. · [notification] Me (My Number): look behind you 🙂 · a text. from my own number. · she's right in front of me. so who's behind me? · PART 3? / Turn around, or keep staring? / Comment TURN or STARE

## Music and sound
All of it is synthesized in `audio.py` with no samples or licensed music:
- drone and room tone
- fluorescent hum and the lights clunking on at 8.4 s
- neck cracks during the head tilt (11–13 s)
- breathing and a heartbeat that speeds up
- a whoosh and a sting on each blink
- an original lullaby hum from 34.2 s
- the phone buzzing (37 s) and the message chime (39.2 s)
- a whisper panned hard left (46 s), a whoosh, and a hard cut to silence at 47 s
- music-box notes on the end card, the same as Part 1

## Changes from the script
None. The beats match `scripts/they-smile-part-2.md`.

## Content notes
Violence is implied only. There's no gore, no real people, brands or places, and no claims of being a true story.
