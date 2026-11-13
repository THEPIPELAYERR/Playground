# Render notes: they-smile-part-3

- **Length / size:** 53.0 s, 1080x1920, 30 fps, H.264 + AAC 192k, 12 MB. Loudness −15.5 LUFS integrated, true peak ≤ −1.5 dB.
- **Made by:** Claude, from code in `projects/they-smile-part-3/`. To rebuild, run `./build.sh` there (about 4 minutes).
- **Format:** a motion comic. `comic.js` is a reusable character and lettering kit (ink, flat colour, halftone); `scene.html` draws ten panels once, then animates camera moves and panel slides.

## Clips used, in order
No camera footage and no stock. Every panel is drawn by code:
1. 0.0 s: the pickup and church van, with infected in the truck bed
2. 4.0 s: the rake lady
3. 8.6 s: Dale holding the door
4. 13.0 s: first-person fist on a tire iron
5. 16.6 s: the impact
6. 20.6 s: faces on the glass
7. 26.6 s: the back-room door
8. 31.0 s: Maddie tied to a chair
9. 37.4 s: Maddie whispering
10. 42.4 s: Grandma
11. 49.0 s: end card

**Nothing here is anyone else's footage, art or characters.** The infected's mark is an original rash, not Crossed's cross. The church name on the van ("Open Door Community Church") is fictional.

## Human angle
**None yet.** It's faceless by design. Voices come from voice actors or AI voices, using the cue sheet in `scripts/they-smile-part-3.md` and `projects/they-smile-part-3/vo-cues.csv`.

## Caption text, as burned in
THERE WERE ELEVEN OF THEM. · VRRRMM · "HI SWEETIE! YOU LOST?" · THEY WERE FRIENDLY. THAT WAS THE WORST PART. · HA HA HA · "DOOR'S OPEN, BUDDY! COME ON IN!" · ELEVEN BEHIND ME. ONE IN FRONT. · I HAD A TIRE IRON. · AND ONE WAY TO GO. · KRAK! · SO I WENT IN. · "HA— HA HA HA!" · CLICK · I LOCKED THE DOOR. · THEY DIDN'T EVEN TRY IT. THEY JUST WATCHED. · "TAKE YOUR TIME!" · THE TRAIL WENT TO THE BACK ROOM. · "...HELLO?" · MADDIE. · "YOU CAME. YOU ACTUALLY CAME." · NO RASH. SHE WAS CLEAN. · "YOU HAVE TO GO. NOW." · "DALE'S NOT THE ONE IN CHARGE." · "SHE IS." · tik tik tik · "SIT DOWN, HONEY." · "WE'VE BEEN WAITING FOR YOU." · PART 4? / WHO IS SHE? / FOLLOW + COMMENT YOUR THEORY

## Music and sound
All of it is synthesized in `audio.py` with no samples or licensed music:
- engines with a rev, and a laughing mob that goes muffled once the door locks (20.6 s)
- giggles from the rake lady and Dale
- the impact thud and the crowd cheering
- the door slam and lock click
- footsteps and a door creak
- the bulb hum and Maddie's shaky breathing
- a heartbeat
- the reveal sting, a rocking-chair creak, knitting clicks and Grandma's humming
- a paper whoosh on each panel change
- the series' music-box notes

## Changes from the script
None.

## Content notes
Comic-style violence only: one tire-iron hit with speed lines and no blood from the hit. There's a blood trail and smears, and the rash. No gore, no sexual content, no real people, brands or places, and no claims of being a true story.
