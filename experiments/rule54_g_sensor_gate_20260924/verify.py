"""Independent bit-parallel G evaluator and direct observed-fiber audit."""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIDTH = 34
MASK = (1 << WIDTH) - 1


def step_bits(x):
    left = ((x << 1) | (x >> (WIDTH - 1))) & MASK
    right = (x >> 1) | ((x & 1) << (WIDTH - 1))
    # Rule 54 outputs one on triples 001, 010, 100, 101.
    return ((~left & ~x & right) | (~left & x & ~right)
            | (left & ~x & ~right) | (left & ~x & right)) & MASK


def g_bits(x):
    y = step_bits(x)
    return y ^ step_bits(y) ^ step_bits(x ^ y)


def best(fibers):
    return sum(max(sum(a in row["winning_actions"] for row in members)
                   for a in (-1, *range(WIDTH))) for members in fibers.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text())
    assert result["schema"] == "rule54-g-sensor-gate-v1"
    source_path = ROOT / result["source"]
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == result["source_sha256"]
    for path, digest in result["source_hashes"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    rows = json.loads(source_path.read_text())["trials"]
    raw, g, single = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in rows:
        state = row["at_decision"]
        raw[state].append(row)
        g[g_bits(state)].append(row)
        single[0].append(row)
    assert len(rows) == result["trials"] == WIDTH ** 2
    assert len(raw) == result["full_source_fibers"]
    assert len(g) == result["full_g_fibers"]
    assert best(single) == result["best_fixed_score"]
    assert best(raw) == result["full_source_score"]
    assert best(g) == result["full_g_score"]
    assert result["loss_from_source"] == best(raw) - best(g) >= 0
    witness = result["g_witness"]
    if witness is not None:
        found = set()
        for item in witness["rows"]:
            matches = [r for r in g[witness["g_word"]]
                       if r["rotation"] == item["rotation"] and r["injury"] == item["injury"]]
            assert len(matches) == 1
            assert all(matches[0][field] == item[field] for field in ("at_decision", "winning_actions"))
            found.add((item["rotation"], item["injury"]))
        assert len(found) == len(witness["rows"]) >= 2
        assert not set.intersection(*(set(item["winning_actions"]) for item in witness["rows"]))
        assert result["loss_from_source"] > 0
    else:
        assert result["loss_from_source"] == 0
    assert result["predictions"]["P1_g_loses_at_least_one"] == (
        "supported" if result["loss_from_source"] else "failed")
    assert result["predictions"]["P2_g_never_beats_source"] == "supported"
    print("Independent bit-parallel G and fiber counts verified")


if __name__ == "__main__":
    main()
