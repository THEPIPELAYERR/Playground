import json, numpy as np, soundfile as sf, difflib, re
a,sr=sf.read("/home/claude/a.wav",dtype="float32")
W=json.load(open("/home/claude/build/src_words.json"))
# (start_ts_of_first_word, ts_of_last_word, script text, scene)
SEG=[(7.68,10.24,"The M*A*S*H finale has a chicken in it.","hook"),
(12.00,12.88,"It was never a chicken.","hook2"),
(27.60,33.52,"Goodbye, Farewell and Amen aired February 28th, 1983, on CBS.","date"),
(36.72,41.36,"About 106 million US viewers. Still the most-watched scripted episode.","viewers"),
(54.80,56.56,"Hawkeye is in a psychiatric hospital.","hospital"),
(60.24,61.92,"Then a bus, and an enemy patrol.","bus"),
(63.20,65.44,"Hawkeye tells the woman to keep her chicken quiet.","quiet"),
(69.60,70.16,"It was her baby.","baby"),
(71.52,74.72,"He buried that memory under one word: chicken.","word"),
(84.40,86.00,"The armistice ends the war.","armistice"),
(105.12,108.72,"Winchester teaches Chinese POW musicians Mozart.","mozart"),
(110.72,115.04,"Later, most of them are killed, and music pains him.","music"),
(116.32,121.60,"Klinger, who spent years trying to get home, marries Soon-Lee and stays in Korea.","klinger"),
(131.60,133.52,"BJ can't say goodbye out loud.","bj"),
(135.44,140.80,"As Hawkeye's helicopter lifts off, he sees GOODBYE spelled in stones.","stones"),
(162.24,165.44,"I've never heard the word chicken the same way since.","end")]
def rms(t0,t1):
    x=a[int(t0*sr):int(t1*sr)]; return float(np.sqrt((x**2).mean()+1e-12))
noise=np.percentile([rms(t,t+0.05) for t in np.arange(0,len(a)/sr-0.05,0.05)],15)
thr=max(noise*3,0.004)
def find_end(t):
    t+=0.2
    while t<len(a)/sr-0.2:
        if max(rms(t,t+0.05),rms(t+0.05,t+0.1),rms(t+0.1,t+0.15))<thr: return t+0.05
        t+=0.02
    return t
def find_start(t):
    s=t-0.05
    while s>t-0.5 and rms(s-0.05,s)>thr: s-=0.02
    return s-0.06
out=[];caps=[];scenes=[];cur=0.0
GAP={"hook2":0.35,"date":0.5}
for i,(f,l,text,sc) in enumerate(SEG):
    s=find_start(f); e=find_end(l)
    s=min(s,f-0.22); e=max(e,l+0.7)
    prv=[w[1] for w in W if w[1]<f-0.05]
    if prv: s=max(s,prv[-1]+0.35)
    # don't run into the next spoken word
    nxt=[w[1] for w in W if w[1]>l+0.05]
    if nxt: e=min(e,nxt[0]-0.08)
    clip=a[int(s*sr):int(e*sr)].copy()
    fade=int(0.015*sr); clip[:fade]*=np.linspace(0,1,fade); clip[-fade:]*=np.linspace(1,0,fade)
    gap=0.28 if i else 0.35
    out.append(np.zeros(int(gap*sr),dtype="float32")); cur+=gap
    t0=cur
    asr=[w for w in W if f-0.01<=w[1]<=l+0.01]
    sw=text.split()
    norm=lambda x:re.sub(r"[^a-z0-9]","",x.lower())
    sm=difflib.SequenceMatcher(None,[norm(w[0]) for w in asr],[norm(x) for x in sw])
    times=[None]*len(sw)
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag in("equal","replace"):
            for k in range(j2-j1):
                src=i1+min(k*(i2-i1)//max(j2-j1,1),i2-i1-1) if i2>i1 else None
                if src is not None and (tag=="equal" or i2-i1==j2-j1 or k==0): times[j1+k]=asr[src][1]
    # fill gaps by interpolation between known times
    known=[(k,t) for k,t in enumerate(times) if t is not None]
    for k in range(len(sw)):
        if times[k] is None:
            prev=[x for x in known if x[0]<k]; nx=[x for x in known if x[0]>k]
            p=prev[-1] if prev else (-1,s); n=nx[0] if nx else (len(sw),e)
            times[k]=p[1]+(n[1]-p[1])*(k-p[0])/(n[0]-p[0])
    for k,wd in enumerate(sw): caps.append({"w":wd,"t":round(t0+times[k]-s,3),"scene":sc})
    out.append(clip); cur+=len(clip)/sr
    scenes.append({"scene":sc,"t0":round(t0,3),"t1":round(cur,3),"text":text})
out.append(np.zeros(int(1.2*sr),dtype="float32")); cur+=1.2
v=np.concatenate(out)
sf.write("voice.wav",v,sr)
json.dump({"caps":caps,"scenes":scenes,"dur":cur},open("timeline.json","w"),indent=1)
print(round(cur,2)); [print(x["scene"],x["t0"],x["t1"]) for x in scenes]
