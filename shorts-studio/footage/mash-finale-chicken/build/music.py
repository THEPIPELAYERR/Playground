import json, numpy as np, soundfile as sf
T=json.load(open("timeline.json")); sr=48000; D=T["dur"]; n=int(D*sr); t=np.arange(n)/sr
m=np.zeros(n)
def env(a,r,L):
    e=np.ones(L); A=int(a*sr); R=int(r*sr); e[:A]=np.linspace(0,1,A); e[-R:]*=np.linspace(1,0,R); return e
def tone(f,s,L,amp,a=0.02,r=0.3,harm=(1,0.5,0.25)):
    i0=int(s*sr); L=min(int(L*sr),n-i0)
    if L<=0: return
    tt=np.arange(L)/sr; x=sum(h*np.sin(2*np.pi*f*(k+1)*tt) for k,h in enumerate(harm))
    m[i0:i0+L]+=amp*x*env(a,r,L)
sc={s["scene"]:s for s in T["scenes"]}
# 1) heartbeat under the hook and the secret
def beat(t0,t1,bpm,amp):
    k=t0
    while k<t1:
        for off,a2 in ((0,1),(0.18,0.6)):
            i0=int((k+off)*sr); L=int(0.18*sr)
            if i0+L<n:
                tt=np.arange(L)/sr; m[i0:i0+L]+=amp*a2*np.sin(2*np.pi*(58-60*tt)*tt)*np.exp(-tt*22)
        k+=60/bpm
beat(0,sc["date"]["t0"],66,0.55)
beat(sc["hospital"]["t0"],sc["armistice"]["t0"],78,0.45)
beat(sc["stones"]["t0"],sc["end"]["t0"],90,0.5)
# 2) pad chords, layered more as the story goes on (A minor / F / C / G)
prog=[(220,261.6,329.6),(174.6,220,261.6),(130.8,164.8,196),(196,246.9,293.7)]
start=sc["date"]["t0"]; L=4.0; k=0; i=0
while start+k<sc["end"]["t0"]:
    ch=prog[i%4]; s0=start+k
    layer=0.05+0.05*min(1,(s0-start)/(sc["stones"]["t0"]-start))  # louder toward the payoff
    if sc["baby"]["t0"]-0.2<s0<sc["word"]["t1"]: layer*=0.4
    for f in ch: tone(f,s0,L+0.6,layer,a=0.8,r=1.2,harm=(1,0.3,0.1))
    if s0>sc["mozart"]["t0"]:
        for j,f in enumerate(ch): tone(f*2,s0+j*0.5,0.9,layer*0.6,a=0.01,r=0.7,harm=(1,0.2))
    k+=L; i+=1
# 3) final resolve on A minor, soft
for f in (110,220,261.6,329.6): tone(f,sc["end"]["t0"],D-sc["end"]["t0"],0.07,a=0.3,r=2.0,harm=(1,0.3))
# 4) impact on every scene cut (low boom + short noise)
rng=np.random.default_rng(1)
for s in T["scenes"][1:]:
    i0=int((s["t0"]-0.02)*sr); L=int(0.6*sr)
    if i0+L<n:
        tt=np.arange(L)/sr
        m[i0:i0+L]+=0.35*np.sin(2*np.pi*(70-40*tt)*tt)*np.exp(-tt*7)+0.05*rng.standard_normal(L)*np.exp(-tt*30)
# 5) riser into the stones payoff
s0=sc["bj"]["t0"]; s1=sc["stones"]["t0"]; L=int((s1-s0)*sr); tt=np.arange(L)/sr
m[int(s0*sr):int(s0*sr)+L]+=0.12*(tt/tt[-1])**2*rng.standard_normal(L)*0.5
m/=np.abs(m).max(); m*=0.8
sf.write("music.wav",m.astype("float32"),sr)
