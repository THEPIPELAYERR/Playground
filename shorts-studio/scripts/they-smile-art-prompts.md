# They Smile: art prompt pack

Generate these with a free image tool on your phone (Bing Image Creator, Ideogram, Leonardo or Meta AI), then upload them in chat. Claude animates them: camera moves, layered depth, lighting, rain and dust, shake on hits, blinks and mouths (if you make the mouth variants), plus sound and subtitles timed to `vo-cues.csv`.

**Look we're going for:** gritty, adult horror-comic illustration with realistic people. Heavy inks, hard light, rain, blood-red accents. It's inspired by mature horror and antihero comics and adult animation, but **never name those titles in a prompt**: tools block it or water it down, and the art should be ours.

---

## 1. Paste this style block at the end of EVERY prompt

> gritty mature horror comic illustration, realistic anatomy and detailed expressive faces, heavy black ink shadows with sharp fine cross-hatching, bold clean linework, cinematic hard rim lighting, deep blacks, muted desaturated colors with blood-red accents, wet rain-slick night atmosphere, dramatic composition, highly detailed, vertical 9:16

**If the tool has a negative prompt / "avoid" box:**

> cartoon, chibi, anime, cute, 3d render, plastic skin, text, watermark, logo, speech bubbles, comic panel borders, extra fingers, deformed hands, cross-shaped scar, gore, exposed wounds

**Settings:** portrait / 9:16 (or 1080×1920 or larger). If you get several results, pick the one that looks most like the description, not the prettiest.

---

## 2. The rash ("the bloom"): use these exact words every time

> a crusted blood-red blistering rash spreading from the corners of the mouth across the cheeks and chin, bloodshot eyes, a too-wide delighted grin, tiny specks of dried blood on the skin

The infected look like **normal people** apart from the bloom. No monsters, no glowing eyes, no torn skin.

---

## 3. Characters: make these first

Make each one as a **character sheet** first. Save your favorite, then use your tool's "use as reference" / "remix" / "edit" feature with that image for every shot of the character, so the face stays the same. Always paste the character block word for word.

**Character-sheet prompt:**
> character reference sheet, front view and three-quarter view, full head and shoulders, plain light gray background, [CHARACTER BLOCK], [STYLE BLOCK]

| File name | Character block (copy exactly) |
|---|---|
| `char-dale.png` | **Dale**: a heavyset white man in his mid-50s, balding with short graying brown hair on the sides, stubble, a tired friendly face, wearing a faded red gas-station work vest over a gray t-shirt with a white name tag reading DALE, + the bloom |
| `char-brenda.png` | **Brenda (rake lady)**: a plump white woman in her 50s, auburn hair in pink foam curlers, a fuzzy pink bathrobe over a nightgown, a garden rake resting on her shoulder, + the bloom |
| `char-hank.png` | **Hank (trucker)**: a big bearded man in his 40s, a red trucker cap, a red-and-black flannel shirt, thick forearms, + the bloom |
| `char-maddie.png` | **Maddie**: a 19-year-old woman, long dirty-blonde hair, a gray hoodie, a tear-streaked frightened face, **clean skin with no rash at all** |
| `char-grandma.png` | **Grandma**: a tiny frail woman in her late 80s, white hair in a neat bun, round wire glasses, a mustard-yellow cardigan over a white blouse, a gentle closed-mouth smile and calm kind eyes, + the bloom (lighter, around the mouth) |
| `char-crowd.png` | **The pack**: a group of five ordinary townspeople (a teenage boy in a green hoodie, a bald man in his 60s in a navy t-shirt, a woman with a long dark ponytail in a yellow t-shirt, Hank, Brenda), all with the bloom, all grinning |

The narrator is never seen. Only his hands and arm appear: *a man's hand in a dark olive jacket sleeve*.

---

## 4. Part 3 shots (one image per shot)

Each line is the prompt (add the character block and the style block). The ➜ says what Claude will animate, so you can tell what matters in the frame.

| # | File name | Prompt | ➜ Animation |
|---|---|---|---|
| 1 | `p3-01-truck.png` | low angle on a dark rural road at night, a battered red pickup truck driving straight at the viewer with blinding headlights, five grinning townspeople with the bloom standing in the truck bed, a white church van behind it marked OPEN DOOR COMMUNITY CHURCH, a lit gas station canopy at the left edge, stars, light rain | Truck pushes in at the camera, headlight bloom, rain, bounce |
| 2 | `p3-02-brenda.png` | Brenda, close-up from the chest up, leaning toward the viewer and waving with one hand, out-of-focus headlights and taillights behind her at night, rain | Lean in, parallax, the wave hand moves |
| 3 | `p3-03-dale-door.png` | Dale standing in the doorway of a bright fluorescent-lit gas station convenience store, holding the glass door open with one arm, laughing with his head tipped back, a smiley face smeared in blood on the glass door, shelves of snacks behind him | Laugh shake, flickering lights |
| 4 | `p3-04-tire-iron.png` | first-person view, a man's hand in a dark olive jacket sleeve gripping a steel tire iron in the foreground, the glowing gas station ahead across a wet parking lot at night, Dale a tiny silhouette waiting in the doorway | A walking bob, the store grows |
| 5 | `p3-05-hit.png` | Dale reeling backward inside the store, mid-laugh, as a steel tire iron swings through the frame with motion blur, dramatic impact lighting, no blood, no wound | Swing blur, white flash, camera shake |
| 6 | `p3-06-dale-floor.png` | top-down view of Dale lying on his back on a dirty store floor, still laughing hysterically, arms spread, fluorescent light | A tilt down, laugh shake |
| 7 | `p3-07-glass.png` | view from inside a dark store looking out through a glass door, the pack's grinning faces and flat palms pressed against the glass, Hank licking the glass, blinding headlights behind them, smeared glass, rain on the outside | Faces push in, the glass shine moves |
| 8 | `p3-08-hallway.png` | a narrow employee hallway at the back of a gas station, a wooden door marked EMPLOYEES ONLY slightly ajar with warm yellow light spilling out, a smeared trail of blood on the floor leading under the door, a mop bucket, sickly green walls | A dolly forward, the light flickers |
| 9 | `p3-09-maddie.png` | Maddie tied to a wooden chair with rope in a cramped storage room, cardboard boxes on metal shelves, a single bare bulb hanging above her, crying, looking up at the viewer | The bulb swings, the light moves, shivering |
| 10 | `p3-10-maddie-close.png` | extreme close-up of Maddie's face, whispering, her eyes sliding to the side toward a dark corner, tears, warm low light | Slow push, eyes/mouth (see section 5) |
| 11 | `p3-11-grandma.png` | Grandma in a wooden rocking chair in a dark corner of a storage room, lit by a single small lamp, knitting a long red scarf patterned with little white smiley faces, a ball of red yarn on the floor, looking up at the viewer over her glasses | The chair rocks, the lamp flickers, a push-in |

---

## 5. Optional, but it makes them talk: mouth and eye variants

For the talking close-ups (shots 2, 3, 10, 11), make **two extra versions of the same image** using your tool's **edit** feature (Leonardo, Ideogram and Meta can; Bing can't). Change only the mouth, or only the eyes:

- `…-mouth-open.png`: "same image, mouth open mid-word"
- `…-eyes-closed.png`: "same image, eyes closed"

Claude swaps between them to sync with the voices and blinks. Without them, the shots still move (camera, light, shake); the mouths just won't.

---

## 6. Uploading
- Use the file names above so Claude knows which shot is which.
- Send them in batches if you like; partial sets are fine, and Claude will tell you what's missing.
- If a tool refuses a prompt (blood words can trigger filters), drop "blood" and use "dark red smears". Claude can add the red in animation.

## 7. Same pack for later episodes
Keep your favorite character sheets. Parts 1, 2 and 4 reuse the same cast, the bloom wording and the style block, so the whole series looks like one show.
