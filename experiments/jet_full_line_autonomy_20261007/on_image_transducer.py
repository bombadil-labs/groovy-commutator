#!/usr/bin/env python3
"""Rule54 J5 on-image (non-deterministic) symbolic transducer.

Source: 15-bit edges, 14-bit source contexts; input J5, output A6.
Use triangular recurrence to reconstruct the entire next J5. Runnable
without dependencies. This is not a minimal DFA, a compression result,
or an off-image extension. Prospective gate: see corresponding protocol.
"""
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

RULE = 54
STATES, EDGES = 1 << 14, 1 << 15


def h(l, c, r):
    return (RULE >> (4 * l + 2 * c + r)) & 1


def evolve_middle(w, width):
    return sum(h((w >> j) & 1, (w >> (j + 1)) & 1,
                 (w >> (j + 2)) & 1) << j for j in range(width - 2))


def truth_tables():
    a = [[((w >> 1) & 1) ^ h(w & 1, (w >> 1) & 1, (w >> 2) & 1)
          for w in range(8)]]
    for k in range(1, 7):
        width = 2*k + 3
        mask = (1 << (width - 2)) - 1
        p = a[-1]
        a.append([p[evolve_middle(w, width)] ^
                  h(p[w & mask], p[(w >> 1) & mask], p[(w >> 2) & mask])
                  for w in range(1 << width)])
    return a


def jet(w, width, a):
    return sum(a[k][(w >> ((width - 2*k - 3)//2)) &
                    ((1 << (2*k + 3)) - 1)] << (k-1)
               for k in range(1, 6))


def ring_step(s, n):
    return sum(h((s >> ((i-1) % n)) & 1, (s >> i) & 1,
                 (s >> ((i+1) % n)) & 1) << i for i in range(n))


def window15(s, n, i):
    return sum(((s >> ((i+j-7) % n)) & 1) << j for j in range(15))


def check_rings(inputs, outputs, missing):
    rows = []
    for n in (8, 10, 12):
        size = 1 << n
        evolved = [ring_step(s, n) for s in range(size)]
        a = [[s ^ evolved[s] for s in range(size)]]
        for k in range(1, 7):
            p = a[-1]
            a.append([p[evolved[s]] ^ evolved[p[s]] for s in range(size)])
        fibers = defaultdict(lambda: [None, 0])
        errors = conflicts = 0
        for s in range(size):
            before = tuple(sum(((a[k][s] >> i) & 1) << (k-1)
                               for k in range(1, 6)) for i in range(n))
            after = tuple(sum(((a[k][evolved[s]] >> i) & 1) << (k-1)
                              for k in range(1, 6)) for i in range(n))
            for i in range(n):
                w = window15(s, n, i)
                errors += (inputs[w] != before[i] or
                           outputs[w] != after[i] or
                           missing[w] != ((a[6][s] >> i) & 1))
            fiber = fibers[before]
            if fiber[0] is not None and fiber[0] != after:
                conflicts += 1
            fiber[0] = after
            fiber[1] += 1
        sizes = [f[1] for f in fibers.values()]
        rows.append(dict(n=n, source_states=size, images=len(fibers),
                         nontrivial_fibers=sum(x > 1 for x in sizes),
                         maximum_fiber=max(sizes), conflicts=conflicts,
                         label_errors=errors))
    return rows


def check_local_decoder(inputs, missing):
    rows = []
    for t in range(32):
        # Fixed non-random period-24 binary configurations.
        s = sum(((j//(1+t%5) + j//(2+(3*t)%7) +
                  ((j*(t+3)) >> 2) + (j%3 == t%3)) & 1) << j
                for j in range(24))
        observed = [inputs[window15(s, 24, i)] for i in range(-6, 7)]
        cache = {}
        def field(k, x):
            key = k, x
            if key not in cache:
                hx = ring_step(x, 24)
                cache[key] = x ^ hx if k == 0 else (
                    field(k-1, hx) ^ ring_step(field(k-1, x), 24))
            return cache[key]
        truth = field(6, s) & 1
        active = set(range(STATES))
        counts = []
        for pos, symbol in enumerate(observed):
            nxt = set()
            for code in active:
                state = code if pos <= 6 else code >> 1
                latched = 0 if pos <= 6 else code & 1
                for bit in (0, 1):
                    edge = state + (bit << 14)
                    if inputs[edge] != symbol:
                        continue
                    dest = edge >> 1
                    nxt.add(dest if pos < 6 else
                            ((dest << 1) | (missing[edge] if pos == 6
                                            else latched)))
            active = nxt
            counts.append(len(active))
        outputs = sorted({code & 1 for code in active})
        rows.append(dict(case=t, source_hex=hex(s), native_A6=truth,
                         possible_A6=outputs, max_contexts=max(counts),
                         final_contexts=len(active), live_counts=counts))
    return rows


def main():
    a = truth_tables()
    label13 = [jet(w, 13, a) for w in range(1 << 13)]
    inputs = [label13[(w >> 1) & 8191] for w in range(EDGES)]
    missing = a[6]
    outputs = [jet(evolve_middle(w, 15), 13, a) for w in range(EDGES)]
    failures = 0
    for w in range(EDGES):
        lo, mid, hi = (label13[w & 8191], inputs[w],
                       label13[(w >> 2) & 8191])
        after = 0
        for bit in range(5):
            carry = missing[w] if bit == 4 else ((mid >> (bit + 1)) & 1)
            after |= (h((lo >> bit) & 1, (mid >> bit) & 1,
                        (hi >> bit) & 1) ^ carry) << bit
        failures += after != outputs[w]
    rings = check_rings(inputs, outputs, missing)
    blocks = check_local_decoder(inputs, missing)
    result = dict(schema='rule54-on-image-transducer-v1',
                  states=STATES, edges=EDGES,
                  distinct_input_letters=len(set(inputs)),
                  distinct_local_input_output_pairs=len(set(zip(inputs, outputs))),
                  triangular_errors=failures, rings=rings,
                  blocks_tested=len(blocks), distinct_sources=len({b['source_hex'] for b in blocks}),
                  all_blocks_singleton=all(b['possible_A6'] == [b['native_A6']] for b in blocks),
                  max_live_contexts=max(b['max_contexts'] for b in blocks),
                  final_contexts_range=(min(b['final_contexts'] for b in blocks),
                                        max(b['final_contexts'] for b in blocks)),
                  block_summaries=[{k:v for k,v in b.items() if k!='live_counts'} for b in blocks],
                  note='Finite-ring and selected-block implementation tests, not full-line peer review.')
    print(json.dumps(result, indent=2))
    assert not failures and all(x['label_errors'] == x['conflicts'] == 0 for x in rings)
    assert result['all_blocks_singleton']


if __name__ == '__main__':
    main()
