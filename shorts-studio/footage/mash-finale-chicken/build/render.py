import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

T = json.load(open("timeline.json"))
W, H, FPS = 1080, 1920, 30
DUR = T["dur"]
PAPER = (245, 240, 228); INK = (26, 26, 30); MUT = (120, 114, 104)
OLIVE = (86, 98, 52); RED = (176, 48, 38); CARD = (252, 249, 241); LINE = (222, 214, 198)
NIGHT = (22, 24, 30); NIGHTCARD = (34, 37, 46)
SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SERIF_M = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
_fc = {}
def F(p, s):
    k = (p, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(p, s)
    return _fc[k]

def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def mix(c1, c2, a):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * a) for i in range(3))

CHAP = {"hook": 0, "hook2": 0, "date": 1, "viewers": 1, "hospital": 2, "bus": 2, "quiet": 2, "baby": 2,
        "word": 2, "armistice": 3, "mozart": 3, "music": 3, "klinger": 3, "bj": 4, "stones": 4, "end": 5}
CHAP_LABEL = ["THE HOOK", "THE BROADCAST", "THE SECRET", "THE WAR ENDS", "GOODBYE", "SINCE THEN"]
DARK = {"bus", "baby", "word"}

def wrap(d, text, font, maxw):
    lines, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=font) > maxw and line: lines.append(line); line = w
        else: line = t
    if line: lines.append(line)
    return lines

def text_block(img, text, y, size, color, lt, delay=0.0, font=SERIF, maxw=900, gap=1.18, align="center"):
    """Fade + rise in. Returns bottom y."""
    a = ease((lt - delay) / 0.4)
    if a <= 0: return y
    f = F(font, size)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    rise = int((1 - a) * 28)
    for ln in wrap(d, text, f, maxw):
        tw = d.textlength(ln, font=f)
        x = (W - tw) / 2 if align == "center" else 90
        d.text((x, y + rise), ln, font=f, fill=color + (int(255 * a),))
        y += int(size * gap)
    img.alpha_composite(layer)
    return y

def panel(img, box, lt, delay=0.0, fill=CARD, outline=LINE, r=36):
    a = ease((lt - delay) / 0.4)
    if a <= 0: return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box; rise = int((1 - a) * 30)
    d.rounded_rectangle([x0, y0 + rise, x1, y1 + rise], r, fill=fill + (int(255 * a),),
                        outline=outline + (int(255 * a),), width=3)
    img.alpha_composite(layer)

def label(img, text, x, y, lt, delay=0.0, color=OLIVE, size=30, center=False):
    a = ease((lt - delay) / 0.4)
    if a <= 0: return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    f = F(MONO, size)
    if center: x = (W - d.textlength(text, font=f)) / 2
    d.text((x, y), text, font=f, fill=color + (int(255 * a),))
    img.alpha_composite(layer)

def chicken(d, cx, cy, s, color, alpha=255, outline=False, wobble=0.0):
    c = color + (alpha,)
    w = 6 if outline else 0
    def E(box):
        if outline: d.ellipse(box, outline=c, width=w)
        else: d.ellipse(box, fill=c)
    # tail feathers
    for i, ang in enumerate((-40, -15, 10)):
        a = math.radians(ang + 180)
        tx, ty = cx - 0.55 * s, cy - 0.15 * s
        pts = [(tx, ty), (tx + math.cos(a - 0.25) * 0.55 * s, ty + math.sin(a - 0.25) * 0.55 * s - 0.25 * s),
               (tx + math.cos(a + 0.25) * 0.55 * s, ty + math.sin(a + 0.25) * 0.55 * s - 0.25 * s)]
        if outline: d.polygon(pts, outline=c, width=w)
        else: d.polygon(pts, fill=c)
    E([cx - 0.7 * s, cy - 0.45 * s, cx + 0.45 * s, cy + 0.45 * s])  # body
    hx, hy = cx + 0.42 * s, cy - 0.55 * s + wobble
    E([hx - 0.25 * s, hy - 0.25 * s, hx + 0.25 * s, hy + 0.25 * s])  # head
    comb = RED + (alpha,)
    for i in range(3):
        bx = hx - 0.15 * s + i * 0.12 * s
        d.ellipse([bx - 0.08 * s, hy - 0.4 * s, bx + 0.08 * s, hy - 0.2 * s], fill=comb)
    d.polygon([(hx + 0.22 * s, hy - 0.05 * s), (hx + 0.42 * s, hy + 0.03 * s), (hx + 0.22 * s, hy + 0.1 * s)],
              fill=(214, 150, 40, alpha))
    eye = (PAPER if not outline else color) + (alpha,)
    d.ellipse([hx + 0.04 * s, hy - 0.09 * s, hx + 0.12 * s, hy - 0.01 * s], fill=eye if not outline else c)
    for lx in (cx - 0.15 * s, cx + 0.1 * s):  # legs
        d.line([lx, cy + 0.42 * s, lx, cy + 0.72 * s], fill=(214, 150, 40, alpha), width=max(4, int(s * 0.05)))

# 5x7 bitmap letters for GOODBYE in stones
GL = {"G": ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
      "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
      "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
      "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
      "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
      "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"]}
STONES = []
for li, ch in enumerate("GOODBYE"):
    for r, row in enumerate(GL[ch]):
        for c, v in enumerate(row):
            if v == "1": STONES.append((li * 6 + c, r, (li * 7 + r * 3 + c * 5) % 11))
STONES.sort(key=lambda s: (s[0], s[1]))

def helicopter(d, cx, cy, s, t, color):
    c = color + (255,)
    d.ellipse([cx - 0.6 * s, cy - 0.3 * s, cx + 0.4 * s, cy + 0.3 * s], fill=c)
    d.line([cx + 0.3 * s, cy - 0.05 * s, cx + 1.3 * s, cy - 0.15 * s], fill=c, width=max(3, int(s * 0.12)))
    d.line([cx + 1.25 * s, cy - 0.35 * s, cx + 1.25 * s, cy + 0.05 * s], fill=c, width=max(2, int(s * 0.07)))
    span = abs(math.cos(t * 40)) * 1.1 * s + 0.15 * s
    d.line([cx - 0.1 * s - span, cy - 0.42 * s, cx - 0.1 * s + span, cy - 0.42 * s], fill=c, width=max(2, int(s * 0.06)))
    d.line([cx - 0.1 * s, cy - 0.42 * s, cx - 0.1 * s, cy - 0.3 * s], fill=c, width=max(2, int(s * 0.06)))
    d.line([cx - 0.5 * s, cy + 0.45 * s, cx + 0.3 * s, cy + 0.45 * s], fill=c, width=max(2, int(s * 0.06)))

def staff(d, y0, color, w=4):
    for i in range(5): d.line([140, y0 + i * 34, 940, y0 + i * 34], fill=color, width=w)

NOTES = [(210, 4), (300, 2), (390, 3), (480, 1), (570, 2), (660, 0), (750, 3), (840, 1)]
def note(d, x, step, y0, color, dy=0):
    y = y0 + 136 - step * 17 - 17 + dy
    d.ellipse([x - 24, y - 17, x + 24, y + 17], fill=color)
    d.line([x + 21, y, x + 21, y - 120], fill=color, width=7)

def scene(img, sc, lt, sd, t):
    d = ImageDraw.Draw(img)
    dark = sc in DARK
    ink = PAPER if dark else INK
    if sc == "hook":
        a = ease(lt / 0.5)
        chicken(d, 540, 760 + int((1 - a) * 60), 330, INK, int(255 * a), wobble=math.sin(t * 9) * 6)
    elif sc == "hook2":
        # chicken turns into an outline, a red line strikes through it
        chicken(d, 540, 760, 330, MUT, 255, outline=True)
        k = ease(lt / 0.5)
        d.line([250, 1020, 250 + int(580 * k), 500], fill=RED, width=22)
        text_block(img, "It was never a chicken.", 1150, 96, RED, lt, 0.1)
    elif sc == "date":
        panel(img, (150, 330, 930, 1110), lt)
        a = ease(lt / 0.4)
        if a > 0:
            d.rounded_rectangle([150, 330 + int((1 - a) * 30), 930, 500 + int((1 - a) * 30)], 36, fill=OLIVE)
            d.rectangle([150, 440 + int((1 - a) * 30), 930, 500 + int((1 - a) * 30)], fill=OLIVE)
        label(img, "FEBRUARY 1983", 0, 390, lt, 0.05, PAPER, 44, center=True)
        text_block(img, "28", 540, 300, INK, lt, 0.15, font=SERIF)
        label(img, "AIRED ON CBS", 0, 960, lt, 0.5, MUT, 40, center=True)
        text_block(img, "“Goodbye, Farewell and Amen”", 1190, 64, INK, lt, 0.3)
    elif sc == "viewers":
        k = ease((lt - 0.2) / 2.6)
        n = int(106_000_000 * k)
        label(img, "US VIEWERS", 0, 470, lt, 0.0, OLIVE, 40, center=True)
        f = F(SERIF, 150); s = f"{n:,}"
        d.text(((W - d.textlength(s, font=f)) / 2, 540), s, font=f, fill=INK)
        bw = int(760 * k)
        d.rounded_rectangle([160, 780, 160 + max(bw, 30), 830], 25, fill=OLIVE)
        text_block(img, "Still the most-watched scripted episode in US TV history.", 1000, 60, INK, lt, 1.6)
    elif sc == "hospital":
        panel(img, (190, 380, 890, 1060), lt)
        a = ease(lt / 0.4)
        if a > 0:
            y = int((1 - a) * 30)
            d.rectangle([420, 520 + y, 660, 900 + y], outline=INK, width=10)  # door
            d.rectangle([450, 560 + y, 630, 680 + y], outline=INK, width=6)  # window
            d.ellipse([610, 720 + y, 636, 746 + y], fill=INK)
        label(img, "WHERE IT STARTS", 0, 950, lt, 0.2, MUT, 34, center=True)
    elif sc == "bus":
        # night road with a bus and enemy-patrol flashlights
        d.line([0, 960, W, 960], fill=(60, 64, 76), width=6)
        bx = 140 + int(lt * 40)
        d.rounded_rectangle([bx, 690, bx + 560, 930], 30, fill=(70, 76, 60))
        for i in range(5): d.rectangle([bx + 40 + i * 100, 730, bx + 110 + i * 100, 800], fill=(200, 180, 110))
        for wx in (bx + 110, bx + 450): d.ellipse([wx - 50, 890, wx + 50, 990], fill=(10, 10, 12))
        for i, px in enumerate((780, 880, 980)):
            on = (math.sin(t * 3 + i * 1.7) > -0.2) and lt > 1.0 + i * 0.25
            if on: d.polygon([(px, 640), (px - 70, 1000), (px + 40, 1000)], fill=(90, 90, 70))
            d.ellipse([px - 14, 620, px + 14, 648], fill=RED if on else (90, 40, 40))
        label(img, "ENEMY PATROL", 640, 560, lt, 1.0, RED, 34)
    elif sc == "quiet":
        chicken(d, 540, 760, 290, INK, 255, wobble=math.sin(t * 14) * 10)
        label(img, "SHHH", 0, 330, lt, 0.4, RED, 60, center=True)
    elif sc == "baby":
        text_block(img, "It was her baby.", 820, 110, PAPER, lt, 0.15)
    elif sc == "word":
        text_block(img, "He buried that memory under one word:", 600, 64, (190, 186, 176), lt, 0.0)
        a = ease((lt - 2.3) / 0.35)
        if a > 0:
            f = F(SERIF, int(124 + (1 - a) * 50)); s = "“CHICKEN.”"
            d.text(((W - d.textlength(s, font=f)) / 2, 900), s, font=f, fill=mix(NIGHT, RED, a))
    elif sc == "armistice":
        panel(img, (150, 440, 930, 1000), lt)
        label(img, "ARMISTICE", 0, 520, lt, 0.05, OLIVE, 44, center=True)
        a = ease((lt - 0.3) / 0.5)
        if a > 0: d.line([260, 760, 260 + int(560 * a), 760], fill=INK, width=8)
        text_block(img, "The war ends.", 620, 96, INK, lt, 0.15)
        label(img, "KOREA", 0, 830, lt, 0.5, MUT, 36, center=True)
    elif sc in ("mozart", "music"):
        staff(d, 640, INK if sc == "mozart" else MUT)
        for i, (x, step) in enumerate(NOTES):
            if sc == "mozart":
                if lt > 0.3 + i * 0.4: note(d, x, step, 640, INK)
            else:
                fall = max(0.0, lt - 0.8 - i * 0.25)
                if fall < 1.6:
                    c = mix(INK, PAPER, min(1.0, fall / 1.6))
                    note(d, x, step, 640, c, dy=int(fall * fall * 180))
        lbl = "MOZART" if sc == "mozart" else "AFTER"
        label(img, lbl, 0, 470, lt, 0.0, OLIVE, 44, center=True)
        txt = ("Winchester teaches Chinese POW musicians Mozart." if sc == "mozart"
               else "Later, most of them are killed. Now music pains him.")
    elif sc == "klinger":
        panel(img, (170, 380, 910, 1020), lt)
        a = ease((lt - 0.2) / 0.5)
        if a > 0:
            px, py = 540, 640 - int((1 - a) * 80)
            d.ellipse([px - 90, py - 90, px + 90, py + 90], fill=RED)
            d.polygon([(px - 78, py + 45), (px + 78, py + 45), (px, py + 200)], fill=RED)
            d.ellipse([px - 36, py - 36, px + 36, py + 36], fill=CARD)
        label(img, "MARRIES SOON-LEE", 0, 850, lt, 0.4, INK, 40, center=True)
        label(img, "STAYS IN KOREA", 0, 920, lt, 0.6, OLIVE, 40, center=True)
    elif sc == "bj":
        panel(img, (190, 440, 890, 960), lt)
        f = F(SERIF, 120)
        a = ease((lt - 0.3) / 0.4)
        s = "Good—"
        d.text(((W - d.textlength(s, font=f)) / 2, 600), s, font=f, fill=mix(CARD, MUT, a))
    elif sc == "stones":
        # top-down ground; stones appear one by one; camera pulls up as the helicopter lifts
        z = 1.0 - 0.14 * ease(lt / sd)
        cell = 23 * z; gw = 41 * cell
        ox, oy = (W - gw) / 2, 760 - 3.5 * cell
        d.rounded_rectangle([60, 520, W - 60, 1060], 40, fill=(232, 222, 198))
        shown = int(len(STONES) * ease((lt - 0.3) / (sd * 0.55)))
        for i, (gx, gy, v) in enumerate(STONES[:shown]):
            x, y = ox + gx * cell, oy + gy * cell
            g = 120 - v * 5
            d.ellipse([x + 1, y + 1, x + cell - 1, y + cell - 2], fill=(g, g - 6, g - 14), outline=(60, 56, 50))
        hs = 130 * (1 - 0.45 * ease(lt / sd))
        helicopter(d, 540, 1230 - int(ease(lt / sd) * 160), hs, t, INK)
    elif sc == "end":
        chicken(d, 540, 760, 300, INK, 255, outline=True)

def topbar(img, sc, dark):
    d = ImageDraw.Draw(img)
    ink = (200, 196, 186) if dark else INK
    d.text((70, 110), "TV HISTORY · M*A*S*H", font=F(MONO, 30), fill=ink)
    d.text((70, 155), CHAP_LABEL[CHAP[sc]], font=F(MONO, 26), fill=RED if not dark else (220, 120, 110))
    for i in range(6):
        x = W - 90 - (5 - i) * 40
        if i <= CHAP[sc]: d.ellipse([x - 11, 121, x + 11, 143], fill=ink)
        else: d.ellipse([x - 11, 121, x + 11, 143], outline=ink, width=3)

# caption chunks: up to 4 words, break after punctuation, never across scenes
CAPS = T["caps"]; chunks = []; cur = []
for i, c in enumerate(CAPS):
    cur.append(c)
    nxt = CAPS[i + 1] if i + 1 < len(CAPS) else None
    if len(cur) == 4 or c["w"][-1] in ".,:!?" or nxt is None or nxt["scene"] != c["scene"]:
        chunks.append(cur); cur = []
def captions(img, t, dark):
    d = ImageDraw.Draw(img)
    act = None
    for i, ch in enumerate(chunks):
        end = chunks[i + 1][0]["t"] if i + 1 < len(chunks) else DUR
        if ch[0]["t"] - 0.05 <= t < end and t < ch[-1]["t"] + 1.2: act = ch
    if not act or act[0]["scene"] in ("baby", "hook2"): return
    words = [c["w"] for c in act]
    size = 76
    while d.textlength(" ".join(words), font=F(SERIF, size)) > 960: size -= 4
    f = F(SERIF, size)
    total = d.textlength(" ".join(words), font=f)
    x = (W - total) / 2; y = 1530
    curi = max([i for i, c in enumerate(act) if c["t"] <= t + 0.03], default=-1)
    for i, c in enumerate(act):
        wl = d.textlength(c["w"], font=f)
        if i == curi:
            col = PAPER if dark else INK
            d.line([x, y + size * 1.42, x + wl, y + size * 1.42], fill=RED, width=7)
        elif i < curi: col = (170, 166, 156) if dark else (88, 84, 78)
        else: col = (95, 95, 100) if dark else (180, 172, 160)
        d.text((x, y), c["w"], font=f, fill=col)
        x += wl + d.textlength(" ", font=f)

SC = T["scenes"]
def scene_at(t):
    for i, s in enumerate(SC):
        nxt = SC[i + 1]["t0"] if i + 1 < len(SC) else DUR + 1
        if t < nxt: return s, (nxt if i + 1 < len(SC) else DUR) - s["t0"]
    return SC[-1], DUR - SC[-1]["t0"]

def frame(t):
    s, sd = scene_at(t)
    sc = s["scene"]; lt = max(0.0, t - s["t0"] + 0.25)
    dark = sc in DARK
    img = Image.new("RGBA", (W, H), (NIGHT if dark else PAPER) + (255,))
    scene(img, sc, lt, sd, t)
    # slow push-in on the scene so no shot sits still
    z = 1.0 + 0.045 * (lt / max(sd, 0.1))
    if z > 1.001:
        cw, ch = int(W / z), int(H / z)
        x0, y0 = (W - cw) // 2, int((H - ch) * 0.42)
        img = img.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
    topbar(img, sc, dark)
    captions(img, t, dark)
    # quick flash into each new scene
    if lt < 0.33:
        a = 1 - lt / 0.33
        ov = Image.new("RGBA", (W, H), (NIGHT if dark else PAPER) + (int(160 * a),))
        img.alpha_composite(ov)
    return img.convert("RGB")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for i, s in enumerate(SC):
            frame(s["t0"] + min(1.8, (s["t1"] - s["t0"]) * 0.8)).save(f"still_{i:02d}_{s['scene']}.jpg", quality=80)
        sys.exit()
    n = int(DUR * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                          "-pix_fmt", "yuv420p", "video.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    print("frames", n)
