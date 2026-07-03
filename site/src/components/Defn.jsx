import { useState } from 'react';
import { BADGE_WALK, BADGE_WATCH } from './RunSig.jsx';

// Definition blocks: the Concepts page's formula notation, tokenized so
// each part can carry a role color and a tap-to-reveal gloss. The roles
// make one visual promise, kept across these blocks, the RunSig badges,
// and the Explorer's cards alike: amber marks the thing that walks (a
// base, fed its own output), teal the thing that watches (a gauge,
// evaluated once per row). States stay ink; rules/tables are purple.
//
// A line is { parts, note }. A part is { t, r?, g?, k? }: `t` is the text
// (string or JSX), `r` a role key below, `g` an optional gloss revealed on
// click, `k` a plain-string label for the gloss line when `t` is JSX.
// Parts with a gloss render with a dotted underline; one gloss is open at
// a time, shown inside the block so it works identically on touch.
//
// This page renders on a light background only, so the role colors here
// are darker than the badge colors RunSig uses (which must also survive
// the Explorer's dark panels).
export const ROLE_COLORS = {
  state: 'var(--ink)',
  watch: 'oklch(0.42 0.09 195)',
  walk: 'oklch(0.5 0.13 75)',
  rule: 'oklch(0.45 0.12 300)',
  plain: 'var(--ink-soft)',
};

export default function Defn({ lines }) {
  const [open, setOpen] = useState(null); // [lineIdx, partIdx] | null
  const openPart = open ? lines[open[0]].parts[open[1]] : null;
  return (
    <div style={{ background: 'var(--bg-alt)', border: '1px solid var(--rule)', padding: '0.9rem 1.1rem', borderRadius: 8, margin: '0 0 1.1rem' }}>
      {lines.map((line, li) => (
        <div key={li} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: '1rem', margin: '0.15em 0', flexWrap: 'wrap' }}>
          <span className="gc-mono" style={{ fontSize: '0.86rem' }}>
            {line.parts.map((p, pi) => {
              const color = ROLE_COLORS[p.r || 'plain'];
              if (!p.g) return <span key={pi} style={{ color }}>{p.t}</span>;
              const isOpen = open && open[0] === li && open[1] === pi;
              return (
                <button
                  key={pi}
                  onClick={() => setOpen(isOpen ? null : [li, pi])}
                  title={typeof p.g === 'string' ? p.g : undefined}
                  style={{
                    background: isOpen ? 'rgba(42,36,32,0.08)' : 'none', border: 'none', padding: '0 1px',
                    font: 'inherit', cursor: 'pointer', color, borderBottom: '1px dotted currentColor', borderRadius: 2,
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
          <span className="gc-mono" style={{ fontWeight: 700, color: ROLE_COLORS[openPart.r || 'plain'] }}>
            {openPart.k || (typeof openPart.t === 'string' ? openPart.t.trim() : '')}
          </span>{' '}&mdash; {openPart.g}
        </div>
      )}
    </div>
  );
}

// Re-exported so pages can reference the badge-tier colors without
// importing RunSig directly.
export { BADGE_WALK, BADGE_WATCH };
