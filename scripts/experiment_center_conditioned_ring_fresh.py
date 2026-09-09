#!/usr/bin/env python3
"""Exact fresh-size transfer solver for frozen center-conditioned rule-ring pairs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

RING = ((0, -1), (1, -1), (1, 0), (1, 1),
        (0, 1), (-1, 1), (-1, 0), (-1, -1))
RING_INDEX = {p: i for i, p in enumerate(RING)}
PAIRS = ((14, 31), (39, 54), (54, 39), (85, 170), (91, 41), (187, 17))


def d4_maps():
    fs = (
        lambda x, y: (x, y), lambda x, y: (-y, x),
        lambda x, y: (-x, -y), lambda x, y: (y, -x),
        lambda x, y: (-x, y), lambda x, y: (x, -y),
        lambda x, y: (y, x), lambda x, y: (-y, -x),
    )
    return tuple(dict.fromkeys(tuple(RING_INDEX[f(x, y)] for x, y in RING) for f in fs))


D4 = d4_maps()


def transform(code, mapping):
    out = 0
    for i in range(8):
        out |= ((code >> i) & 1) << mapping[i]
    return out


CANON = tuple(min(transform(r, m) for m in D4) for r in range(256))


def rowbit(row, n, x):
    return (row >> (x % n)) & 1


def ring_from_rows(a, b, c, n, x):
    vals = (
        rowbit(a, n, x), rowbit(a, n, x + 1),
        rowbit(b, n, x + 1), rowbit(c, n, x + 1),
        rowbit(c, n, x), rowbit(c, n, x - 1),
        rowbit(b, n, x - 1), rowbit(a, n, x - 1),
    )
    return sum(v << i for i, v in enumerate(vals))


def triple_valid(a, b, c, n, pair):
    return all(CANON[ring_from_rows(a, b, c, n, x)] == pair[rowbit(b, n, x)] for x in range(n))


def transitions(n, pair):
    rows = range(1 << n)
    trans = {}
    edges = 0
    for a in rows:
        for b in rows:
            cs = tuple(c for c in rows if triple_valid(a, b, c, n, pair))
            if cs:
                trans[(a, b)] = cs
                edges += len(cs)
    return trans, edges


def enumerate_fields(n, pair):
    trans, edges = transitions(n, pair)
    fields = []
    for r0 in range(1 << n):
        for r1 in range(1 << n):
            if (r0, r1) not in trans:
                continue
            rows = [r0, r1]

            def visit():
                if len(rows) == n:
                    if (r0 in trans.get((rows[-2], rows[-1]), ()) and
                            r1 in trans.get((rows[-1], r0), ())):
                        fields.append(tuple(rows))
                    return
                for nxt in trans.get((rows[-2], rows[-1]), ()):
                    rows.append(nxt)
                    visit()
                    rows.pop()

            visit()
    return fields, trans, edges


def field_state(rows, n):
    return sum(row << (y * n) for y, row in enumerate(rows))


def bit(state, n, x, y):
    return (state >> ((y % n) * n + (x % n))) & 1


def ring_code(state, n, x, y):
    return sum(bit(state, n, x + dx, y + dy) << i for i, (dx, dy) in enumerate(RING))


def pair_of_state(state, n):
    seen = (set(), set())
    for y in range(n):
        for x in range(n):
            c = bit(state, n, x, y)
            seen[c].add(CANON[ring_code(state, n, x, y)])
            if len(seen[c]) > 1:
                return None
    if not seen[0] or not seen[1]:
        return None
    return next(iter(seen[0])), next(iter(seen[1]))


def selector_step(state, n, axis):
    out = 0
    for y in range(n):
        for x in range(n):
            ring = ring_code(state, n, x, y)
            center = bit(state, n, x, y)
            if axis == "horizontal":
                q = 4 * ((ring >> 6) & 1) + 2 * center + ((ring >> 2) & 1)
            else:
                q = 4 * (ring & 1) + 2 * center + ((ring >> 4) & 1)
            out |= ((ring >> q) & 1) << (y * n + x)
    return out


def persistence(state, n, axis):
    frozen = set(PAIRS)
    seen = {}
    current = state
    seq = []
    for t in range(65):
        pair = pair_of_state(current, n)
        seq.append(None if pair is None else list(pair))
        if pair not in frozen:
            return {"valid_steps": t, "cycle_length": None, "pair_sequence": seq}
        if current in seen:
            return {"valid_steps": t, "cycle_length": t - seen[current], "pair_sequence": seq}
        seen[current] = t
        current = selector_step(current, n, axis)
    return {"valid_steps": 65, "cycle_length": None, "pair_sequence": seq}


def row_text(row, n):
    return "".join(str(rowbit(row, n, x)) for x in range(n))


def solve(n, pair):
    fields, trans, edges = enumerate_fields(n, pair)
    witness = fields[0] if fields else None
    records = []
    for rows in fields:
        state = field_state(rows, n)
        assert pair_of_state(state, n) == pair
        records.append({
            "rows": [row_text(r, n) for r in rows],
            "state": state,
            "horizontal": persistence(state, n, "horizontal"),
            "vertical": persistence(state, n, "vertical"),
        })
    return {
        "pair": list(pair),
        "field_count": len(fields),
        "transition_edge_count": edges,
        "transition_state_count": len(trans),
        "witness_audit": witness is None or pair_of_state(field_state(witness, n), n) == pair,
        "fields": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results/center_conditioned_ring_fresh_20260909.json"))
    args = parser.parse_args()
    result = {
        "protocol": "docs/research/protocols/center-conditioned-ring-fresh-size-20260909.md",
        "sizes": {str(n): [solve(n, p) for p in PAIRS] for n in (5, 6)},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        n: [[*r["pair"], r["field_count"]] for r in rows]
        for n, rows in result["sizes"].items()
    }, indent=2))


if __name__ == "__main__":
    main()
