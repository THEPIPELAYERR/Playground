"""Sound design for "They Smile - Part 1". Synthesized, no samples, no licenses needed.
Usage: python3 audio.py timeline.json out.wav
"""
import json, sys, wave
import numpy as np

SR = 48000
tl = json.load(open(sys.argv[1]))
DUR = tl["end"]
N = int(DUR * SR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)


def lowpass(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= ((f > lo) & (f < hi))
    return np.fft.irfft(X, len(x))


def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * (1 - pan) ** 0.5 if pan > 0 else sig
    R[i:i + len(sig)] += sig * (1 + pan) ** 0.5 if pan < 0 else sig


def env(n, attack, decay):
    k = np.arange(n) / SR
    return np.minimum(1, k / max(attack, 1e-4)) * np.exp(-k / decay)


def seg(sec):
    return np.arange(int(sec * SR)) / SR


def ramp(x0, x1, y0, y1):
    return np.clip((t - x0) / (x1 - x0), 0, 1) * (y1 - y0) + y0


sting = tl["sting"]; endcard = tl["endCard"]; hook_end = tl["hookEnd"]

# ---- drone bed: detuned low sines + rumble, swelling with dread, cut at the sting
dread = np.clip((t - 3) / 38, 0, 1)
lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.13 * t)
drone = (np.sin(2 * np.pi * 41.2 * t) + 0.8 * np.sin(2 * np.pi * 43.7 * t + 1)
         + 0.35 * np.sin(2 * np.pi * 82.4 * t) + 0.2 * np.sin(2 * np.pi * 116.5 * t * (1 + 0.002 * np.sin(t)))
         # upper partials so the bed is still audible on phone speakers
         + 0.22 * np.sin(2 * np.pi * 164.8 * t) + 0.14 * np.sin(2 * np.pi * 233.1 * t + 2) + 0.08 * np.sin(2 * np.pi * 349.2 * t * (1 + 0.003 * np.sin(0.7 * t))))
rumble = lowpass(rng.standard_normal(N), 120) * 3
hiss = bandpass(rng.standard_normal(N), 3000, 9000) * 0.02
bed = (drone * 0.13 + rumble * 0.08) * lfo * (0.35 + 0.65 * dread) + hiss
bed *= np.where(t < sting - 0.06, 1.0, 0.0)                  # hard cut right before the sting
bed += (drone * 0.05 + hiss) * ramp(endcard, endcard + 1.5, 0, 1) * (t >= endcard)  # returns softly on end card
L += bed; R += bed

# ---- hook hits
for at in (0.15, 1.3):
    s = seg(1.6)
    boom = np.sin(2 * np.pi * (55 * np.exp(-s * 2)) * s * 2) * env(len(s), 0.002, 0.5)
    crack = lowpass(rng.standard_normal(len(s)), 2500) * env(len(s), 0.001, 0.06)
    add(np.tanh(2 * (boom + crack)) * 0.55, at)

# ---- message sounds
for at, cls, _ in tl["msgs"]:
    if "emoji" in cls: continue
    s = seg(0.18)
    if cls.startswith("in"):
        tone = (np.sin(2 * np.pi * 880 * s) * (s < 0.06) + np.sin(2 * np.pi * 660 * s) * (s >= 0.06))
        add(tone * env(len(s), 0.003, 0.05), at, 0.12)
    else:
        f = 900 + 900 * s / 0.18
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
        add(tone * env(len(s), 0.005, 0.04), at, 0.16 if "panic" in cls else 0.10)

# ---- knocks on the cooler door (thump + wood + short room echo)
for at in tl["knocks"]:
    s = seg(0.6)
    thump = np.sin(2 * np.pi * 85 * s) * env(len(s), 0.001, 0.09)
    wood = bandpass(rng.standard_normal(len(s)), 200, 1800) * env(len(s), 0.0005, 0.025) * 3
    k = np.tanh(1.5 * (thump + wood))
    for d, g in ((0, 1.0), (0.045, 0.35), (0.11, 0.18), (0.19, 0.08)):
        add(k, at + d, 0.7 * g, pan=-0.3)

# ---- heartbeat from the first knock to the final silence, speeding up
hb_t = tl["knocks"][0]
while hb_t < sting - 0.5:
    prog = (hb_t - tl["knocks"][0]) / (sting - tl["knocks"][0])
    for off, g in ((0, 1.0), (0.22, 0.7)):
        s = seg(0.3)
        beat = np.sin(2 * np.pi * 52 * s) * env(len(s), 0.004, 0.07)
        beat += bandpass(rng.standard_normal(len(s)), 90, 450) * env(len(s), 0.002, 0.03) * 2.5  # audible on phones
        add(beat, hb_t + off, (0.25 + 0.45 * prog) * g)
    hb_t += 1.15 - 0.6 * prog

# ---- riser during the final typing bubble
r0, r1 = tl["typingFinal"]
rs = (t >= r0) & (t < sting - 0.06)
p = np.clip((t - r0) / (sting - 0.06 - r0), 0, 1)
riser_noise = bandpass(rng.standard_normal(N), 400, 6000) * 0.06
riser_tone = np.sin(2 * np.pi * np.cumsum(180 + 620 * p ** 2) / SR) * 0.05
riser = (riser_noise + riser_tone) * p ** 2 * rs
L += riser; R += riser

# ---- sting on the smiley: dissonant cluster + slam, distorted, long tail
s = seg(3.5)
cluster = sum(np.sin(2 * np.pi * f * s * (1 - 0.03 * s)) for f in (110, 116.5, 155.6, 233.1, 311.1, 329.6))
slam = lowpass(rng.standard_normal(len(s)), 4000) * env(len(s), 0.0005, 0.12) * 4
sub = np.sin(2 * np.pi * 38 * s) * env(len(s), 0.002, 0.8) * 2
st = np.tanh(0.9 * (cluster * env(len(s), 0.003, 0.9) + slam + sub)) * 0.8
add(st, sting, 1.0, pan=0.0)
# delayed ghost copy for width
Rghost = np.zeros(N); i = int((sting + 0.017) * SR); Rghost[i:i + len(st)] = st[: N - i] * 0.4
R += Rghost

# ---- music-box note on "PART 2?"
for at, f in ((endcard + 0.6, 1046.5), (endcard + 1.4, 987.8), (endcard + 2.4, 1396.9)):
    s = seg(2.0)
    note = (np.sin(2 * np.pi * f * s) + 0.3 * np.sin(2 * np.pi * 2 * f * s) + 0.1 * np.sin(2 * np.pi * 3.01 * f * s))
    add(note * env(len(s), 0.002, 0.45), at, 0.10)

# fade out the last 0.6 s
fade = np.clip((DUR - t) / 0.6, 0, 1)
L *= fade; R *= fade
peak = max(np.abs(L).max(), np.abs(R).max())
L /= peak / 0.9; R /= peak / 0.9
pcm = (np.stack([L, R], 1) * 32767).astype(np.int16)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("wrote", sys.argv[2], f"{DUR}s")
