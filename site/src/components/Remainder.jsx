import { useEffect, useRef, useState } from 'react';
import Nav from './Nav.jsx';
import Watermark from './Watermark.jsx';
import couplingData from '../data/critical_coupling.json';

// ---------------------------------------------------------------------------
// The Remainder -- a guided walk through one night of experiments.
// Every demo on this page computes live from the engine; the numbers the
// prose quotes were established at scale by scripts/experiment_remainder_*.py,
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
  footprint: [170, 204, 236, 240],
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
    testRows: field.slice(half, steps - 1),
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

// 2D power spectrum of a (steps x n) binary field, both dims cropped/padded
// to `size` (power of two). Returns { power: Float64Array(size*size),
// concentration: top-1% share of non-DC power }.
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
  // fftshift so DC sits at the center and the dispersion lines read as lines
  for (let t = 0; t < size; t++) {
    for (let i = 0; i < size; i++) {
      const st = (t + size / 2) % size, si = (i + size / 2) % size;
      const v = mx > 0 ? L[st * size + si] / mx : 0;
      const o = (t * size + i) * 4;
      // cream -> teal -> ink ramp
      img.data[o] = Math.round(241 + (42 - 241) * v);
      img.data[o + 1] = Math.round(234 + (96 - 234) * (v < 0.5 ? v * 2 * 0.65 : 0.65 + (v - 0.5) * 2 * 0.35));
      img.data[o + 2] = Math.round(217 + (60 - 217) * v);
      img.data[o + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
}

// ---- shared: compute a divergence field ------------------------------------

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

// ---- Stop 1: the triptych ---------------------------------------------------

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
  const labels = ['90 vs 150 — commute: nothing left over', '110 vs 54 — structured: a legible leftover', '110 vs 30 — noisy: an illegible one'];
  return (
    <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap', margin: '0.4rem 0 0.8rem' }}>
      {refs.map((r, i) => (
        <div key={i} style={{ width: 170 }}>
          <canvas className="gc-field" ref={r} style={{ width: 170, height: 170 }}></canvas>
          <div style={capStyle}>{labels[i]}</div>
        </div>
      ))}
    </div>
  );
}

// ---- Stop 2: the autonomy experiment ---------------------------------------

const AUTONOMY_PAIRS = [
  { a: 110, b: 54, label: '110 / 54 (structured)' },
  { a: 110, b: 30, label: '110 / 30 (noisy)' },
  { a: 32, b: 71, label: '32 / 71 (structured, exact)' },
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
        {[[fieldRef, 'the remainder, full run'], [predRef, 'its own law, predicting the unseen half'], [errRef, 'errors (red = the law was wrong)']].map(([r, cap]) => (
          <div key={cap} style={{ width: 190 }}>
            <canvas className="gc-field" ref={r} style={{ width: 190, height: 190 }}></canvas>
            <div style={capStyle}>{cap}</div>
          </div>
        ))}
      </div>
      {stats && (
        <div style={statStyle}>
          held-out accuracy <strong>{(stats.acc * 100).toFixed(2)}%</strong>
          {' '}&middot; contradiction mass in training <strong>{(stats.contra * 100).toFixed(2)}%</strong>
          {' '}&middot; contexts visited <strong>{stats.nCtx}/{stats.buckets}</strong>
        </div>
      )}
    </div>
  );
}

// ---- Stop 3: the soliton ----------------------------------------------------

function SolitonDemo() {
  const [engineRef, ready] = useEngine();
  const [verdict, setVerdict] = useState('running…');
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
        setVerdict(`verified in your browser just now: every one of the ${F.length - 1} steps of this run satisfies diff(t+1) = shift${k > 0 ? 'right' : 'left'}(diff(t)), exactly.`);
        return;
      }
    }
    setVerdict('this seed did not lock to a pure shift (it happens for some initial conditions — reroll by reloading).');
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div style={{ display: 'flex', gap: '1.1rem', flexWrap: 'wrap', alignItems: 'flex-start' }}>
      <div style={{ width: 190 }}>
        <canvas className="gc-field" ref={ref} style={{ width: 190, height: 190 }}></canvas>
        <div style={capStyle}>the remainder of 138 vs 205</div>
      </div>
      <p style={{ ...pBody, maxWidth: '38ch', fontSize: '0.9rem' }}>
        This pair's remainder obeys <span className="gc-code">rule 170</span> &mdash; the pure shift.{' '}
        {verdict}
      </p>
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
      {[[s1, 'spectrum of the 110/54 remainder', 0], [s2, 'spectrum of the 110/30 remainder', 1]].map(([r, cap, i]) => (
        <div key={cap} style={{ width: 210 }}>
          <canvas ref={r} style={{ width: 210, height: 210, imageRendering: 'pixelated', border: '1px solid var(--rule)', borderRadius: 6, display: 'block' }}></canvas>
          <div style={capStyle}>{cap}{conc && <> &middot; top-1% share <strong>{(conc[i] * 100).toFixed(0)}%</strong></>}</div>
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
    // blind search over lags k and shifts s for the deepest rhyme,
    // density estimated on every 4th row
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
        {[[rawRef, 'rule 110, raw — ether everywhere'], [resRef, 'the same run, rhymed against itself — only the gliders survive']].map(([r, cap]) => (
          <div key={cap} style={{ width: 210 }}>
            <canvas className="gc-field" ref={r} style={{ width: 210, height: 210 }}></canvas>
            <div style={capStyle}>{cap}</div>
          </div>
        ))}
      </div>
      {found && (
        <div style={statStyle}>
          deepest rhyme found blind at lag <strong>{found.k}</strong>, shift <strong>{found.s <= 128 ? found.s : found.s - 256}</strong>
          {' '}&middot; residual density <strong>{found.d.toFixed(3)}</strong> (raw: {found.rawDensity.toFixed(3)})
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
          let r = 241, g = 234, b = 217;                    // void: cream
          if (rows[t].s[i]) { r = 42; g = 36; b = 32; }     // live: ink
          else if (rows[t].a[i]) { r = 209; g = 154; b = 60; } // absential: amber
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
        <div style={capStyle}>rule 236 — live cells (ink) grow into their own halo (amber); the silhouette never moves</div>
      </div>
      {nums && (
        <div style={{ ...statStyle, margin: 0 }}>
          live cells: <strong>{nums.live0} &rarr; {nums.live1}</strong> (grows)<br />
          footprint (live+halo): <strong>{nums.closed0} &rarr; {nums.closed1}</strong> (conserved)
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
        <text x={padL + w / 2} y={H - 2} textAnchor="middle" fontFamily="IBM Plex Mono, monospace" fontSize="10" fill={INK_SOFT}>coupling density &alpha;</text>
        <path d={path('quenched')} fill="none" stroke="var(--accent)" strokeWidth="2.2" />
        <path d={path('annealed')} fill="none" stroke={RED} strokeWidth="2.2" />
        <circle cx={x(1)} cy={y(curves.annealed.comp[curves.annealed.comp.length - 1])} r="5" fill="none" stroke={RED} strokeWidth="2" />
        <text x={x(0.62)} y={y(0.15)} fontFamily="IBM Plex Mono, monospace" fontSize="10" fill="var(--accent)">quenched (fixed dry sites)</text>
        <text x={x(0.30)} y={y(0.9)} fontFamily="IBM Plex Mono, monospace" fontSize="10" fill={RED}>annealed (flickering)</text>
      </svg>
      <p className="gc-mono" style={{ fontSize: '0.7rem', color: INK_SOFT, margin: '0.3rem 0 0' }}>
        y: compressibility of layer A (0 frozen &middot; ~0.45 structured &middot; 1 noise) &middot; circled: the snap back to order at exactly &alpha; = 1
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
  const caps = ['α = 0.6, quenched — pinned but coherent', 'α = 0.85, flickering — coupling noise as heat', 'α = 1.0 — full fidelity, structure returns'];
  return (
    <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap', margin: '1rem 0 0' }}>
      {refs.map((r, i) => (
        <div key={i} style={{ width: 170 }}>
          <canvas className="gc-field" ref={r} style={{ width: 170, height: 170 }}></canvas>
          <div style={capStyle}>{caps[i]}</div>
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
    // decimation: keep every other cell of every other row (block map h = b0,
    // one of the three verified self-maps of rule 90 in results/scale_rhyme.csv).
    // Rendered at the same display size, the half-resolution field should be
    // pixel-for-pixel the same picture.
    const coarse = [];
    for (let t = 0; t < steps; t += 2) {
      coarse.push(Uint8Array.from({ length: n / 2 }, (_, i) => T[t][2 * i]));
    }
    if (coarseRef.current) e.renderFieldToCanvas(coarseRef.current, coarse, ON, CREAM);
  }, [ready]);   // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <div style={{ display: 'flex', gap: '0.9rem', flexWrap: 'wrap' }}>
      {[[fineRef, 'rule 90'], [coarseRef, 'rule 90, every other cell, every other step']].map(([r, cap]) => (
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
          Everything on this site eventually points at the same picture: two rules, one shared origin, order
          swapped, and the field of their disagreement unrolling down the page. This page walks through one long
          night of asking that picture a question it had been begging the whole time. Seven stops. Bring nothing;
          everything is computed in front of you.
        </p>

        {/* STOP 1 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 1</div>
          <h2 style={h2Style}>The itch</h2>
          <p style={pBody}>
            Run two rules against each other &mdash; A-then-B versus B-then-A &mdash; and XOR the two unfoldings.
            What's left is the <strong>remainder</strong>: the part of the relationship that neither vanishes nor
            explains itself. Three textures keep appearing:
          </p>
          <Triptych />
          <p style={pBody}>
            The left one is silence. The right one is static. But the middle one <em>does something</em> &mdash;
            it ripples, it persists, it looks for all the world like it's alive. Which should be impossible to
            take seriously, because a remainder is a shadow: every bit of it is mechanically determined by the two
            hidden trajectories that cast it. It has no dynamics of its own. It <em>can't</em>.
          </p>
          <p style={pBody}>And yet.</p>
        </section>

        {/* STOP 2 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 2</div>
          <h2 style={h2Style}>Interrogate the shadow</h2>
          <p style={pBody}>
            Here is a simple, slightly disrespectful experiment. Ignore the substrates entirely. Pretend the shadow
            is a citizen: assume it has its own local law, learn that law by watching the first half of its life
            (for every 5-cell neighborhood it exhibits, record what it does next), then cover everything up and ask
            the learned law to predict a future it has never seen &mdash; one step at a time, graded against
            reality.
          </p>
          <AutonomyDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            Click between the pairs and watch the red panel. For the noisy pair the law fails on roughly a third of
            all cells, and here is the damning detail: giving it a wider neighborhood barely helps, because the
            missing information isn't nearby &mdash; it's in the hidden substrates, permanently off-stage. The
            noisy remainder really is a shadow. But the structured pair's errors nearly vanish, and for pair
            32/71 they vanish <em>exactly</em>. At scale (200 sampled pairs,{' '}
            <span className="gc-code">experiment_remainder_autonomy.py</span>): the median live structured
            remainder scores <strong>1.000</strong> on held-out future with <strong>zero</strong> contradictions in
            seventy thousand transitions &mdash; while visiting nearly every context it could express, so this is
            not a frozen field coasting on repetition.
          </p>
          <p style={pBody}>
            Sit with what that means. In the structured regime, the disagreement between two processes{' '}
            <strong>keeps its own law</strong>. You can throw away the parents and the orphan still knows how to
            behave. That is a measurable, falsifiable definition of the thing this site keeps circling: a
            relationship becomes a thing when its remainder closes over its own vocabulary. (Honesty clause: closed{' '}
            <em>on its attractor</em> &mdash; the law is exact where the relationship actually lives, not over all
            conceivable states.)
          </p>
        </section>

        {/* STOP 3 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 3</div>
          <h2 style={h2Style}>The remainder is a soliton</h2>
          <p style={pBody}>
            Then it got weirder. Dozens of structured pairs have remainders so simple they are{' '}
            <em>elementary rules</em> &mdash; full 8-entry lookup tables, extracted from observation. And every
            single one extracted came out as rule 170 or rule 240. Those are the two shifts. The relationship is a
            wave: a pattern of disagreement that never changes shape, only glides.
          </p>
          <SolitonDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            We had a beautiful explanation ready: maybe these pairs satisfy an exact algebra, A&#8728;B equal to
            B&#8728;A <em>up to translation</em> &mdash; order mattering only as a change of reference frame. It
            was tested exhaustively over every state at n=12, and it is false for every pair. Zero for
            thirty-four. The real mechanism is humbler and stranger: both orderings fall into{' '}
            <em>traveling-wave attractors</em> of the same velocity, and the disagreement inherits the drift. The
            wave isn't in the algebra. It's in where the dynamics settles &mdash; the relationship survives because
            both parents surf.
          </p>
        </section>

        {/* STOP 4 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 4</div>
          <h2 style={h2Style}>Look with waves</h2>
          <p style={pBody}>
            If remainders drift, their portraits in wave-space should be lines. Take the 2D Fourier transform of
            the whole space-time field &mdash; every spatial frequency crossed with every temporal frequency
            &mdash; and coherent traveling structure collapses onto <em>dispersion lines</em> &omega; = v&middot;k,
            whose slope is a velocity. Noise, by definition, fills the plane.
          </p>
          <SpectrumDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            The structured remainder's power piles onto a few sharp lines &mdash; at scale, the median structured
            pair puts <strong>97%</strong> of its spectral power into 1% of the bins; noisy pairs manage 9%. And
            for the soliton pairs of stop 3, the line's slope reads <strong>exactly &plusmn;1.00 cells per
            step</strong>, sign matching rule 170 versus 240: the spectrum reads the remainder's law straight off
            the picture.
          </p>
          <p style={pBody}>
            Fourier gave us one more gift, aimed at a different itch: <em>d&eacute;j&agrave; vu as an
            instrument</em>. XOR a trajectory against a lagged, shifted copy of itself and scan all lags and
            shifts &mdash; a rhyme spectrum. Wherever the field has a periodic background, some offset cancels it
            perfectly, and what survives the cancellation is exactly the parts that <em>break</em> the pattern:
          </p>
          <RhymeDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            Nothing in that search knew rule 110 has an ether, or what its lattice vector is. The rhyme found it
            blind and handed back the gliders. (Rule 30, the control, has no deep rhyme anywhere: its best offset
            still leaves ~37% disagreement.) One sentence to keep: <strong>structure is having somewhere to rhyme
            to.</strong>
          </p>
        </section>

        {/* STOP 5 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 5</div>
          <h2 style={h2Style}>Weigh everything</h2>
          <p style={pBody}>
            A night this strange deserves bookkeeping. For every rule and every quantity this site cares about
            &mdash; live cells, absential halo, void, footprint, activity &mdash; we checked <em>exact</em>{' '}
            conservation over every state, exhaustively, at two ring sizes
            (<span className="gc-code">experiment_conservation_kinematics.py</span>). The atlas came back with
            jewelry in it:
          </p>
          <ul style={{ ...pBody, paddingLeft: '1.2em' }}>
            <li style={{ marginBottom: '0.5em' }}>
              Mass conservers: <RuleList rules={CONSERVERS.live} /> &mdash; the known number-conserving five. Halo
              conservers: <RuleList rules={CONSERVERS.absential} /> &mdash; note the pattern: each mass-conserver's
              vacuum-filling twin (its rule number XOR 1). Rule 184 conserves mass but not halo; its twin 185
              conserves halo but not mass.
            </li>
            <li style={{ marginBottom: '0.5em' }}>
              Activity conservers: <RuleList rules={CONSERVERS.activity} /> &mdash; <em>exactly</em> the six
              universally reversible rules. Conserved rate-of-change and reversibility are the same short list.
            </li>
            <li>
              And one loner: rule 236 conserves its <em>silhouette</em> while growing &mdash;
            </li>
          </ul>
          <SilhouetteDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            For the record, because negative results are load-bearing here: we also measured mass, halo, activity
            and velocity for the whole Life bestiary, and E=mc&sup2; did <em>not</em> fall out &mdash; still lifes
            have zero activity, oscillators have internal energy at rest, and no clean invariant ties E to
            m&middot;v across the spaceships. The speed of light, though, is not a metaphor in this universe: c is
            one cell per step, exactly, with Life's proven c/2 and c/4 ship limits sitting obediently under it.
          </p>
        </section>

        {/* STOP 6 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 6</div>
          <h2 style={h2Style}>Turn the coupling knob</h2>
          <p style={pBody}>
            The pre-hoc result elsewhere on this site was binary: couple two layers of boring rules and structure
            appears. Binary results hide dials. So: gate the coupling through a mask of density &alpha; &mdash;
            at 0 the layers are strangers, at 1 the full emergent system &mdash; and ask <em>how much coupling
            emergence needs</em>. Two ways to be partially coupled: <strong>quenched</strong> (some cells are
            permanently deaf) and <strong>annealed</strong> (every cell flickers).
          </p>
          <CouplingChart />
          <CouplingTriptych />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            The prediction was a phase transition at some critical &alpha;. Wrong, in the most instructive way.
            Quenched deafness barely matters: one permanently deaf cell in a hundred costs <em>nothing</em>, and
            structure degrades gracefully all the way down. But flickering is catastrophic: at &alpha; &asymp; 0.85
            the system is indistinguishable from noise &mdash; <em>worse</em> than no coupling at all &mdash; and
            order snaps back only at exactly &alpha; = 1. Intermittency in the coupling channel behaves like
            temperature. The lesson reads like it was written for people rather than automata:{' '}
            <strong>structure isn't bought with the amount of coupling; it's bought with its fidelity.</strong> An
            unreliable relationship is worse than none.
          </p>
        </section>

        {/* STOP 7 */}
        <section style={{ padding: '1.4rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>stop 7</div>
          <h2 style={h2Style}>Zoom out until it rhymes</h2>
          <p style={pBody}>
            Last stop, longest lens. Call rule B a <em>coarse image</em> of rule A if watching A through a blur
            &mdash; two cells merged into one, two steps into one &mdash; is exactly B. This is renormalization,
            done to 8-bit rules, and it's small enough here to do <em>exhaustively</em>: every rule, every block
            map, every state, all hits re-verified at a larger size
            (<span className="gc-code">experiment_scale_rhyme.py</span>). Some rules turn out to be their own
            coarse image. Watch:
          </p>
          <ScaleDemo />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            Same picture. Not similar &mdash; <em>same</em>, verified state-by-state. Rule 90 draws a fractal{' '}
            <em>because</em> it is a fixed point of coarse-graining; the self-similarity you can see is a theorem
            you can check. And the full list of fixed points lands with a thud: the affine family{' '}
            <RuleList rules={FIXED_POINTS.affine} />, the shifts <RuleList rules={FIXED_POINTS.shifts} />, and the
            absorbing sponges <RuleList rules={FIXED_POINTS.absorbing} />. The affine rules are this site's
            oldest characters &mdash; the crystals, the ones whose commutator is constant. The crystals are also
            the scale-invariant ones. And Class IV &mdash; the interesting, alive-looking rules &mdash; appears
            nowhere on the list. <strong>Complexity doesn't live at the fixed points. It lives in the flow between
            them.</strong>
          </p>
        </section>

        {/* CODA */}
        <section style={{ padding: '1.6rem 0 0.4rem', borderTop: '1px solid var(--rule)' }}>
          <div style={kicker}>coda</div>
          <h2 style={h2Style}>What we're holding now</h2>
          <p style={pBody}>
            Walk back through the stops and notice they were one sentence the whole time. A relationship leaves a
            remainder. In the structured regime the remainder <em>keeps its own law</em> &mdash; sometimes so
            perfectly it is simply another rule, a wave with a velocity Fourier can read. Its bookkeeping has
            conservation laws. Its coupling demands fidelity, not quantity. And the whole picture repeats across
            scale exactly for the rules that have stopped being interesting &mdash; the crystals &mdash; while
            everything alive lives in between.
          </p>
          <p style={pBody}>
            The door this opens is the one we haven't walked through yet: if the remainder of two rules can{' '}
            <em>be</em> a rule, then &ldquo;taking the relationship&rdquo; is an operation &mdash; R(A,B) &mdash;
            and rule space is partially closed under it. Does R iterate? Does it have fixed points? Is any pair's
            remainder Class IV &mdash; a relationship whose own physics is complex? Nobody knows. The instruments
            are all on the <a href="explorer.html" style={{ color: 'var(--accent)' }}>explorer</a> page, and the
            receipts are in <span className="gc-code">NOTES.md &sect;9</span> and{' '}
            <span className="gc-code">scripts/</span>.
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
