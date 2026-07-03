import { useState } from 'react';
import { BADGE_WALK, BADGE_WATCH } from './RunSig.jsx';

// Definition blocks and inline operator references for the Concepts page.
//
// One shared GLOSSARY drives both: any Defn token or prose <Op> whose text
// (or explicit `k`) matches a glossary key is clickable EVERYWHERE it
// appears, not just in the block that defines it -- a reader meeting `G`
// four sections after its definition can tap it right there. Clickable
// tokens render bold with a dotted underline; a per-use `g` on a Defn part
// overrides the glossary gloss (used where a definition wants extra detail
// or live content, e.g. the rule-table glyphs bound to the pinned panel).
//
// Role colors make one visual promise, kept across these blocks, the
// RunSig badges, and the Explorer's cards alike: amber marks the thing
// that walks (a base, fed its own output), teal the thing that watches (a
// gauge, evaluated once per row). States stay ink; rules/tables purple.
// This page renders on a light background only, so these are darker than
// the badge colors RunSig uses (which must survive dark panels too).
export const ROLE_COLORS = {
  state: 'var(--ink)',
  watch: 'oklch(0.42 0.09 195)',
  walk: 'oklch(0.5 0.13 75)',
  rule: 'oklch(0.45 0.12 300)',
  plain: 'var(--ink-soft)',
};

export const GLOSSARY = {
  S: { r: 'state', g: 'a state: one row of bits.' },
  seed: { r: 'state', g: 'the starting row — row zero of every picture.' },
  R: { r: 'rule', g: "a rule's eight-entry lookup table: one output bit per three-cell neighborhood." },
  'φ': { r: 'rule', g: "the rule as a function: look up every cell's neighborhood in the table, all at once — row in, row out." },
  'μ': { r: 'rule', g: 'the memory rule: applied to the previous state before it is XORed back in (see reversible memory).' },
  x: { r: 'state', g: 'the fourth input: one extra bit per cell, alongside left/self/right, choosing which of two rules applies.' },
  C: { r: 'watch', g: 'comparison: XOR two rows bit by bit — 1 marks every position where they disagree.' },
  I: { r: 'watch', g: 'integration: the same XOR as C, pointed the other way — fold a difference back into a state.' },
  D: { r: 'watch', g: 'the derivative: D(S) = S ⊕ φ(S) — 1 marks every cell about to change.' },
  'D²': { r: 'watch', g: 'the second derivative: D applied to its own output — which cells of the change-mask are about to change.' },
  E: { r: 'walk', g: 'evolution: one step of the rule, E(S) = φ(S). The map that walks most orbits on this page.' },
  'E₁₁₀': { r: 'walk', g: 'one step of rule 110: the table applied to every cell of a row at once. Row in, row out.' },
  G: { r: 'watch', g: 'the Groovy Commutator: G(S) = C(D(E(S)), E(D(S))) — where evolve-then-differentiate and differentiate-then-evolve disagree.' },
  'D∘E': { r: 'watch', g: 'evolve, then differentiate: D(E(S)) — the ordinary derivative, read one row later.' },
  'E∘D': { r: 'watch', g: 'differentiate, then evolve: E(D(S)) — the change-mask fed back through the rule as if it were a state.' },
  N: { r: 'watch', g: 'the closed neighborhood: on wherever a cell or either of its neighbors is on.' },
  A: { r: 'watch', g: 'the absential field: cells that are off but adjacent to a live cell.' },
  V: { r: 'watch', g: 'the void field: cells that are off with no live neighbor.' },
  id: { r: 'watch', g: 'the do-nothing map: returns its input unchanged.' },
  NOT: { r: 'watch', g: 'flip every bit.' },
  orbit: { r: 'plain', g: 'feed a map its own output, forever; the collected rows are the orbit.' },
  run: { r: 'plain', g: 'run(gauge, base): the base walks, the gauge watches — every picture on this site is one of these.' },
  engine: { r: 'walk', g: 'engine(F) = run(F, F): the map is its own base, walking on its own output.' },
  gauge: { r: 'watch', g: 'the watcher: evaluated once on each row of the walk; what it reports is what gets drawn.' },
  base: { r: 'walk', g: 'the walker: the map that gets iterated. It owns the orbit.' },
  U: { r: 'watch', g: "the engine-side commutator: engine(D∘E) ⊕ engine(E∘D) — the field The Walk studies." },
};

// 'G(S)' -> 'G', 'run(E, E)' -> 'run', 'D²(S)' -> 'D²', 'φ' -> 'φ'.
function keyFromText(text) {
  const head = text.includes('(') ? text.slice(0, text.indexOf('(')) : text;
  return head.trim();
}

function resolve(part) {
  const key = part.k || (typeof part.t === 'string' ? keyFromText(part.t) : '');
  const entry = GLOSSARY[key] || null;
  return {
    key,
    role: part.r || (entry && entry.r) || 'plain',
    gloss: part.g || (entry && entry.g) || null,
  };
}

// A definition block. A line is { parts, note }; a part is { t, r?, g?, k? }:
// `t` the text (string or JSX), `r` a role override, `g` a gloss override,
// `k` an explicit glossary key / gloss label when `t` is JSX or ambiguous.
export default function Defn({ lines }) {
  const [open, setOpen] = useState(null); // [lineIdx, partIdx] | null
  const openPart = open ? lines[open[0]].parts[open[1]] : null;
  const openMeta = openPart ? resolve(openPart) : null;
  return (
    <div style={{ background: 'var(--bg-alt)', border: '1px solid var(--rule)', padding: '0.9rem 1.1rem', borderRadius: 8, margin: '0 0 1.1rem' }}>
      {lines.map((line, li) => (
        <div key={li} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: '1rem', margin: '0.15em 0', flexWrap: 'wrap' }}>
          <span className="gc-mono" style={{ fontSize: '0.86rem' }}>
            {line.parts.map((p, pi) => {
              const { role, gloss } = resolve(p);
              const color = ROLE_COLORS[role];
              if (!gloss) return <span key={pi} style={{ color }}>{p.t}</span>;
              const isOpen = open && open[0] === li && open[1] === pi;
              return (
                <button
                  key={pi}
                  onClick={() => setOpen(isOpen ? null : [li, pi])}
                  title={typeof gloss === 'string' ? gloss : undefined}
                  style={{
                    background: isOpen ? 'rgba(42,36,32,0.08)' : 'none', border: 'none', padding: '0 1px',
                    font: 'inherit', fontWeight: 700, cursor: 'pointer', color, borderBottom: '1px dotted currentColor', borderRadius: 2,
                  }}
                >{p.t}</button>
              );
            })}
          </span>
          {line.note && <span className="gc-mono" style={{ color: 'var(--ink-soft)', fontSize: '0.7rem' }}>{line.note}</span>}
        </div>
      ))}
      {openPart && (
        <div style={{ marginTop: '0.55rem', paddingTop: '0.5rem', borderTop: '1px dashed var(--rule)', fontSize: '0.8rem', color: 'var(--ink-soft)', maxWidth: '58ch' }}>
          <span className="gc-mono" style={{ fontWeight: 700, color: ROLE_COLORS[openMeta.role] }}>
            {openMeta.key || (typeof openPart.t === 'string' ? openPart.t.trim() : '')}
          </span>{' '}&mdash; {openMeta.gloss}
        </div>
      )}
    </div>
  );
}

// An operator name in running prose: styled like gc-code, clickable
// anywhere it appears, popping its glossary definition in place. Falls
// back to a plain code tag when the text isn't in the glossary.
export function Op({ k, children }) {
  const [open, setOpen] = useState(false);
  const text = typeof children === 'string' ? children : '';
  const key = k || keyFromText(text);
  const entry = GLOSSARY[key];
  if (!entry) return <code className="gc-code">{children}</code>;
  const color = ROLE_COLORS[entry.r || 'plain'];
  return (
    <span style={{ position: 'relative', display: 'inline-block' }}>
      <button
        className="gc-code"
        onClick={() => setOpen((o) => !o)}
        onBlur={() => setOpen(false)}
        title={entry.g}
        style={{
          border: 'none', borderBottom: '1px dotted ' + color, borderRadius: 4, cursor: 'pointer',
          fontFamily: "'IBM Plex Mono', monospace", fontSize: '0.92em', fontWeight: 700, lineHeight: 'inherit',
          color, padding: '0.12em 0.4em',
        }}
      >{children}</button>
      {open && (
        <span style={{
          position: 'absolute', left: 0, top: '100%', marginTop: 4, zIndex: 30,
          background: '#fff', border: '1px solid var(--rule)', borderRadius: 6,
          boxShadow: '0 4px 14px rgba(42,36,32,0.18)', padding: '0.5rem 0.7rem',
          fontSize: '0.78rem', fontWeight: 400, color: 'var(--ink-soft)', textAlign: 'left',
          width: 'max-content', maxWidth: 'min(44ch, 78vw)', whiteSpace: 'normal',
        }}>
          <span className="gc-mono" style={{ fontWeight: 700, color }}>{key}</span> &mdash; {entry.g}
        </span>
      )}
    </span>
  );
}

// Re-exported so pages can reference the badge-tier colors without
// importing RunSig directly.
export { BADGE_WALK, BADGE_WATCH };
