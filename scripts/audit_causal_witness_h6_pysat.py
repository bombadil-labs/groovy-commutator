"""Independent PySAT/CNF audit for the 12 Research032 h=6 recovery cases."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pysat.solvers import Minisat22

CASES = [
    (122, '00100000', (1, 4)),
    (122, '00100000', (1, 5)),
    (122, '00100000', (3, 6)),
    (122, '00100000', (3, 7)),
    (122, '00100000', (4, 5)),
    (122, '00100000', (6, 7)),
    (161, '00000100', (0, 1)),
    (161, '00000100', (0, 4)),
    (161, '00000100', (1, 4)),
    (161, '00000100', (2, 3)),
    (161, '00000100', (2, 6)),
    (161, '00000100', (3, 6)),
]
HORIZON = 6
MACRO_LEN = 13
FINE_LEN = 39
FINE_TICKS = 18


class CNFBuilder:
    def __init__(self):
        self.next_var = 1
        self.clauses = []

    def var(self):
        v = self.next_var
        self.next_var += 1
        return v

    def unit(self, v, value):
        self.clauses.append([v if value else -v])

    def equal(self, a, b):
        self.clauses.append([-a, b])
        self.clauses.append([a, -b])

    def truth_gate(self, inputs, output, table):
        assert len(inputs) == 3 and len(table) == 8
        for idx in range(8):
            bits = ((idx >> 2) & 1, (idx >> 1) & 1, idx & 1)
            clause = []
            for v, bit in zip(inputs, bits):
                clause.append(-v if bit else v)
            clause.append(output if table[idx] else -output)
            self.clauses.append(clause)


def bit_pattern(symbol):
    return tuple((symbol >> i) & 1 for i in range(3))


def rule_table(rule):
    return tuple((rule >> idx) & 1 for idx in range(8))


def target_table(target):
    return tuple(map(int, target))


def evolve(builder, row, table):
    out = []
    for i in range(len(row) - 2):
        z = builder.var()
        builder.truth_gate((row[i], row[i + 1], row[i + 2]), z, table)
        out.append(z)
    return out


def replay(word, rule):
    row = []
    for symbol in word:
        row.extend(bit_pattern(symbol))
    for _ in range(FINE_TICKS):
        row = [((rule >> (4 * row[i] + 2 * row[i + 1] + row[i + 2])) & 1)
               for i in range(len(row) - 2)]
    assert len(row) == 3
    return row[0] | (row[1] << 1) | (row[2] << 2)


def solve_axis(rule, target, pair, axis):
    builder = CNFBuilder()
    a0 = [builder.var() for _ in range(FINE_LEN)]
    b0 = [builder.var() for _ in range(FINE_LEN)]
    abit = bit_pattern(pair[0])
    bbit = bit_pattern(pair[1])
    changed = set(range(3 * axis, 3 * axis + 3))
    for i in range(FINE_LEN):
        if i in changed:
            j = i - 3 * axis
            builder.unit(a0[i], abit[j])
            builder.unit(b0[i], bbit[j])
        else:
            builder.equal(a0[i], b0[i])
    rt = rule_table(rule)
    arow = a0
    brow = b0
    for _ in range(FINE_TICKS):
        arow = evolve(builder, arow, rt)
        brow = evolve(builder, brow, rt)
    assert len(arow) == len(brow) == 3
    ta = builder.var()
    tb = builder.var()
    tt = target_table(target)
    builder.truth_gate(tuple(arow), ta, tt)
    builder.truth_gate(tuple(brow), tb, tt)
    builder.clauses.append([ta, tb])
    builder.clauses.append([-ta, -tb])

    with Minisat22(bootstrap_with=builder.clauses) as solver:
        is_sat = solver.solve()
        if not is_sat:
            return {'axis': axis, 'status': 'unsat'}
        model = set(x for x in solver.get_model() if x > 0)
    word_a = []
    word_b = []
    for block in range(MACRO_LEN):
        sa = 0
        sb = 0
        for j in range(3):
            i = 3 * block + j
            if a0[i] in model:
                sa |= 1 << j
            if b0[i] in model:
                sb |= 1 << j
        word_a.append(sa)
        word_b.append(sb)
    out_a = replay(word_a, rule)
    out_b = replay(word_b, rule)
    va = int(target[out_a])
    vb = int(target[out_b])
    assert va != vb
    return {
        'axis': axis,
        'status': 'sat',
        'word_a': word_a,
        'word_b': word_b,
        'fine_output_a': out_a,
        'fine_output_b': out_b,
        'target_a': va,
        'target_b': vb,
        'fine_ticks': FINE_TICKS,
        'replay_pass': True,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    rows = []
    for rule, target, pair in CASES:
        axes = [solve_axis(rule, target, pair, axis) for axis in range(MACRO_LEN)]
        sat_axes = [x for x in axes if x['status'] == 'sat']
        rows.append({
            'rule': rule,
            'target': target,
            'pair': f'{pair[0]}-{pair[1]}',
            'axes': axes,
            'h6_witness_exists': bool(sat_axes),
            'first_witness': sat_axes[0] if sat_axes else None,
        })
    out = {
        'ok': True,
        'solver': 'Minisat22 via python-sat',
        'encoding': 'manual CNF over two fine-ECA shrinking cones',
        'horizon': HORIZON,
        'cases': rows,
        'sat_cases': sum(r['h6_witness_exists'] for r in rows),
        'unsat_cases': sum(not r['h6_witness_exists'] for r in rows),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
