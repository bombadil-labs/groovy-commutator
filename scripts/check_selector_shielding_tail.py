"""Fresh validation of the post-census shielding prefix code.

See docs/research/protocols/selector-shielding-tail-validation-20260908.md.
Run --tail 7, --tail 8, and --tail 78, then --aggregate.
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
PROTOCOL = "docs/research/protocols/selector-shielding-tail-validation-20260908.md"
HORIZON = 64
TAILS = {"7": {7}, "8": {8}, "78": {7, 8}}
UPPER = {-5, 0}


def encode(row: int, support: set[int]) -> set[tuple[int, int]]:
    out = set()
    for i in support:
        out.add((row, 2 * i + 1))
        out.add((row + 1, 2 * i))
    return out


def prefixes() -> list[set[int]]:
    out = []
    for mask in range(1 << 6):
        s = {0}
        for j in range(6):
            if (mask >> j) & 1:
                s.add(j + 1)
        out.append(s)
    return out


def predicted_negative(s: set[int]) -> int | None:
    if 1 not in s:
        return 4
    if 2 in s or 3 not in s:
        return 5
    if 4 not in s or not ({5, 6} & s):
        return 8
    if 5 in s and 6 in s:
        return 15
    return None


def value(delta, t, y, x):
    return background(t, x) ^ int((y, x) in delta)


def run_case(lower: set[int]) -> tuple[dict, int, int]:
    dc = encode(0, UPPER) | encode(2, lower)
    sc = set(dc)
    dl = encode(2, lower)
    sl = set(dl)
    first_neg = first_lower = None
    fields = points = 0

    for t in range(HORIZON + 1):
        if dc != sc:
            raise AssertionError(f"coupled dense/sparse mismatch B={sorted(lower)} t={t}")
        if dl != sl:
            raise AssertionError(f"reference dense/sparse mismatch B={sorted(lower)} t={t}")
        fields += 2
        points += len(dc) + len(dl)
        diff = dc ^ dl
        if first_lower is None and any(y >= 3 for y, _ in diff):
            first_lower = t
        if first_neg is None:
            for y, x in diff:
                if y == 2 and value(dl, t, 2, x) == 1 and value(dc, t, 2, x) == 0:
                    first_neg = t
                    break
        if t < HORIZON:
            dc = dense_step(dc, t); sc = sparse_step(sc, t)
            dl = dense_step(dl, t); sl = sparse_step(sl, t)

    pred = predicted_negative(lower)
    expected_lower = None if pred is None else pred + 1
    passed = first_neg == pred and first_lower == expected_lower
    return ({
        "lower": sorted(lower),
        "predicted_negative": pred,
        "observed_negative": first_neg,
        "predicted_lower_difference": expected_lower,
        "observed_lower_difference": first_lower,
        "predicted_status": "shielded-through-64" if pred is None else "unshielded-by-64",
        "observed_status": "shielded-through-64" if first_neg is None and first_lower is None else "unshielded-by-64",
        "passes": passed,
    }, fields, points)


def run_tail(name: str) -> dict:
    tail = TAILS[name]
    rows = []
    fields = points = 0
    for prefix in prefixes():
        lower = prefix | tail
        row, f, p = run_case(lower)
        rows.append(row); fields += f; points += p
    failures = [r for r in rows if not r["passes"]]
    result = {
        "tail": sorted(tail),
        "cases": len(rows),
        "ok": not failures,
        "status_counts": dict(Counter(r["observed_status"] for r in rows)),
        "predicted_status_counts": dict(Counter(r["predicted_status"] for r in rows)),
        "failures": failures,
        "rows": rows,
        "checked_complete_fields": fields,
        "checked_changed_points": points,
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
            "dense_kernel": hashlib.sha256((ROOT / "scripts/experiment_pulse_scattering.py").read_bytes()).hexdigest(),
            "sparse_kernel": hashlib.sha256((ROOT / "scripts/audit_pulse_scattering.py").read_bytes()).hexdigest(),
        },
    }
    out = ROOT / f"results/selector_shielding_tail_20260908_{name}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("tail", "cases", "ok", "status_counts", "checked_complete_fields", "checked_changed_points")}, indent=2))
    if failures:
        print(json.dumps(failures[:10], indent=2))
        raise SystemExit(1)
    return result


def aggregate() -> dict:
    parts = [json.loads((ROOT / f"results/selector_shielding_tail_20260908_{name}.json").read_text()) for name in TAILS]
    result = {
        "ok": all(p["ok"] for p in parts),
        "cases": sum(p["cases"] for p in parts),
        "tails": [p["tail"] for p in parts],
        "status_counts": dict(Counter(r["observed_status"] for p in parts for r in p["rows"])),
        "prediction_failures": sum(len(p["failures"]) for p in parts),
        "checked_complete_fields": sum(p["checked_complete_fields"] for p in parts),
        "checked_changed_points": sum(p["checked_changed_points"] for p in parts),
        "source_sha256": parts[0]["source_sha256"],
    }
    out = ROOT / "results/selector_shielding_tail_20260908_summary.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        raise SystemExit(1)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tail", choices=tuple(TAILS))
    ap.add_argument("--aggregate", action="store_true")
    args = ap.parse_args()
    if args.aggregate:
        aggregate()
    elif args.tail:
        run_tail(args.tail)
    else:
        ap.error("choose --tail or --aggregate")


if __name__ == "__main__":
    main()
