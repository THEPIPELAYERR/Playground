"""Sound design for "They Smile - Part 3" (2D animation). Synthesized, no samples, no licenses needed.
Usage: python3 audio.py timeline.json out.wav
"""
import json, sys, wave
import numpy as np

SR = 48000
tl = json.load(open(sys.argv[1]))
DUR = tl["end"]
N = int(DUR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(37)
L = np.zeros(N); R = np.zeros(N)


def filt(x, lo=None, hi=None):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    if lo: X *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** 4)
    if hi: X *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X, len(x))


def add(sig, at, gain=1.0, pan=0.0):
    """pan -1 = left, +1 = right"""
    i = int(at * SR)
    if i >= N: return
    if i < 0: sig = sig[-i:]; i = 0
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt((1 - pan) / 2) * 1.414
    R[i:i + len(sig)] += sig * np.sqrt((1 + pan) / 2) * 1.414


def env(n, attack, decay):
    k = np.arange(n) / SR
    return np.minimum(1, k / max(attack, 1e-4)) * np.exp(-k / decay)


def seg(sec):
    return np.arange(int(sec * SR)) / SR


def win(a, b, fade=0.05):
    return np.clip((t - a) / fade, 0, 1) * np.clip((b - t) / fade, 0, 1)


def laugh(n, f0=170.0, rate=0.17, seed=0):
    """A giggle: n 'ha' syllables, breathy onset, falling pitch, through a crude 'a' formant."""
    r = np.random.default_rng(seed)
    out = np.zeros(int((n * rate + 0.4) * SR))
    for i in range(n):
        st = int((i * rate + r.uniform(-0.015, 0.015)) * SR)
        f = f0 * (1.2 - 0.3 * i / max(n - 1, 1)) * r.uniform(0.95, 1.05)
        s = seg(0.13 + r.uniform(0, 0.04))
        jitter = 1 + 0.02 * np.sin(2 * np.pi * r.uniform(5, 9) * s)
        ph = 2 * np.pi * np.cumsum(f * jitter) / SR
        voiced = sum(np.sin(k * ph) / k for k in range(1, 25))
        voiced = filt(voiced, 250, 3200) + 0.6 * filt(voiced, 550, 1300)          # vowel colour
        e = np.minimum(1, s / 0.012) * np.exp(-s / 0.06)
        h = filt(r.standard_normal(len(s)), 900, 3500) * np.exp(-s / 0.02) * 0.6  # the 'h'
        syl = voiced * e * 0.5 + h
        st = max(0, st); m = min(len(syl), len(out) - st)
        out[st:st + m] += syl[:m]
    return np.tanh(out * 1.5)



sh = [s_[0] for s_ in tl["shots"]]
endcard = tl["endCard"]; impact = tl["impact"]; lock = tl["lock"]; reveal = tl["reveal"]

# outside gets muffled once he locks the door
outside_gain = np.where(t < lock, 1.0, 0.35)

# ---- engines idling outside (pickup + van), a rev on "VRRRMM"
eng = sum(np.sin(2 * np.pi * 41 * k * t * (1 + 0.012 * np.sin(2 * np.pi * 0.4 * t))) / k for k in range(1, 14))
eng = filt(eng, 30, 500) + filt(rng.standard_normal(N), 200, 1400) * 0.25
rev = np.exp(-((t - 1.2) / 0.6) ** 2)
eg = (0.09 + 0.12 * rev) * np.clip(1 - (t - 13) / 4, 0.35, 1) * (t < reveal)
E = eng * eg * outside_gain
E = np.where(t < lock, E, filt(E, hi=300))
L += E; R += E * 0.9

# ---- the mob laughing outside, muffled after the lock
for vv in range(9):
    vr = np.random.default_rng(300 + vv)
    at = vr.uniform(0, 2)
    while at < sh[6] + 1:
        g = laugh(int(vr.integers(3, 8)), f0=vr.uniform(110, 270), rate=vr.uniform(0.13, 0.2), seed=int(vr.integers(1e6)))
        if at > lock: g = filt(g, 100, 700)
        quiet = 0.35 if 13 < at < impact else 1.0
        add(g, at, (0.07 if at < lock else 0.04) * quiet, pan=vr.uniform(-0.8, 0.8))
        at += vr.uniform(1.2, 3.0)

# ---- named giggles
add(laugh(5, f0=260, rate=0.15, seed=41), 4.5, 0.32, pan=0.2)          # rake lady
add(laugh(3, f0=150, rate=0.22, seed=42), 8.85, 0.45)                   # Dale: HA HA HA
add(laugh(6, f0=160, rate=0.14, seed=43), 18.6, 0.45, pan=0.15)         # Dale, after the hit
add(filt(laugh(4, f0=200, rate=0.16, seed=44), 100, 900), 24.9, 0.2)    # "take your time!"

# ---- dread drone and heartbeat once he decides
dread = np.clip((t - 13) / 30, 0, 1)
drone = (np.sin(2 * np.pi * 38.9 * t) + 0.7 * np.sin(2 * np.pi * 41.2 * t + 1) + 0.25 * np.sin(2 * np.pi * 155.6 * t + 2) + 0.12 * np.sin(2 * np.pi * 233.1 * t))
d = drone * 0.1 * dread * (t < endcard)
L += d; R += d
hb = 13.2
while hb < endcard - 0.5:
    prog = min(1, (hb - 13.2) / 30)
    quiet = 0.5 if hb > reveal + 1 else 1.0
    for off, g in ((0, 1.0), (0.2, 0.7)):
        s = seg(0.3)
        beat = np.sin(2 * np.pi * 52 * s) * env(len(s), 0.004, 0.07) + filt(rng.standard_normal(len(s)), 90, 450) * env(len(s), 0.002, 0.03) * 2.5
        add(beat, hb + off, (0.25 + 0.4 * prog) * g * quiet)
    hb += 1.05 - 0.4 * prog

# ---- KRAK
s = seg(1.2)
hit = np.tanh(3 * (np.sin(2 * np.pi * (90 * np.exp(-s * 6)) * s * 3) * env(len(s), 0.001, 0.12) + filt(rng.standard_normal(len(s)), 400, 6000) * env(len(s), 0.0005, 0.03) * 3))
add(hit, impact + 0.08, 0.95)
add(sum(laugh(5, f0=f, rate=0.13, seed=600 + k) for k, f in enumerate((130, 170, 210, 250))) / 2.5, impact + 0.35, 0.35)   # the crowd cheers

# ---- door slam + lock click
s = seg(0.8)
slam = np.tanh(2.5 * (np.sin(2 * np.pi * 70 * s) * env(len(s), 0.001, 0.1) + filt(rng.standard_normal(len(s)), 200, 3000) * env(len(s), 0.0005, 0.04) * 2))
add(slam, lock + 0.02, 0.7)
s = seg(0.12)
click = filt(rng.standard_normal(len(s)), 1500, 9000) * env(len(s), 0.0002, 0.004) * 3 + np.sin(2 * np.pi * 2800 * s) * env(len(s), 0.0002, 0.01)
add(click, lock + 0.25, 0.6, pan=0.4); add(click, lock + 0.33, 0.45, pan=0.4)

# ---- footsteps down the hall, the door creaking open
for k, at in enumerate((27.0, 27.65, 28.3)):
    s = seg(0.3)
    add(filt(rng.standard_normal(len(s)), 60, 900) * env(len(s), 0.002, 0.04) * 2 + np.sin(2 * np.pi * 80 * s) * env(len(s), 0.002, 0.05), at, 0.35, pan=(-0.2 if k % 2 else 0.2))
s = seg(1.3)
cf = 180 + 90 * np.sin(2 * np.pi * 0.8 * s) + 30 * np.sin(2 * np.pi * 7 * s)
creak = np.sign(np.sin(2 * np.pi * np.cumsum(cf) / SR)) * (0.5 + 0.5 * np.sin(2 * np.pi * 23 * s))
add(filt(creak, 300, 2500) * np.sin(np.pi * s / 1.3), sh[7] - 0.2, 0.08)

# ---- back room: bulb hum, Maddie's shaky breathing
bulb = sum(np.sin(2 * np.pi * 120 * k * t) / k for k in range(1, 6)) * 0.01 * ((t >= sh[7]) & (t < endcard))
L += bulb; R += bulb
for at in np.arange(sh[7] + 0.3, reveal, 1.25):
    s = seg(0.55)
    add(filt(rng.standard_normal(len(s)), 500, 3000) * np.sin(np.pi * s / 0.55) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * s)), at, 0.05)

# ---- the reveal: a deep sting, then the rocking chair, knitting needles and her humming
s = seg(3.0)
st = np.tanh(1.2 * (sum(np.sin(2 * np.pi * f * s) for f in (65.4, 69.3, 98, 138.6)) * env(len(s), 0.01, 1.0) + np.sin(2 * np.pi * 32 * s) * env(len(s), 0.005, 0.9) * 2))
add(st, reveal + 0.05, 0.6)
for at in np.arange(reveal + 0.6, endcard, 1.7):
    s = seg(0.5)
    cf = 140 + 60 * s
    add(filt(np.sign(np.sin(2 * np.pi * np.cumsum(cf) / SR)), 200, 1800) * np.sin(np.pi * s / 0.5) ** 2, at, 0.04, pan=-0.2)
for at in np.arange(reveal + 0.2, endcard, 0.32):
    s = seg(0.05)
    add(np.sin(2 * np.pi * 3400 * s) * env(len(s), 0.0002, 0.006) + filt(rng.standard_normal(len(s)), 2000, 8000) * env(len(s), 0.0002, 0.003), at, 0.12, pan=0.1)
notes = [(0, 392), (0.9, 349.2), (1.8, 329.6), (2.7, 293.7), (4.0, 329.6), (4.6, 349.2), (5.2, 311.1)]
for off, f in notes:
    s = seg(0.95)
    ph = 2 * np.pi * np.cumsum(f * 0.5 * (1 + 0.01 * np.sin(2 * np.pi * 5 * s))) / SR   # an octave down: an old woman humming
    voice = filt(sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 14)), 150, 1300)
    add(voice * np.minimum(1, s / 0.15) * np.clip((0.95 - s) / 0.3, 0, 1), reveal + 0.9 + off, 0.07)

# ---- animation sync: the tire-iron swing, palms slapping the glass, the whip pan into Grandma
s = seg(0.22)
add(filt(rng.standard_normal(len(s)), 300, 4000) * np.sin(np.pi * s / 0.22) ** 2 * (s / 0.22), impact - 0.04, 0.45)
for at in tl.get("slaps", []):
    s = seg(0.15)
    add(filt(rng.standard_normal(len(s)), 400, 5000) * env(len(s), 0.0005, 0.02) * 2 + np.sin(2 * np.pi * 180 * s) * env(len(s), 0.001, 0.03), at, 0.3, pan=float(np.sin(at * 7)) * 0.6)
s = seg(0.5)
add(filt(rng.standard_normal(len(s)), 500, 7000) * np.sin(np.pi * s / 0.5) ** 2, tl.get("whip", reveal - 0.5), 0.4)

# ---- end card: the series' music-box notes
for at, f in ((endcard + 0.4, 1046.5), (endcard + 1.2, 987.8), (endcard + 2.2, 1396.9)):
    s = seg(2.0)
    note = (np.sin(2 * np.pi * f * s) + 0.3 * np.sin(2 * np.pi * 2 * f * s) + 0.1 * np.sin(2 * np.pi * 3.01 * f * s))
    add(note * env(len(s), 0.002, 0.45), at, 0.09)

gate = (t < endcard) | (t >= endcard + 0.25)
L *= gate; R *= gate
fade = np.clip((DUR - t) / 0.6, 0, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L /= peak / 0.9; R /= peak / 0.9
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", sys.argv[2], f"{DUR}s")
