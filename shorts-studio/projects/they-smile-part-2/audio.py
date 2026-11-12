"""Sound design for "They Smile - Part 2: The Stare-Down". Synthesized, no samples, no licenses needed.
Usage: python3 audio.py timeline.json out.wav
"""
import json, sys, wave
import numpy as np

SR = 48000
tl = json.load(open(sys.argv[1]))
DUR = tl["end"]
N = int(DUR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(23)
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


endcard = tl["endCard"]; cut = tl["cut"]; stop = tl["stopSmile"]

# ---- night outside: wind, crickets (go quiet when he stops smiling)
wind = filt(rng.standard_normal(N), 60, 500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)) * 0.9
ph = (t % 0.83) / 0.11
chirp_env = np.where(ph < 1, np.sin(np.pi * np.clip(ph, 0, 1)) ** 2, 0) * (0.5 + 0.5 * np.sin(2 * np.pi * 30 * t)) ** 4
crick = np.sin(2 * np.pi * 4400 * t) * chirp_env * 0.012
outside = (wind * 0.05 + crick) * win(0, stop, 0.4)
L += outside; R += outside * 0.9

# ---- muffled store hum through the glass + the neon sign buzz
hum = sum(np.sin(2 * np.pi * 120 * k * t) / k for k in range(1, 6)) * 0.012
neon = sum(np.sin(2 * np.pi * 60 * k * t) / k for k in range(2, 10)) * 0.006
L += (hum + neon * 1.4) * win(tl["hookEnd"] - 0.2, cut, 0.1); R += (hum + neon * 0.6) * win(tl["hookEnd"] - 0.2, cut, 0.1)

# ---- dread drone, dropping out when he stops smiling
dread = np.clip((t - 3) / 40, 0, 1)
drone = (np.sin(2 * np.pi * 38.9 * t) + 0.7 * np.sin(2 * np.pi * 41.2 * t + 1) + 0.25 * np.sin(2 * np.pi * 155.6 * t + 2)
         + 0.15 * np.sin(2 * np.pi * 233.1 * t * (1 + 0.003 * np.sin(0.5 * t))) + 0.1 * np.sin(2 * np.pi * 311.1 * t))
d = drone * 0.12 * (0.3 + 0.7 * dread) * win(tl["hookEnd"] - 0.3, stop, 0.3)
L += d; R += d

# ---- hook hits
for at in (0.15, 1.2):
    s = seg(1.6)
    boom = np.sin(2 * np.pi * (55 * np.exp(-s * 2)) * s * 2) * env(len(s), 0.002, 0.5)
    crack = filt(rng.standard_normal(len(s)), hi=2500) * env(len(s), 0.001, 0.06)
    add(np.tanh(2 * (boom + crack)) * 0.5, at)

# ---- Dale's giggles, muffled by the glass
for i, (at, n) in enumerate(tl["laughs"]):
    g = laugh(n, f0=150 + 15 * (i % 2), rate=0.16, seed=i + 1)
    add(filt(g, 120, 2400), at, 0.32 if n < 6 else 0.42)

# ---- he leans into the glass: a squeak as his face drags on it
s = seg(0.6)
sq = np.sin(2 * np.pi * np.cumsum(700 + 500 * s / 0.6 + 60 * np.sin(2 * np.pi * 37 * s)) / SR)
add(sq * np.sin(np.pi * s / 0.6) ** 2 * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 23 * s))), tl["lean"][0] + 0.7, 0.05)

# ---- crowbar on the glass
for at in tl["taps"]:
    s = seg(0.5)
    tink = sum(a * np.sin(2 * np.pi * f * s) * np.exp(-s / dcy) for f, a, dcy in ((2350, 1, 0.12), (3720, 0.6, 0.08), (5110, 0.4, 0.05), (1180, 0.5, 0.15)))
    thud = np.sin(2 * np.pi * 150 * s) * env(len(s), 0.001, 0.03)
    add(tink * 0.5 + thud * 0.6, at, 0.45)

# ---- heartbeat once the stare starts, speeding up
hb = 25.0
while hb < cut - 0.2:
    prog = (hb - 25.0) / (cut - 25.0)
    for off, g in ((0, 1.0), (0.2, 0.7)):
        s = seg(0.3)
        beat = np.sin(2 * np.pi * 52 * s) * env(len(s), 0.004, 0.07) + filt(rng.standard_normal(len(s)), 90, 450) * env(len(s), 0.002, 0.03) * 2.5
        add(beat, hb + off, (0.3 + 0.5 * prog) * g)
    hb += 1.1 - 0.55 * prog

# ---- the pack: distant laughter that grows, from many voices
c0 = tl["crowd"]
for v in range(12):
    vr = np.random.default_rng(100 + v)
    at = c0 + vr.uniform(0, 3) + v * 0.6
    while at < cut - 0.3:
        g = laugh(int(vr.integers(3, 8)), f0=vr.uniform(110, 260), rate=vr.uniform(0.13, 0.2), seed=int(vr.integers(1e6)))
        dist = 1 - np.clip((at - c0) / (cut - c0), 0, 1)               # gets closer
        g = filt(g, 150, 900 + 2500 * (1 - dist))
        add(g, at, 0.05 + 0.12 * (1 - dist), pan=vr.uniform(-0.8, 0.8))
        at += vr.uniform(1.0, 2.6)

# ---- engines coming up Route 9 with the headlights, moving right to left
h0 = tl["headlights"]
eng = sum(np.sin(2 * np.pi * 43 * k * t * (1 + 0.01 * np.sin(2 * np.pi * 0.3 * t))) / k for k in range(1, 12))
eng = filt(eng, 30, 400) + filt(rng.standard_normal(N), 300, 1800) * 0.3
eg = np.clip((t - h0) / 6, 0, 1) ** 1.5 * (t < cut) * 0.12
pan = np.clip(1 - (t - h0) / 7, -0.6, 1)
L += eng * eg * np.sqrt((1 - pan) / 2) * 1.414; R += eng * eg * np.sqrt((1 + pan) / 2) * 1.414

# ---- a low swell as he looks past, then the whole pack laughs right behind you, hard cut
lp = tl["lookPast"]
s = seg(cut - lp)
add(filt(rng.standard_normal(len(s)), 60, 600) * (s / (cut - lp)) ** 2 * 0.8, lp)
burst = sum(laugh(6, f0=f, rate=0.14, seed=500 + k) for k, f in enumerate((120, 150, 180, 210, 250)))
add(burst / 3, cut - 0.25, 0.9, pan=0.0)

# ---- end card: the series' music-box notes
for at, f in ((endcard + 0.4, 1046.5), (endcard + 1.2, 987.8), (endcard + 2.2, 1396.9)):
    s = seg(2.0)
    note = (np.sin(2 * np.pi * f * s) + 0.3 * np.sin(2 * np.pi * 2 * f * s) + 0.1 * np.sin(2 * np.pi * 3.01 * f * s))
    add(note * env(len(s), 0.002, 0.45), at, 0.09)

# hard cut to silence before the end card, then fade at the very end
gate = (t < endcard) | (t >= endcard + 0.3)
L *= gate; R *= gate
fade = np.clip((DUR - t) / 0.6, 0, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L /= peak / 0.9; R /= peak / 0.9
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", sys.argv[2], f"{DUR}s")
