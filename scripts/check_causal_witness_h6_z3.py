"""Independent Z3 recovery for the 12 h=6 cases censored by the MDD."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from z3 import And, Bool, BoolVal, Not, Or, Solver, sat

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
MACRO_LEN = 2 * HORIZON + 1
FINE_LEN = 3 * MACRO_LEN
FINE_TICKS = 3 * HORIZON


def bit_pattern(symbol: int):
    return tuple((symbol >> i) & 1 for i in range(3))


def eca_expr(left, center, right, rule: int):
    terms = []
    for idx in range(8):
        if not ((rule >> idx) & 1):
            continue
        bits = ((idx >> 2) & 1, (idx >> 1) & 1, idx & 1)
        vars_ = (left, center, right)
        terms.append(And(*[v if b else Not(v) for v, b in zip(vars_, bits)]))
    if not terms:
        return BoolVal(False)
    return Or(*terms)


def target_expr(bits, target: str):
    terms = []
    for symbol, out in enumerate(map(int, target)):
        if not out:
            continue
        pattern = bit_pattern(symbol)
        terms.append(And(*[v if b else Not(v) for v, b in zip(bits, pattern)]))
    if not terms:
        return BoolVal(False)
    return Or(*terms)


def shrink(row, rule: int):
    return [eca_expr(row[i], row[i + 1], row[i + 2], rule) for i in range(len(row) - 2)]


def replay(word, rule: int):
    row = []
    for symbol in word:
        row.extend(bit_pattern(symbol))
    for _ in range(FINE_TICKS):
        row = [((rule >> (4 * row[i] + 2 * row[i + 1] + row[i + 2])) & 1)
               for i in range(len(row) - 2)]
    assert len(row) == 3
    return row[0] | (row[1] << 1) | (row[2] << 2)


def solve_axis(rule: int, target: str, pair, axis: int):
    a, b = pair
    solver = Solver()
    shared = [Bool(f'c_{i}') for i in range(FINE_LEN)]
    row_a = []
    row_b = []
    changed = set(range(3 * axis, 3 * axis + 3))
    abit = bit_pattern(a)
    bbit = bit_pattern(b)
    for i in range(FINE_LEN):
        if i in changed:
            j = i - 3 * axis
            row_a.append(BoolVal(bool(abit[j])))
            row_b.append(BoolVal(bool(bbit[j])))
        else:
            row_a.append(shared[i])
            row_b.append(shared[i])
    for _ in range(FINE_TICKS):
        row_a = shrink(row_a, rule)
        row_b = shrink(row_b, rule)
    assert len(row_a) == len(row_b) == 3
    solver.add(target_expr(row_a, target) != target_expr(row_b, target))
    status = solver.check()
    if status != sat:
        return {'axis': axis, 'status': 'unsat'}
    model = solver.model()
    word_a = []
    word_b = []
    for block in range(MACRO_LEN):
        if block == axis:
            word_a.append(a)
            word_b.append(b)
            continue
        symbol = 0
        for j in range(3):
            i = 3 * block + j
            if bool(model.eval(shared[i], model_completion=True)):
                symbol |= 1 << j
        word_a.append(symbol)
        word_b.append(symbol)
    out_a = replay(word_a, rule)
    out_b = replay(word_b, rule)
    ta = int(target[out_a])
    tb = int(target[out_b])
    assert ta != tb
    return {
        'axis': axis,
        'status': 'sat',
        'word_a': word_a,
        'word_b': word_b,
        'fine_output_a': out_a,
        'fine_output_b': out_b,
        'target_a': ta,
        'target_b': tb,
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
        'solver': 'z3',
        'encoding': 'paired 39-cell shrinking fine-ECA cones for 18 ticks',
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
