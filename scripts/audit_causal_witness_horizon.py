"""Independent scalar audit of the four Research031 horizon-3 witnesses."""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule_int  # noqa:E402

A = 8
CASES = [
    (35, "00000001", 2, 6),
    (49, "00000001", 2, 3),
    (59, "01111111", 1, 5),
    (115, "01111111", 4, 5),
]


def macro_rule_scalar(rule):
    g = [0] * 512
    for left in range(8):
        for center in range(8):
            for right in range(8):
                state = left | (center << 3) | (right << 6)
                for _ in range(3):
                    state = apply_rule_int(state, 9, rule)
                g[64 * left + 8 * center + right] = (state >> 3) & 7
    return g


def evolve_word(word, g, t):
    x = list(word)
    for _ in range(t):
        x = [g[64 * x[i] + 8 * x[i + 1] + x[i + 2]] for i in range(len(x) - 2)]
    assert len(x) == 1
    return x[0]


def fine_center(word, rule, t):
    bits = []
    for symbol in word:
        bits += [(symbol >> i) & 1 for i in range(3)]
    lut = [(rule >> i) & 1 for i in range(8)]
    x = bits
    for _ in range(3 * t):
        x = [lut[4 * x[i] + 2 * x[i + 1] + x[i + 2]] for i in range(len(x) - 2)]
    assert len(x) == 3
    return x[0] | (x[1] << 1) | (x[2] << 2)


def search(rule, key, a, b):
    target = tuple(map(int, key))
    g = macro_rule_scalar(rule)
    counts = {}
    for t in range(4):
        length = 2 * t + 1
        checked = 0
        found = None
        for axis in range(length):
            others = [i for i in range(length) if i != axis]
            for context in itertools.product(range(A), repeat=length - 1):
                word_a = [0] * length
                word_b = [0] * length
                word_a[axis] = a
                word_b[axis] = b
                for pos, value in zip(others, context):
                    word_a[pos] = value
                    word_b[pos] = value
                out_a = evolve_word(word_a, g, t)
                out_b = evolve_word(word_b, g, t)
                checked += 1
                if target[out_a] != target[out_b]:
                    found = {
                        "horizon": t,
                        "axis": axis,
                        "word_a": word_a,
                        "word_b": word_b,
                        "macro_output_a": out_a,
                        "macro_output_b": out_b,
                        "target_a": target[out_a],
                        "target_b": target[out_b],
                        "contexts_checked_until_witness": checked,
                    }
                    if t == 3:
                        fine_a = fine_center(word_a, rule, t)
                        fine_b = fine_center(word_b, rule, t)
                        assert fine_a == out_a and fine_b == out_b
                        found["fine_output_a"] = fine_a
                        found["fine_output_b"] = fine_b
                        found["fine_ticks"] = 9
                    break
            if found:
                break
        counts[str(t)] = checked
        if found:
            if t < 3:
                raise AssertionError((rule, key, a, b, "premature witness", found))
            return {
                "rule": rule,
                "target": key,
                "pair": f"{a}-{b}",
                "no_witness_context_counts_h0_h2": {k: v for k, v in counts.items() if int(k) < 3},
                "witness": found,
            }
    raise AssertionError((rule, key, a, b, "no h3 witness"))


def reflection(rule):
    out = 0
    for idx in range(8):
        left, center, right = (idx >> 2) & 1, (idx >> 1) & 1, idx & 1
        src = 4 * right + 2 * center + left
        out |= ((rule >> src) & 1) << idx
    return out


def complement_conjugate(rule):
    out = 0
    for idx in range(8):
        left, center, right = (idx >> 2) & 1, (idx >> 1) & 1, idx & 1
        src = 4 * (1 - left) + 2 * (1 - center) + (1 - right)
        out |= (1 - ((rule >> src) & 1)) << idx
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    rows = [search(*case) for case in CASES]
    orbit = sorted({35, reflection(35), complement_conjugate(35), reflection(complement_conjugate(35))})
    assert orbit == [35, 49, 59, 115]
    out = {
        "ok": True,
        "method": "independent scalar macro rule, exhaustive contexts through h2, explicit h3 witness, direct fine-ECA replay",
        "standard_symmetry_orbit": orbit,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
