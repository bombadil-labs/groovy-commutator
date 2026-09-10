import { useCallback, useEffect, useRef, useState } from 'react';
import Nav from './Nav.jsx';
import Watermark from './Watermark.jsx';
import { AmbientCA2D } from './AmbientCA.jsx';
import InstrumentViewer from './InstrumentViewer.jsx';
import RunSig from './RunSig.jsx';
import Defn, { Op } from './Defn.jsx';
import PossibilityDemo from './PossibilityDemo.jsx';
import { buildSeedUrl } from '../lib/exploreSeed.js';

// Run signatures (see the #run section): a field states which gauge it is
// and whose orbit it rides; base strings like 'E_110' render with
// subscripts via RunSig. Badges appear only from the #run section down --
// earlier viewers stay unsigned so the notation is never shown before the
// page defines it. Gauges on this page always share the base's rule, so
// badge gauges omit the rule slot ('D', not 'D(·,110)'); the Explorer,
// where the slots can genuinely differ per card, spells them out.
const sigRaw = (r) => ({ gauge: 'id', base: `E_${r}` });
const sigGauge = (g, r) => ({ gauge: g, base: `E_${r}` });

// Explorer's own dark-theme card palette (not shared with this light-theme
// page) -- used only when building ?seed= links, so cards read correctly
// once they land there.
const EXPLORE_COLORS = { cream: 'oklch(0.94 0.02 90)', teal: 'oklch(0.72 0.1 195)', amber: 'oklch(0.72 0.14 75)', purple: 'oklch(0.7 0.13 300)', red: 'oklch(0.66 0.15 22)', blue: 'oklch(0.7 0.13 240)', green: 'oklch(0.7 0.13 150)' };

// Consistent "symbol — role" labels for every viewer across this page.
const L_E = 'E(S) — base state';
const L_D = 'D(S) — derivative';
const L_D2 = 'D²(S) — 2nd derivative';
const L_DE = 'D(E(S)) — evolve-then-differentiate';
const L_ED = 'E(D(S)) — differentiate-then-evolve';
const L_G = 'G(S) — commutator';
const L_A = 'A(S) — absential';
const L_V = 'V(S) — void';

function defaultInitState(n) {
  const arr = new Array(n).fill(0);
  arr[Math.floor(n / 2)] = 1;
  return arr;
}

// Deliberately low-res: every canvas on this page is CSS-scaled up to a
// fixed display size (see InstrumentViewer / gc-field's image-rendering:
// pixelated), so fewer cells means bigger, more legible pixels -- the
// Explorer keeps a much finer 100x100 grid for actual exploration.
const N_CELLS = 24;
const STEPS = 24;
const ON_COLOR = '#2a2420';
const OFF_COLOR = '#fbfaf7';
const ACCENT = 'oklch(0.5 0.1 195)';
const INK_SOFT = '#6b6055';

// The eight (neighborhood -> output) entries of an elementary rule, in the
// same all-on-to-all-off order used everywhere on this page. Pure bit math,
// so it works before the engine module has loaded.
const ruleRows = (n) => [7, 6, 5, 4, 3, 2, 1, 0].map((idx) => ({ idx, l: (idx >> 2) & 1, c: (idx >> 1) & 1, r: idx & 1, out: (n >> idx) & 1 }));

const RULE_CATALOG = [
  { num: 0, cls: 'I' },
  { num: 4, cls: 'II' },
  { num: 184, cls: 'II' },
  { num: 30, cls: 'III' },
  { num: 110, cls: 'IV' },
  { num: 54, cls: 'IV' },
  { num: 90, cls: null },
];

// The one deliberate spot of color on this page's diagrams -- everything
// else stays black/white so the 0/1 reading never competes with a color
// legend. A class is otherwise-invisible metadata (only known for the 7
// catalog rules above), so a small dot earns its keep here.
const CLASS_COLOR = { I: 'oklch(0.7 0.02 90)', II: 'oklch(0.6 0.12 195)', III: 'oklch(0.6 0.16 22)', IV: 'oklch(0.55 0.14 300)' };
const CLASS_COLOR_UNKNOWN = 'var(--rule)';

const PAIR_PRESETS = [
  { a: 90, b: 150, regime: 'commute', note: 'both linear, weights align' },
  { a: 90, b: 165, regime: 'crystalline', note: 'linear vs affine-biased' },
  { a: 110, b: 30, regime: 'noisy', note: 'Class IV vs Class III' },
  { a: 110, b: 54, regime: 'structured', note: 'Class IV vs Class IV-ish' },
  { a: 184, b: 250, regime: 'drain', note: 'low image-ratio pair' },
];

// Literal colors for canvas fillStyle -- canvas doesn't resolve CSS custom
// properties, so this mirrors (not references) the --commute/etc tokens.
const REGIME_CANVAS_COLOR = {
  commute: 'oklch(0.58 0.13 150)',
  crystalline: 'oklch(0.58 0.13 240)',
  noisy: 'oklch(0.58 0.13 300)',
  structured: 'oklch(0.6 0.14 75)',
  drain: 'oklch(0.56 0.15 22)',
};

const TOC = [
  ['#boolean', 'Bits & XOR'],
  ['#ca', 'Cellular automata'],
  ['#state', 'State → State'],
  ['#run', 'Every picture is a run'],
  ['#calculus', 'Boolean calculus'],
  ['#secondderivative', 'Second derivative'],
  ['#evolvederivative', 'Evolving the derivative'],
  ['#commutator', 'The Groovy Commutator G'],
  ['#possibility', 'What can happen next?'],
  ['#absential', 'Absential cells'],
  ['#engines', 'Engines'],
  ['#secondorder', 'Reversible memory'],
  ['#coupling', 'Coupling rules'],
  ['#prehoc', 'The fourth input'],
  ['#rulefield', 'Rule fields'],
  ['#resonance', 'Four meanings of resonance'],
];

const pill = { fontFamily: "'IBM Plex Mono',monospace", fontSize: '0.76rem', fontWeight: 600, textDecoration: 'none', background: 'var(--bg-alt)', color: 'var(--ink-soft)', padding: '0.35rem 0.7rem', borderRadius: 999 };
const sectionKicker = { fontFamily: "'IBM Plex Mono',monospace", fontSize: '0.74rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '.06em', color: 'var(--ink-soft)' };
const h2Style = { fontFamily: "'Lora',serif", fontSize: '1.35rem', margin: '0.3em 0 0.5em', fontWeight: 600 };
const h3Style = { fontFamily: "'Lora',serif", fontSize: '1.1rem', margin: '1.4em 0 0.5em', fontWeight: 600 };
const pBody = { fontSize: '0.98rem', color: 'var(--ink-soft)', margin: '0 0 1.1rem', maxWidth: '60ch' };

const CLASS_EXAMPLES = [
  { rule: 0, cls: 'I' },
  { rule: 4, cls: 'II' },
  { rule: 30, cls: 'III' },
  { rule: 110, cls: 'IV' },
];

// Fixed, non-interactive reference examples -- one per informal Wolfram
// class -- computed once on mount, independent of whatever rule the
// reader later picks in the interactive panel below.
function ClassExamples() {
  const refsRef = useRef(CLASS_EXAMPLES.map(() => ({ current: null })));
  useEffect(() => {
    let cancelled = false;
    import('../lib/groovy-engine.js').then((engine) => {
      if (cancelled) return;
      const n = 90, steps = 90;
      const s0 = engine.randomState(n, 7);
      CLASS_EXAMPLES.forEach((ex, i) => {
        const field = engine.evolveTrajectory(s0, ex.rule, steps);
        const canvas = refsRef.current[i].current;
        if (canvas) engine.renderFieldToCanvas(canvas, field, '#2a2420', '#f1ead9');
      });
    });
    return () => { cancelled = true; };
  }, []);

  return (
    <div style={{ display: 'flex', gap: '0.8rem', flexWrap: 'wrap', margin: '0 0 1.1rem' }}>
      {CLASS_EXAMPLES.map((ex, i) => (
        <div key={ex.rule} style={{ flex: '1 1 120px', minWidth: 100, maxWidth: 160 }}>
          <canvas className="gc-field" ref={refsRef.current[i]} style={{ width: '100%', height: 'auto', aspectRatio: '1' }}></canvas>
          <div className="gc-mono" style={{ fontSize: '0.7rem', color: 'var(--ink-soft)', marginTop: '0.3rem', textAlign: 'center' }}>
            Class {ex.cls} &middot; rule {ex.rule}
          </div>
        </div>
      ))}
    </div>
  );
}

// Fixed demo for the #run section: one walk (rule 110 from a single seed
// cell), watched two ways. Deliberately independent of the interactive rule
// panel, which doesn't debut until the calculus section further down.
const RUN_DEMO_RULE = 110;
function RunExamples() {
  const [fields, setFields] = useState(null);
  useEffect(() => {
    let cancelled = false;
    import('../lib/groovy-engine.js').then((engine) => {
      if (cancelled) return;
      const s0 = Uint8Array.from(defaultInitState(N_CELLS));
      const raw = engine.evolveTrajectory(s0, RUN_DEMO_RULE, STEPS);
      const flipped = raw.map((row) => Uint8Array.from(row, (b) => (b ? 0 : 1)));
      setFields({ raw, flipped });
    });
    return () => { cancelled = true; };
  }, []);
  return (
    <InstrumentViewer
      items={[
        { label: 'id — every footprint, unchanged', sig: { gauge: 'id', base: `E_${RUN_DEMO_RULE}` }, field: fields && fields.raw, color: ON_COLOR },
        { label: 'NOT — every footprint, flipped', sig: { gauge: 'NOT', base: `E_${RUN_DEMO_RULE}` }, field: fields && fields.flipped, color: ACCENT },
      ]}
    />
  );
}

// The one standard way a rule's neighborhood -> output mapping is drawn
// anywhere on this page (except inside actual formula/code blocks):
// three black/white input cells, an arrow, one output cell. `outlined`
// wraps the whole glyph in a border, for grouping several of these
// together as "one entry in a table" (vs. loose, for a plainer inline
// list). `onToggleOut`, when given, makes the *entire* glyph clickable
// (not just the output cell) -- clicking anywhere still only flips the
// output bit, since the inputs are fixed by definition; the bigger target
// is just easier to hit. Omit it for a read-only reference glyph. Built
// from spans, not divs, so the interactive version can be a single
// <button> without nesting a button inside a button.
function RuleGlyph({ l, c, r, out, outlined = false, size = 14, onToggleOut }) {
  const boxStyle = (bit, accent) => ({
    width: size, height: size, display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
    fontFamily: "'IBM Plex Mono',monospace", fontSize: Math.round(size * 0.6), fontWeight: 700,
    background: bit ? ON_COLOR : OFF_COLOR, color: bit ? OFF_COLOR : ON_COLOR,
    border: accent ? '1.5px solid var(--accent)' : '1px solid var(--ink)', flex: 'none', lineHeight: 1,
  });
  const inner = (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
      <span style={{ display: 'inline-flex', gap: 1 }}>
        <span style={boxStyle(l)}>{l}</span>
        <span style={boxStyle(c)}>{c}</span>
        <span style={boxStyle(r)}>{r}</span>
      </span>
      <span className="gc-mono" style={{ fontSize: Math.round(size * 0.75), color: 'var(--ink-soft)' }}>&rarr;</span>
      <span style={boxStyle(out, !!onToggleOut)}>{out}</span>
    </span>
  );
  const outlineStyle = outlined ? { border: '1px solid var(--ink-soft)', borderRadius: 4, padding: 3 } : {};
  if (onToggleOut) {
    return (
      <button onClick={onToggleOut} style={{ display: 'inline-flex', alignItems: 'center', background: 'none', border: 'none', padding: 0, cursor: 'pointer', font: 'inherit', ...outlineStyle }}>
        {inner}
      </button>
    );
  }
  return <span style={{ display: 'inline-flex', ...outlineStyle }}>{inner}</span>;
}

// A whole rule's table as one wrapping row of read-only glyphs -- used
// inside Defn glosses so a formula's R token can show the actual table it
// indexes, closing the loop with the rule-builder panel.
function GlyphRow({ rule, size = 12 }) {
  return (
    <span style={{ display: 'inline-flex', gap: 4, flexWrap: 'wrap', verticalAlign: 'middle' }}>
      {ruleRows(rule).map((nb) => <RuleGlyph key={nb.idx} l={nb.l} c={nb.c} r={nb.r} out={nb.out} outlined size={size} />)}
    </span>
  );
}

// A small live-updating canvas thumbnail that doubles as a jump link to
// wherever that field is actually explained -- lets the rule panel show
// "here's what this looks like for your rule" without duplicating the
// explanation itself.
function MiniLinkThumb({ href, canvasRef, label, size = 64 }) {
  return (
    <a href={href} style={{ position: 'relative', display: 'block', textDecoration: 'none', flex: 'none' }} title={'jump to where ' + label + ' is explained'}>
      <canvas className="gc-field" ref={canvasRef} style={{ width: size, height: size }}></canvas>
      <div className="gc-mono" style={{ position: 'absolute', bottom: 3, right: 3, fontSize: '0.58rem', fontWeight: 700, color: '#fff', background: 'rgba(42,36,32,0.7)', padding: '1px 4px', borderRadius: 4 }}>{label}</div>
    </a>
  );
}

// A fixed, hand-computable worked example -- rule 90 (output = left XOR
// right, ignoring the center cell entirely), n=7, one seed cell -- walked
// row by row, cell by cell, so a reader can verify every single bit by
// hand before ever looking at a space-time diagram where this same
// arithmetic runs thousands of times too fast to see. Independent of the
// interactive rule/state above -- deliberately never changes.
const WALK_RULE = 90;
const WALK_N = 7;
const WALK_LUT = Array.from({ length: 8 }, (_, i) => (WALK_RULE >> i) & 1);
const WALK_ROW0 = [0, 0, 0, 1, 0, 0, 0];
// Same all-on-to-all-off order used everywhere else on this page.
const WALK_LUT_ROWS = ruleRows(WALK_RULE);

function walkStep(row) {
  const out = new Array(WALK_N);
  const detail = [];
  for (let i = 0; i < WALK_N; i++) {
    const l = row[(i - 1 + WALK_N) % WALK_N];
    const c = row[i];
    const r = row[(i + 1) % WALK_N];
    const idx = 4 * l + 2 * c + r;
    const bit = WALK_LUT[idx];
    out[i] = bit;
    detail.push({ i, l, c, r, idx, bit });
  }
  return { out, detail };
}

const walkThtd = { padding: '0.25rem 0.55rem', whiteSpace: 'nowrap' };

function WalkCell({ bit }) {
  return (
    <div style={{
      width: 24, height: 24, display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
      fontFamily: "'IBM Plex Mono',monospace", fontSize: '0.72rem', fontWeight: 700,
      background: bit ? ON_COLOR : OFF_COLOR, color: bit ? OFF_COLOR : 'var(--ink-soft)',
      border: '1px solid var(--rule)', flex: 'none',
    }}>{bit}</div>
  );
}

function WalkRow({ row }) {
  return (
    <div style={{ display: 'flex', gap: 2 }}>
      {row.map((bit, i) => <WalkCell key={i} bit={bit} />)}
    </div>
  );
}

function WalkStepTable({ detail, label }) {
  return (
    <div style={{ overflowX: 'auto', margin: '0.5rem 0 1rem' }}>
      <table className="gc-mono" style={{ borderCollapse: 'collapse', fontSize: '0.72rem', width: '100%' }}>
        <thead>
          <tr style={{ color: 'var(--ink-soft)', textAlign: 'left' }}>
            <th style={walkThtd}>cell i</th>
            <th style={walkThtd}>left, self, right</th>
            <th style={walkThtd}>as index</th>
            <th style={walkThtd}>rule 90 says</th>
            <th style={walkThtd}>{label}[i]</th>
          </tr>
        </thead>
        <tbody>
          {detail.map((d) => (
            <tr key={d.i} style={{ borderTop: '1px solid var(--rule)' }}>
              <td style={walkThtd}>{d.i}</td>
              <td style={walkThtd}>{d.l}, {d.c}, {d.r}</td>
              <td style={walkThtd}>{d.l}{d.c}{d.r} = {d.idx}</td>
              <td style={walkThtd}>lookup[{d.idx}] = {d.bit}</td>
              <td style={{ ...walkThtd, fontWeight: 700 }}>{d.bit}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function RuleWalkthrough() {
  const [open, setOpen] = useState(false);
  const s1 = walkStep(WALK_ROW0);
  const s2 = walkStep(s1.out);
  const s3 = walkStep(s2.out);

  return (
    <div style={{ background: 'var(--bg-alt)', border: '1px solid var(--rule)', borderRadius: 8, padding: '1.1rem 1.2rem', margin: '1.2rem 0' }}>
      <button
        onClick={() => setOpen((o) => !o)}
        className="gc-mono"
        style={{ display: 'flex', alignItems: 'center', gap: '0.5em', width: '100%', textAlign: 'left', background: 'none', border: 'none', padding: 0, cursor: 'pointer', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '.05em', color: 'var(--ink-soft)' }}
      >
        <span style={{ display: 'inline-block', transform: open ? 'rotate(90deg)' : 'none', transition: 'transform 0.15s' }}>&#9656;</span>
        Worked example &mdash; rule 90, by hand
      </button>
      {!open && (
        <p style={{ ...pBody, fontSize: '0.92rem', margin: '0.6rem 0 0' }}>
          New to reading these diagrams? Expand this for a slow, deliberately tedious walkthrough &mdash; every cell,
          every row, by hand &mdash; of exactly how one rule turns one row into the next, so nothing below is a
          mystery.
        </p>
      )}
      {open && <>
      <p style={{ ...pBody, fontSize: '0.92rem', marginTop: '0.8rem' }}>
        Rule 90's table, read as three cells in, one cell out, in the same all-on-to-all-off order as everywhere
        else on this page:
      </p>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', margin: '0.5rem 0 1rem' }}>
        {WALK_LUT_ROWS.map((nb) => <RuleGlyph key={nb.idx} l={nb.l} c={nb.c} r={nb.r} out={nb.out} outlined />)}
      </div>
      <p style={{ ...pBody, fontSize: '0.92rem' }}>
        Rule 90 happens to be a special case worth noticing: compare <code className="gc-code">111&rarr;0</code>{' '}
        against <code className="gc-code">101&rarr;0</code> above &mdash; the center bit flips from 1 to 0 and the
        output doesn't change. That holds for every entry in this table: rule 90's output turns out to depend only
        on the left and right neighbors (it's just left XOR right), with the center cell along for the ride. That's
        specific to rule 90, not a fact about rules in general &mdash; normally the center cell matters just as much
        as its neighbors, and each of the eight entries above is independently editable. Seven cells in a ring, one
        seed lit in the middle, index 3:
      </p>
      <WalkRow row={WALK_ROW0} />
      <p style={{ ...pBody, fontSize: '0.92rem', marginTop: '0.8rem' }}>
        To get row 1, every cell looks at its own left/self/right neighbors in row 0 (wrapping around the ends:
        cell 0's left neighbor is cell 6, cell 6's right neighbor is cell 0), reads those three bits as a binary
        index into the table above, and writes down whatever that entry says. All seven cells, one at a time:
      </p>
      <WalkStepTable detail={s1.detail} label="row 1" />
      <WalkRow row={s1.out} />
      <p style={{ ...pBody, fontSize: '0.92rem', marginTop: '0.8rem' }}>
        Same process again, row 1 &rarr; row 2 &mdash; no shortcuts, just the same eight-entry table applied seven
        more times:
      </p>
      <WalkStepTable detail={s2.detail} label="row 2" />
      <WalkRow row={s2.out} />
      <p style={{ ...pBody, fontSize: '0.92rem', marginTop: '0.8rem' }}>
        And once more, row 2 &rarr; row 3:
      </p>
      <WalkStepTable detail={s3.detail} label="row 3" />
      <WalkRow row={s3.out} />
      <p style={{ ...pBody, fontSize: '0.92rem', marginTop: '1rem' }}>
        Now stack those four rows in the order they were computed, oldest on top, and stop reading the individual
        bits:
      </p>
      <div style={{ display: 'inline-flex', flexDirection: 'column', gap: 2, background: OFF_COLOR, padding: 4, border: '1px solid var(--rule)' }}>
        <WalkRow row={WALK_ROW0} />
        <WalkRow row={s1.out} />
        <WalkRow row={s2.out} />
        <WalkRow row={s3.out} />
      </div>
      <p style={{ ...pBody, fontSize: '0.92rem', marginTop: '0.8rem' }}>
        That's it &mdash; that's the whole trick behind every space-time diagram on this site, including the ones
        below. Every "weird pattern" from here on is exactly this arithmetic: one small lookup table, applied to
        every cell, one row at a time, just run for hundreds of steps and thousands of cells instead of seven and
        three, too fast and too small to watch bit by bit. When a diagram looks like noise or like lace, there's
        nothing hidden in it beyond what you just did by hand above.
      </p>
      </>}
    </div>
  );
}

// Compact live demo of two mutually pre-hoc coupled layers -- the mechanism
// is explained in the section around it; the full experimental findings
// live on the questions page. Self-contained (imports the engine itself)
// so it doesn't touch the sticky rule panel's plumbing.
// Deterministic pseudo-random 0/1 rows for the Explorer deep-link seed --
// the link is built at render time, before the engine module is loaded, so
// it can't use the engine's randomState.
function seedRow(n, seed) {
  let x = seed >>> 0 || 1;
  return Array.from({ length: n }, () => {
    x ^= x << 13; x >>>= 0; x ^= x >> 17; x ^= x << 5; x >>>= 0;
    return x & 1;
  });
}

function seedBytes(n, seed) {
  let x = seed >>> 0 || 1;
  return Array.from({ length: n }, () => {
    x ^= x << 13; x >>>= 0; x ^= x >> 17; x ^= x << 5; x >>>= 0;
    return x & 0xff;
  });
}

function PrehocMiniDemo() {
  const [seed, setSeed] = useState(3);
  const engineRef = useRef(null);
  const aRef = useRef(null);
  const bRef = useRef(null);

  useEffect(() => {
    let cancelled = false;
    import('../lib/groovy-engine.js').then((engine) => {
      if (cancelled) return;
      engineRef.current = engine;
      draw();
    });
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  useEffect(() => { draw(); });

  function draw() {
    const engine = engineRef.current;
    if (!engine) return;
    const { randomState, coupledTrajectory, rule4FromPair, renderFieldToCanvas } = engine;
    const res = coupledTrajectory(randomState(90, seed), randomState(90, seed + 101),
      rule4FromPair(77, 55), rule4FromPair(44, 23), 90);
    if (aRef.current) renderFieldToCanvas(aRef.current, res.a, ON_COLOR, '#f1ead9');
    if (bRef.current) renderFieldToCanvas(bRef.current, res.b, 'oklch(0.5 0.1 195)', '#f1ead9');
  }

  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1.2rem', flexWrap: 'wrap' }}>
      {[[aRef, 'layer A: rule 77 or 55, chosen per cell by B', 'layer A shown'],
        [bRef, 'layer B: rule 44 or 23, chosen per cell by A', 'layer B shown']].map(([ref, label, note]) => (
        <div key={label} style={{ width: 160 }}>
          <canvas className="gc-field" ref={ref} style={{ width: 160, height: 160 }}></canvas>
          <div className="gc-mono" style={{ fontSize: '0.66rem', color: INK_SOFT, marginTop: 3 }}>{label}</div>
          <div style={{ marginTop: '0.25rem' }}><RunSig sig={{ engine: 'A⇄B', note }} /></div>
        </div>
      ))}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
        <button onClick={() => setSeed((s) => s + 1)} className="gc-mono"
          style={{ fontSize: '0.72rem', fontWeight: 700, padding: '0.4rem 0.8rem', borderRadius: 7, border: '1px solid var(--rule)', background: '#fff', color: INK_SOFT, cursor: 'pointer' }}>
          reroll ↻
        </button>
        <a href={buildSeedUrl([
          { id: 1, type: 'prehoc', dim: '1d', ruleA0: 77, ruleA1: 55, ruleB0: 44, ruleB1: 23, layer: 'a', ic: seedRow(100, 9), icB: seedRow(100, 77), steps: 100, color: EXPLORE_COLORS.cream },
          { id: 2, type: 'prehoc', dim: '1d', ruleA0: 77, ruleA1: 55, ruleB0: 44, ruleB1: 23, layer: 'b', ic: seedRow(100, 9), icB: seedRow(100, 77), steps: 100, color: EXPLORE_COLORS.teal },
          { id: 3, type: 'prehoc', dim: '1d', ruleA0: 77, ruleA1: 55, ruleB0: 44, ruleB1: 23, layer: 'diff', ic: seedRow(100, 9), icB: seedRow(100, 77), steps: 100, color: EXPLORE_COLORS.purple },
        ])} className="gc-mono" style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--accent)', textDecoration: 'none' }}>
          Explore this &rarr;
        </a>
      </div>
    </div>
  );
}

// Compact live demo of state-gated rule transport (non-uniform CA) --
// mechanism here, findings on the questions page.
function RuleFieldMiniDemo() {
  const [seed, setSeed] = useState(2);
  const engineRef = useRef(null);
  const stateRef = useRef(null);
  const rulesRef = useRef(null);

  useEffect(() => {
    let cancelled = false;
    import('../lib/groovy-engine.js').then((engine) => {
      if (cancelled) return;
      engineRef.current = engine;
      draw();
    });
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  useEffect(() => { draw(); });

  function draw() {
    const engine = engineRef.current;
    if (!engine) return;
    const { randomState, mulberry32, gatedDiffusionTrajectory, renderFieldToCanvas, renderByteFieldToCanvas } = engine;
    const s0 = randomState(90, seed);
    const rng = mulberry32(seed + 40);
    const rf0 = Array.from({ length: 90 }, () => Math.floor(rng() * 256));
    const res = gatedDiffusionTrajectory(s0, rf0, 90);
    if (stateRef.current) renderFieldToCanvas(stateRef.current, res.states, ON_COLOR, '#f1ead9');
    if (rulesRef.current) renderByteFieldToCanvas(rulesRef.current, res.rules);
  }

  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1.2rem', flexWrap: 'wrap' }}>
      {[[stateRef, 'the state, each cell under its own rule', 'state layer shown'],
        [rulesRef, 'the rule field — one color per rule value', 'rule layer shown']].map(([ref, label, note]) => (
        <div key={label} style={{ width: 160 }}>
          <canvas className="gc-field" ref={ref} style={{ width: 160, height: 160 }}></canvas>
          <div className="gc-mono" style={{ fontSize: '0.66rem', color: INK_SOFT, marginTop: 3 }}>{label}</div>
          <div style={{ marginTop: '0.25rem' }}><RunSig sig={{ engine: 'S⇄R', note }} /></div>
        </div>
      ))}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
        <button onClick={() => setSeed((s) => s + 1)} className="gc-mono"
          style={{ fontSize: '0.72rem', fontWeight: 700, padding: '0.4rem 0.8rem', borderRadius: 7, border: '1px solid var(--rule)', background: '#fff', color: INK_SOFT, cursor: 'pointer' }}>
          reroll ↻
        </button>
        <a href={buildSeedUrl([
          { id: 1, type: 'rulefield', dim: '1d', scheme: 'left', layer: 'state', ic: seedRow(100, 21), ruleField: seedBytes(100, 55), steps: 100, color: EXPLORE_COLORS.cream },
          { id: 2, type: 'rulefield', dim: '1d', scheme: 'left', layer: 'rules', ic: seedRow(100, 21), ruleField: seedBytes(100, 55), steps: 100, color: EXPLORE_COLORS.red },
        ])} className="gc-mono" style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--accent)', textDecoration: 'none' }}>
          Explore this &rarr;
        </a>
      </div>
    </div>
  );
}

export default function Concepts() {
  const [rule, setRule] = useState(110);
  const [ruleInputText, setRuleInputText] = useState('110');
  const [initState, setInitState] = useState(() => defaultInitState(N_CELLS));
  const [xorA, setXorA] = useState(0);
  const [xorB, setXorB] = useState(1);
  const [pairIdx, setPairIdx] = useState(2);
  const [secondOrderStatus, setSecondOrderStatus] = useState('computing…');
  const [isStuck, setIsStuck] = useState(false);
  const [ruleDetailOpen, setRuleDetailOpen] = useState(true);
  const [mobileSheetOpen, setMobileSheetOpen] = useState(false);
  const [breakoutLeft, setBreakoutLeft] = useState(0);
  const [viewportWidth, setViewportWidth] = useState(0);
  const [headerHeight, setHeaderHeight] = useState(58);
  const [engineReady, setEngineReady] = useState(false);
  const [computed, setComputed] = useState(null);

  const engineRef = useRef(null);
  const sentinelRef = useRef(null);
  const caRef = useRef(null);
  const miniDRef = useRef(null);
  const miniARef = useRef(null);
  const secondOrderRef = useRef(null);
  const pairRef = useRef(null);
  // Kept in sync with headerHeight state, but read from the setInterval
  // poll below -- that closure is created once on mount and would otherwise
  // never see header-height updates from later resizes.
  const headerHeightRef = useRef(58);

  const measureBreakout = useCallback(() => {
    if (!sentinelRef.current) return;
    const rect = sentinelRef.current.getBoundingClientRect();
    setBreakoutLeft(rect.left);
    setViewportWidth(window.innerWidth);
    // The nav wraps to two lines below ~480px, so its real height varies --
    // a hardcoded top offset leaves this panel's sticky bits rendering
    // partly underneath the (higher z-index) nav on narrow screens.
    const header = document.querySelector('.gc-header');
    if (header) {
      const h = header.getBoundingClientRect().height;
      setHeaderHeight(h);
      headerHeightRef.current = h;
    }
  }, []);

  useEffect(() => {
    import('../lib/groovy-engine.js').then((engine) => {
      engineRef.current = engine;
      setEngineReady(true);
    });
    measureBreakout();
    window.addEventListener('resize', measureBreakout);
    const stickyPoll = setInterval(() => {
      if (!sentinelRef.current) return;
      const stuck = sentinelRef.current.getBoundingClientRect().top <= headerHeightRef.current;
      setIsStuck((prev) => (prev === stuck ? prev : stuck));
    }, 120);
    return () => {
      clearInterval(stickyPoll);
      window.removeEventListener('resize', measureBreakout);
    };
  }, [measureBreakout]);

  // ---- redraw single-rule views whenever rule or initState changes ----
  useEffect(() => {
    if (!engineReady) return;
    const { evolveTrajectory, dTrajectory, d2Trajectory, gTrajectory, deTrajectory, edTrajectory,
      absentialTrajectory, runSecondOrder, verifySecondOrderReversible, renderFieldToCanvas } = engineRef.current;
    const s0 = Uint8Array.from(initState);

    const raw = evolveTrajectory(s0, rule, STEPS);
    if (caRef.current) renderFieldToCanvas(caRef.current, raw, ON_COLOR, '#f1ead9');

    const dField = dTrajectory(s0, rule, STEPS);
    if (miniDRef.current) renderFieldToCanvas(miniDRef.current, dField, ACCENT, '#f1ead9');
    const d2Field = d2Trajectory(s0, rule, STEPS);
    const gField = gTrajectory(s0, rule, STEPS);
    const deField = deTrajectory(s0, rule, STEPS);
    const edField = edTrajectory(s0, rule, STEPS);
    const absField = absentialTrajectory(s0, rule, STEPS);
    if (miniARef.current) renderFieldToCanvas(miniARef.current, absField, 'oklch(0.6 0.14 75)', '#f1ead9');
    // V(S) = NOT(S OR A(S)) -- void is whatever's left once live and
    // absential cells are accounted for (see the partition note below).
    const voidField = raw.map((row, t) => {
      const out = new Uint8Array(row.length);
      for (let i = 0; i < row.length; i++) out[i] = (row[i] || absField[t][i]) ? 0 : 1;
      return out;
    });
    // The #run section's engine field: U[t] = (D∘E)^{t+1}(S0) XOR
    // (E∘D)^{t+1}(S0) -- the same two composites as the G gallery, but each
    // iterated on its OWN output (run(F, F)) instead of measured along E's
    // orbit. Row 0 equals G(S0) exactly; the two constructions then part ways.
    const { applyRule, D: Dop, C: Cop, orbit } = engineRef.current;
    const deMap = (s) => Dop(applyRule(s, rule), rule);   // D o E
    const edMap = (s) => applyRule(Dop(s, rule), rule);   // E o D
    const pRows = orbit(deMap, s0, STEPS).slice(1);
    const qRows = orbit(edMap, s0, STEPS).slice(1);
    const uField = pRows.map((row, t) => Cop(row, qRows[t]));
    setComputed({ raw, d: dField, d2: d2Field, g: gField, de: deField, ed: edField, absential: absField, void: voidField, u: uField });

    const soTraj = runSecondOrder(s0, s0, rule, STEPS);
    if (secondOrderRef.current) renderFieldToCanvas(secondOrderRef.current, soTraj, 'oklch(0.5 0.12 230)', '#f1ead9');
    const reversible = verifySecondOrderReversible(soTraj, rule);
    setSecondOrderStatus(
      reversible
        ? 'confirmed — ran the recurrence backward from the final two states and recovered every earlier state exactly.'
        : 'mismatch found (unexpected — please report this).'
    );
  }, [engineReady, rule, initState]);

  // ---- redraw the cross-rule pair view whenever the preset changes ----
  useEffect(() => {
    if (!engineReady) return;
    const { divergenceTrajectory, randomState, renderFieldToCanvas } = engineRef.current;
    const preset = PAIR_PRESETS[pairIdx];
    const s0 = randomState(N_CELLS, 11);
    const field = divergenceTrajectory(s0, preset.a, preset.b, STEPS);
    if (pairRef.current) renderFieldToCanvas(pairRef.current, field, REGIME_CANVAS_COLOR[preset.regime], '#f1ead9');
  }, [engineReady, pairIdx]);

  function selectRule(num) {
    const clamped = Math.max(0, Math.min(255, num | 0));
    setRule(clamped);
    setRuleInputText(String(clamped));
  }
  function toggleOutputBit(idx) { selectRule(rule ^ (1 << idx)); }
  function handleRuleInputChange(e) {
    const text = e.target.value;
    setRuleInputText(text);
    const n = parseInt(text, 10);
    // Clamp the live rule immediately (so every keystroke gives valid
    // behavior), but leave the displayed text alone until blur -- snapping
    // it mid-typing would make it impossible to type e.g. "200" one digit
    // at a time.
    if (!isNaN(n)) setRule(Math.max(0, Math.min(255, n | 0)));
  }
  function handleRuleInputBlur() {
    const n = parseInt(ruleInputText, 10);
    const clamped = isNaN(n) ? rule : Math.max(0, Math.min(255, n | 0));
    setRule(clamped);
    setRuleInputText(String(clamped));
  }
  function toggleCell(i) {
    setInitState((s) => { const arr = s.slice(); arr[i] = arr[i] ? 0 : 1; return arr; });
  }
  function rerollInit() {
    setInitState(Array.from({ length: N_CELLS }, () => (Math.random() < 0.5 ? 0 : 1)));
  }

  const activeRule = RULE_CATALOG.find((r) => r.num === rule);
  const xorResult = xorA ^ xorB;
  const selectedPreset = PAIR_PRESETS[pairIdx];
  const isAffine = engineReady ? engineRef.current.isAffineRule(rule) : null;
  const selectedGlyphs = engineReady ? engineRef.current.ruleNeighborhoods(rule) : [];

  // Sticky is actively hostile on narrow screens: expanded, this panel is
  // tall enough to cover the entire viewport while pinned, blocking every
  // section it's supposed to accompany. Below the breakpoint it just scrolls
  // with the page like anything else -- scroll up if you want it again.
  const isNarrowViewport = viewportWidth > 0 && viewportWidth < 640;
  const stickyPanelStyle = isNarrowViewport
    ? {
        position: 'static',
        borderTop: '3px solid var(--accent)', borderBottom: '1px solid var(--rule)', background: '#fff',
      }
    : {
        position: 'sticky', top: headerHeight, zIndex: 5,
        borderTop: '3px solid var(--accent)', borderBottom: '1px solid var(--rule)', background: '#fff',
        transition: 'width 0.2s ease, margin-left 0.2s ease, box-shadow 0.2s ease',
        ...(isStuck
          ? { width: viewportWidth, marginLeft: -breakoutLeft, boxShadow: '0 6px 16px rgba(42,36,32,0.16)' }
          : { width: '100%', marginLeft: 0, boxShadow: 'none' }),
      };

  // Shared pieces reused by both the desktop sticky panel and the mobile
  // "chip + full-screen sheet" version below -- same controls, different
  // wrapper.
  const ruleAndPicksRow = (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap', marginBottom: '0.6rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap' }}>
        <span className="gc-mono" style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--ink-soft)' }}>Rule</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: 2 }} title="click a digit to flip that bit">
          {selectedGlyphs.map((nb, i) => (
            <button key={nb.idx} onClick={() => toggleOutputBit(nb.idx)} className="gc-mono"
              style={{
                width: 16, height: 18, padding: 0, cursor: 'pointer', fontSize: '0.72rem', fontWeight: 700, lineHeight: 1,
                background: nb.out ? ON_COLOR : OFF_COLOR, color: nb.out ? OFF_COLOR : ON_COLOR,
                border: '1.5px solid var(--accent)',
                marginRight: i === 3 ? 4 : 0,
              }}>{nb.out}</button>
          ))}
        </div>
        <span className="gc-mono" style={{ fontSize: '0.85rem', color: 'var(--ink-soft)' }}>=</span>
        <input type="number" min="0" max="255" value={ruleInputText} onChange={handleRuleInputChange} onBlur={handleRuleInputBlur}
          className="gc-mono" style={{ width: '4rem', fontSize: '1rem', fontWeight: 700, textAlign: 'center', padding: '0.35rem 0.3rem', borderRadius: 6, border: '1px solid var(--accent)', background: '#fff', color: 'var(--ink)' }} />
        <span className="gc-mono" style={{ fontSize: '0.72rem', color: 'var(--ink-soft)' }}>(0&ndash;255)</span>
      </div>

      <div className="gc-mono" style={{ fontSize: '0.7rem', color: 'var(--ink-soft)' }}>
        quick picks:{' '}
        {RULE_CATALOG.map((r, i) => {
          const active = r.num === rule;
          return (
            <span key={r.num}>
              <button onClick={() => selectRule(r.num)} className="gc-mono" style={{ fontSize: '0.78rem', fontWeight: 700, padding: 0, border: 'none', background: 'none', cursor: 'pointer', textDecoration: active ? 'underline' : 'none', color: active ? ACCENT : INK_SOFT }}>{r.num}</button>
              {i < RULE_CATALOG.length - 1 ? ' · ' : ''}
            </span>
          );
        })}
      </div>
    </div>
  );

  const startingRowInner = (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
      <span className="gc-mono" style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--ink-soft)' }}>Starting row:</span>
      <div style={{ display: 'flex', gap: 1 }}>
        {initState.map((bit, i) => (
          <button key={i} onClick={() => toggleCell(i)} style={{ width: 9, height: 9, padding: 0, border: '1px solid var(--ink)', background: bit ? ON_COLOR : OFF_COLOR, cursor: 'pointer', flex: 'none' }}></button>
        ))}
      </div>
      <button onClick={rerollInit} className="gc-mono" style={{ fontSize: '0.68rem', fontWeight: 700, background: 'none', border: '1px solid var(--rule)', borderRadius: 4, color: 'var(--accent)', cursor: 'pointer', padding: '2px 8px' }}>randomize</button>
    </div>
  );

  const glyphAndThumbsRow = (
    <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', alignItems: 'flex-end', justifyContent: 'space-between', marginTop: '0.8rem' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, auto)', gap: '4px 10px' }}>
        {selectedGlyphs.map((nb) => (
          <div key={nb.idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
            <span className="gc-mono" style={{ fontSize: '0.6rem', color: 'var(--ink-soft)' }}>{nb.idx}</span>
            <RuleGlyph l={nb.l} c={nb.c} r={nb.r} out={nb.out} outlined size={13} onToggleOut={() => toggleOutputBit(nb.idx)} />
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <MiniLinkThumb href="#phi-formal" canvasRef={caRef} label="E(S)" />
        <MiniLinkThumb href="#comparison-differentiation" canvasRef={miniDRef} label="D(S)" />
        <MiniLinkThumb href="#absential" canvasRef={miniARef} label="A(S)" />
      </div>
    </div>
  );

  const statsRowInner = (
    <div className="gc-mono" style={{ display: 'flex', gap: '1.6rem', flexWrap: 'wrap', fontSize: '0.74rem', color: 'var(--ink-soft)' }}>
      <span>rule <strong style={{ color: 'var(--ink)' }}>{rule}</strong></span>
      <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4em' }}>
        class{' '}
        <strong style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4em', color: 'var(--ink)' }}>
          <span style={{ width: 8, height: 8, borderRadius: 99, flex: 'none', background: activeRule && activeRule.cls ? CLASS_COLOR[activeRule.cls] : CLASS_COLOR_UNKNOWN }}></span>
          {activeRule && activeRule.cls ? activeRule.cls : 'unclassified'}
        </strong>
      </span>
      <span>affine (GF2) <strong style={{ color: 'var(--ink)' }}>{isAffine === null ? '…' : isAffine ? 'yes' : 'no'}</strong></span>
      <span>density <strong style={{ color: 'var(--ink)' }}>{selectedGlyphs.reduce((n, g) => n + g.out, 0)}/8 on</strong></span>
    </div>
  );

  return (
    <>
      <Nav active="concepts" />
      <Watermark title="AI-written prose, live-computed demos">
        {' '}The writing on this page was generated by an LLM. The little widgets below it are not: they run the
        real <code className="gc-code">groovy</code> math (XOR, the rule lookup table, the commutator) live in your
        browser, reimplemented from the <a href="https://github.com/mbilokonsky/groovy-commutator">Python source</a>.
        Check that source if anything here matters to you.
      </Watermark>

      <main style={{ maxWidth: 880, margin: '0 auto', padding: '2rem 1.25rem 4rem' }}>

        <div className="gc-mono" style={{ textTransform: 'uppercase', letterSpacing: '.09em', fontSize: '0.78rem', fontWeight: 700, color: 'var(--accent)', marginBottom: '0.5em' }}>concepts</div>
        <h1 style={{ fontFamily: "'Lora',serif", fontSize: 'clamp(1.8rem,5vw,2.4rem)', lineHeight: 1.25, margin: '0 0 0.4em', fontWeight: 600 }}>The building blocks, one at a time</h1>
        <p style={{ fontSize: '1.05rem', color: 'var(--ink-soft)', margin: '0 0 1.4em', maxWidth: '62ch' }}>
          Everything on this site is built from a handful of small pieces. None of them are individually complicated
          &mdash; play with each one before moving to the next.
        </p>

        <nav style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', margin: '0 0 2rem' }}>
          {TOC.map(([href, label]) => <a key={href} href={href} style={pill}>{label}</a>)}
        </nav>

        {/* BOOLEAN SPACE -- the arithmetic, before anything is built with it */}
        <section id="boolean" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={sectionKicker}>Substrate</div>
          <h2 style={h2Style}>Boolean space</h2>
          <p style={pBody}>
            Everything on this site happens in boolean space: every quantity is a single bit &mdash; 0 or 1, off
            or on. No decimals, no negatives, no "almost." That changes what math even is. With only two values,
            operations stop being arithmetic you carry digits through and become <strong>logic gates</strong>:
            AND (1 if both inputs are 1), OR (1 if either is), NOT (flip the bit). Any boolean function, however
            elaborate, is some wiring of gates like these &mdash; including every rule on this page.
          </p>
          <p style={pBody}>
            One gate carries most of the weight here: <strong>XOR</strong> (&oplus;), 1 exactly where its two
            inputs disagree. Click the two bits:
          </p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem', flexWrap: 'wrap' }}>
            <button onClick={() => setXorA(xorA ? 0 : 1)} className="gc-mono" style={{ fontWeight: 800, fontSize: '1.3rem', width: 54, height: 54, borderRadius: 8, border: '1px solid var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', background: xorA ? ON_COLOR : OFF_COLOR, color: xorA ? '#faf7f0' : '#2a2420', cursor: 'pointer' }}>{xorA}</button>
            <span className="gc-mono" style={{ fontSize: '1.1rem', color: 'var(--ink-soft)' }}>&oplus;</span>
            <button onClick={() => setXorB(xorB ? 0 : 1)} className="gc-mono" style={{ fontWeight: 800, fontSize: '1.3rem', width: 54, height: 54, borderRadius: 8, border: '1px solid var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', background: xorB ? ON_COLOR : OFF_COLOR, color: xorB ? '#faf7f0' : '#2a2420', cursor: 'pointer' }}>{xorB}</button>
            <span className="gc-mono" style={{ fontSize: '1.1rem', color: 'var(--ink-soft)' }}>=</span>
            <div className="gc-mono" style={{ fontWeight: 800, fontSize: '1.3rem', width: 54, height: 54, borderRadius: 8, border: '1px solid var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', background: xorResult ? ON_COLOR : OFF_COLOR, color: xorResult ? '#faf7f0' : '#2a2420' }}>{xorResult}</div>
          </div>
          <p style={{ ...pBody, marginTop: '1.1rem', marginBottom: 0 }}>
            XOR earns that job two ways. It's a <em>difference detector</em>: XOR two whole rows bit by bit and
            you get a map of exactly where they disagree. And it's <em>its own inverse</em>: XOR the difference
            back in and you're home again (<code className="gc-code">a &oplus; b &oplus; b = a</code>) &mdash;
            nothing is ever lost. It's also just addition, if addition wraps: 1 + 1 = 0, no carrying.
            Mathematicians call that arithmetic GF(2), "the two-element field." Whenever a later section says{' '}
            <em>compare</em>, <em>integrate</em>, or <em>couple</em>, the machinery underneath is this one gate.
          </p>
        </section>

        {/* CELLULAR AUTOMATA -- general definition, then 1D, then 2D as commentary */}
        <section id="ca" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={sectionKicker}>Substrate</div>
          <h2 style={h2Style}>Cellular automata</h2>
          <p style={pBody}>
            A cellular automaton is a regular grid of cells, each holding a small value (here, just 0 or 1), all
            updating together, forever, according to one shared rule that only ever looks at a cell's local
            neighborhood &mdash; never the whole grid. The grid itself can have any number of dimensions: a line, a
            2D plane, a 3D lattice. The definition doesn't care. What changes as dimension goes up is how big the
            neighborhood is, and how much rule-space there is to explore.
          </p>

          <h3 style={h3Style}>In one dimension</h3>
          <p style={pBody}>
            Start with the simplest case: a single row of cells, arranged in a circle so the last cell's right
            neighbor wraps back around to the first. Each tick, every cell looks at itself and its two immediate
            neighbors &mdash; three cells, eight possible on/off combinations, conventionally listed all-on down to
            all-off (111, 110, 101, 100, 011, 010, 001, 000). A rule is nothing more than a table of eight
            outputs, one per combination. Read those eight outputs off in that order as a binary number and you get
            the <strong>rule number</strong> &mdash; rule 110, rule 30, rule 90, and so on. 256 possible rules
            total. The interactive rule-builder below shows exactly this table: eight small diagrams, three cells on
            the left (the neighborhood, fixed) and one cell on the right (the output, click to flip it and build
            your own rule live).
          </p>

          <RuleWalkthrough />

          <h3 style={h3Style}>Four rough classes</h3>
          <p style={pBody}>
            Wolfram's informal classification of what a rule does, long-run, run from one random starting row:
          </p>
          <ClassExamples />
          <p style={pBody}>
            Class I dies out to a fixed pattern, Class II settles into small repeating cycles, Class III looks like
            noise, and Class IV sits in between &mdash; structured, but not obviously periodic. These labels are
            informal, not rigorous &mdash; see <code className="gc-code">classify.py</code>. Treat them as a
            starting vocabulary, not ground truth.
          </p>

          <h3 style={h3Style}>In more than one dimension</h3>
          <p style={pBody}>
            The same idea generalizes straightforwardly to a grid: each cell looks at its 8 neighbors (the Moore
            neighborhood) instead of 2. Listing outputs for a 512-entry table by hand is unwieldy, so 2D rules are
            usually specified by neighbor <em>count</em> instead of exact pattern &mdash; "born on N neighbors,
            survive on M" (<strong>B/S notation</strong>). Conway's Life is B3/S23. One conventional difference in
            how these get drawn: 1D CA are usually shown with time running down the page, since the row itself
            already fills the horizontal axis; 2D CA use both spatial axes for space, so time has to play out as an
            actual animation instead. Here's Life running on its own, no controls, just for texture:
          </p>
          <AmbientCA2D size={180} />
          <p style={{ ...pBody, marginTop: '1.1rem' }}>
            Rule-space also explodes fast with dimension. 1D elementary CA have 256 possible rules; the B/S family
            of 2D rules alone has 512 &times; 512 = 262,144; a rule sensitive to the exact 2D neighborhood pattern
            (the direct analog of the 1D lookup table, but for 9 cells instead of 3) would have 2<sup>512</sup> of
            them &mdash; a number too large to be worth writing out.
          </p>
          <p style={pBody}>
            Everything below works the 1D case by hand, since it's small enough to see clearly &mdash; but every
            instrument here (derivative, commutator, absential field, reversible memory) is defined identically
            regardless of dimension; only the neighborhood changes. The{' '}
            <a href="explorer.html" style={{ color: 'var(--accent)' }}>explorer</a> lets you build and couple 2D
            rules the same way as 1D.
          </p>

        </section>

        {/* STATE -> STATE -- before any instrument exists: the shape contract everything obeys */}
        <section id="state" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={sectionKicker}>Foundation</div>
          <h2 style={h2Style}>Everything is State &rarr; State</h2>
          <p style={pBody}>
            One step of a rule takes a row of <code className="gc-code">n</code> bits in and returns{' '}
            <em>another row of n bits</em> out. So does every instrument this page builds later: row in, row out,
            same length. Nothing compresses, expands, or reinterprets the state &mdash; which is what makes every
            instrument stackable, comparable, and renderable the same way, and what makes an open-ended{' '}
            <a href="explorer.html" style={{ color: 'var(--accent)' }}>explorer</a> possible at all: nothing needs
            a bespoke UI per instrument, because every instrument is the same shape of thing.
          </p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem', flexWrap: 'wrap' }}>
            <div className="gc-mono" style={{ fontSize: '0.8rem', fontWeight: 700, padding: '0.6rem 0.9rem', border: '1px solid var(--rule)', borderRadius: 7, background: '#fff' }}>State (n bits)</div>
            <span style={{ color: 'var(--accent)', fontSize: '1.1rem' }}>&rarr;</span>
            <div className="gc-mono" style={{ fontSize: '0.8rem', fontWeight: 700, padding: '0.6rem 0.9rem', border: '1px solid var(--accent)', borderRadius: 7, background: 'var(--accent-soft)', color: 'var(--accent-dark)' }}>map</div>
            <span style={{ color: 'var(--accent)', fontSize: '1.1rem' }}>&rarr;</span>
            <div className="gc-mono" style={{ fontSize: '0.8rem', fontWeight: 700, padding: '0.6rem 0.9rem', border: '1px solid var(--rule)', borderRadius: 7, background: '#fff' }}>State (n bits)</div>
          </div>
          <p style={{ ...pBody, marginTop: '1.1rem', marginBottom: 0 }}>
            A map is one tick. Every picture on this page has hundreds of rows &mdash; so one more operation needs
            a name: the one that turns a map into a picture.
          </p>
        </section>

        {/* EVERY PICTURE IS A RUN -- orbit and run, taught before any calculus exists */}
        <section id="run" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={sectionKicker}>Foundation</div>
          <h2 style={h2Style}>Every picture is a run</h2>
          <p style={pBody}>
            Every diagram so far was built by repetition: take a seed row, apply the rule, apply it again, and
            stack the rows as they come. Name the pieces:
          </p>
          <Defn lines={[
            { parts: [
                { t: 'rule 110', r: 'rule', g: <>an eight-entry lookup table &mdash; the same kind the builder above edits. It knows nothing about rows or time; it is just these eight facts: <GlyphRow rule={110} /></> },
              ], note: 'a table' },
            { parts: [
                { t: 'E₁₁₀', r: 'walk', g: 'one step: the table applied to every cell of a row at once. Row in, row out — a State → State map. E for evolve.' },
                { t: '(S)', r: 'state' },
              ], note: 'a map — one tick' },
            { parts: [
                { t: 'orbit', g: 'feed the output back in as the next input, forever. The collected rows are the orbit.' },
                { t: '(' },
                { t: 'E₁₁₀' },
                { t: ', ' },
                { t: 'seed' },
                { t: ') = ' },
                { t: 'seed' },
                { t: ', ' },
                { t: 'E₁₁₀' },
                { t: '(' },
                { t: 'seed' },
                { t: '), ' },
                { t: 'E₁₁₀' },
                { t: '(' },
                { t: 'E₁₁₀' },
                { t: '(' },
                { t: 'seed' },
                { t: ')), …' },
              ], note: 'a history' },
          ]} />
          <p style={pBody}>
            The <strong>orbit</strong> is output fed back as input: row zero is the seed, every next row is the
            map applied to the row above. Every triangle on this page is an orbit. Two things to hold on to: an
            orbit belongs to exactly <em>one</em> map &mdash; &ldquo;whose orbit is this?&rdquo; is always a fair
            question about any picture &mdash; and the orbit is the only place repetition lives. Everything else
            on this page fires once per row.
          </p>
          <Defn lines={[
            { parts: [
                { t: 'id', r: 'watch', g: 'the do-nothing map: returns its input unchanged.' },
                { t: '(S) = S' },
              ], note: 'the do-nothing map' },
            { parts: [
                { t: 'run' },
                { t: '(' },
                { t: 'gauge' },
                { t: ', ' },
                { t: 'base' },
                { t: ') = ' },
                { t: 'gauge' },
                { t: '(' },
                { t: 'seed' },
                { t: '), ' },
                { t: 'gauge' },
                { t: '(' },
                { t: 'base' },
                { t: '(' },
                { t: 'seed' },
                { t: ')), ' },
                { t: 'gauge' },
                { t: '(' },
                { t: 'base' },
                { t: '(' },
                { t: 'base' },
                { t: '(' },
                { t: 'seed' },
                { t: '))), …' },
              ], note: 'one map walks, another watches' },
          ]} />
          <p style={pBody}>
            <strong>run</strong> splits picture-making into two jobs. The <strong>base</strong> walks: it's the
            map applied over and over, exactly as in the orbit. The <strong>gauge</strong> watches: it looks at
            each footprint once, and what it reports is what gets drawn. The plain diagram is{' '}
            <RunSig sig={{ gauge: 'id', base: 'E_110' }} /> &mdash; walk with rule 110, report every footprint
            unchanged. Keep the walk and swap the watcher, and the same history draws a different picture:
          </p>
          <RunExamples />
          <p style={{ ...pBody, marginTop: '1.1rem', marginBottom: 0 }}>
            From here on, every field on this page carries a badge naming its gauge and its base &mdash; amber
            for what walks, teal for what watches. The{' '}
            <a href="explorer.html" style={{ color: 'var(--accent)' }}>explorer</a> is built on exactly this
            split: a source card is a base, and every transform card stacked on one is a gauge &mdash; stacking
            cards is building runs. So far the only watchers are trivial. The next section builds ones worth the
            name.
          </p>
        </section>

        <hr style={{ border: 'none', borderTop: '1px solid var(--rule)', margin: 0 }} />

        {/* RULE + STARTING-ROW PANEL, shared by everything below through Instruments.
            Desktop: sticky, collapsible. Mobile: a small persistent chip that opens
            a full-screen sheet, since sticky-and-expanded is tall enough to cover
            the whole viewport on a phone -- see isNarrowViewport above. */}
        <div style={{ position: 'relative' }}>
          <div ref={sentinelRef} style={{ height: 1 }}></div>

          {isNarrowViewport ? (
            <>
              <div style={{ position: 'sticky', top: headerHeight, zIndex: 5, background: '#fff', borderTop: '3px solid var(--accent)', borderBottom: '1px solid var(--rule)' }}>
                <button onClick={() => setMobileSheetOpen(true)} className="gc-mono" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%', padding: '0.6rem 1.25rem', background: 'none', border: 'none', cursor: 'pointer', fontSize: '0.85rem', fontWeight: 700, color: 'var(--ink)' }}>
                  <span>Rule {rule}</span>
                  <span style={{ color: 'var(--accent)', fontSize: '0.72rem' }}>edit &#9656;</span>
                </button>
              </div>

              {/* display-toggled, not unmounted, so the mini canvases inside
                  keep their drawn pixels between opens instead of flashing
                  blank while the next redraw catches up. */}
              <div style={{ display: mobileSheetOpen ? 'block' : 'none', position: 'fixed', inset: 0, zIndex: 50, background: '#fff', overflowY: 'auto', padding: '1rem 1.25rem 2rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
                  <span className="gc-mono" style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--ink-soft)', textTransform: 'uppercase', letterSpacing: '.05em' }}>Rule editor</span>
                  <button onClick={() => setMobileSheetOpen(false)} className="gc-mono" style={{ fontSize: '0.85rem', fontWeight: 700, background: 'none', border: '1px solid var(--rule)', borderRadius: 6, padding: '0.3rem 0.7rem', cursor: 'pointer', color: 'var(--ink)' }}>&times; close</button>
                </div>
                {ruleAndPicksRow}
                {startingRowInner}
                {glyphAndThumbsRow}
                <div style={{ marginTop: '0.8rem', paddingTop: '0.6rem', borderTop: '1px dashed var(--rule)' }}>
                  {statsRowInner}
                </div>
              </div>
            </>
          ) : (
            <div style={stickyPanelStyle}>
              <div style={{ maxWidth: 880, margin: '0 auto', padding: '0.8rem 1.25rem 0.9rem' }}>
                {ruleAndPicksRow}

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: ruleDetailOpen ? 'flex-start' : 'space-between', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {startingRowInner}
                  {!ruleDetailOpen && (
                    <button onClick={() => setRuleDetailOpen(true)} className="gc-mono" style={{ display: 'flex', alignItems: 'center', gap: '0.3em', fontSize: '0.68rem', fontWeight: 700, color: 'var(--ink-soft)', background: 'none', border: 'none', cursor: 'pointer', padding: '2px 0' }}>
                      <span>&#9656;</span> show rule table
                    </button>
                  )}
                </div>

                {/* Canvas stays mounted (display toggled, not unmounted) so its
                    drawn content survives collapsing the panel -- otherwise
                    reopening would show a blank square until the next redraw. */}
                <div style={{ display: ruleDetailOpen ? 'block' : 'none' }}>
                  {glyphAndThumbsRow}
                </div>

                {ruleDetailOpen && (
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap', marginTop: '0.8rem', paddingTop: '0.6rem', borderTop: '1px dashed var(--rule)' }}>
                    {statsRowInner}
                    <button onClick={() => setRuleDetailOpen(false)} className="gc-mono" style={{ display: 'flex', alignItems: 'center', gap: '0.3em', fontSize: '0.68rem', fontWeight: 700, color: 'var(--ink-soft)', background: 'none', border: 'none', cursor: 'pointer', padding: '2px 0' }}>
                      <span style={{ display: 'inline-block', transform: 'rotate(90deg)' }}>&#9656;</span> hide rule table
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          <section style={{ padding: '1.6rem 0' }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1.4rem', flexWrap: 'wrap' }}>
              <p style={{ fontSize: '0.92rem', color: 'var(--ink-soft)', maxWidth: '60ch', margin: 0 }}>
                Fixed examples end here. This panel stays pinned through the sections below: build any rule
                (click the bits, or type a number 0&ndash;255), edit the starting row, and every field that
                follows recomputes from your choices, live.
              </p>
            </div>
          </section>

          {/* BOOLEAN CALCULUS */}
          <section id="calculus" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
            <div style={sectionKicker}>Foundation</div>
            <h2 style={h2Style}>Boolean calculus</h2>
            <p style={pBody}>
              The watchers worth having are built from two ingredients the page already has: the rule table, and
              XOR. First, the table lookup written as a formula:
            </p>

            <h3 id="phi-formal" style={h3Style}>Neighborhoods and rules, formally</h3>
            <Defn lines={[
              { parts: [
                  { t: <>&phi;(S)<sub>i</sub></>, r: 'rule', k: 'φ(S)ᵢ', g: 'cell i of the row the rule produces: look the neighborhood up in the table, write down the answer.' },
                  { t: ' = ' },
                  { t: <>R<sub>4&middot;S(i&minus;1) + 2&middot;S(i) + S(i+1)</sub></>, r: 'rule', k: 'R[…]', g: <>the rule's eight-entry table, indexed by reading cell i's neighborhood (left, self, right) as a binary number 0&ndash;7. For rule {rule} &mdash; the table the pinned panel is editing right now: <GlyphRow rule={rule} /></> },
                ], note: "one cell's next value" },
            ]} />
            <p style={pBody}>
              This is the rule-table lookup from above, written as a formula instead of a diagram: read cell i's own
              three-cell neighborhood off <Op>S</Op> (left, self, right), treat those three
              bits as a binary number 0&ndash;7, and use that number to index into the rule's eight-entry table{' '}
              <Op>R</Op> &mdash; exactly the lookup the worked example above walked through
              by hand, and exactly what the rule-builder's eight little diagrams show, one entry each.{' '}
              <Op>φ(S)</Op> (no subscript) means doing that for every cell{' '}
              <code className="gc-code">i</code> at once, producing a whole new row the same length as{' '}
              <Op>S</Op>. Every formula from here on treats <Op>φ</Op>{' '}
              as a given, already-understood building block &mdash; one call evolves an entire state by one step.
            </p>

            <h3 id="comparison-differentiation" style={h3Style}>Comparison and differentiation</h3>
            <Defn lines={[
              { parts: [
                  { t: 'C', r: 'watch', g: 'comparison: XOR two rows, bit by bit. 1 marks every position where they disagree.' },
                  { t: '(a, b) = a ⊕ b' },
                ], note: 'comparison' },
              { parts: [
                  { t: 'D', r: 'watch', g: 'the derivative: compare a state against what the rule makes of it. 1 marks every cell about to change.' },
                  { t: '(S) = ' },
                  { t: 'C', r: 'watch' },
                  { t: '(S, ' },
                  { t: 'φ', r: 'rule' },
                  { t: '(S)) = S ⊕ ' },
                  { t: 'φ', r: 'rule' },
                  { t: '(S)' },
                ], note: 'what changed' },
            ]} />
            <p style={pBody}>
              <Op>C</Op> is XOR, named for the role it plays: comparing two states bit by
              bit. <Op>D</Op> uses it to ask the smallest possible question about a rule
              &mdash; compare the state to what the rule turns it into, one step later. It's the first watcher
              worth a badge. Base state and <Op>D(S)</Op>, for Rule {rule}:
            </p>
            <InstrumentViewer
              items={[
                { label: L_E, sig: sigRaw(rule), field: computed && computed.raw, color: ON_COLOR },
                { label: L_D, sig: sigGauge('D', rule), field: computed && computed.d, color: ACCENT },
              ]}
              exploreHref={buildSeedUrl([
                { id: 1, type: 'source', dim: '1d', rule, ic: initState, steps: STEPS, color: EXPLORE_COLORS.cream },
                { id: 2, type: 'transform', dim: '1d', from: 1, op: 'd', rule, color: EXPLORE_COLORS.teal },
              ])}
            />

            <h3 style={h3Style}>Integration, and why evolution is Euler's method in disguise</h3>
            <Defn lines={[
              { parts: [
                  { t: 'I', r: 'watch', g: 'integration: the same XOR as C, pointed the other way — fold a difference back into a state.' },
                  { t: '(a, b) = a ⊕ b' },
                ], note: 'integration' },
              { parts: [
                  { t: 'E', r: 'walk', g: 'evolution — the same E as the badges: one step of the rule.' },
                  { t: '(S) = ' },
                  { t: 'I', r: 'watch' },
                  { t: '(S, ' },
                  { t: 'D', r: 'watch' },
                  { t: '(S))' },
                ], note: 'evolution' },
            ]} />
            <p style={pBody}>
              <Op>I</Op> is XOR asked in the opposite direction from{' '}
              <Op>C</Op>: not "how do these two states differ," but "fold this difference
              back into a state." That's Euler's method, discretized to bits: numerical integration updates{' '}
              <code className="gc-code">y</code> by <code className="gc-code">y + h&middot;f(y)</code> each step;
              here the step size <code className="gc-code">h</code> is 1, addition is XOR, and the rate of change{' '}
              <code className="gc-code">f</code> is <Op>D</Op>. Expand the definition and
              everything cancels:
            </p>
            <Defn lines={[
              { parts: [
                  { t: 'E' }, { t: '(S) = ' }, { t: 'I' }, { t: '(S, ' }, { t: 'D' }, { t: '(S)) = S ⊕ (S ⊕ ' },
                  { t: 'φ' }, { t: '(S)) = ' }, { t: 'φ' }, { t: '(S)' },
                ] },
            ]} />
            <p style={pBody}>
              Integrating the derivative back into the state is evolution. That identity &mdash; differentiate,
              integrate, and you're back to the rule's own step &mdash; is what earns the word{' '}
              <em>calculus</em> here, and it's checkable by hand from the two definitions above.
            </p>

            <h3 style={h3Style}>The rule slot</h3>
            <p style={pBody}>
              <Op>E</Op> and <Op>D</Op> are both defined straight
              from &phi; &mdash; with the rule slot written out,{' '}
              <code className="gc-code">E(S,&phi;) = &phi;(S)</code> and{' '}
              <code className="gc-code">D(S,&phi;) = S &oplus; &phi;(S)</code>. The slot matters: any rule can fill
              it, not just the one that generated the state, which is why the{' '}
              <a href="explorer.html" style={{ color: 'var(--accent)' }}>explorer</a>'s D card asks you for a rule.
              The badges on this page leave the slot implicit &mdash; here it always matches the base's rule &mdash;
              but the explorer writes it out (<code className="gc-code">D(&middot;,110)</code>), because there the
              two can differ.
            </p>
          </section>

          {/* (The former in-flow #run section moved above the rule panel; see the
              Foundation sections before the calculus. The engine half of it now
              lives in #engines, after the commutator.) */}

          {/* INSTRUMENTS: D², G, ABSENTIAL, SECOND-ORDER */}
          <section id="secondderivative" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
            <div style={sectionKicker}>Instrument</div>
            <h2 style={h2Style}>The second derivative</h2>
            <Defn lines={[
              { parts: [{ t: 'D²' }, { t: '(S) = ' }, { t: 'D' }, { t: '(' }, { t: 'D' }, { t: '(S))' }] },
            ]} />
            <p style={pBody}>
              The obvious next move once <Op>D</Op> exists: apply it to its own output,
              under the same rule. Base state, <Op>D(S)</Op>, and{' '}
              <Op>D²(S)</Op>, for Rule {rule}:
            </p>
            <InstrumentViewer
              items={[
                { label: L_E, sig: sigRaw(rule), field: computed && computed.raw, color: ON_COLOR },
                { label: L_D, sig: sigGauge('D', rule), field: computed && computed.d, color: ACCENT },
                { label: L_D2, sig: sigGauge('D²', rule), field: computed && computed.d2, color: 'oklch(0.55 0.14 30)' },
              ]}
              exploreHref={buildSeedUrl([
                { id: 1, type: 'source', dim: '1d', rule, ic: initState, steps: STEPS, color: EXPLORE_COLORS.cream },
                { id: 2, type: 'transform', dim: '1d', from: 1, op: 'd', rule, color: EXPLORE_COLORS.teal },
                { id: 3, type: 'transform', dim: '1d', from: 2, op: 'd', rule, color: EXPLORE_COLORS.red },
              ])}
            />
            <p style={{ ...pBody, marginTop: '1.1rem' }}>
              Read the teal panel as "which cells are about to change" &mdash; it's <Op>D(S)</Op>,
              the difference between <Op>E(S)</Op> and what the rule turns it into next.
              The red panel is the same
              question asked one level up: treat <em>that</em> difference field as a state in its own right, and ask
              which of <em>its</em> cells are about to change under the same rule. Not a property of the original
              state directly &mdash; a property of how the state is changing.
            </p>
          </section>

          <section id="evolvederivative" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
            <div style={sectionKicker}>Instrument</div>
            <h2 style={h2Style}>Evolving the derivative</h2>
            <Defn lines={[
              { parts: [{ t: 'E' }, { t: '(' }, { t: 'D' }, { t: '(S)) = ' }, { t: 'φ' }, { t: '(' }, { t: 'D' }, { t: '(S))' }] },
            ]} />
            <p style={pBody}>
              <Op>D(S)</Op> is a mask &mdash; "which cells are about to change" &mdash;
              not a state of live cells. <Op>φ</Op> doesn't care: it sees a row of
              bits and looks each neighborhood up in the same eight-entry table it always uses, so it will happily
              take the mask as input. <Op k="E∘D">E(D(S))</Op> does exactly that: reinterpret the
              derivative field as a fresh state under the same rule, and ask what the rule predicts happens to it
              next. Whether the answer says anything real about the rule or the state is a question for the panels
              below, not for the definition. Base state, <Op>D(S)</Op>, and{' '}
              <Op k="E∘D">E(D(S))</Op>, for Rule {rule}:
            </p>
            <InstrumentViewer
              items={[
                { label: L_E, sig: sigRaw(rule), field: computed && computed.raw, color: ON_COLOR },
                { label: L_D, sig: sigGauge('D', rule), field: computed && computed.d, color: ACCENT },
                { label: L_ED, sig: sigGauge('E∘D', rule), field: computed && computed.ed, color: 'oklch(0.6 0.14 75)' },
              ]}
              exploreHref={buildSeedUrl([
                { id: 1, type: 'source', dim: '1d', rule, ic: initState, steps: STEPS, color: EXPLORE_COLORS.cream },
                { id: 2, type: 'transform', dim: '1d', from: 1, op: 'd', rule, color: EXPLORE_COLORS.teal },
                { id: 3, type: 'transform', dim: '1d', from: 2, op: 'e', rule, color: EXPLORE_COLORS.amber },
              ])}
            />
            <p style={{ ...pBody, marginTop: '1.1rem' }}>
              This is exactly the ingredient the next section needs: the Groovy Commutator compares this field
              &mdash; differentiate, then evolve &mdash; against its mirror image, evolve then differentiate.
              Having it defined and looked at on its own first should make that comparison easier to read.
            </p>
          </section>

          <section id="commutator" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)', background: 'var(--bg)' }}>
            <div style={sectionKicker}>Instrument</div>
            <h2 style={h2Style}>The Groovy Commutator G</h2>
            <Defn lines={[
              { parts: [
                  { t: 'G' }, { t: '(S) = ' }, { t: 'C' }, { t: '(' },
                  { t: 'D' }, { t: '(' }, { t: 'E' }, { t: '(S)), ' },
                  { t: 'E' }, { t: '(' }, { t: 'D' }, { t: '(S)))' },
                ] },
            ]} />
            <p style={pBody}>
              Evolve-then-differentiate (<Op k="D∘E">D(E(S))</Op>), compared against
              differentiate-then-evolve (<Op k="E∘D">E(D(S))</Op>, defined above): does order agree?
              Same construction as the commutator <code className="gc-code">[A,B] = AB - BA</code> from ordinary
              algebra &mdash; does applying two operations one way give the same result as applying them the other
              way.
            </p>
            <p style={pBody}>
              Think of <Op>S</Op> as sitting at position 0 and <Op>E(S)</Op> at
              position 1. <Op>D(S)</Op> compares those two, so it straddles positions 0 and
              1 &mdash; call it position 0.5. <Op k="D∘E">D(E(S))</Op> is that same comparison, one
              full step later: it straddles 1 and 2, position 1.5 &mdash; which is exactly why{' '}
              <Op k="D∘E">D(E(S))</Op> turns out to equal the ordinary{' '}
              <Op>D(S)</Op> trajectory from a few sections back, read one row later
              (<code className="gc-code">D(E(S<sub>t</sub>)) = D(S<sub>t+1</sub>)</code>, exactly, not
              approximately). <Op k="E∘D">E(D(S))</Op> reaches for that same nominal position 1.5
              by a completely different, weirder route: it evolves whatever's sitting at 0.5 forward by one step
              &mdash; except position 0.5 was never a real point on the trajectory to begin with, just a mask. Two
              different paths, both aimed at the same target. <Op>G(S)</Op> is the question
              of whether they actually land there together.
            </p>
            <p style={pBody}>
              <strong>The affine implication:</strong> if <Op>φ</Op> is GF(2)-affine,
              <Op>G(S)</Op> equals its constant bias for every <Op>S</Op>. The converse fails:
              nonlinear rules 4 and 200 also have <Op>G(S)</Op> = 0.
              Rule {rule}'s affine status is checked against its own lookup table:{' '}
              {isAffine === null ? 'checking…'
                : isAffine ? <>this rule is GF(2)-affine &mdash; <Op>G</Op> is the same constant for every state, every step.</>
                : (rule === 4 || rule === 200) ? 'this rule is nonlinear, but its commutator is identically zero.'
                : <>this rule is nonlinear and <Op>G</Op> varies across possible states; a particular orbit may still settle.</>}
              {' '}<a href="research/affine-converse.html" style={{ color: 'var(--accent)' }}>Read the correction and exhaustive checks.</a>
            </p>
            <p style={pBody}>
              Worth flipping through the quick-pick rules above and watching what happens to the purple panel: rule{' '}
              90 is affine with no bias, so <Op>G(S)</Op> goes flat black &mdash; confirms
              the theorem directly, even though the teal and amber panels feeding into it are each still churning
              on their own. Rule 30 (class III) makes <Op>G(S)</Op> churn with no visible
              structure. Rule 110 or 54 (class IV) is the interesting middle case:{' '}
              <Op>G(S)</Op> is neither constant nor noise, it has visible structure of its
              own. Rule 4 has <Op>G(S)</Op> = 0 identically; Rule 184 (class II) can settle into periodic
              behavior. Same four panels, four qualitatively different stories, just
              by changing the rule number.
            </p>
            <InstrumentViewer
              items={[
                { label: L_E, sig: sigRaw(rule), field: computed && computed.raw, color: ON_COLOR },
                { label: L_DE, sig: sigGauge('D∘E', rule), field: computed && computed.de, color: ACCENT },
                { label: L_ED, sig: sigGauge('E∘D', rule), field: computed && computed.ed, color: 'oklch(0.6 0.14 75)' },
                { label: L_G, sig: sigGauge('G', rule), field: computed && computed.g, color: 'oklch(0.5 0.13 300)' },
              ]}
              exploreHref={buildSeedUrl([
                { id: 1, type: 'source', dim: '1d', rule, ic: initState, steps: STEPS, color: EXPLORE_COLORS.cream },
                { id: 2, type: 'transform', dim: '1d', from: 1, op: 'e', rule, color: EXPLORE_COLORS.teal },
                { id: 3, type: 'transform', dim: '1d', from: 2, op: 'd', rule, color: EXPLORE_COLORS.blue },
                { id: 4, type: 'transform', dim: '1d', from: 1, op: 'd', rule, color: EXPLORE_COLORS.amber },
                { id: 5, type: 'transform', dim: '1d', from: 4, op: 'e', rule, color: EXPLORE_COLORS.red },
                { id: 6, type: 'transform', dim: '1d', from: 1, op: 'g', rule, color: EXPLORE_COLORS.purple },
              ])}
            />
          </section>

          <section id="possibility" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
            <div style={sectionKicker}>Order and possibility</div>
            <h2 style={h2Style}>What can happen next?</h2>
            <p style={pBody}>
              The commutator tells us whether two orders reach the same state. A further question is what
              each resulting state lets us do. A different state can have different options, or the same
              options reached through different actions.
            </p>
            <PossibilityDemo />
            <p style={pBody}>
              Here an option missing after one step returns after two. Possibility depends on the actions
              available and the time allowed. Counting options also leaves out which outcomes they are,
              and which action sequence reaches each one.
            </p>
            <p style={pBody}>
              These are exact, simple examples. The choices come from our interventions; the automaton
              is not inventing new actions. The{' '}
              <a href="research/future-repertoire.html" style={{ color: 'var(--accent)' }}>research experiment</a>
              {' '}keeps the full definitions, counterexamples, and finite enumeration. The wider{' '}
              <a href="research/history-and-possibility.html" style={{ color: 'var(--accent)' }}>history-and-possibility program</a>
              {' '}asks how useful constructions can themselves become operations for later activity.
            </p>
          </section>

          <section id="absential" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
            <div style={sectionKicker}>Instrument &mdash; newer, less validated</div>
            <h2 style={h2Style}>Absential cells</h2>
            <p style={pBody}>
              A cell can be off because it's entirely outside any live cell's influence (<strong>void</strong>)
              &mdash; or off but adjacent to something alive, which philosopher Terrence Deacon calls{' '}
              <strong>absential</strong>: absence that does causal work by virtue of what it's next to.
            </p>
            <p style={pBody}>
              Everything so far has been built from XOR alone &mdash; GF(2) addition. Writing this one down needs two
              more familiar pieces of boolean algebra: <strong>OR</strong> (&or;, true if either input is true) and{' '}
              <strong>NOT</strong> (&not;, flips a bit). A cell's closed neighborhood is on if it or either neighbor
              is on; a cell is absential if its neighborhood is on but it itself isn't:
            </p>
            <Defn lines={[
              { parts: [{ t: 'N' }, { t: '(S) = ' }, { t: 'S' }, { t: ' ∨ left(S) ∨ right(S)' }], note: 'closed neighborhood' },
              { parts: [{ t: 'A' }, { t: '(S) = ' }, { t: 'N' }, { t: '(S) ∧ ¬' }, { t: 'S' }], note: 'absential field' },
              { parts: [{ t: 'V' }, { t: '(S) = ¬' }, { t: 'N' }, { t: '(S) = ¬' }, { t: 'S' }, { t: ' ∧ ¬' }, { t: 'A' }, { t: '(S)' }], note: 'void field' },
            ]} />
            <p style={pBody}>
              <Op>S</Op>, <Op>A(S)</Op>, and{' '}
              <Op>V(S)</Op> partition every cell into exactly one of three categories
              &mdash; live, absential, or void &mdash; with no overlap and nothing left over.
            </p>
            <InstrumentViewer
              items={[
                { label: L_E, sig: sigRaw(rule), field: computed && computed.raw, color: ON_COLOR },
                { label: L_A, sig: sigGauge('A', rule), field: computed && computed.absential, color: 'oklch(0.6 0.14 75)' },
                { label: L_V, sig: sigGauge('V', rule), field: computed && computed.void, color: 'oklch(0.6 0.13 240)' },
              ]}
              exploreHref={buildSeedUrl([
                { id: 1, type: 'source', dim: '1d', rule, ic: initState, steps: STEPS, color: EXPLORE_COLORS.cream },
                { id: 2, type: 'transform', dim: '1d', from: 1, op: 'absential', rule, color: EXPLORE_COLORS.amber },
              ])}
            />
            <p style={{ ...pBody, marginTop: '1.1rem' }}>
              Overlay mode is worth trying here specifically: all three fields are mutually exclusive by
              construction, so a correct overlay should show zero magenta (the 2+ layers highlight) anywhere on the
              grid &mdash; toggle layers off and on to check it. <Op>V(S)</Op> isn't wired
              into the explorer yet, so the Explore link above carries <Op>S</Op> and{' '}
              <Op>A(S)</Op> only.
            </p>
            <p style={{ fontSize: '0.92rem', color: 'var(--ink-soft)', maxWidth: '60ch', margin: 0 }}>
              Open question this raises: does this field's own compressibility work as a faster Class-IV detector
              than looking at <Op>G(S)</Op> or <Op>E(S)</Op>{' '}
              directly? First test didn't confirm it &mdash; see the{' '}
              <a href="questions.html#absential" style={{ color: 'var(--accent)' }}>questions page</a>.
            </p>
          </section>

          {/* ENGINES: the reflexive run, defined where composites first make it interesting */}
          <section id="engines" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
            <div style={sectionKicker}>Engine</div>
            <h2 style={h2Style}>Letting a map walk itself</h2>
            <p style={pBody}>
              Every instrument above is a gauge: <Op>D</Op>,{' '}
              <Op>D²</Op>, <Op>E∘D</Op>,{' '}
              <Op>G</Op>, <Op>A</Op>, and{' '}
              <Op>V</Op> all watch a walk that <Op>E</Op>{' '}
              provides. The remaining move is to make a map <em>walk</em> &mdash; feed it its own output, instead
              of showing it someone else's.
            </p>
            <Defn lines={[
              { parts: [
                  { t: 'engine', r: 'walk', g: 'a run whose map is its own base: every row is the map fed its previous output.' },
                  { t: '(F) = ' },
                  { t: 'run' },
                  { t: '(' },
                  { t: 'F', r: 'watch' },
                  { t: ', ' },
                  { t: 'F', r: 'walk' },
                  { t: ')' },
                ], note: 'the map is its own base' },
            ]} />
            <p style={pBody}>
              For plain <Op>E</Op> this changes nothing &mdash;{' '}
              <Op>run(E, E)</Op> is the orbit again, shifted one row. For a composite it
              changes everything. <Op k="E∘D">E(D(S))</Op> riding{' '}
              <Op>E</Op>'s orbit and <Op k="E∘D">E(D(S))</Op> walking on
              its own output are two different pictures: same map, same XORs, different thing being iterated.
            </p>
            <p style={pBody}>
              Here are the commutator's two ingredients, <Op>D∘E</Op> and{' '}
              <Op>E∘D</Op>, XORed against each other both ways from one shared
              seed. As gauges on <Op>E</Op>'s orbit they make{' '}
              <Op>G</Op> &mdash; the same purple field as two sections up. As engines
              they make a field{' '}
              <a href="remainder.html" style={{ color: 'var(--accent)' }}>The Walk</a> calls{' '}
              <Op>U</Op>. The panels agree on their first row exactly, then part ways:
            </p>
            <InstrumentViewer
              items={[
                { label: "G — gauges riding E's orbit", sig: { text: 'run(D∘E, E_' + rule + ') ⊕ run(E∘D, E_' + rule + ')' }, field: computed && computed.g, color: 'oklch(0.5 0.13 300)' },
                { label: 'U — engines, self-fed', sig: { text: 'engine(D∘E) ⊕ engine(E∘D)' }, field: computed && computed.u, color: 'oklch(0.6 0.15 22)' },
              ]}
            />
            <p style={{ ...pBody, marginTop: '1.1rem', marginBottom: 0 }}>
              Try rule 90 in the pinned panel: both fields go flat &mdash; for affine rules the two constructions
              agree forever, one more face of the affine theorem. For most rules they disagree, and whether that
              disagreement can follow a rule of its own is The Walk, this site's research frontier. The{' '}
              <span className="gc-mono" style={{ fontSize: '0.85em', fontWeight: 700 }}>ENGINE</span> label on the
              sections below marks constructions of this shape: fields that walk on their own output rather than
              watching <Op>E</Op>'s.
            </p>
          </section>

          <section id="secondorder" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
            <div style={sectionKicker}>Engine</div>
            <h2 style={h2Style}>Reversible memory (second-order CA)</h2>
            <Defn lines={[
              { parts: [{ t: 'S' }, { t: '(t+1) = ' }, { t: 'φ' }, { t: '(' }, { t: 'S' }, { t: '(t)) ⊕ ' }, { t: 'S' }, { t: '(t−1)' }] },
            ]} />
            <p style={pBody}>
              A different shape of the same underlying move as comparison and coupling: compute two things
              separately, then XOR them together. Here the two things are the rule's ordinary output and a
              time-shifted copy of the same layer, one step back &mdash; and because XOR is its own inverse, running
              the recurrence backward exactly recovers every earlier state. That's the standard Margolus&ndash;Fredkin
              trick for giving 1D CA memory and reversibility at once, for <em>any</em> rule, not just famous ones.
            </p>
            <p style={pBody}>
              The economy is the striking part: two rows &mdash; current and previous &mdash; are enough to run
              forever in either direction, even though most rules <Op>φ</Op> aren't
              invertible and <Op>S(t+1)</Op> alone can't recover{' '}
              <Op>S(t)</Op>. The one extra row of memory carries exactly the missing
              information.
            </p>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1.4rem', flexWrap: 'wrap' }}>
              <div>
                <canvas className="gc-field" ref={secondOrderRef}></canvas>
                <div className="gc-mono" style={{ fontSize: '0.72rem', color: 'var(--ink-soft)', marginTop: '0.4rem', maxWidth: 160 }}>second-order Rule {rule}</div>
                <div style={{ marginTop: '0.25rem' }}><RunSig sig={{ engine: `2nd-order ${rule}`, note: 'walks (S(t), S(t−1)) pairs' }} /></div>
              </div>
              <p style={{ fontSize: '0.88rem', color: 'var(--ink-soft)', maxWidth: '42ch', margin: 0 }}>
                Reversibility check, run live in your browser right now: {secondOrderStatus}
              </p>
            </div>
            <p style={{ ...pBody, marginTop: '1.1rem' }}>
              One generalization worth knowing about: pass the memory through a rule of its own before XOR-ing it
              in &mdash; <code className="gc-code">S(t+1) = &phi;(S(t)) &oplus; &mu;(S(t&minus;1))</code>. The
              construction stays reversible exactly when <Op>μ</Op> is itself
              invertible, and only six elementary rules are invertible on every ring size (15, 51, 85, 170, 204,
              240 &mdash; the identity, complement, and shift family; the standard construction above is just{' '}
              <code className="gc-code">&mu; = 204</code>, the identity). The natural-sounding variant &ldquo;feed
              the <em>derivative</em> of the past in as the memory&rdquo; is the special case{' '}
              <code className="gc-code">&mu; = &phi;&oplus;204</code> &mdash; so it keeps reversibility only for{' '}
              <code className="gc-code">&phi; &isin; {'{'}0, 60, 102, 153, 195, 255{'}'}</code>, essentially the
              additive family. For every other rule, <Op>D</Op>-memory trades
              reversibility away. Verified exhaustively in{' '}
              <code className="gc-code">scripts/experiment_memory_variants.py</code>.
            </p>
          </section>
        </div>

        {/* COUPLING */}
        <section id="coupling" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={sectionKicker}>Engine</div>
          <h2 style={h2Style}>Coupling two rules</h2>
          <p style={{ ...pBody, marginBottom: '1rem' }}>
            Everything above acts on one state under one rule. The natural next move: let two <em>different</em>{' '}
            rules act on the same shared starting state, and ask whether the order they're applied in matters. Run
            one shared starting row two ways &mdash; A-then-B, and B-then-A &mdash; and watch the two paths disagree
            over time. The disagreement reliably settles into one of five shapes: <strong>commute</strong> (the
            paths never disagree at all), <strong>crystalline</strong> (a disagreement that freezes into a fixed
            pattern), <strong>noisy</strong> (indistinguishable from static), <strong>structured</strong>{' '}
            (disagreement with visible pattern of its own), or <strong>drain</strong> (both paths collapse into the
            same dead end):
          </p>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', margin: '0 0 1.2rem' }}>
            {PAIR_PRESETS.map((p, idx) => {
              const active = idx === pairIdx;
              return (
                <button key={idx} onClick={() => setPairIdx(idx)} className="gc-mono"
                  style={{ fontSize: '0.78rem', fontWeight: 700, padding: '0.45rem 0.7rem', borderRadius: 7, border: '1px solid ' + (active ? ACCENT : '#e4dac8'), background: active ? ACCENT : '#fff', color: active ? '#fff' : INK_SOFT, cursor: 'pointer', whiteSpace: 'nowrap' }}>
                  {p.a} vs {p.b}
                </button>
              );
            })}
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1.4rem', flexWrap: 'wrap' }}>
            <div>
              <canvas className="gc-field" ref={pairRef}></canvas>
              <div style={{ marginTop: '0.3rem' }}><RunSig sig={{ text: `engine(${selectedPreset.b}∘${selectedPreset.a}) ⊕ engine(${selectedPreset.a}∘${selectedPreset.b})` }} /></div>
            </div>
            <p style={{ fontSize: '0.92rem', color: 'var(--ink-soft)', maxWidth: '42ch', margin: 0 }}>
              <span className="gc-mono" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4em', fontWeight: 700, fontSize: '0.78rem', padding: '0.2rem 0.6rem', borderRadius: 999, color: '#fff', background: `var(--${selectedPreset.regime})`, textTransform: 'uppercase' }}>{selectedPreset.regime}</span>
              <br /><br />{selectedPreset.a} vs {selectedPreset.b} &mdash; {selectedPreset.note}. Pattern above is
              computed live from one shared random row; regime label is the documented classification for this pair.
            </p>
          </div>
          <p style={{ fontSize: '0.92rem', color: 'var(--ink-soft)', margin: '1.1rem 0 0', maxWidth: '60ch' }}>
            <strong>Structured divergence has no single-rule analog</strong> &mdash; for one rule against itself
            there's nowhere for "persistently related but never identical" to live. It only shows up once two
            distinct rules are in play. Coupling rules at scale &mdash; which regimes are common, what predicts
            them &mdash; is exactly the kind of thing this construction makes askable; see the{' '}
            <a href="questions.html" style={{ color: 'var(--accent)' }}>questions page</a> for what's actually been
            found.
          </p>
        </section>

        {/* THE FOURTH INPUT (pre-hoc composition) */}
        <section id="prehoc" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={sectionKicker}>Engine &mdash; newer</div>
          <h2 style={h2Style}>The fourth input (pre-hoc composition)</h2>
          <p style={pBody}>
            Every composition above &mdash; <Op>D</Op>, reversible memory, coupling
            &mdash; computes two finished fields and
            then XORs or compares them: composition <em>after</em> the rule has run. There's a second, more invasive
            option: give the rule's own lookup table a <strong>fourth input</strong>, alongside left/self/right,
            before &phi; is ever evaluated. One extra binary input doubles the table from 8 entries to 16 &mdash;
            and the doubled table has a tidy reading:
          </p>
          <Defn lines={[
            { parts: [
                { t: 'f(l, c, r, ' },
                { t: 'x' },
                { t: ') = ' },
                { t: 'x' },
                { t: <> ? &phi;<sub>1</sub>(l,c,r) : &phi;<sub>0</sub>(l,c,r)</> },
              ], note: 'a 16-entry table IS a rule pair' },
          ]} />
          <p style={pBody}>
            Every 4-input rule is exactly an <em>ordered pair of elementary rules</em>, with x choosing per cell,
            per step, which of the two applies. Only 512 of the 65,536 possible tables can be rewritten as
            &ldquo;compute one rule, then XOR x in afterward&rdquo; &mdash; the other 99.2% are genuinely new
            territory, unreachable by post-hoc composition.
          </p>
          <p style={pBody}>
            <strong>But there's a trap, and it's a theorem.</strong> If the fourth input is computed from the{' '}
            <em>same state at the same time</em> &mdash; say <code className="gc-code">x = D(S)</code>, or{' '}
            <code className="gc-code">x = A(S)</code>, the absential field from a few sections up &mdash; the
            whole thing collapses back into a single ordinary elementary rule. (Two facts fall out of proving
            this: <Op>A(S)</Op> <em>is</em> elementary rule 50, and{' '}
            <code className="gc-code">D(&middot;,&psi;)</code> <em>is</em> elementary rule{' '}
            <code className="gc-code">&psi;&oplus;204</code>.) The fourth input only escapes the collapse when it comes from another{' '}
            <em>time</em> (that's reversible memory, above) or another <em>trajectory</em> &mdash; a second layer
            with its own dynamics. Two layers, each using the other as its fourth input, live:
          </p>
          <PrehocMiniDemo />
          <p style={{ fontSize: '0.92rem', color: 'var(--ink-soft)', maxWidth: '60ch', margin: '1.1rem 0 0' }}>
            All four component rules here (77, 55, 44, 23) are frozen or periodic on their own &mdash; the structure
            you're seeing belongs to the coupling, not to any part. What that means at scale is on the{' '}
            <a href="questions.html#extended-neighborhoods" style={{ color: 'var(--accent)' }}>questions page</a>.
          </p>
        </section>

        {/* RULE FIELDS (non-uniform CA) */}
        <section id="rulefield" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={sectionKicker}>Engine &mdash; newest</div>
          <h2 style={h2Style}>Rule fields (a rule per cell)</h2>
          <p style={pBody}>
            One more wall to knock down. Everything above still assumes one shared global rule &mdash; the rule is
            a fixed number sitting <em>outside</em> the State &rarr; State world everything else lives in.
            Non-uniform CA give every cell its <em>own</em> rule: the rule field is now an array the same shape as
            the state, its 8 bit-planes are literally state-shaped binary fields, and every instrument on this page
            applies to it unchanged. This is the field's founding idea, not an exotic one &mdash; von Neumann's
            self-reproducing automaton stored its construction instructions as patterns in the same substrate they
            acted on.
          </p>
          <p style={pBody}>
            The same trap as the fourth input appears here, one level up: if each cell's rule is <em>re-read from
            the state around it every step</em> (&ldquo;the state writes its own rules&rdquo;), the whole system is
            provably just one uniform CA with a bigger neighborhood. Self-reference at a single time step is always
            just a bigger neighborhood. The rule field becomes a genuine second citizen only when it{' '}
            <em>persists</em> &mdash; when it has memory. The simplest honest version: rules stay put where the
            state is dead, and a live cell copies its left neighbor's rule over its own. The state gates transport
            of rules through the medium the rules themselves animate:
          </p>
          <RuleFieldMiniDemo />
          <p style={{ fontSize: '0.92rem', color: 'var(--ink-soft)', maxWidth: '60ch', margin: '1.1rem 0 0' }}>
            Watch the right panel: rule territories hold where the state is quiet and get invaded where it's
            active. That asymmetry turns out to be a selection pressure &mdash; see the{' '}
            <a href="questions.html#rule-as-state" style={{ color: 'var(--accent)' }}>questions page</a> for the
            evolution that falls out of it.
          </p>
        </section>

        <section id="resonance" style={{ padding: '1.6rem 0', borderTop: '1px solid var(--rule)' }}>
          <div style={sectionKicker}>Law, state, and interpretation</div>
          <h2 style={h2Style}>Four questions about resonance</h2>
          <p style={pBody}>
            Some states may fit a rule in a useful way. “Resonance” names that question;
            it is not yet a single score. To make the relationship precise, declare
            the law, the state family, and the interpretation connecting them.
          </p>
          <div style={{ overflowX: 'auto', margin: '1rem 0' }}>
            <table style={{ borderCollapse: 'collapse', width: '100%', minWidth: 620, fontSize: '0.9rem', color: 'var(--ink-soft)' }}>
              <caption style={{ textAlign: 'left', marginBottom: '0.6rem' }}>Different claims need different evidence.</caption>
              <thead>
                <tr style={{ textAlign: 'left', color: 'var(--ink)' }}>
                  <th scope="col" style={{ padding: '0.65rem', width: '20%' }}>Relationship</th>
                  <th scope="col" style={{ padding: '0.65rem', width: '32%' }}>What must hold</th>
                  <th scope="col" style={{ padding: '0.65rem' }}>Example and boundary</th>
                </tr>
              </thead>
              <tbody>
                <tr style={{ borderTop: '1px solid var(--rule)', verticalAlign: 'top' }}>
                  <th scope="row" style={{ padding: '0.65rem', textAlign: 'left', color: 'var(--ink)' }}>Preservation</th>
                  <td style={{ padding: '0.65rem' }}>
                    F(B) ⊆ B: evolution keeps states inside the family B. Individual states may keep changing.
                  </td>
                  <td style={{ padding: '0.65rem' }}>
                    All 256 axial laws preserve fields copied along the added axis. This follows from translation symmetry;
                    it does not identify the induced law inside that family.{' '}
                    <a href="research/dimensional-vision-and-interpretation.html#refinement-preserving-the-beam-versus-preserving-the-old-law">Source</a>
                  </td>
                </tr>
                <tr style={{ borderTop: '1px solid var(--rule)', verticalAlign: 'top' }}>
                  <th scope="row" style={{ padding: '0.65rem', textAlign: 'left', color: 'var(--ink)' }}>Faithful representation</th>
                  <td style={{ padding: '0.65rem' }}>
                    H ∘ E = E ∘ F: encoding and evolution agree, at the declared cadence and on the declared family.
                  </td>
                  <td style={{ padding: '0.65rem' }}>
                    For 66 axial sources, the copied field executes the original lower-dimensional law at the same macro cadence.{' '}
                    <a href="research/guard-free-axial-lift.html">Exact compatibility</a>
                  </td>
                </tr>
                <tr style={{ borderTop: '1px solid var(--rule)', verticalAlign: 'top' }}>
                  <th scope="row" style={{ padding: '0.65rem', textAlign: 'left', color: 'var(--ink)' }}>Restoration</th>
                  <td style={{ padding: '0.65rem' }}>
                    Declared perturbations return toward a valid family or a specified trajectory, under an explicit metric and domain.
                  </td>
                  <td style={{ padding: '0.65rem' }}>
                    After a fixed one-cell perturbation on the Rule23 code's 2×7 torus, 28 of 128 initial states regain valid code
                    after four ticks; only 18 match undamaged evolution.{' '}
                    <a href="research/knowledge/encoding-is-not-repair.html">Validity versus content</a>.
                    The Rule32 physical cap also has an expanding one-cell defect.{' '}
                    <a href="research/rule32-physical-cap.html">Non-repair example</a>
                  </td>
                </tr>
                <tr style={{ borderTop: '1px solid var(--rule)', verticalAlign: 'top' }}>
                  <th scope="row" style={{ padding: '0.65rem', textAlign: 'left', color: 'var(--ink)' }}>Endogenous organization</th>
                  <td style={{ padding: '0.65rem' }}>
                    The unfolding establishes or maintains the relevant organization and interpretation, with initial resources declared.
                  </td>
                  <td style={{ padding: '0.65rem' }}>
                    Endogenous establishment of the interpretation remains open. Guarded constructions supply prepared organization;
                    successful execution alone does not show that it formed itself.{' '}
                    <a href="research/knowledge/dimensional-beam.html">Open question</a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p style={pBody}>
            These properties do not imply one another in general. Returning to some valid state can change its content.
            Preserved geometry and successful decoding do not establish attraction or spontaneous preparation.
          </p>
          <p style={pBody}>
            A further exact control concerns changing the ambient law. If H and H′ agree on a shared invariant family B,
            their derivative observations A = I ⊕ H and A′ = I ⊕ H′, and their finite-depth observed-future tuples, agree there. The{' '}
            <a href="research/correction-future-coordinates.html">triangular coordinate theorem</a>{' '}
            then relates their correction tuples by an invertible local recoding. At each fixed finite depth, whole-field
            fibers and factor existence agree on B; coordinate radius and cost can differ. This is an analytic consequence,
            not a completed second-lift census.
          </p>
          <p style={{ ...pBody, marginBottom: 0 }}>
            Read the <a href="research/dimensional-vision-and-interpretation.html">dimensional vision note</a>{' '}
            and the <a href="research/knowledge/representation-contract.html">representation contract</a>{' '}
            for the broader question. The vision remains open; giving these distinctions an explanation does not change its evidence status.
          </p>
        </section>

        {/* CLOSING POINTER -- questions (incl. rules birthing rules, and everything still open) live on their own page now */}
        <section style={{ padding: '1.6rem 0 2rem', borderTop: '1px solid var(--rule)' }}>
          <p style={pBody}>
            That's the set of instruments and engines built on this calculus so far. What happens when you push them further
            &mdash; a state that generates its own successor rule, what actually predicts the drain regime, whether
            a rule could live in the same shape as the data it acts on &mdash; is exactly what the{' '}
            <a href="questions.html" style={{ color: 'var(--accent)' }}>questions page</a> is for.
          </p>
        </section>

      </main>

      <footer className="gc-footer">
        <div className="gc-footer-inner">
          Source, library code, and full research notes live in the{' '}
          <a href="https://github.com/mbilokonsky/groovy-commutator">GitHub repository</a>.
        </div>
      </footer>
    </>
  );
}
