// The run-signature badge: a rendered field states which gauge it is and
// whose orbit it rides, in the notation of the Concepts page's run calculus
// (run(gauge, base); engine(F) = run(F, F)). Deriving these from real props
// -- instead of freehand caption strings -- is what keeps "an unsigned
// picture" from being expressible. On the Concepts page badges deliberately
// start at the #run section (nothing above it is badged, so the notation is
// never shown before it's defined); the Explorer badges every card.
//
// Role colors, shared with the Concepts page's Defn blocks: amber = the
// thing that walks (a base), teal = the thing that watches (a gauge).
// These are mid-lightness so they read on both this repo's light page
// background and the Explorer's dark card panels.

export const BADGE_WALK = 'oklch(0.6 0.13 75)';
export const BADGE_WATCH = 'oklch(0.55 0.11 195)';

const SUBSCRIPT_DIGITS = { 0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉' };

// 'E_110' -> 'E₁₁₀' (underscore-digit runs become Unicode subscripts).
export function sub(s) {
  return String(s).replace(/_(\d+)/g, (_, d) => d.split('').map((c) => SUBSCRIPT_DIGITS[c]).join(''));
}

export function formatSig(sig) {
  if (!sig) return '';
  if (sig.text) return sub(sig.text);
  if (sig.engine) return `engine(${sub(sig.engine)})`;
  return `run(${sub(sig.gauge)}, ${sub(sig.base)})`;
}

export default function RunSig({ sig, style }) {
  if (!sig) return null;
  const isEngine = Boolean(sig.engine) || (sig.text && sig.text.includes('engine('));
  let body;
  if (sig.text) {
    body = sub(sig.text);
  } else if (sig.engine) {
    // The engine's map both walks and watches; walking is the part that
    // makes it an engine, so it gets the walk color.
    body = <>engine(<span style={{ color: BADGE_WALK }}>{sub(sig.engine)}</span>)</>;
  } else {
    body = <>run(<span style={{ color: BADGE_WATCH }}>{sub(sig.gauge)}</span>, <span style={{ color: BADGE_WALK }}>{sub(sig.base)}</span>)</>;
  }
  return (
    <span
      className="gc-mono"
      title={isEngine
        ? 'engine(F) = run(F, F): the map is its own base -- each row is F fed its previous output' + (sig.note ? ` (${sig.note})` : '')
        : 'run(gauge, base): the gauge evaluated once on each row of the base’s orbit'}
      style={{
        display: 'inline-block',
        fontSize: '0.68rem',
        fontWeight: 600,
        padding: '0.12rem 0.45rem',
        borderRadius: 6,
        border: `1px solid ${isEngine ? 'var(--accent)' : 'var(--rule)'}`,
        background: 'var(--bg-alt)',
        color: isEngine ? 'var(--accent)' : 'var(--ink-soft)',
        whiteSpace: 'nowrap',
        ...style,
      }}
    >
      {body}
      {sig.note && !sig.text ? <span style={{ fontWeight: 400, opacity: 0.8 }}> &middot; {sig.note}</span> : null}
    </span>
  );
}
