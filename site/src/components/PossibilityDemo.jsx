import { useState } from 'react';
import { applyRule } from '../lib/groovy-engine.js';

const names = { 0: 'Reset', 51: 'Flip' };
const describe = (state) => state.every((bit) => bit === 0) ? 'All zeros' : 'All ones';
const follow = (state, rules) => rules.reduce((current, rule) => applyRule(current, rule), state);

export default function PossibilityDemo() {
  const [steps, setSteps] = useState(1);
  const start = new Uint8Array(6);
  const resetThenFlip = follow(start, [0, 51]);
  const flipThenReset = follow(start, [51, 0]);
  const words = steps === 1 ? [[0], [51]] : [[0, 0], [0, 51], [51, 0], [51, 51]];
  const rows = words.map((word) => ({
    label: word.map((rule) => names[rule]).join(' → '),
    left: describe(follow(resetThenFlip, word)),
    right: describe(follow(flipThenReset, word)),
  }));
  const cell = { padding: '0.65rem', borderBottom: '1px solid var(--rule)', textAlign: 'left' };
  return (
    <div style={{ padding: '1rem', background: 'var(--bg-alt)', borderRadius: 8, margin: '1rem 0', maxWidth: 700 }}>
      <p style={{ margin: '0 0 1rem', fontSize: '1rem' }}>
        Start with six zeros. <strong>Reset</strong> sets every cell to zero; <strong>Flip</strong> reverses every bit.
        Reset then Flip leaves all ones. Flip then Reset leaves all zeros.
      </p>
      <fieldset style={{ border: 0, padding: 0, margin: '0 0 1rem' }}>
        <legend style={{ fontWeight: 600, marginBottom: '0.5rem' }}>How many further steps can you take?</legend>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          {[1, 2].map((count) => (
            <button key={count} type="button" aria-pressed={steps === count} onClick={() => setSteps(count)}
              style={{ padding: '0.6rem 0.9rem', border: '1px solid var(--ink-soft)', borderRadius: 5,
                cursor: 'pointer', font: 'inherit', color: steps === count ? 'var(--bg)' : 'var(--ink)',
                background: steps === count ? 'var(--ink)' : 'var(--bg)' }}>
              Exactly {count === 1 ? 'one step' : 'two steps'}
            </button>
          ))}
        </div>
      </fieldset>
      <div role="region" aria-label="Outcomes after each action sequence" tabIndex={0} style={{ overflowX: 'auto' }}>
        <table style={{ borderCollapse: 'collapse', width: '100%', minWidth: 420, fontSize: '1rem' }}>
          <caption style={{ textAlign: 'left', marginBottom: '0.5rem', color: 'var(--ink-soft)' }}>
            Fixed example: Reset is Rule 0; Flip is Rule 51.
          </caption>
          <thead><tr>
            <th scope="col" style={cell}>Next actions</th>
            <th scope="col" style={cell}>After Reset → Flip</th>
            <th scope="col" style={cell}>After Flip → Reset</th>
          </tr></thead>
          <tbody>{rows.map((row) => <tr key={row.label}>
            <th scope="row" style={{ ...cell, fontWeight: 400 }}>{row.label}</th>
            <td style={cell}>{row.left}</td><td style={cell}>{row.right}</td>
          </tr>)}</tbody>
        </table>
      </div>
      <p aria-live="polite" style={{ margin: '1rem 0 0', fontSize: '1rem' }}>
        {steps === 1
          ? 'With one step, the first preparation can reach only all zeros; the second can reach all zeros or all ones.'
          : 'With two steps, both can reach all zeros or all ones. But Flip → Flip still produces different results: the same options do not mean the same actions work.'}
      </p>
    </div>
  );
}
