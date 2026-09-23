#!/usr/bin/env python3
"""Small exact replays for the reusable-descriptions proof/explainer.

No census or fitted rule. Complete seven-bit cones certify the displayed
Rule-32 identities; the note supplies the general arithmetic proof.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / 'results/reusable_descriptions_20260923.json'
PINNED = [
    'docs/research/protocols/reusable-descriptions-20260923.md',
    'scripts/verify_reusable_descriptions.py',
    'site/src/lib/reusable-description-model.mjs',
]


def valuation(n: int, k: int) -> int:
    return next((j for j in range(k) if n % (2 ** (j + 1))), k)


def partition(k: int, depth: int) -> list[dict]:
    m = 2 ** k
    words: dict[tuple, list] = {}
    for r in range(m):
        word = tuple(valuation(r + t, k) for t in range(depth + 1))
        words.setdefault(word, []).append(r)
    groups = list(words.items())
    labels = {r: i for i, (_, rs) in enumerate(groups) for r in rs}
    return [dict(word=list(w), residues=rs,
                 nextGroups=list(dict.fromkeys(labels[(r + 1) % m] for r in rs)))
            for w, rs in groups]


def local(rule: int, a: int, b: int, c: int) -> int:
    # A table of rule outputs, indexed from 000 to 111.
    return int(f'{rule:08b}'[::-1][4 * a + 2 * b + c])


def crop_step(rule: int, row: list[int]) -> list[int]:
    return [local(rule, *row[i:i + 3]) for i in range(len(row) - 2)]


def xor(a: list[int], b: list[int]) -> list[int]:
    assert len(a) == len(b)
    return [int(x != y) for x, y in zip(a, b)]


def crop_g(rule: int, row: list[int]) -> list[int]:
    e = crop_step(rule, row)
    d = xor(row[1:-1], e)
    return xor(xor(e[1:-1], crop_step(rule, e)), crop_step(rule, d))


def ring_step(rule: int, row: list[int]) -> list[int]:
    return crop_step(rule, [row[-1], *row, row[0]])


def ring_g(rule: int, row: list[int]) -> list[int]:
    e = ring_step(rule, row)
    return xor(xor(e, ring_step(rule, e)), ring_step(rule, xor(row, e)))


def bits(row: list[int]) -> str:
    return ''.join(map(str, row))


def verify() -> dict:
    arithmetic = []
    for k in (1, 2, 3, 4):
        m = 2 ** k
        ps = [partition(k, h) for h in range(m)]
        assert len(ps[-1]) == m
        for x, y in itertools.product(range(m), repeat=2):
            assert valuation(x * y, k) == min(valuation(x, k) + valuation(y, k), k)
            if x != y:
                # At this nonnegative time x reaches residue zero and y cannot.
                t = (-x) % m
                assert valuation(x + t, k) == k > valuation(y + t, k)
        arithmetic.append(dict(k=k, modulus=m,
                               values=[valuation(r, k) for r in range(m)], partitions=ps))

    patterns = set()
    for word in itertools.product((0, 1), repeat=7):
        s = list(word)
        y = crop_g(32, s)
        patterns.add(bits(y))
        assert bits(y) != '101'
        assert crop_step(32, xor(s[1:-1], crop_step(32, s))) == [0, 0, 0]
        expected = crop_g(32, crop_step(32, s))
        assert crop_step(128, y) == expected == crop_step(160, y)
    assert patterns == {'000', '001', '010', '011', '100', '110', '111'}
    assert [i for i in range(8) if (128 >> i & 1) != (160 >> i & 1)] == [5]

    s = [int(x) for x in '0101010']
    y = ring_g(32, s)
    cases = []
    for rule in (128, 160):
        e = ring_step(rule, y)
        d = xor(y, e)
        cases.append(dict(rule=rule, next=bits(e), next2=bits(ring_step(rule, e)),
                          difference=bits(d), evolvedDifference=bits(ring_step(rule, d)),
                          g=bits(ring_g(rule, y))))
    c = [1 - x for x in s]
    witness = dict(zeroG=bits(ring_g(32, [0] * 7)), oneG=bits(ring_g(32, [1] * 7)),
                   operand=bits(s), operandG=bits(y), complement=bits(c),
                   complementG=bits(ring_g(32, c)))
    assert witness['zeroG'] == witness['oneG']
    assert witness['operandG'] != witness['complementG']
    assert cases[0]['next'] == cases[1]['next']
    assert cases[0]['g'] != cases[1]['g']
    return dict(arithmetic=arithmetic, ca=dict(source=bits(s), sourceNext=bits(ring_step(32, s)),
                                             y=bits(y), cases=cases, xorWitness=witness))


def record() -> dict:
    return dict(schema=1, scope='Exact proof examples; no statistical experiment',
                sha256={p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in PINNED},
                checks=dict(source_cone_length=7, source_cones=128, arithmetic_caps=[1, 2, 3, 4]),
                examples=verify())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Create the evidence once; refuse overwrite.')
    args = parser.parse_args()
    result = record()
    if args.write:
        with RESULT.open('x') as out:
            json.dump(result, out, indent=2)
            out.write('\n')
        print(f'Created {RESULT.relative_to(ROOT)}')
    else:
        assert json.loads(RESULT.read_text()) == result, 'Evidence or pinned implementation changed.'
        print('Verified: four arithmetic controls, 128 complete cones, both operation witnesses, all hashes.')


if __name__ == '__main__':
    main()
