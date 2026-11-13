// Animation character kit for "They Smile". Clean cartoon lines, flat colour, one soft cel-shadow tone.
// Characters take animation params: talk (mouth open 0..1), blink (0..1), headRot, bodyDx, breath, look.
// Everything draws into the global context `x` (swap it to draw into an offscreen panel).
let x;
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const lerp = (a, b, p) => a + (b - a) * p;
const ease = p => { p = clamp(p, 0, 1); return p * p * (3 - 2 * p); };
function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
const rgb = (c, k = 1, a = 1) => `rgba(${clamp(c[0] * k, 0, 255) | 0},${clamp(c[1] * k, 0, 255) | 0},${clamp(c[2] * k, 0, 255) | 0},${a})`;
const INK = '#141012';

function path(fn) { const p = new Path2D(); fn(p); return p; }
function ink(p, w) { x.lineWidth = w; x.strokeStyle = INK; x.lineJoin = 'round'; x.lineCap = 'round'; x.stroke(p); }
function fillInk(p, fill, w) { x.fillStyle = fill; x.fill(p); if (w) ink(p, w); }
function halftone() { /* comic-only effect: off in the animated style */ }
function blobPath(cx, cy, rad, r, n = 9, jag = 0.35) {
  return path(p => { for (let i = 0; i <= n; i++) { const a = i / n * Math.PI * 2, rr = rad * (1 - jag / 2 + jag * r()); const px = cx + Math.cos(a) * rr, py = cy + Math.sin(a) * rr * 0.8; i ? p.lineTo(px, py) : p.moveTo(px, py); } p.closePath(); });
}

// ---------------------------------------------------------------- people
// p: { skin:[r,g,b], female, age 0..1, hair:{style,color}, expr:'grin'|'scared'|'calm'|'whisper'|'laugh',
//      rash, look:[dx,dy], outfit, outfitColor, beard, stubble, glasses, tears, blood, seed, rot, tongue, name, ropes }
function person(cx, cy, r, p) {
  x.save(); x.translate(cx, cy); x.rotate(p.rot || 0); x.scale(r * (p.flip ? -1 : 1), r);
  const lw = Math.max(1.1, r * 0.013) / r;
  const sk = p.skin, skS = rgb(sk, 0.8), skD = rgb(sk, 0.62);
  const hc = p.hair.color;
  const R = rng(p.seed || 1);
  const F = !!p.female;
  const talk = p.talk || 0, blink = p.blink || 0;
  // --- hair behind the head
  if (p.hair.style === 'long') fillInk(path(q => { q.moveTo(-0.86, -0.3); q.bezierCurveTo(-1.02, -1.28, 1.02, -1.28, 0.86, -0.3); q.lineTo(1.05, 1.75); q.lineTo(-1.05, 1.75); q.closePath(); }), rgb(hc, 0.75), lw * 1.2);
  if (p.hair.style === 'bun') { const b = path(q => q.arc(0.05, -1.02, 0.3, 0, Math.PI * 2)); fillInk(b, rgb(hc), lw * 1.2); halftone(b, rgb(hc, 0.75), 0.04, 0.012, [-0.3, -1.35, 0.4, -0.7]); }
  // --- shoulders / clothes (they move with breathing / laughing)
  x.save(); x.translate(p.bodyDx || 0, (p.breath || 0) * 0.03);
  const body = path(q => { q.moveTo(-1.55, 2.7); q.lineTo(-1.48, 1.8); q.quadraticCurveTo(-1.38, 1.32, -0.6, 1.16); q.lineTo(-0.3, 1.0); q.lineTo(0.3, 1.0); q.lineTo(0.6, 1.16); q.quadraticCurveTo(1.38, 1.32, 1.48, 1.8); q.lineTo(1.55, 2.7); q.closePath(); });
  const oc = p.outfitColor || [110, 120, 135];
  const base = p.outfit === 'vest' ? [128, 134, 142] : oc;
  fillInk(body, rgb(base), lw * 1.5);
  if (p.outfit === 'flannel') { x.save(); x.clip(body); x.strokeStyle = 'rgba(20,10,10,0.55)'; x.lineWidth = 0.07; for (let k = -2; k < 2; k += 0.28) { x.beginPath(); x.moveTo(k, 0.9); x.lineTo(k, 2.8); x.stroke(); x.beginPath(); x.moveTo(-2, 1.2 + (k + 2) * 0.5); x.lineTo(2, 1.2 + (k + 2) * 0.5); x.stroke(); } x.restore(); }
  if (p.outfit === 'vest') {
    for (const sd of [-1, 1]) { const v = path(q => { q.moveTo(sd * 0.32, 1.02); q.lineTo(sd * 0.62, 1.17); q.quadraticCurveTo(sd * 1.3, 1.32, sd * 1.4, 1.8); q.lineTo(sd * 1.46, 2.7); q.lineTo(sd * 0.42, 2.7); q.lineTo(sd * 0.5, 1.6); q.closePath(); }); fillInk(v, rgb(oc), lw * 1.3); }
    const tag = path(q => q.rect(-1.05, 1.62, 0.5, 0.2)); fillInk(tag, '#f4f1e8', lw);
    x.fillStyle = INK; x.font = '900 0.13px Inter, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(p.name || 'DALE', -0.8, 1.725);
  }
  if (p.outfit === 'robe') { for (const sd of [-1, 1]) fillInk(path(q => { q.moveTo(sd * 0.3, 1.0); q.lineTo(sd * 0.75, 1.15); q.lineTo(sd * 0.15, 2.7); q.lineTo(sd * 0.02, 2.7); q.closePath(); }), rgb(oc, 1.15), lw); fillInk(path(q => { q.moveTo(-0.12, 1.05); q.lineTo(0.12, 1.05); q.lineTo(0.02, 2.0); q.closePath(); }), '#f6dbe4', lw * 0.7); }
  if (p.outfit === 'cardigan') {
    fillInk(path(q => { q.moveTo(-0.42, 1.03); q.lineTo(0.42, 1.03); q.lineTo(0.12, 1.55); q.lineTo(-0.12, 1.55); q.closePath(); }), '#f2ede2', lw);
    for (const sd of [-1, 1]) ink(path(q => { q.moveTo(sd * 0.12, 1.55); q.lineTo(sd * 0.14, 2.7); }), lw);
    for (let k = 0; k < 3; k++) fillInk(path(q => q.arc(-0.2, 1.8 + k * 0.3, 0.05, 0, Math.PI * 2)), '#6b4a1a', lw * 0.6);
  }
  if (p.outfit === 'hoodie') {
    fillInk(path(q => { q.moveTo(-0.75, 1.15); q.quadraticCurveTo(0, 1.55, 0.75, 1.15); q.quadraticCurveTo(0, 1.3, -0.75, 1.15); }), rgb(oc, 0.8), lw);
    for (const sd of [-1, 1]) ink(path(q => { q.moveTo(sd * 0.2, 1.35); q.lineTo(sd * 0.24, 1.95); }), lw);
  }
  // cel shadow on the body
  const bs = path(q => { q.moveTo(0.55, 1.1); q.quadraticCurveTo(0.9, 1.8, 0.7, 2.7); q.lineTo(1.7, 2.7); q.lineTo(1.7, 1.0); q.closePath(); });
  x.save(); x.clip(body); x.fillStyle = 'rgba(10,5,20,0.28)'; x.fill(bs); halftone(bs, 'rgba(10,5,20,0.3)', 0.05, 0.014, [0.4, 1.0, 1.6, 2.7]); x.restore();
  if (p.ropes) {
    x.strokeStyle = '#7a4f24'; x.lineWidth = 0.09; x.lineCap = 'butt';
    for (const [a, b] of [[[-1.5, 1.7], [1.5, 2.15]], [[-1.5, 2.15], [1.5, 1.75]], [[-1.5, 2.45], [1.5, 2.45]]]) { x.beginPath(); x.moveTo(...a); x.lineTo(...b); x.stroke(); }
    x.strokeStyle = INK; x.lineWidth = lw * 0.7; for (const [a, b] of [[[-1.5, 1.66], [1.5, 2.11]], [[-1.5, 1.74], [1.5, 2.19]], [[-1.5, 2.11], [1.5, 1.71]], [[-1.5, 2.19], [1.5, 1.79]]]) { x.beginPath(); x.moveTo(...a); x.lineTo(...b); x.stroke(); }
  }
  x.restore();
  // head turns / tilts around the neck
  x.save(); x.translate(0, 1.0); x.rotate(p.headRot || 0); x.translate(0, -1.0);
  // --- neck
  const neck = path(q => q.rect(-0.27, 0.55, 0.54, 0.62));
  fillInk(neck, rgb(sk), lw);
  fillInk(path(q => { q.moveTo(-0.27, 0.6); q.quadraticCurveTo(0, 1.02, 0.27, 0.6); q.lineTo(0.27, 0.9); q.quadraticCurveTo(0, 1.05, -0.27, 0.9); q.closePath(); }), skS, 0);
  if (p.age > 0.7) for (let k = 0; k < 2; k++) ink(path(q => { q.moveTo(-0.2, 0.98 + k * 0.08); q.quadraticCurveTo(0, 1.02 + k * 0.08, 0.2, 0.98 + k * 0.08); }), lw * 0.6);
  // --- ears
  for (const sd of [-1, 1]) { const e = path(q => q.ellipse(sd * 0.71, 0.05, 0.1, 0.18, 0, 0, Math.PI * 2)); fillInk(e, sd > 0 ? skS : rgb(sk), lw); ink(path(q => { q.moveTo(sd * 0.7, -0.05); q.quadraticCurveTo(sd * 0.78, 0.05, sd * 0.71, 0.15); }), lw * 0.6); }
  // --- head
  const jw = F ? 0.38 : 0.44, cw = F ? 0.68 : 0.73, chin = F ? 0.96 : 1.0;
  const head = path(q => {
    q.moveTo(0, -1); q.bezierCurveTo(0.56, -1, 0.74, -0.6, cw, -0.15);
    q.bezierCurveTo(cw, 0.3, 0.6 + (p.age > 0.7 ? 0.05 : 0), 0.62, jw, 0.83); q.quadraticCurveTo(0.2, chin, 0, chin);
    q.quadraticCurveTo(-0.2, chin, -jw, 0.83); q.bezierCurveTo(-0.6 - (p.age > 0.7 ? 0.05 : 0), 0.62, -cw, 0.3, -cw, -0.15); q.bezierCurveTo(-0.74, -0.6, -0.56, -1, 0, -1); q.closePath();
  });
  fillInk(head, rgb(sk), 0);
  x.save(); x.clip(head);
  const hs = path(q => { q.moveTo(0.2, -1.1); q.bezierCurveTo(0.44, -0.6, 0.52, -0.2, 0.44, 0.2); q.bezierCurveTo(0.38, 0.55, 0.3, 0.78, 0.1, 1.05); q.lineTo(1, 1.05); q.lineTo(1, -1.1); q.closePath(); });
  x.fillStyle = skS; x.fill(hs); halftone(hs, skD, 0.035, 0.011, [0.1, -1.1, 1, 1.1]);
  if (p.stubble) halftone(path(q => { q.moveTo(-0.75, 0.15); q.bezierCurveTo(-0.6, 0.9, 0.6, 0.9, 0.75, 0.15); q.lineTo(0.75, 1.1); q.lineTo(-0.75, 1.1); q.closePath(); }), 'rgba(40,30,30,0.35)', 0.03, 0.008, [-0.8, 0.1, 0.8, 1.1]);
  // the bloom: a crusted red rash spreading from the mouth up the cheeks
  if (p.rash) {
    const rr = rng((p.seed || 1) * 31 + 7);
    const spots = [[0, 0.5, 0.2], [-0.36, 0.42, 0.15], [0.36, 0.42, 0.15], [-0.46, 0.18, 0.12], [0.46, 0.18, 0.12], [0, 0.82, 0.13], [-0.25, 0.7, 0.11], [0.25, 0.7, 0.11], [-0.5, -0.02, 0.08], [0.5, -0.02, 0.08]];
    for (const [sx, sy, sr] of spots) {
      fillInk(blobPath(sx + (rr() - 0.5) * 0.06, sy + (rr() - 0.5) * 0.05, sr * p.rash, rr, 11, 0.5), 'rgba(196,38,40,0.88)', 0);
      x.lineWidth = lw * 0.6; x.strokeStyle = '#6a0d12'; x.stroke(blobPath(sx, sy, sr * p.rash * 0.9, rr, 11, 0.5));
      fillInk(blobPath(sx, sy, sr * p.rash * 0.45, rr, 8, 0.5), 'rgba(120,14,20,0.9)', 0);
    }
    x.fillStyle = 'rgba(170,25,30,0.85)';
    for (let k = 0; k < 40; k++) { const a = rr() * Math.PI * 2, d = 0.3 + rr() * 0.45; x.beginPath(); x.arc(Math.cos(a) * d * 0.8, 0.45 + Math.sin(a) * d * 0.6 - 0.1, 0.008 + rr() * 0.02, 0, Math.PI * 2); x.fill(); }
  }
  if (p.blood) { x.fillStyle = '#8c0b10'; const br = rng((p.seed || 1) * 13); for (let k = 0; k < 14; k++) { x.beginPath(); x.arc(-0.6 + br() * 1.1, -0.7 + br() * 1.5, 0.008 + br() * 0.025, 0, Math.PI * 2); x.fill(); } }
  // wrinkles
  if (p.age > 0.4) {
    const n = p.age > 0.75 ? 3 : 2;
    for (let k = 0; k < n; k++) ink(path(q => { q.moveTo(-0.32, -0.55 - k * 0.07); q.quadraticCurveTo(0, -0.6 - k * 0.07, 0.32, -0.55 - k * 0.07); }), lw * 0.5);
    for (const sd of [-1, 1]) ink(path(q => { q.moveTo(sd * 0.18, -0.0); q.quadraticCurveTo(sd * 0.3, 0.07, sd * 0.42, -0.01); }), lw * 0.5);
  }
  x.restore();
  ink(head, lw * 1.6);
  // --- hair in front
  const hcol = rgb(hc), hS = rgb(hc, 0.7);
  const st = p.hair.style;
  if (st === 'short' || st === 'buzz') { const h = path(q => { q.moveTo(-0.75, -0.2); q.bezierCurveTo(-0.82, -1.12, 0.82, -1.12, 0.75, -0.2); q.lineTo(0.66, -0.46); q.quadraticCurveTo(0.3, -0.76, 0, -0.7); q.quadraticCurveTo(-0.3, -0.76, -0.66, -0.46); q.closePath(); }); fillInk(h, hcol, lw * 1.3); halftone(h, hS, 0.04, 0.012, [0, -1.1, 0.8, -0.2]); }
  if (st === 'balding') for (const sd of [-1, 1]) { fillInk(path(q => { q.moveTo(sd * 0.75, -0.42); q.quadraticCurveTo(sd * 0.82, 0.0, sd * 0.7, 0.12); q.lineTo(sd * 0.64, -0.3); q.quadraticCurveTo(sd * 0.6, -0.6, sd * 0.4, -0.85); q.quadraticCurveTo(sd * 0.7, -0.75, sd * 0.75, -0.42); q.closePath(); }), hcol, lw); }
  if (st === 'long') {
    fillInk(path(q => { q.moveTo(-0.76, -0.2); q.bezierCurveTo(-0.84, -1.16, 0.84, -1.16, 0.76, -0.2); q.quadraticCurveTo(0.55, -0.66, 0.1, -0.56); q.quadraticCurveTo(-0.35, -0.74, -0.76, -0.2); q.closePath(); }), hcol, lw * 1.3);
    for (const sd of [-1, 1]) fillInk(path(q => { q.moveTo(sd * 0.76, -0.35); q.quadraticCurveTo(sd * 0.86, 0.5, sd * 1.0, 1.7); q.lineTo(sd * 0.72, 1.75); q.quadraticCurveTo(sd * 0.62, 0.6, sd * 0.62, -0.3); q.closePath(); }), sd > 0 ? hS : hcol, lw * 1.2);
    x.strokeStyle = 'rgba(255,255,255,0.55)'; x.lineWidth = lw * 1.2; x.beginPath(); x.moveTo(-0.45, -0.88); x.quadraticCurveTo(-0.15, -0.98, 0.15, -0.95); x.stroke();
  }
  if (st === 'curlers') {
    fillInk(path(q => { q.moveTo(-0.8, -0.15); q.bezierCurveTo(-0.95, -1.2, 0.95, -1.2, 0.8, -0.15); q.quadraticCurveTo(0.5, -0.62, 0, -0.6); q.quadraticCurveTo(-0.5, -0.62, -0.8, -0.15); q.closePath(); }), hcol, lw * 1.3);
    for (const [cx2, cy2, a] of [[-0.5, -0.82, -0.6], [-0.18, -1.0, -0.2], [0.18, -1.0, 0.2], [0.5, -0.82, 0.6], [-0.75, -0.45, -1.1], [0.75, -0.45, 1.1]]) {
      x.save(); x.translate(cx2, cy2); x.rotate(a); fillInk(path(q => q.roundRect(-0.13, -0.08, 0.26, 0.16, 0.06)), '#f08db4', lw); x.restore();
    }
  }
  if (st === 'bun') { const h = path(q => { q.moveTo(-0.75, -0.2); q.bezierCurveTo(-0.82, -1.12, 0.82, -1.12, 0.75, -0.2); q.quadraticCurveTo(0.6, -0.7, 0.03, -0.78); q.quadraticCurveTo(-0.6, -0.7, -0.75, -0.2); q.closePath(); }); fillInk(h, hcol, lw * 1.3); for (let k = -2; k <= 2; k++) ink(path(q => { q.moveTo(k * 0.12, -0.82); q.quadraticCurveTo(k * 0.2, -0.95, k * 0.1, -1.02); }), lw * 0.5); }
  if (st === 'cap') {
    fillInk(path(q => { q.moveTo(-0.78, -0.35); q.bezierCurveTo(-0.85, -1.2, 0.85, -1.2, 0.78, -0.35); q.closePath(); }), rgb(p.hair.capColor || [40, 60, 120]), lw * 1.3);
    fillInk(path(q => q.ellipse(0, -0.38, 0.95, 0.14, 0, 0, Math.PI * 2)), rgb(p.hair.capColor || [40, 60, 120], 0.8), lw * 1.3);
  }
  if (p.beard) { const b = path(q => { q.moveTo(-0.72, 0.05); q.bezierCurveTo(-0.72, 0.7, -0.4, 1.12, 0, 1.14); q.bezierCurveTo(0.4, 1.12, 0.72, 0.7, 0.72, 0.05); q.lineTo(0.6, 0.15); q.bezierCurveTo(0.5, 0.55, 0.3, 0.42, 0, 0.42); q.bezierCurveTo(-0.3, 0.42, -0.5, 0.55, -0.6, 0.15); q.closePath(); }); fillInk(b, hcol, lw * 1.2); halftone(b, hS, 0.035, 0.012, [-0.8, 0, 0.8, 1.2]); }
  // --- brows
  const e = p.expr || 'calm';
  const browY = { grin: -0.38, laugh: -0.4, scared: -0.34, calm: -0.3, whisper: -0.32 }[e];
  for (const sd of [-1, 1]) {
    const inner = e === 'scared' || e === 'whisper' ? browY - 0.08 : browY + 0.02, outer = e === 'scared' || e === 'whisper' ? browY + 0.06 : browY + 0.02, mid = e === 'grin' || e === 'laugh' ? browY - 0.06 : browY - 0.02;
    const th = (p.age > 0.75 ? 0.035 : F ? 0.045 : 0.065);
    fillInk(path(q => { q.moveTo(sd * 0.1, inner); q.quadraticCurveTo(sd * 0.3, mid - th, sd * 0.5, outer); q.quadraticCurveTo(sd * 0.3, mid + th * 0.4, sd * 0.1, inner + th); q.closePath(); }), p.age > 0.75 ? '#c9c4bb' : rgb(hc, 0.8), lw * 0.6);
  }
  // --- eyes
  const lk = p.look || [0, 0];
  for (const sd of [-1, 1]) {
    const ex = sd * 0.29, ey = -0.12, w = 0.15;
    const h = { grin: 0.06, laugh: 0.035, scared: 0.1, calm: 0.045, whisper: 0.08 }[e];
    const low = { grin: 0.25, laugh: 0.1, scared: 1.25, calm: 0.7, whisper: 1.0 }[e];
    const eye = path(q => { q.moveTo(ex - w, ey); q.quadraticCurveTo(ex, ey - h * 1.7, ex + w, ey); q.quadraticCurveTo(ex, ey + h * low, ex - w, ey); q.closePath(); });
    fillInk(eye, p.rash ? '#f4e2da' : '#fbf8f1', 0);
    x.save(); x.clip(eye);
    if (p.rash) { x.strokeStyle = 'rgba(190,40,40,0.7)'; x.lineWidth = lw * 0.5; for (let k = 0; k < 4; k++) { x.beginPath(); x.moveTo(ex - sd * w, ey + (k - 1.5) * 0.02); x.lineTo(ex - sd * w * 0.5, ey + (k - 1.5) * 0.01); x.stroke(); } }
    const ir = e === 'scared' ? 0.045 : 0.06;
    const ix = ex + lk[0] * 0.06, iy = ey + lk[1] * 0.03 - (e === 'calm' ? 0.01 : 0);
    fillInk(path(q => q.arc(ix, iy, ir, 0, Math.PI * 2)), p.iris || '#5a3b22', lw * 0.6);
    fillInk(path(q => q.arc(ix, iy, ir * 0.48, 0, Math.PI * 2)), INK, 0);
    fillInk(path(q => q.arc(ix - ir * 0.35, iy - ir * 0.35, ir * 0.25, 0, Math.PI * 2)), '#fff', 0);
    x.restore();
    ink(path(q => { q.moveTo(ex - w * 1.05, ey + 0.01); q.quadraticCurveTo(ex, ey - h * 1.75, ex + w * 1.05, ey); }), lw * 2.0);
    ink(path(q => { q.moveTo(ex - w * 0.8, ey + h * low * 0.35); q.quadraticCurveTo(ex, ey + h * low * 0.55, ex + w * 0.9, ey + 0.005); }), lw * 0.7);
    if (blink > 0.02) {
      const top = ey - h * 1.8, lid = top + blink * (h * 1.8 + h * low * 0.6 + 0.01);
      x.save(); x.clip(eye); x.fillStyle = sd > 0 ? skS : rgb(sk); x.fillRect(ex - w - 0.05, top - 0.05, w * 2 + 0.1, lid - top + 0.05); x.restore();
      ink(path(q => { q.moveTo(ex - w, Math.min(lid, ey)); q.quadraticCurveTo(ex, lid + 0.01, ex + w, Math.min(lid, ey)); }), lw * 1.6);
    }
    if (F) for (let k = 0; k < 3; k++) ink(path(q => { q.moveTo(ex + sd * (w - 0.01 * k), ey - 0.01 - k * 0.012); q.lineTo(ex + sd * (w + 0.05), ey - 0.04 - k * 0.025); }), lw * 0.7);
    if (e === 'grin' || e === 'laugh') ink(path(q => { q.moveTo(ex - w * 0.7, ey + 0.1); q.quadraticCurveTo(ex, ey + 0.15, ex + w * 0.8, ey + 0.09); }), lw * 0.7);
    if (p.age > 0.4) for (let k = 0; k < 3; k++) ink(path(q => { q.moveTo(ex + sd * (w + 0.02), ey + (k - 1) * 0.03); q.lineTo(ex + sd * (w + 0.09), ey + (k - 1) * 0.05); }), lw * 0.5);
    if (p.tears) { const tr = path(q => { q.moveTo(ex - 0.03, ey + 0.08); q.quadraticCurveTo(ex - 0.06, ey + 0.3, ex - 0.02, ey + 0.5); q.quadraticCurveTo(ex + 0.02, ey + 0.3, ex + 0.03, ey + 0.08); q.closePath(); }); fillInk(tr, 'rgba(150,205,255,0.85)', lw * 0.5); }
  }
  if (p.glasses) {
    for (const sd of [-1, 1]) { const g = path(q => q.ellipse(sd * 0.29, -0.11, 0.21, 0.17, 0, 0, Math.PI * 2)); x.fillStyle = 'rgba(200,220,255,0.12)'; x.fill(g); ink(g, lw * 1.3); x.fillStyle = 'rgba(255,255,255,0.85)'; x.beginPath(); x.moveTo(sd * 0.29 - 0.12, -0.2); x.lineTo(sd * 0.29 - 0.05, -0.24); x.lineTo(sd * 0.29 - 0.14, -0.05); x.closePath(); x.fill(); }
    ink(path(q => { q.moveTo(-0.08, -0.13); q.quadraticCurveTo(0, -0.17, 0.08, -0.13); }), lw * 1.2);
  }
  // --- nose
  fillInk(path(q => { q.moveTo(0.04, -0.02); q.quadraticCurveTo(0.12, 0.18, 0.12, 0.25); q.lineTo(0.03, 0.27); q.closePath(); }), skS, 0);
  ink(path(q => { q.moveTo(0.03, -0.02); q.quadraticCurveTo(0.12, 0.17, 0.11, 0.25); q.quadraticCurveTo(0.03, 0.31, -0.08, 0.27); }), lw * 1.1);
  for (const sd of [-1, 1]) fillInk(path(q => q.ellipse(sd * 0.055, 0.265, 0.03, 0.015, 0, 0, Math.PI * 2)), INK, 0);
  // --- mouth
  if (e === 'grin' || e === 'laugh') {
    const mw = e === 'laugh' ? 0.36 : 0.4, mb = (e === 'laugh' ? 0.86 : 0.74) + 0.2 * talk;
    const m = path(q => { q.moveTo(-mw, 0.42); q.quadraticCurveTo(0, 0.5, mw, 0.42); q.quadraticCurveTo(0, mb, -mw, 0.42); q.closePath(); });
    fillInk(m, '#5a0f16', 0);
    x.save(); x.clip(m);
    fillInk(path(q => { q.moveTo(-mw, 0.42); q.quadraticCurveTo(0, 0.5, mw, 0.42); q.lineTo(mw, 0.5); q.quadraticCurveTo(0, 0.62, -mw, 0.5); q.closePath(); }), '#f6f1e4', lw * 0.6);
    for (let k = -3; k <= 3; k++) ink(path(q => { q.moveTo(k * 0.09, 0.47); q.lineTo(k * 0.09, 0.56); }), lw * 0.45);
    const mBot = (0.42 + mb) / 2;   // the visible bottom of the mouth
    fillInk(path(q => q.ellipse(0, mBot - 0.05, 0.2, 0.09, 0, 0, Math.PI * 2)), p.tongue ? '#e4707a' : '#c9545f', 0);
    if (p.blood) fillInk(path(q => q.rect(-0.2, 0.5, 0.15, 0.04)), 'rgba(140,10,15,0.8)', 0);
    x.restore();
    ink(m, lw * 1.5);
    if (p.tongue) {
      const mB = (0.42 + mb) / 2, len = 0.34 * p.tongue, sw = p.tongueSway || 0, tw = 0.15;
      const tip = [sw * 0.6, mB + len];
      const tg = path(q => { q.moveTo(-tw, mB - 0.06); q.bezierCurveTo(-tw - 0.02, mB + len * 0.6, tip[0] - tw * 0.9, tip[1] + 0.04, tip[0], tip[1] + 0.04); q.bezierCurveTo(tip[0] + tw * 0.9, tip[1] + 0.04, tw + 0.02, mB + len * 0.6, tw, mB - 0.06); q.closePath(); });
      fillInk(tg, '#e4707a', lw * 1.2);
      ink(path(q => { q.moveTo(0, mB - 0.02); q.quadraticCurveTo(sw * 0.3, mB + len * 0.5, tip[0], tip[1] - 0.06); }), lw * 0.7);   // centre groove
      x.fillStyle = 'rgba(255,255,255,0.5)'; x.beginPath(); x.ellipse(-tw * 0.45 + sw * 0.3, mB + len * 0.45, 0.025, len * 0.22 + 0.01, 0, 0, Math.PI * 2); x.fill();   // wet shine
      ink(path(q => { q.moveTo(-mw * 0.55, mB - 0.01); q.quadraticCurveTo(0, mB + 0.03, mw * 0.55, mB - 0.01); }), lw * 1.2);   // lower lip line over the tongue root
    }
    for (const sd of [-1, 1]) ink(path(q => { q.moveTo(sd * 0.2, 0.2); q.quadraticCurveTo(sd * (mw + 0.12), 0.32, sd * (mw + 0.05), 0.55); }), lw * 1.1);
  } else if (e === 'scared' || e === 'whisper') {
    const ow = (e === 'scared' ? 0.15 : 0.1) * (0.75 + 0.5 * talk), bot = 0.56 + (e === 'scared' ? 0.2 : 0.1) * (0.45 + 0.9 * talk);
    const m = path(q => { q.moveTo(-ow, 0.56); q.quadraticCurveTo(0, 0.5, ow, 0.56); q.quadraticCurveTo(0, bot, -ow, 0.56); q.closePath(); });
    fillInk(m, '#3a0c12', lw * 1.2);
    if (F) fillInk(path(q => { q.moveTo(-ow - 0.03, 0.56); q.quadraticCurveTo(0, bot + 0.08, ow + 0.03, 0.56); q.quadraticCurveTo(0, bot + 0.02, -ow - 0.03, 0.56); q.closePath(); }), '#c9757a', lw * 0.6);
  } else {
    const m = path(q => { q.moveTo(-0.26, 0.5); q.quadraticCurveTo(0, 0.62, 0.26, 0.49); });
    if (talk > 0.05) fillInk(path(q => { q.moveTo(-0.17, 0.53); q.quadraticCurveTo(0, 0.56, 0.17, 0.53); q.quadraticCurveTo(0, 0.56 + 0.18 * talk, -0.17, 0.53); q.closePath(); }), '#4a1418', lw);
    if (F) fillInk(path(q => { q.moveTo(-0.24, 0.51); q.quadraticCurveTo(0, 0.68, 0.24, 0.5); q.quadraticCurveTo(0, 0.6, -0.24, 0.51); q.closePath(); }), '#c46c74', 0);
    ink(m, lw * 1.4);
    for (const sd of [-1, 1]) ink(path(q => { q.moveTo(sd * 0.26, 0.45); q.quadraticCurveTo(sd * 0.31, 0.5, sd * 0.27, 0.55); }), lw * 0.8);
  }
  x.restore();
  x.restore();
}

// hands. type: 'wave' | 'fist' | 'palm'
function hand(cx, cy, r, rot, type, skin) {
  x.save(); x.translate(cx, cy); x.rotate(rot); x.scale(r, r);
  const lw = Math.max(1.6, r * 0.03) / r;
  const sk = rgb(skin), skS = rgb(skin, 0.8);
  if (type === 'fist') {
    const f = path(q => q.roundRect(-0.55, -0.45, 1.1, 0.95, 0.3)); fillInk(f, sk, lw * 1.5);
    for (let k = 0; k < 4; k++) { const fy = -0.35 + k * 0.22; fillInk(path(q => q.roundRect(-0.62, fy, 0.42, 0.22, 0.1)), k % 2 ? skS : sk, lw); }
    fillInk(path(q => { q.moveTo(-0.2, -0.45); q.quadraticCurveTo(0.35, -0.6, 0.55, -0.2); q.lineTo(0.3, -0.1); q.quadraticCurveTo(0.1, -0.35, -0.2, -0.3); q.closePath(); }), sk, lw);
    halftone(f, 'rgba(80,40,30,0.3)', 0.06, 0.018, [0, -0.5, 0.6, 0.5]);
  } else {
    const spread = type === 'palm' ? 0.22 : 0.15;
    const palm = path(q => q.roundRect(-0.45, -0.3, 0.9, 0.85, 0.28)); fillInk(palm, sk, lw * 1.4);
    for (let k = 0; k < 4; k++) { x.save(); x.translate(-0.33 + k * 0.22, -0.28); x.rotate((k - 1.5) * spread); fillInk(path(q => q.roundRect(-0.09, -0.7 + Math.abs(k - 1.5) * 0.12, 0.18, 0.75 - Math.abs(k - 1.5) * 0.12, 0.09)), sk, lw * 1.2); x.restore(); }
    x.save(); x.translate(0.42, 0.15); x.rotate(0.9); fillInk(path(q => q.roundRect(-0.09, -0.5, 0.18, 0.55, 0.09)), sk, lw * 1.2); x.restore();
    if (type === 'palm') { x.fillStyle = 'rgba(255,240,230,0.55)'; x.beginPath(); x.ellipse(0, 0.12, 0.3, 0.32, 0, 0, Math.PI * 2); x.fill(); ink(path(q => { q.moveTo(-0.3, 0.05); q.quadraticCurveTo(0, 0.2, 0.32, 0.0); }), lw * 0.6); }
  }
  x.restore();
}

// ---------------------------------------------------------------- lettering
function wrapText(txt, maxW) { const words = txt.split(' '), lines = []; let cur = ''; for (const w of words) { const tr = cur ? cur + ' ' + w : w; if (x.measureText(tr).width > maxW && cur) { lines.push(cur); cur = w; } else cur = tr; } lines.push(cur); return lines; }
// style: 'normal' | 'infected' (wobbly edge, pink) | 'whisper' (dashed) | 'small'
function balloon(txt, cx, cy, tail, style, alpha = 1, maxW = 620) {
  x.save(); x.globalAlpha = alpha;
  const size = style === 'small' ? 40 : 46;
  x.font = `800 ${size}px Inter, sans-serif`; x.textAlign = 'center'; x.textBaseline = 'middle';
  const lines = wrapText(txt.toUpperCase(), maxW), lh = size * 1.18;
  const tw = Math.max(...lines.map(l => x.measureText(l).width)), th = lines.length * lh;
  const rx = tw / 2 + 60, ry = th / 2 + 42;
  const R = rng(Math.round(cx * 7 + cy));
  const b = new Path2D(), tl = new Path2D();
  const n = 48;
  for (let i = 0; i <= n; i++) { const a = i / n * Math.PI * 2; const wob = style === 'infected' ? 1 + (R() - 0.5) * 0.09 : 1; const px = cx + Math.cos(a) * rx * wob, py = cy + Math.sin(a) * ry * wob; i ? b.lineTo(px, py) : b.moveTo(px, py); }
  b.closePath();
  if (tail) { const a = Math.atan2(tail[1] - cy, tail[0] - cx), bx = cx + Math.cos(a) * rx * 0.8, by = cy + Math.sin(a) * ry * 0.8, pa = a + Math.PI / 2;
    const dd = Math.hypot(tail[0] - bx, tail[1] - by), maxT = 150 + Math.abs(Math.sin(a)) * 40; if (dd > maxT) tail = [bx + (tail[0] - bx) / dd * maxT, by + (tail[1] - by) / dd * maxT]; tl.moveTo(bx + Math.cos(pa) * 34, by + Math.sin(pa) * 34); tl.quadraticCurveTo((bx + tail[0]) / 2, (by + tail[1]) / 2, tail[0], tail[1]); tl.lineTo(bx - Math.cos(pa) * 34, by - Math.sin(pa) * 34); tl.closePath(); }
  // stroke both at double width, then fill both: the outline survives outside, the seam disappears inside
  x.lineWidth = 10; x.strokeStyle = INK; x.lineJoin = 'round'; if (style === 'whisper') x.setLineDash([22, 14]);
  x.stroke(b); if (tail) x.stroke(tl); x.setLineDash([]);
  x.fillStyle = style === 'infected' ? '#ffe9e6' : '#fffdf6'; x.fill(b); if (tail) x.fill(tl);
  x.fillStyle = style === 'infected' ? '#7a0a10' : INK;
  lines.forEach((l, i) => x.fillText(l, cx, cy - th / 2 + lh * (i + 0.5)));
  x.restore();
}
function captionBox(txt, x0, y0, alpha = 1, maxW = 820) {
  x.save(); x.globalAlpha = alpha;
  x.font = '800 44px Inter, sans-serif'; x.textAlign = 'left'; x.textBaseline = 'middle';
  const lines = wrapText(txt.toUpperCase(), maxW), lh = 54;
  const tw = Math.max(...lines.map(l => x.measureText(l).width));
  x.fillStyle = 'rgba(0,0,0,0.35)'; x.fillRect(x0 + 10, y0 + 10, tw + 56, lines.length * lh + 36);
  x.fillStyle = '#f4e6ad'; x.fillRect(x0, y0, tw + 56, lines.length * lh + 36);
  x.lineWidth = 5; x.strokeStyle = INK; x.strokeRect(x0, y0, tw + 56, lines.length * lh + 36);
  x.fillStyle = INK; lines.forEach((l, i) => x.fillText(l, x0 + 28, y0 + 18 + lh * (i + 0.5)));
  x.restore();
}
function sfx(txt, cx, cy, size, rot, fill, alpha = 1, scale = 1) {
  x.save(); x.globalAlpha = alpha; x.translate(cx, cy); x.rotate(rot); x.scale(scale, scale);
  x.font = `italic 900 ${size}px "Inter Display", Inter, sans-serif`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.lineJoin = 'round';
  x.lineWidth = size * 0.2; x.strokeStyle = INK; x.strokeText(txt, size * 0.06, size * 0.06); x.strokeText(txt, 0, 0);
  x.fillStyle = fill; x.fillText(txt, 0, 0);
  x.lineWidth = size * 0.035; x.strokeStyle = 'rgba(255,255,255,0.6)'; x.strokeText(txt, -size * 0.02, -size * 0.02);
  x.restore();
}
