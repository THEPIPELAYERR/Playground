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
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)


def filt(x, lo=None, hi=None):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    if lo: X *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** 4)
    if hi: X *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X, len(x))


def add(sig, at, gain=1.0, pan=0.0):
    """pan -1 = left, +1 = right"""
    i = int(at * SR)
    if i >= N or i + len(sig) <= 0: return
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


end_scene = tl["turn"][1]; endcard = tl["endCard"]; lights = tl["lightsOn"]

# ---- low drone + room tone (scene only), swelling with dread
dread = np.clip((t - 3) / 40, 0, 1)
drone = (np.sin(2 * np.pi * 38.9 * t) + 0.7 * np.sin(2 * np.pi * 41.2 * t + 1) + 0.3 * np.sin(2 * np.pi * 77.8 * t)
         + 0.2 * np.sin(2 * np.pi * 155.6 * t + 2) + 0.12 * np.sin(2 * np.pi * 233.1 * t * (1 + 0.003 * np.sin(0.5 * t))))
room = filt(rng.standard_normal(N), hi=180) * 2.5 + filt(rng.standard_normal(N), lo=2500, hi=8000) * 0.015
bed = (drone * 0.11 + room * 0.06) * (0.3 + 0.7 * dread) * win(tl["hookEnd"] - 0.3, end_scene, 0.3)
L += bed; R += bed

# ---- fluorescent hum: 120 Hz buzz with harmonics, on once the lights come on, with flicker dropouts
buzz = sum(np.sin(2 * np.pi * 120 * k * t) / k for k in range(1, 9)) * 0.022
buzz_gate = np.clip((t - lights) / 0.02, 0, 1) * (t < end_scene)
flick = (np.floor(np.clip(t - lights, 0, 9) * 20) % 3 != 0) | (t > lights + 0.6)   # matches the on-screen flicker
L += buzz * buzz_gate * flick; R += buzz * buzz_gate * flick * 0.8

# ---- hook hits
for at in (0.15, 1.2):
    s = seg(1.6)
    boom = np.sin(2 * np.pi * (55 * np.exp(-s * 2)) * s * 2) * env(len(s), 0.002, 0.5)
    crack = filt(rng.standard_normal(len(s)), hi=2500) * env(len(s), 0.001, 0.06)
    add(np.tanh(2 * (boom + crack)) * 0.5, at)

# ---- lights clunk on
s = seg(0.5)
clunk = np.tanh(3 * (np.sin(2 * np.pi * 70 * s) * env(len(s), 0.001, 0.05) + filt(rng.standard_normal(len(s)), 300, 3000) * env(len(s), 0.0005, 0.02) * 2))
for d in (0, 0.1, 0.2, 0.45):
    add(clunk, lights + d, 0.35)

# ---- neck cracks while her head tilts
for at in (tl["tilt"][0] + 0.4, tl["tilt"][0] + 1.1, tl["tilt"][0] + 1.7):
    s = seg(0.08)
    add(filt(rng.standard_normal(len(s)), 800, 6000) * env(len(s), 0.0003, 0.006) * 3, at, 0.35, pan=0.1)

# ---- his breathing (copied by her), from "copying my breathing" on
b0 = 25.5
br = filt(rng.standard_normal(N), 300, 2500) * 0.08
breath_env = np.clip(np.sin(2 * np.pi * (t - b0) / 3.2), 0, 1) ** 2 * win(b0, end_scene - 0.4, 0.5)
L += br * breath_env; R += br * breath_env

# ---- heartbeat from "so we stare", speeding up
hb = 20.0
while hb < end_scene - 0.3:
    prog = (hb - 20.0) / (end_scene - 20.0)
    for off, g in ((0, 1.0), (0.2, 0.7)):
        s = seg(0.3)
        beat = np.sin(2 * np.pi * 52 * s) * env(len(s), 0.004, 0.07)
        beat += filt(rng.standard_normal(len(s)), 90, 450) * env(len(s), 0.002, 0.03) * 2.5
        add(beat, hb + off, (0.3 + 0.5 * prog) * g)
    hb += 1.1 - 0.55 * prog

# ---- blinks: soft whoosh as the eyes close, then a sting when she's closer
for i, (bt, _, _) in enumerate(tl["blinks"]):
    s = seg(0.25)
    add(filt(rng.standard_normal(len(s)), 200, 1500) * np.sin(np.pi * s / 0.25) * 0.4, bt - 0.08, 0.6)
    s = seg(2.5)
    cluster = sum(np.sin(2 * np.pi * f * s * (1 - 0.02 * s)) for f in (110, 116.5, 164.8, 233.1, 246.9))
    slam = filt(rng.standard_normal(len(s)), hi=4000) * env(len(s), 0.0005, 0.1) * 3
    sub = np.sin(2 * np.pi * 36 * s) * env(len(s), 0.002, 0.7) * 2
    st = np.tanh((0.8 + 0.4 * i) * (cluster * env(len(s), 0.003, 0.7) + slam + sub)) * (0.6 + 0.25 * i)
    add(st, bt + 0.1)

# ---- her humming: a slow, slightly-off lullaby, through a crude vocal formant
notes = [(0, 392), (0.9, 349.2), (1.8, 329.6), (2.7, 293.7), (4.2, 329.6), (5.1, 349.2), (6.0, 311.1), (7.8, 293.7), (8.7, 277.2)]
h0 = 34.2
for off, f in notes:
    s = seg(1.1)
    vib = 1 + 0.008 * np.sin(2 * np.pi * 5.2 * s)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    voice = sum(np.sin(k * ph) / k ** 1.3 for k in range(1, 12))
    voice = filt(voice, 180, 1400)
    e = np.minimum(1, s / 0.15) * np.clip((1.1 - s) / 0.3, 0, 1)
    add(voice * e, h0 + off, 0.06, pan=0.0)

# ---- phone buzz in his pocket: two pulses
for at in (tl["buzz"][0], tl["buzz"][0] + 0.7):
    s = seg(0.45)
    v = np.sign(np.sin(2 * np.pi * 165 * s)) * (0.6 + 0.4 * np.sin(2 * np.pi * 28 * s))
    add(filt(v, 80, 900) * np.minimum(1, s / 0.02) * np.clip((0.45 - s) / 0.03, 0, 1), at, 0.22, pan=0.35)

# ---- message chime
for off, f in ((0, 1318.5), (0.12, 1760)):
    s = seg(0.6)
    add((np.sin(2 * np.pi * f * s) + 0.2 * np.sin(4 * np.pi * f * s)) * env(len(s), 0.002, 0.15), tl["notif"] + off, 0.09)

# ---- a whisper right behind him (hard-panned, breathy), then the whip-pan whoosh and a hard cut
s = seg(0.9)
whisper = filt(rng.standard_normal(len(s)), 1500, 7000) * np.sin(np.pi * s / 0.9) ** 2 * (0.7 + 0.3 * np.sin(2 * np.pi * 7 * s))
add(whisper, tl["whisper"], 0.35, pan=-0.9)
t0, t1 = tl["turn"]
s = seg(t1 - t0)
add(filt(rng.standard_normal(len(s)), 300, 5000) * (s / (t1 - t0)) ** 2 * 0.6, t0)

# ---- end card: same music-box notes as Part 1 so the series sounds like one thing
for at, f in ((endcard + 0.4, 1046.5), (endcard + 1.2, 987.8), (endcard + 2.2, 1396.9)):
    s = seg(2.0)
    note = (np.sin(2 * np.pi * f * s) + 0.3 * np.sin(2 * np.pi * 2 * f * s) + 0.1 * np.sin(2 * np.pi * 3.01 * f * s))
    add(note * env(len(s), 0.002, 0.45), at, 0.09)

# hard cut to silence at the end of the scene (everything still ringing gets chopped), then fade at the very end
cut = (t < end_scene) | (t >= endcard + 0.3)
L *= cut; R *= cut
fade = np.clip((DUR - t) / 0.6, 0, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L /= peak / 0.9; R /= peak / 0.9
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", sys.argv[2], f"{DUR}s")
