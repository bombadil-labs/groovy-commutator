import { useEffect, useRef, useState } from 'react';
import Nav from './Nav.jsx';
import Watermark from './Watermark.jsx';
import Defn, { Op } from './Defn.jsx';
import RunSig from './RunSig.jsx';
import couplingData from '../data/critical_coupling.json';

// ---------------------------------------------------------------------------
// The Remainder -- a guided walk through one night of experiments, written
// for a reader arriving cold: every term is built before it is used.
// Every demo computes live from the engine; the statistics the prose quotes
// were established at scale by scripts/experiment_remainder_*.py,
// experiment_fourier.py, experiment_conservation_kinematics.py,
// experiment_critical_coupling.py and experiment_scale_rhyme.py, and the
// live widgets re-derive their local versions in front of the reader.
// ---------------------------------------------------------------------------

const ON = '#2a2420';
const CREAM = '#f1ead9';
const ACCENT = 'oklch(0.5 0.1 195)';
const AMBER = 'oklch(0.6 0.14 75)';
const RED = 'oklch(0.55 0.18 25)';
const INK_SOFT = '#6b6055';

const pBody = { fontSize: '1rem', color: 'var(--ink-soft)', margin: '0 0 1.15rem', maxWidth: '64ch', lineHeight: 1.7 };
const h2Style = { fontFamily: "'Lora',serif", fontSize: '1.45rem', margin: '0.2em 0 0.6em', fontWeight: 600 };
const kicker = { fontFamily: "'IBM Plex Mono',monospace", fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '.07em', color: 'var(--accent)' };
const capStyle = { fontFamily: "'IBM Plex Mono',monospace", fontSize: '0.68rem', color: INK_SOFT, marginTop: 4 };
const statStyle = { fontFamily: "'IBM Plex Mono',monospace", fontSize: '0.78rem', color: 'var(--ink)', background: 'var(--bg-alt)', border: '1px solid var(--rule)', borderRadius: 7, padding: '0.55rem 0.8rem', margin: '0.8rem 0 0', maxWidth: '64ch' };

// Established exhaustively by scripts/experiment_conservation_kinematics.py
// (n=12 AND n=13) and scripts/experiment_scale_rhyme.py (n=12, re-verified
// n=16) -- quoted here rather than recomputed, like the regime counts on the
// questions page.
const CONSERVERS = {
  live: [170, 184, 204, 226, 240],
  absential: [170, 171, 185, 204, 205, 227, 240, 241],
  activity: [15, 51, 85, 170, 204, 240],
};
const FIXED_POINTS = {
  affine: [60, 90, 102, 150, 153, 165, 195],
  shifts: [170, 204, 240],
  absorbing: [128, 136, 192, 238, 252, 254],
};

// ---- small numerics used by the demos ------------------------------------

function rollRow(row, k) {
  const n = row.length, out = new Uint8Array(n);
  for (let i = 0; i < n; i++) out[i] = row[(i - k + 2 * n) % n];
  return out;
}

function rowsEqual(a, b) {
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}

// Fit the best deterministic radius-r rule to the field's transitions on the
// first half; one-step-predict the second half from its own actual rows.
// Mirrors scripts/experiment_remainder_autonomy.py.
function fitAndTest(field, radius) {
  const steps = field.length, n = field[0].length;
  const width = 2 * radius + 1, buckets = 1 << width;
  const ctxRow = (row) => {
    const out = new Int32Array(n);
    for (let i = 0; i < n; i++) {
      let c = 0;
      for (let off = -radius; off <= radius; off++) c = (c << 1) | row[(i + off + n) % n];
      out[i] = c;
    }
    return out;
  };
  const half = Math.floor((steps - 1) / 2);
  const counts = new Int32Array(buckets * 2);
  for (let t = 0; t < half; t++) {
    const cx = ctxRow(field[t]);
    for (let i = 0; i < n; i++) counts[cx[i] * 2 + field[t + 1][i]]++;
  }
  const rule = new Uint8Array(buckets), seen = new Uint8Array(buckets);
  let contra = 0, total = 0;
  for (let c = 0; c < buckets; c++) {
    const z = counts[c * 2], o = counts[c * 2 + 1];
    rule[c] = o > z ? 1 : 0;
    seen[c] = z + o > 0 ? 1 : 0;
    contra += Math.min(z, o);
    total += z + o;
  }
  let ones = 0, cells = 0;
  for (let t = 0; t < half; t++) for (let i = 0; i < n; i++) { ones += field[t + 1][i]; cells++; }
  const majorityBit = ones * 2 > cells ? 1 : 0;
  const predField = [], errField = [];
  let correct = 0, tested = 0;
  for (let t = half; t < steps - 1; t++) {
    const cx = ctxRow(field[t]);
    const pred = new Uint8Array(n), err = new Uint8Array(n);
    for (let i = 0; i < n; i++) {
      pred[i] = seen[cx[i]] ? rule[cx[i]] : majorityBit;
      err[i] = pred[i] === field[t + 1][i] ? 0 : 1;
      if (!err[i]) correct++;
      tested++;
    }
    predField.push(pred);
    errField.push(err);
  }
  return {
    acc: correct / tested,
    contraMass: total ? contra / total : 0,
    nCtx: seen.reduce((a, b) => a + b, 0),
    buckets,
    predField,
    errField,
  };
}

// In-place iterative radix-2 FFT (length must be a power of two).
function fft(re, im) {
  const n = re.length;
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) { [re[i], re[j]] = [re[j], re[i]]; [im[i], im[j]] = [im[j], im[i]]; }
  }
  for (let len = 2; len <= n; len <<= 1) {
    const ang = -2 * Math.PI / len, wr = Math.cos(ang), wi = Math.sin(ang);
    for (let i = 0; i < n; i += len) {
      let cr = 1, ci = 0;
      for (let k = 0; k < len / 2; k++) {
        const a = i + k, b = i + k + len / 2;
        const vr = re[b] * cr - im[b] * ci, vi = re[b] * ci + im[b] * cr;
        re[b] = re[a] - vr; im[b] = im[a] - vi;
        re[a] += vr; im[a] += vi;
        const nr = cr * wr - ci * wi; ci = cr * wi + ci * wr; cr = nr;
      }
    }
  }
}

// 2D power spectrum of a (steps x n) binary field, both dims cropped to
// `size` (power of two).
function powerSpectrum(field, size) {
  const re = [], im = [];
  let mean = 0;
  for (let t = 0; t < size; t++) for (let i = 0; i < size; i++) mean += field[t][i];
  mean /= size * size;
  for (let t = 0; t < size; t++) {
    re.push(Float64Array.from({ length: size }, (_, i) => field[t][i] - mean));
    im.push(new Float64Array(size));
  }
  for (let t = 0; t < size; t++) fft(re[t], im[t]);
  const cr = new Float64Array(size), ci = new Float64Array(size);
  for (let i = 0; i < size; i++) {
    for (let t = 0; t < size; t++) { cr[t] = re[t][i]; ci[t] = im[t][i]; }
    fft(cr, ci);
    for (let t = 0; t < size; t++) { re[t][i] = cr[t]; im[t][i] = ci[t]; }
  }
  const P = new Float64Array(size * size);
  for (let t = 0; t < size; t++) for (let i = 0; i < size; i++) P[t * size + i] = re[t][i] ** 2 + im[t][i] ** 2;
  P[0] = 0;
  const sorted = Float64Array.from(P).sort().reverse();
  const k = Math.max(1, Math.floor(sorted.length * 0.01));
  let top = 0, tot = 0;
  for (let i = 0; i < sorted.length; i++) { tot += sorted[i]; if (i < k) top += sorted[i]; }
  return { power: P, concentration: tot > 0 ? top / tot : 1 };
}

function drawSpectrum(canvas, P, size) {
  canvas.width = size; canvas.height = size;
  const ctx = canvas.getContext('2d');
  const img = ctx.createImageData(size, size);
  let mx = 0;
  const L = new Float64Array(size * size);
  for (let i = 0; i < P.length; i++) { L[i] = Math.log1p(P[i]); if (L[i] > mx) mx = L[i]; }
  // fftshift so "no stripes at all" sits at the center of the picture
  for (let t = 0; t < size; t++) {
    for (let i = 0; i < size; i++) {
      const st = (t + size / 2) % size, si = (i + size / 2) % size;
      const v = mx > 0 ? L[st * size + si] / mx : 0;
      const o = (t * size + i) * 4;
      img.data[o] = Math.round(241 + (42 - 241) * v);
      img.data[o + 1] = Math.round(234 + (96 - 234) * (v < 0.5 ? v * 2 * 0.65 : 0.65 + (v - 0.5) * 2 * 0.35));
      img.data[o + 2] = Math.round(217 + (60 - 217) * v);
      img.data[o + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
}

// ---- shared helpers ---------------------------------------------------------

function useEngine() {
  const ref = useRef(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    let cancel = false;
    import('../lib/groovy-engine.js').then((e) => { if (!cancel) { ref.current = e; setReady(true); } });
    return () => { cancel = true; };
  }, []);
  return [ref, ready];
}

function divergence(engine, a, b, n, steps, burn, seed) {
  const F = engine.divergenceTrajectory(engine.randomState(n, seed), a, b, steps + burn);
  return F.slice(burn);
}

// ---- Stop 0: a single rule running -----------------------------------------

function SoloRun() {
  const [engineRef, ready] = useEngine();
  const ref = useRef(null);
  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const T = e.evolveTrajectory(e.randomState(160, 2), 110, 160);
    if (ref.current) e.renderFieldToCanvas(ref.current, T, ON, CREAM);
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div style={{ width: 190, margin: '0.4rem 0 0.8rem' }}>
      <canvas className="gc-field" ref={ref} style={{ width: 190, height: 190 }}></canvas>
      <div style={capStyle}>one rule, one history — the top row is the start; each row below it is one tick later</div>
      <div style={{ marginTop: 5 }}><RunSig sig={{ gauge: 'id', base: 'E_110' }} /></div>
    </div>
  );
}

// ---- Stop 1: how the disagreement picture is made ---------------------------

function TwoClocks() {
  const [engineRef, ready] = useEngine();
  const refs = [useRef(null), useRef(null), useRef(null)];
  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const n = 160, steps = 160, a = 110, b = 54;
    let p1 = e.randomState(n, 5), p2 = p1.slice();
    const F1 = [], F2 = [], D = [];
    for (let t = 0; t < steps; t++) {
      F1.push(p1); F2.push(p2); D.push(e.C(p1, p2));
      p1 = e.applyRule(e.applyRule(p1, a), b);
      p2 = e.applyRule(e.applyRule(p2, b), a);
    }
    if (refs[0].current) e.renderFieldToCanvas(refs[0].current, F1, ON, CREAM);
    if (refs[1].current) e.renderFieldToCanvas(refs[1].current, F2, ON, CREAM);
    if (refs[2].current) e.renderFieldToCanvas(refs[2].current, D, AMBER, CREAM);
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  const caps = ['history 1: rule A then rule B, every tick', 'history 2: rule B then rule A, every tick', 'the remainder: every square where they differ'];
  const sigs = [{ engine: '54∘110' }, { engine: '110∘54' }, { text: 'engine(54∘110) ⊕ engine(110∘54)' }];
  return (
    <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap', margin: '0.4rem 0 0.8rem' }}>
      {refs.map((r, i) => (
        <div key={i} style={{ width: 170 }}>
          <canvas className="gc-field" ref={r} style={{ width: 170, height: 170 }}></canvas>
          <div style={capStyle}>{caps[i]}</div>
          <div style={{ marginTop: 5 }}><RunSig sig={sigs[i]} /></div>
        </div>
      ))}
    </div>
  );
}

function Triptych() {
  const [engineRef, ready] = useEngine();
  const refs = [useRef(null), useRef(null), useRef(null)];
  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const specs = [[90, 150, 'var(--commute)'], [110, 54, 'oklch(0.55 0.14 75)'], [110, 30, 'oklch(0.55 0.12 300)']];
    specs.forEach(([a, b, color], i) => {
      const F = divergence(e, a, b, 160, 160, 20, 5);
      if (refs[i].current) e.renderFieldToCanvas(refs[i].current, F, color, CREAM);
    });
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  const labels = ['rules 90 & 150 — the histories never differ: blank', 'rules 110 & 54 — they differ, and the difference has a pattern', 'rules 110 & 30 — they differ like static'];
  const sigs = [
    { text: 'engine(150∘90) ⊕ engine(90∘150)' },
    { text: 'engine(54∘110) ⊕ engine(110∘54)' },
    { text: 'engine(30∘110) ⊕ engine(110∘30)' },
  ];
  return (
    <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap', margin: '0.4rem 0 0.8rem' }}>
      {refs.map((r, i) => (
        <div key={i} style={{ width: 170 }}>
          <canvas className="gc-field" ref={r} style={{ width: 170, height: 170 }}></canvas>
          <div style={capStyle}>{labels[i]}</div>
          <div style={{ marginTop: 5 }}><RunSig sig={sigs[i]} /></div>
        </div>
      ))}
    </div>
  );
}

// ---- Stop 2: the autonomy experiment ---------------------------------------

const AUTONOMY_PAIRS = [
  { a: 110, b: 54, label: '110 & 54 (patterned)' },
  { a: 110, b: 30, label: '110 & 30 (static)' },
  { a: 32, b: 71, label: '32 & 71 (patterned, exact)' },
];

function AutonomyDemo() {
  const [engineRef, ready] = useEngine();
  const [pairIdx, setPairIdx] = useState(0);
  const [stats, setStats] = useState(null);
  const fieldRef = useRef(null);
  const predRef = useRef(null);
  const errRef = useRef(null);

  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const { a, b } = AUTONOMY_PAIRS[pairIdx];
    const F = divergence(e, a, b, 200, 360, 40, 9);
    const res = fitAndTest(F, 2);
    if (fieldRef.current) e.renderFieldToCanvas(fieldRef.current, F, ACCENT, CREAM);
    if (predRef.current) e.renderFieldToCanvas(predRef.current, res.predField, ON, CREAM);
    if (errRef.current) e.renderFieldToCanvas(errRef.current, res.errField, RED, CREAM);
    setStats({ acc: res.acc, contra: res.contraMass, nCtx: res.nCtx, buckets: res.buckets });
  }, [ready, pairIdx]);   // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', margin: '0 0 0.9rem' }}>
        {AUTONOMY_PAIRS.map((p, i) => (
          <button key={p.label} onClick={() => setPairIdx(i)} className="gc-mono"
            style={{ fontSize: '0.76rem', fontWeight: 700, padding: '0.4rem 0.8rem', borderRadius: 7, cursor: 'pointer', border: '1px solid var(--accent)', background: i === pairIdx ? 'var(--accent)' : '#fff', color: i === pairIdx ? '#fff' : 'var(--accent)' }}>
            {p.label}
          </button>
        ))}
      </div>
      <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap' }}>
        {[[fieldRef, 'the remainder, whole run', true], [predRef, 'what the learned rulebook predicts, for the half it was never shown'], [errRef, 'every square the rulebook got wrong (red)']].map(([r, cap, badge]) => (
          <div key={cap} style={{ width: 190 }}>
            <canvas className="gc-field" ref={r} style={{ width: 190, height: 190 }}></canvas>
            <div style={capStyle}>{cap}</div>
            {badge && <div style={{ marginTop: 5 }}><RunSig sig={{ text: `engine(${AUTONOMY_PAIRS[pairIdx].b}∘${AUTONOMY_PAIRS[pairIdx].a}) ⊕ engine(${AUTONOMY_PAIRS[pairIdx].a}∘${AUTONOMY_PAIRS[pairIdx].b})` }} /></div>}
          </div>
        ))}
      </div>
      {stats && (
        <div style={statStyle}>
          score on the unseen half <strong>{(stats.acc * 100).toFixed(2)}%</strong>
          {' '}&middot; self-contradictions while learning <strong>{(stats.contra * 100).toFixed(2)}%</strong>
          {' '}&middot; distinct five-cell patterns witnessed <strong>{stats.nCtx}/{stats.buckets}</strong>
        </div>
      )}
    </div>
  );
}

// ---- Stop 3: the soliton ----------------------------------------------------

function SolitonDemo() {
  const [engineRef, ready] = useEngine();
  const [verdict, setVerdict] = useState('checking, live…');
  const ref = useRef(null);
  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const F = divergence(e, 138, 205, 180, 300, 50, 3);
    if (ref.current) e.renderFieldToCanvas(ref.current, F, AMBER, CREAM);
    for (const k of [1, -1]) {
      let all = true;
      for (let t = 0; t < F.length - 1; t++) {
        if (!rowsEqual(F[t + 1], rollRow(F[t], k))) { all = false; break; }
      }
      if (all) {
        setVerdict(`Checked in your browser just now: on every one of this run's ${F.length - 1} ticks, the next row of the remainder is exactly the previous row slid one square to the ${k > 0 ? 'right' : 'left'}. No exceptions.`);
        return;
      }
    }
    setVerdict('This particular starting row did not settle into a pure slide (some starts don’t — reload to reroll).');
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div style={{ display: 'flex', gap: '1.1rem', flexWrap: 'wrap', alignItems: 'flex-start' }}>
      <div style={{ width: 190 }}>
        <canvas className="gc-field" ref={ref} style={{ width: 190, height: 190 }}></canvas>
        <div style={capStyle}>the remainder of rules 138 & 205 — stripes drifting sideways forever</div>
        <div style={{ marginTop: 5 }}><RunSig sig={{ text: 'engine(205∘138) ⊕ engine(138∘205)' }} /></div>
      </div>
      <p style={{ ...pBody, maxWidth: '38ch', fontSize: '0.9rem' }}>{verdict}</p>
    </div>
  );
}

// ---- Stop 4: spectra + rhyme -------------------------------------------------

function SpectrumDemo() {
  const [engineRef, ready] = useEngine();
  const [conc, setConc] = useState(null);
  const s1 = useRef(null), s2 = useRef(null);
  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const SIZE = 256;
    const Fs = divergence(e, 110, 54, SIZE, SIZE, 40, 5);
    const Fn = divergence(e, 110, 30, SIZE, SIZE, 40, 5);
    const ps = powerSpectrum(Fs, SIZE);
    const pn = powerSpectrum(Fn, SIZE);
    if (s1.current) drawSpectrum(s1.current, ps.power, SIZE);
    if (s2.current) drawSpectrum(s2.current, pn.power, SIZE);
    setConc([ps.concentration, pn.concentration]);
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap' }}>
      {[[s1, 'the patterned remainder (110 & 54): its energy lies on a few sharp lines', 0], [s2, 'the static remainder (110 & 30): its energy is everywhere at once', 1]].map(([r, cap, i]) => (
        <div key={cap} style={{ width: 210 }}>
          <canvas ref={r} style={{ width: 210, height: 210, imageRendering: 'pixelated', border: '1px solid var(--rule)', borderRadius: 6, display: 'block' }}></canvas>
          <div style={capStyle}>{cap}{conc && <> &middot; share held by the brightest 1%: <strong>{(conc[i] * 100).toFixed(0)}%</strong></>}</div>
        </div>
      ))}
    </div>
  );
}

function RhymeDemo() {
  const [engineRef, ready] = useEngine();
  const [found, setFound] = useState(null);
  const rawRef = useRef(null), resRef = useRef(null);
  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const n = 256, steps = 300, burn = 64;
    const T = e.evolveTrajectory(e.randomState(n, 12), 110, steps + burn).slice(burn);
    if (rawRef.current) e.renderFieldToCanvas(rawRef.current, T, ON, CREAM);
    let best = { k: 0, s: 0, d: 1 };
    for (let k = 1; k <= 12; k++) {
      for (let s = 0; s < n; s++) {
        let diff = 0, cells = 0;
        for (let t = k; t < T.length; t += 4) {
          const rowB = T[t - k];
          for (let i = 0; i < n; i++) { diff += T[t][i] ^ rowB[(i - s + n) % n]; cells++; }
        }
        const d = diff / cells;
        if (d < best.d) best = { k, s, d };
      }
    }
    const resid = [];
    for (let t = best.k; t < T.length; t++) resid.push(Uint8Array.from({ length: n }, (_, i) => T[t][i] ^ T[t - best.k][(i - best.s + n) % n]));
    if (resRef.current) e.renderFieldToCanvas(resRef.current, resid, RED, CREAM);
    setFound({ ...best, rawDensity: T.reduce((a, row) => a + row.reduce((x, y) => x + y, 0), 0) / (T.length * n) });
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div>
      <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap' }}>
        {[[rawRef, 'rule 110, raw — wallpaper almost everywhere'], [resRef, 'the same run with its best-matching past subtracted — the wallpaper cancels; only the travelers survive']].map(([r, cap]) => (
          <div key={cap} style={{ width: 210 }}>
            <canvas className="gc-field" ref={r} style={{ width: 210, height: 210 }}></canvas>
            <div style={capStyle}>{cap}</div>
          </div>
        ))}
      </div>
      {found && (
        <div style={statStyle}>
          best echo found by blind search: <strong>{found.k}</strong> ticks back,{' '}
          <strong>{found.s <= 128 ? found.s : found.s - 256}</strong> squares over
          {' '}&middot; disagreement after subtracting it: <strong>{found.d.toFixed(3)}</strong> (before: {found.rawDensity.toFixed(3)})
        </div>
      )}
    </div>
  );
}

// ---- Stop 5: conservation ----------------------------------------------------

function SilhouetteDemo() {
  const [engineRef, ready] = useEngine();
  const [nums, setNums] = useState(null);
  const ref = useRef(null);
  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const n = 200, steps = 120;
    const rng = e.mulberry32(21);
    let s = Uint8Array.from({ length: n }, () => (rng() < 0.22 ? 1 : 0));
    const live = [], closed = [], rows = [];
    for (let t = 0; t < steps; t++) {
      const A = e.absentialField(s);
      rows.push({ s: s.slice(), a: A });
      live.push(s.reduce((x, y) => x + y, 0));
      closed.push(s.reduce((x, y) => x + y, 0) + A.reduce((x, y) => x + y, 0));
      s = e.applyRule(s, 236);
    }
    const canvas = ref.current;
    if (canvas) {
      canvas.width = n; canvas.height = steps;
      const ctx = canvas.getContext('2d');
      const img = ctx.createImageData(n, steps);
      for (let t = 0; t < steps; t++) {
        for (let i = 0; i < n; i++) {
          const o = (t * n + i) * 4;
          let r = 241, g = 234, b = 217;
          if (rows[t].s[i]) { r = 42; g = 36; b = 32; }
          else if (rows[t].a[i]) { r = 209; g = 154; b = 60; }
          img.data[o] = r; img.data[o + 1] = g; img.data[o + 2] = b; img.data[o + 3] = 255;
        }
      }
      ctx.putImageData(img, 0, 0);
    }
    setNums({ live0: live[0], live1: live[steps - 1], closed0: closed[0], closed1: closed[steps - 1] });
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div style={{ display: 'flex', gap: '1.1rem', flexWrap: 'wrap', alignItems: 'flex-start' }}>
      <div style={{ width: 220 }}>
        <canvas ref={ref} style={{ width: 220, height: 132, imageRendering: 'pixelated', border: '1px solid var(--rule)', borderRadius: 6, display: 'block', background: CREAM }}></canvas>
        <div style={capStyle}>rule 236 — on cells (ink) grow into their halo (amber), but the outline never moves</div>
      </div>
      {nums && (
        <div style={{ ...statStyle, margin: 0 }}>
          on cells: <strong>{nums.live0} &rarr; {nums.live1}</strong> (grows)<br />
          outline, i.e. on + halo: <strong>{nums.closed0} &rarr; {nums.closed1}</strong> (never changes)
        </div>
      )}
    </div>
  );
}

// ---- Stop 6: the coupling knob -------------------------------------------------

function CouplingChart() {
  const curves = couplingData.curves['77,55|44,23'];
  const W = 520, H = 220, padL = 40, padR = 14, padT = 12, padB = 34;
  const w = W - padL - padR, h = H - padT - padB;
  const x = (a) => padL + a * w;
  const y = (c) => padT + (1 - Math.min(c, 1.05) / 1.05) * h;
  const path = (m) => curves[m].alpha.map((a, i) => `${i ? 'L' : 'M'}${x(a).toFixed(1)},${y(curves[m].comp[i]).toFixed(1)}`).join('');
  return (
    <>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 'auto', maxWidth: 520, display: 'block' }}>
        <line x1={padL} y1={padT} x2={padL} y2={padT + h} stroke="#e4dac8" />
        <line x1={padL} y1={padT + h} x2={padL + w} y2={padT + h} stroke="#e4dac8" />
        {[0, 0.5, 1].map((v) => (
          <text key={v} x={x(v)} y={H - 16} textAnchor={v === 0 ? 'start' : 'middle'} fontFamily="IBM Plex Mono, monospace" fontSize="10" fill={INK_SOFT}>{v}</text>
        ))}
        {[0, 0.5, 1].map((v) => (
          <text key={'y' + v} x={padL - 6} y={y(v) + 3} textAnchor="end" fontFamily="IBM Plex Mono, monospace" fontSize="10" fill={INK_SOFT}>{v}</text>
        ))}
        <text x={padL + w / 2} y={H - 2} textAnchor="middle" fontFamily="IBM Plex Mono, monospace" fontSize="10" fill={INK_SOFT}>fraction of cells whose listening line is connected</text>
        <path d={path('quenched')} fill="none" stroke="var(--accent)" strokeWidth="2.2" />
        <path d={path('annealed')} fill="none" stroke={RED} strokeWidth="2.2" />
        <circle cx={x(1)} cy={y(curves.annealed.comp[curves.annealed.comp.length - 1])} r="5" fill="none" stroke={RED} strokeWidth="2" />
        <text x={x(0.62)} y={y(0.15)} fontFamily="IBM Plex Mono, monospace" fontSize="10" fill="var(--accent)">some cells permanently deaf</text>
        <text x={x(0.26)} y={y(0.9)} fontFamily="IBM Plex Mono, monospace" fontSize="10" fill={RED}>every cell's line flickering</text>
      </svg>
      <p className="gc-mono" style={{ fontSize: '0.7rem', color: INK_SOFT, margin: '0.3rem 0 0' }}>
        vertical axis: how noise-like the result is (0 = frozen, ~0.45 = patterned, 1 = pure static) &middot; circled: order returning all at once at exactly 1
      </p>
    </>
  );
}

function CouplingTriptych() {
  const [engineRef, ready] = useEngine();
  const refs = [useRef(null), useRef(null), useRef(null)];
  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const n = 100, steps = 100;
    const ta = e.rule4FromPair(77, 55), tb = e.rule4FromPair(44, 23);
    const run = (alpha, mode, seed) => {
      const rng = e.mulberry32(seed);
      let A = e.randomState(n, seed), B = e.randomState(n, seed + 31);
      let mask = Uint8Array.from({ length: n }, () => (rng() < alpha ? 1 : 0));
      const out = [];
      for (let t = 0; t < steps; t++) {
        out.push(A);
        if (mode === 'annealed') mask = Uint8Array.from({ length: n }, () => (rng() < alpha ? 1 : 0));
        const xa = Uint8Array.from({ length: n }, (_, i) => B[i] & mask[i]);
        const nA = e.applyRule4(A, xa, ta);
        B = e.applyRule4(B, A, tb);
        A = nA;
      }
      return out;
    };
    const specs = [[0.6, 'quenched', 41], [0.85, 'annealed', 41], [1.0, 'quenched', 41]];
    specs.forEach(([alpha, mode, seed], i) => {
      const F = run(alpha, mode, seed);
      if (refs[i].current) e.renderFieldToCanvas(refs[i].current, F, ON, CREAM);
    });
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  const caps = ['60% of lines connected, permanently — dented but coherent', '85% connected but flickering — the flicker itself becomes static', '100%, steady — the pattern returns'];
  const notes = ['60% wired, fixed', '85% wired, flickering', '100% wired'];
  return (
    <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap', margin: '1rem 0 0' }}>
      {refs.map((r, i) => (
        <div key={i} style={{ width: 170 }}>
          <canvas className="gc-field" ref={r} style={{ width: 170, height: 170 }}></canvas>
          <div style={capStyle}>{caps[i]}</div>
          <div style={{ marginTop: 5 }}><RunSig sig={{ engine: 'A⇄B', note: notes[i] }} /></div>
        </div>
      ))}
    </div>
  );
}

// ---- Stop 7: scale rhyme --------------------------------------------------------

function ScaleDemo() {
  const [engineRef, ready] = useEngine();
  const fineRef = useRef(null), coarseRef = useRef(null);
  useEffect(() => {
    if (!ready) return;
    const e = engineRef.current;
    const n = 256, steps = 256;
    const s0 = new Uint8Array(n); s0[n >> 1] = 1;
    const T = e.evolveTrajectory(s0, 90, steps);
    if (fineRef.current) e.renderFieldToCanvas(fineRef.current, T, ON, CREAM);
    // decimation: keep every other cell of every other row (one of the three
    // verified self-maps of rule 90 in results/scale_rhyme.csv). Rendered at
    // the same display size, the half-resolution copy is the same picture.
    const coarse = [];
    for (let t = 0; t < steps; t += 2) {
      coarse.push(Uint8Array.from({ length: n / 2 }, (_, i) => T[t][2 * i]));
    }
    if (coarseRef.current) e.renderFieldToCanvas(coarseRef.current, coarse, ON, CREAM);
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap' }}>
      {[[fineRef, 'rule 90, full resolution'], [coarseRef, 'the same run, keeping only every other cell and every other tick']].map(([r, cap]) => (
        <div key={cap} style={{ width: 210 }}>
          <canvas className="gc-field" ref={r} style={{ width: 210, height: 210 }}></canvas>
          <div style={capStyle}>{cap}</div>
        </div>
      ))}
    </div>
  );
}

// ---- the page --------------------------------------------------------------------

function RuleList({ rules }) {
  return <span className="gc-code">{rules.join(', ')}</span>;
}

export default function Remainder() {
  return (
    <>
      <Nav active="remainder" />
      <Watermark title="AI-written prose, live-computed demos">
        {' '}The writing on this page was generated by an LLM, narrating one night of its own experiments. Every
        visual below is computed live in your browser by the real engine; the quoted statistics come from the
        checked-in scripts (<code className="gc-code">scripts/experiment_remainder_*.py</code> and friends) and{' '}
        <code className="gc-code">NOTES.md</code> &sect;9.
      </Watermark>

      <main style={{ maxWidth: 880, margin: '0 auto', padding: '2rem 1.25rem 4rem' }}>
        <div style={kicker}>the walk</div>
        <h1 style={{ fontFamily: "'Lora',serif", fontSize: 'clamp(1.8rem,5vw,2.4rem)', lineHeight: 1.25, margin: '0 0 0.4em', fontWeight: 600 }}>
          The night the remainder became a thing
        </h1>
        <p style={{ fontSize: '1.05rem', color: 'var(--ink-soft)', margin: '0 0 2.2rem', maxWidth: '64ch', lineHeight: 1.7 }}>
          This is the story of one long night of experiments, told from the beginning &mdash; you don't need to
          have read anything else on this site. It ends at a question we had been trying to ask for months without
          managing to say it: <em>when does the relationship between two processes become a thing in its own
          right &mdash; with its own law?</em> If you <em>have</em> read the{' '}
          <a href="concepts.html" style={{ color: 'var(--accent)' }}>Concepts page</a>, its vocabulary &mdash;
          runs, engines, the walker and the watcher &mdash; will name everything here as we go. Every picture on
          this page is computed in your browser as you read it. Nothing is a stock illustration.
        </p>

        {/* STOP 0 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 0</div>
          <h2 style={h2Style}>The whole universe in one paragraph</h2>
          <p style={pBody}>
            Picture a row of about two hundred squares, each either on (ink) or off (cream). Time moves in ticks.
            At every tick, each square looks at exactly three things &mdash; itself and its immediate left and
            right neighbors &mdash; and consults a fixed table that says what to become next. All squares update
            at once, every tick, forever. That table is called a <strong>rule</strong>, and because three squares
            can only be on/off in 8 combinations, a rule is just 8 yes/no answers &mdash; which means there are
            exactly 256 possible rules, numbered 0 to 255. To see a rule's whole personality at once, we draw
            time downward: the first row is the starting condition, and each row below it is one tick later.
          </p>
          <SoloRun />
          <p style={pBody}>
            That's everything. No physics, no randomness after the first row, no hidden machinery &mdash; just a
            row of squares repeatedly consulting an 8-line table. (If you want to compute one of these by hand,
            square by square, the <a href="concepts.html" style={{ color: 'var(--accent)' }}>Concepts page</a>{' '}
            walks through it slowly. In its vocabulary, the badge under the picture already says all of this:
            rule 110 walks, the do-nothing map <Op>id</Op> watches.) The astonishment of the field is that some
            of these 256 tables produce pictures like the one above &mdash; churning, particle-crossed, never
            settling &mdash; from six lines of arithmetic.
          </p>
        </section>

        {/* STOP 1 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 1</div>
          <h2 style={h2Style}>Two histories, one question</h2>
          <p style={pBody}>
            Now take <em>two</em> rules, A and B, and one shared starting row. Make two copies of that row and let
            each copy live out its own history. Both histories use both rules &mdash; on every tick, each copy
            applies one rule and then the other. The <em>only</em> difference between them is the order inside the
            tick: copy 1 always does A-then-B, copy 2 always does B-then-A. Same ingredients, same starting point,
            different order of operations. Does the order matter?
          </p>
          <p style={pBody}>
            To find out, compare the two histories square by square, moment by moment, and mark every square where
            they disagree. Those marks form a picture of their own &mdash; the same shape as the two histories,
            showing only the difference between them:
          </p>
          <TwoClocks />
          <p style={pBody}>
            We call that third picture the <strong>remainder</strong>: what's left over when you subtract one
            history from the other. It is the portrait of a <em>relationship</em> &mdash; not of either process,
            but of how they fail to be interchangeable. In the calculus the{' '}
            <a href="concepts.html#engines" style={{ color: 'var(--accent)' }}>Concepts page</a> builds, this has
            a compact spelling:
          </p>
          <Defn lines={[
            { parts: [{ t: 'engine' }, { t: '(B∘A)' }], note: 'history 1: A-then-B, fed its own output forever' },
            { parts: [{ t: 'engine' }, { t: '(A∘B)' }], note: 'history 2: same maps, other order' },
            { parts: [
                { t: 'remainder', k: 'remainder' },
                { t: '(A, B) = ' },
                { t: 'engine' },
                { t: '(B∘A) ⊕ ' },
                { t: 'engine' },
                { t: '(A∘B)' },
              ], note: 'their disagreement, cell by cell' },
          ]} />
          <p style={pBody}>
            Each history is an <Op>engine</Op> &mdash; a map walking on its own output &mdash; and the remainder
            is the XOR of two engine runs. That spelling is why this page exists: a <Op>gauge</Op>'s pictures add
            up (the XOR of two gauges over one walk is just another gauge over that walk), but engines make no
            such promise. Nothing guarantees the XOR of two engines is anything at all. Run this comparison for
            many different pairs of rules and three kinds of remainder keep appearing:
          </p>
          <Triptych />
          <p style={pBody}>
            Blank means the order never mattered. Static means the two histories disagree everywhere, patternlessly
            &mdash; the relationship has no shape. But the middle case is the strange one: the two histories
            disagree <em>in an organized way</em>, indefinitely. The disagreement ripples. It persists. It looks,
            frankly, like it's up to something.
          </p>
        </section>

        {/* STOP 2 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 2</div>
          <h2 style={h2Style}>Interrogating a shadow</h2>
          <p style={pBody}>
            Here's why that should be impossible to take seriously. The remainder is not a simulation. Nothing
            computes it. Each of its squares just answers a bookkeeping question &mdash; &ldquo;do the two real
            histories disagree here?&rdquo; &mdash; the way a shadow on a wall just reports where an object blocks
            the light. A shadow can move, stretch, and dance, but nothing about the shadow <em>causes</em> its next
            shape; the object does. Here, the two real histories are the object. The remainder is their shadow. It
            has no machinery of its own. It <em>can't</em> have a law of its own.
          </p>
          <p style={pBody}>
            So we tested exactly that, with an experiment simple enough to state in one breath. Cover up the two
            real histories entirely; look only at the remainder. For the first half of its run, keep a tally: every time
            some five-square stretch of it (a square plus two neighbors on each side) shows a particular on/off
            pattern, write down what the middle square did on the next tick. That tally is a <strong>rulebook
            written purely by watching the shadow</strong>. Then take the second half &mdash; which
            the rulebook has never seen &mdash; and make it predict, square by square, tick by tick. Grade it
            against what actually happened.
          </p>
          <AutonomyDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            Click between the pairs and watch the red panel. For the static pair (110 &amp; 30), the shadow-rulebook
            fails on roughly a third of all squares &mdash; and here's the damning detail from the full study:
            giving it a wider window barely helps, because what it's missing isn't <em>nearby</em>, it's{' '}
            <em>off-stage</em>, locked in the two covered-up histories. That remainder really is just a shadow.
            But for the patterned pair the errors nearly vanish &mdash; and for the pair 32 &amp; 71 they vanish{' '}
            <em>completely</em>: a perfect score on every tick of a future it was never shown, with zero
            self-contradictions while learning. At scale (200 sampled pairs,{' '}
            <span className="gc-code">experiment_remainder_autonomy.py</span>), the typical patterned remainder
            scores a perfect 1.000 &mdash; while actively using nearly every five-square pattern it could express,
            so this is not a frozen picture coasting on repetition.
          </p>
          <p style={pBody}>
            Stop and feel how strange that is. The question we had been circling all year turns out to be askable
            in one sentence: <strong>under what conditions does a mere <em>view</em> of a system follow its own
            rule &mdash; and can we recover that rule by watching?</strong> And the answer is: it depends on the
            relationship. When two processes disagree like static, their disagreement stays a shadow &mdash; no law
            to recover. When they disagree in an organized way, the disagreement <em>keeps its own law</em>, and
            you can learn that law without ever seeing the processes underneath. (One honest fine-print line: the
            recovered law is exact for every situation the remainder actually gets into &mdash; we can't promise it
            for situations this particular run never visits.)
          </p>
          <p style={pBody}>
            In the calculus, the whole stop compresses to one line: <strong>when is the XOR of two{' '}
            <Op>engine</Op> runs itself an engine run?</strong> The static remainder is the default answer &mdash;
            a shadow, its next row not a function of its current one, because the missing information lives in the
            two covered-up walkers. The patterned remainder is the exception: the shadow closes up and walks on
            its own output, like any other engine.
          </p>
        </section>

        {/* STOP 3 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 3</div>
          <h2 style={h2Style}>Some remainders are travelers</h2>
          <p style={pBody}>
            Then it got weirder. For dozens of rule pairs, the recovered law came out so simple it fit in the same
            8-line format as the original 256 rules &mdash; the shadow's law is itself <em>one of the rules of
            this universe</em>. Formally: the remainder isn't just <em>an</em> engine, it's{' '}
            <Op>engine</Op>(E<sub>170</sub>) or <Op>engine</Op>(E<sub>240</sub>) &mdash; the two &ldquo;slide
            everything one square over&rdquo; rules. In other words: these remainders are
            patterns of disagreement that never change shape at all. They only drift. Physicists have a word for a
            wave that travels without changing shape &mdash; a <em>soliton</em>.
          </p>
          <SolitonDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            We had a beautiful explanation ready, and it deserves a public funeral. The hope: maybe for these pairs,
            doing A-then-B literally equals doing B-then-A and then sliding the whole row one square &mdash; order
            mattering only as a change of viewpoint, like two people describing the same parade from opposite
            curbs. Elegant, algebraic &mdash; and false. We checked it against every possible configuration at
            small sizes: it holds for none of the 34 pairs. The true reason is humbler: each of the two histories,
            run long enough, settles into a repeating pattern that <em>travels</em> &mdash; and two travelers
            moving at the same speed disagree in a pattern that travels with them. The wave isn't in the algebra.
            It's in where the dynamics comes to rest.
          </p>
        </section>

        {/* STOP 4 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 4</div>
          <h2 style={h2Style}>Looking with waves</h2>
          <p style={pBody}>
            If remainders drift, there's a classic instrument for seeing it: the Fourier transform. Don't let the
            name intimidate; the idea is a change of question. Instead of asking &ldquo;which squares are
            on?&rdquo;, ask &ldquo;how much of this picture is made of <em>stripes</em> &mdash; for every possible
            stripe spacing and every possible stripe speed?&rdquo; and lay the answers out as a new picture. A
            pattern gliding at a steady speed answers &ldquo;a lot&rdquo; only along one straight line of that
            picture (and the line's slope <em>is</em> the speed). Pure static answers &ldquo;a little&rdquo;
            everywhere at once.
          </p>
          <SpectrumDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            The patterned remainder's energy collapses onto a few sharp lines &mdash; in the full study, the
            typical patterned pair packs <strong>97%</strong> of its energy into 1% of the picture, while static
            pairs manage 9%. And for the traveler pairs of stop 3, the line's slope reads exactly one square per
            tick, in the direction their recovered rule said. Two completely different instruments &mdash;
            rulebook-learning and stripe-counting &mdash; agreeing about what the shadow is doing.
          </p>
          <p style={pBody}>
            The same trick, turned inward, answers an old itch of ours about d&eacute;j&agrave; vu. Take a single
            rule's history and slide a copy of it back in time and sideways in space, every possible amount, asking
            each time: how well does the past line up with the present? Rule 110 &mdash; the most famous of the 256
            &mdash; fills its world with a repeating background texture (aficionados call it the <em>ether</em>)
            crossed by particle-like travelers (<em>gliders</em>). We told the search nothing about any of that:
          </p>
          <RhymeDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            The blind search finds the exact slide at which the wallpaper repeats &mdash; and subtracting that echo
            cancels the wallpaper and hands back <em>only the gliders</em>, the parts that break the pattern. (Rule
            30, our control, has no repeating background: its best echo still leaves ~37% disagreement. Nothing
            cancels because nothing repeats.) The sentence we kept from this stop: <strong>structure is having
            somewhere to rhyme to.</strong>
          </p>
        </section>

        {/* STOP 5 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 5</div>
          <h2 style={h2Style}>Weighing everything</h2>
          <p style={pBody}>
            A night this strange deserves bookkeeping, so we did some accounting on all 256 rules. For each one we
            asked: as the picture evolves, what stays <em>exactly</em> constant, for every possible starting row?
            The count of on-squares? The count of <strong>halo</strong> squares (off, but right next to an on
            square &mdash; the one-square-thick fringe around every pattern; the Concepts page calls this field{' '}
            <Op>A</Op>, the absential field)? The count of squares that change per tick? This is checked by brute force over every configuration, so the answers are theorems, not
            observations. Three jewels came back:
          </p>
          <ul style={{ ...pBody, paddingLeft: '1.2em' }}>
            <li style={{ marginBottom: '0.5em' }}>
              Exactly five rules never change their on-count: <RuleList rules={CONSERVERS.live} /> (a known
              classic, and our sanity check). But the rules that never change their <em>halo</em> count are{' '}
              <RuleList rules={CONSERVERS.absential} /> &mdash; and the pattern in that list is exact: it's the
              conservers again, each optionally modified in a single table line (the one that decides whether an
              empty, isolated square turns on). Rule 184 preserves its mass but not its halo; its one-line-different
              twin 185 preserves the halo but not the mass.
            </li>
            <li style={{ marginBottom: '0.5em' }}>
              The rules whose <em>rate of change</em> is constant are exactly <RuleList rules={CONSERVERS.activity} />{' '}
              &mdash; precisely the six rules known to be perfectly reversible. Two lists compiled for different
              reasons, and they coincide, member for member.
            </li>
            <li>
              And one loner, rule 236, conserves its <em>outline</em> while growing inside it:
            </li>
          </ul>
          <SilhouetteDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            For the record, because our negative results are load-bearing: we also measured mass, halo, speed and
            activity for the classic bestiary of Conway's Game of Life (the 2D cousin of these rules), hunting for
            a clean energy law &mdash; and E=mc&sup2; did <em>not</em> fall out. Still objects here have zero
            activity; blinking objects have activity while standing still; no tidy formula ties it together yet.
            What <em>is</em> literal in this universe: a speed limit. Influence propagates at most one square per
            tick &mdash; a true speed of light, with Life's famous spaceships provably capped at half and a
            quarter of it.
          </p>
        </section>

        {/* STOP 6 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 6</div>
          <h2 style={h2Style}>How much coupling does a pattern need?</h2>
          <p style={pBody}>
            One more construction, explained from scratch. Elsewhere on this site we found rule pairs with a
            party trick: run <em>two</em> rows side by side, and give every square one extra input &mdash; a
            listening line to the square directly across from it in the other row, which selects which of two
            tables the square consults this tick. Choose the four tables right and something remarkable happens:
            four rules that are each utterly boring alone (they freeze or blink) produce rich, persistent
            patterns when wired together. The structure lives entirely in the <em>coupling</em>. (On the{' '}
            <a href="concepts.html#prehoc" style={{ color: 'var(--accent)' }}>Concepts page</a> the listening line
            is the <em>fourth input</em>, and the wired-together pair is the engine the badges below write as{' '}
            <Op>engine</Op>(A⇄B).)
          </p>
          <p style={pBody}>
            That's an all-or-nothing fact, and all-or-nothing facts hide dials. So: turn the listening down.
            Connect only a fraction of the lines and ask how much coupling the pattern actually needs. Two very
            different ways to be partially connected: cut some lines <em>permanently</em> (some squares are just
            deaf), or make every line <em>flicker</em> (each square's connection randomly drops in and out, tick
            by tick, same average).
          </p>
          <CouplingChart />
          <CouplingTriptych />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            We expected a tipping point &mdash; some critical fraction where structure switches on. Wrong, in the
            most instructive way. Permanent deafness is almost harmless: cut one line in a hundred and nothing is
            lost; cut a third of them and the pattern is dented but alive. Flicker is what kills. At 85%
            flickering connectivity &mdash; <em>more</em> total listening than the dented-but-alive case &mdash;
            the system is indistinguishable from static, and order returns only when the flickering stops
            entirely. An intermittent connection isn't a weaker connection; it's a noise source. The lesson reads
            like it was written for people rather than automata: <strong>what builds structure isn't how much
            coupling you have &mdash; it's whether the coupling can be trusted.</strong>
          </p>
        </section>

        {/* STOP 7 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 7</div>
          <h2 style={h2Style}>Zooming out until it rhymes</h2>
          <p style={pBody}>
            Last stop, longest lens. Take any rule's history and <em>squint</em>: merge each pair of neighboring
            squares into one, and keep only every other tick &mdash; a half-resolution summary of the same events.
            Now ask a precise question: is there a rule whose ordinary behavior is exactly what this summary shows?
            When the answer is the <em>same rule you started with</em>, the rule is scale-invariant &mdash; it
            looks like itself from twice as far away. This universe is small enough that we could check every
            rule, every way of merging, every configuration, exhaustively. Watch what that means for rule 90:
          </p>
          <ScaleDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            Same picture. Not <em>similar</em> &mdash; the same, square for square, and the exhaustive check
            proves it's no accident of this run. Rule 90 draws an endlessly nested triangle <em>because</em>{' '}
            zooming out is a symmetry it possesses; the fractal is what that symmetry looks like. (Squinting is
            also, quietly, the one operation on this site that breaks the State&nbsp;&rarr;&nbsp;State contract
            &mdash; the summary row has half the squares of the original. The calculus lives at a fixed size;
            scale is a door it hasn't formalized yet.) The full list of
            self-similar rules turned out to be short and pointed: <RuleList rules={FIXED_POINTS.affine} /> (the
            &ldquo;crystal&rdquo; family &mdash; the rules this site's oldest theorem singled out as perfectly
            orderly, whose remainders are always constant), plus the trivial sliders and copiers{' '}
            <RuleList rules={FIXED_POINTS.shifts} />, plus a family of rules that only ever fill in and absorb{' '}
            <RuleList rules={FIXED_POINTS.absorbing} />. And the celebrated complex rules &mdash; 110 and its kin,
            the ones that look most alive &mdash; are <em>nowhere on the list</em>. Perfect order survives any
            zoom. Complexity lives at particular scales, in the space between the things that don't change.
          </p>
        </section>

        {/* CODA */}
        <section style={{ padding: '1.6rem 0 0.4rem', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>coda</div>
          <h2 style={h2Style}>What we're holding now</h2>
          <p style={pBody}>
            Walk it back and it was one thought the whole way. Two processes, run against each other, leave a
            remainder &mdash; a picture of their relationship and nothing else. Usually that picture is what it
            ought to be: a shadow. But under conditions we can now name and test, the shadow closes up and keeps
            a law of its own &mdash; sometimes a law so crisp it's just another rule of the same universe, a wave
            with a speed you can read off a stripe-chart. Relationships, here, can be <em>things</em>: with laws,
            with conserved quantities, with a demand for faithful coupling, embedded in a world where perfect
            order is scale-free and everything interesting is not.
          </p>
          <p style={pBody}>
            And the door we haven't opened yet is right there in the phrasing. If the remainder of two rules can
            itself <em>be</em> a rule &mdash; if <Op>engine</Op>(B∘A) ⊕ <Op>engine</Op>(A∘B) is sometimes an
            engine with its own name &mdash; then &ldquo;take the relationship&rdquo; is an operation: feed in two
            rules, get a third. Does applying it again and again settle somewhere? Is there a pair whose
            relationship is as complex as rule 110 itself &mdash; a shadow with an inner life? Nobody knows. The
            instruments are on the <a href="explorer.html" style={{ color: 'var(--accent)' }}>explorer</a> page;
            the receipts are in <span className="gc-code">NOTES.md &sect;9</span> and{' '}
            <span className="gc-code">scripts/</span>. The walk continues.
          </p>
        </section>
      </main>

      <footer className="gc-footer">
        <div className="gc-footer-inner">
          Every claim on this page traces to a checked-in script in the{' '}
          <a href="https://github.com/mbilokonsky/groovy-commutator">GitHub repository</a>; the demos above
          recompute their local versions live.
        </div>
      </footer>
    </>
  );
}
