import { futurePartition, caExample } from '../lib/reusable-description-model.mjs';

const root = document.getElementById('reusable-descriptions-lab');
const find = id => root.querySelector(`#${id}`);
const alphabet = 'ABCDEFGH';
const formatWord = word => word.map(v => v === 3 ? '3+' : v).join(' · ');

function drawArithmetic() {
  const depth = Number(find('rd-depth').value);
  const groups = futurePartition(3, depth);
  const bad = groups.findIndex(g => g.nextGroups.length > 1);
  find('rd-groups').innerHTML = groups.map((g, i) => `<div class="rd-group" role="listitem" data-conflict="${i === bad}" aria-label="Group ${alphabet[i]}: remainders ${g.residues.join(', ')}; counts ${g.word.join(', ')}${i === bad ? '; conflicting next states' : ''}"><span class="rd-group-name">${alphabet[i]}</span><div class="rd-members">${g.residues.map(r => `<span class="rd-member">${r}</span>`).join('')}</div><span class="rd-group-word text-small">${formatWord(g.word)}</span></div>`).join('');
  find('rd-arithmetic-status').textContent = bad < 0
    ? '8 distinguishable states · every next state is determined'
    : `${groups.length} distinguishable states · group ${alphabet[bad]} still has conflicting successors`;
  if (bad < 0) {
    find('rd-arithmetic-witness').innerHTML = '<div class="text-small">Repair: retain the remainder, 0–7 (three bits).</div><div class="text-small">Next remainder: 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 0</div>';
    return;
  }
  const g = groups[bad];
  const first = g.residues[0];
  const labelOf = r => groups.findIndex(item => item.residues.includes(r % 8));
  const other = g.residues.find(r => labelOf(r + 1) !== labelOf(first + 1));
  const rows = [first, other].map(r => {
    const next = groups[labelOf(r + 1)].word;
    return `<div class="rd-word"><span>r = ${r}</span><span class="rd-word-value">${formatWord(g.word)}</span><span aria-label="increment">→</span><span class="rd-word-value rd-word-output">${formatWord(next)}</span></div>`;
  });
  find('rd-arithmetic-witness').innerHTML = '<div class="text-small">Current description → description after adding one</div>' + rows.join('');
}

function bitRow(label, word, { query = false, different = false } = {}) {
  const bits = [...word].map((b, i) => `<span class="rd-bit" data-bit="${b}" data-query="${query && i >= 2 && i <= 4}" data-different="${different && i === 3}">${b}</span>`).join('');
  return `<div class="rd-bit-row" aria-label="${label}: ${word}"><span class="rd-bit-label text-small">${label}</span><span class="rd-bits" aria-hidden="true">${bits}</span></div>`;
}

function drawCA(stage) {
  root.querySelectorAll('[data-rd-stage]').forEach(b => b.setAttribute('aria-pressed', String(Number(b.dataset.rdStage) === stage)));
  const e = caExample();
  let rows = bitRow('Source S', e.source) + bitRow('Its G: Y', e.y) + bitRow('Next Y', e.cases[0].next);
  if (stage === 0) {
    rows += bitRow('Next again', e.cases[0].next2);
    find('rd-ca-status').textContent = 'Both rules give exactly the same evolution.';
    find('rd-ca-choices').innerHTML = '<div class="text-small">Rules 128 and 160 agree on every valid G₃₂ field.</div>';
  } else {
    rows += bitRow('Difference', e.cases[0].difference, { query: true });
    if (stage === 1) {
      find('rd-ca-status').textContent = 'The difference contains 101; valid G₃₂ fields never do.';
      find('rd-ca-choices').innerHTML = '<div class="text-small">Underlined: the newly encountered neighborhood.</div><div class="text-small">Its rule output is not fixed by valid-field evolution.</div>';
    } else {
      find('rd-ca-status').textContent = 'Same valid evolution · different next G';
      find('rd-ca-choices').innerHTML = e.cases.map(c => `<div class="rd-choice"><div class="rd-choice-label text-small">Rule ${c.rule}: 101 → ${c.rule === 128 ? 0 : 1}</div>${bitRow('Rule on Δ', c.evolvedDifference, { different: true })}${bitRow('Native G', c.g, { different: true })}</div>`).join('');
    }
  }
  find('rd-ca-rows').innerHTML = rows;
}

find('rd-depth').addEventListener('change', drawArithmetic);
root.querySelectorAll('[data-rd-stage]').forEach(b => b.addEventListener('click', () => drawCA(Number(b.dataset.rdStage))));
drawArithmetic();
drawCA(0);
