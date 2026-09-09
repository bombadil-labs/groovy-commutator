"""Frozen targeted shielding-family census.

See docs/research/protocols/selector-shielding-family-20260908.md.
Run one upper-separation shard with --k K, then --aggregate.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from experiment_pulse_scattering import background, dense_step
from audit_pulse_scattering import sparse_step

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = "docs/research/protocols/selector-shielding-family-20260908.md"
HORIZON = 64
KS = tuple(range(1, 9))


def encode(row: int, support: set[int]) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for i in support:
        out.add((row, 2 * i + 1))
        out.add((row + 1, 2 * i))
    return out


def lower_shapes() -> list[tuple[int, ...]]:
    out = []
    for mask in range(1 << 6):
        s = [0]
        for j in range(6):
            if (mask >> j) & 1:
                s.append(j + 1)
        out.append(tuple(s))
    return out


def value(delta: set[tuple[int, int]], t: int, y: int, x: int) -> int:
    return background(t, x) ^ int((y, x) in delta)


def run_case(k: int, b: tuple[int, ...]) -> tuple[dict, int, int]:
    upper = {-k, 0}
    lower = set(b)
    dense_c = encode(0, upper) | encode(2, lower)
    sparse_c = set(dense_c)
    dense_l = encode(2, lower)
    sparse_l = set(dense_l)

    first_negative = None
    first_lower_difference = None
    checked_fields = 0
    checked_points = 0

    for t in range(HORIZON + 1):
        if dense_c != sparse_c:
            raise AssertionError(f"coupled dense/sparse mismatch k={k} B={b} t={t}")
        if dense_l != sparse_l:
            raise AssertionError(f"reference dense/sparse mismatch k={k} B={b} t={t}")
        checked_fields += 2
        checked_points += len(dense_c) + len(dense_l)

        diff = dense_c ^ dense_l
        if first_lower_difference is None and any(y >= 3 for y, _ in diff):
            first_lower_difference = t

        if first_negative is None:
            for y, x in diff:
                if y != 2:
                    continue
                if value(dense_l, t, 2, x) == 1 and value(dense_c, t, 2, x) == 0:
                    first_negative = t
                    break

        if t < HORIZON:
            dense_c = dense_step(dense_c, t)
            sparse_c = sparse_step(sparse_c, t)
            dense_l = dense_step(dense_l, t)
            sparse_l = sparse_step(sparse_l, t)

    shielded = first_negative is None and first_lower_difference is None
    return ({
        "k": k,
        "upper": [-k, 0],
        "lower": list(b),
        "lower_mass": len(b),
        "lower_span": max(b) + 1,
        "first_negative_row2": first_negative,
        "first_lower_halfplane_difference": first_lower_difference,
        "status": "shielded-through-64" if shielded else "unshielded-by-64",
    }, checked_fields, checked_points)


def run_shard(k: int) -> dict:
    rows = []
    fields = points = 0
    for b in lower_shapes():
        row, f, p = run_case(k, b)
        rows.append(row)
        fields += f
        points += p
    result = {
        "k": k,
        "cases": len(rows),
        "horizon": HORIZON,
        "summary": dict(Counter(r["status"] for r in rows)),
        "checked_complete_fields": fields,
        "checked_changed_points": points,
        "rows": rows,
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
            "dense_kernel": hashlib.sha256((ROOT / "scripts/experiment_pulse_scattering.py").read_bytes()).hexdigest(),
            "sparse_kernel": hashlib.sha256((ROOT / "scripts/audit_pulse_scattering.py").read_bytes()).hexdigest(),
        },
    }
    out = ROOT / f"results/selector_shielding_family_20260908_k{k}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("k", "cases", "summary", "checked_complete_fields", "checked_changed_points")}, indent=2))
    return result


def aggregate() -> dict:
    parts = []
    for k in KS:
        path = ROOT / f"results/selector_shielding_family_20260908_k{k}.json"
        parts.append(json.loads(path.read_text()))
    rows = [r for p in parts for r in p["rows"]]
    if len(rows) != 512 or len({(r["k"], tuple(r["lower"])) for r in rows}) != 512:
        raise AssertionError("shards do not cover the exact frozen 512-case family")
    shields = [r for r in rows if r["status"] == "shielded-through-64"]
    result = {
        "domain": {"k": [1, 8], "lower_shapes": 64, "cases": 512, "horizon": HORIZON},
        "summary": dict(Counter(r["status"] for r in rows)),
        "shielded_cases": shields,
        "shielded_by_k": {str(k): sum(r["k"] == k for r in shields) for k in KS},
        "checked_complete_fields": sum(p["checked_complete_fields"] for p in parts),
        "checked_changed_points": sum(p["checked_changed_points"] for p in parts),
        "source_sha256": parts[0]["source_sha256"],
    }
    out = ROOT / "results/selector_shielding_family_20260908_summary.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("domain", "summary", "shielded_by_k", "checked_complete_fields", "checked_changed_points")}, indent=2))
    for row in shields:
        print("SHIELD", row["k"], row["lower"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, choices=KS)
    parser.add_argument("--aggregate", action="store_true")
    args = parser.parse_args()
    if args.aggregate:
        aggregate()
    elif args.k is not None:
        run_shard(args.k)
    else:
        parser.error("choose --k K or --aggregate")


if __name__ == "__main__":
    main()
