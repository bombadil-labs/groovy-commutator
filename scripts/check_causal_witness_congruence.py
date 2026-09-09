"""Research032: sufficient all-time target-congruence certificates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from experiment_causal_witness_horizon import TARGETS, macro_rule, pkey

A = 8
PAIR_LIST = [(a, b) for a in range(A) for b in range(a + 1, A)]
H5_UNRESOLVED_CENSORED = {122: 6, 126: 21, 129: 21, 146: 21, 161: 6, 182: 21}


def greatest_target_congruence(g, target):
    rel = [[target[a] == target[b] for b in range(A)] for a in range(A)]
    rounds = 0
    while True:
        nxt = [[False] * A for _ in range(A)]
        for a in range(A):
            for b in range(A):
                if not rel[a][b]:
                    continue
                ok = True
                for x in range(A):
                    for y in range(A):
                        if not rel[int(g[64 * a + 8 * x + y])][int(g[64 * b + 8 * x + y])]:
                            ok = False
                            break
                        if not rel[int(g[64 * x + 8 * a + y])][int(g[64 * x + 8 * b + y])]:
                            ok = False
                            break
                        if not rel[int(g[64 * x + 8 * y + a])][int(g[64 * x + 8 * y + b])]:
                            ok = False
                            break
                    if not ok:
                        break
                nxt[a][b] = ok
        assert all(nxt[a][a] for a in range(A))
        assert all(nxt[a][b] == nxt[b][a] for a in range(A) for b in range(A))
        assert all(not (nxt[a][b] and nxt[b][c]) or nxt[a][c]
                   for a in range(A) for b in range(A) for c in range(A))
        rounds += 1
        if nxt == rel:
            return rel, rounds
        rel = nxt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()

    total = 0
    per_rule = []
    max_rounds = 0
    for rule in range(256):
        g = macro_rule(rule)
        certs = []
        count = 0
        for target in TARGETS:
            rel, rounds = greatest_target_congruence(g, target)
            max_rounds = max(max_rounds, rounds)
            for a, b in PAIR_LIST:
                if rel[a][b]:
                    count += 1
                    certs.append({'target': pkey(target), 'pair': f'{a}-{b}'})
        total += count
        row = {'rule': rule, 'certified_pair_targets': count}
        if rule in H5_UNRESOLVED_CENSORED:
            row['h5_unresolved'] = H5_UNRESOLVED_CENSORED[rule]
            row['covers_all_h5_unresolved'] = count == H5_UNRESOLVED_CENSORED[rule]
            row['certificates'] = certs
        per_rule.append(row)

    selected = [r for r in per_rule if r['rule'] in H5_UNRESOLVED_CENSORED]
    assert total == 47352, total
    assert {r['rule'] for r in selected if r['covers_all_h5_unresolved']} == {126, 129, 146, 182}
    assert {r['rule'] for r in selected if not r['covers_all_h5_unresolved']} == {122, 161}
    out = {
        'ok': True,
        'method': 'greatest fixed point of one-coordinate target-respecting substitutivity',
        'h5_unresolved_total': 52712,
        'congruence_certified_total': total,
        'certified_fraction_of_h5_unresolved': total / 52712,
        'noncongruence_remainder': 52712 - total,
        'max_refinement_rounds': max_rounds,
        'censored_rules': selected,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
