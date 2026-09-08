"""Frozen selector-relative shielding validation.

See docs/research/protocols/selector-shielding-20260908.md.
The witness and horizon are fixed before evaluation.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import time

from experiment_pulse_scattering import background, canonical_digest, dense_step
from audit_pulse_scattering import sparse_step

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/selector_shielding_20260908.json"
PROTOCOL = "docs/research/protocols/selector-shielding-20260908.md"
HORIZON = 1024
A = {-5, 0}
B = {0, 1, 3, 4, 6}


def encode_strip(row: int, support: set[int]) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for i in support:
        out.add((row, 2 * i + 1))
        out.add((row + 1, 2 * i))
    return out


def seed_coupled() -> set[tuple[int, int]]:
    return encode_strip(0, A) | encode_strip(2, B)


def seed_lower() -> set[tuple[int, int]]:
    return encode_strip(2, B)


def value(delta: set[tuple[int, int]], t: int, y: int, x: int) -> int:
    return background(t, x) ^ int((y, x) in delta)


def vulnerable_row2_sites(
    row2_contamination: set[int],
    reference: set[tuple[int, int]],
    t: int,
) -> set[int]:
    """Which contaminated row-2 sites are selected by any row-3 destination?

    A row-3 destination can shift horizontally by only -1, 0, +1, so a
    contaminated source q can only be selected by destinations q-1, q, q+1.
    Under row-3 shielding the coupled and reference selectors are identical;
    use the reference row to avoid coupling the diagnostic to the contaminant.
    """
    vulnerable: set[int] = set()
    for q in row2_contamination:
        for x in (q - 1, q, q + 1):
            center = value(reference, t, 3, x)
            if center != 0:
                continue  # this destination reads row 4, not row 2
            left = value(reference, t, 3, x - 1)
            right = value(reference, t, 3, x + 1)
            sx = x + left + right - 1
            if sx == q:
                vulnerable.add(q)
                break
    return vulnerable


def row_support(delta: set[tuple[int, int]], row: int) -> list[int]:
    return sorted(x for y, x in delta if y == row)


def diff_rows(coupled: set[tuple[int, int]], reference: set[tuple[int, int]]):
    diff = coupled ^ reference
    rows: dict[int, set[int]] = {}
    for y, x in diff:
        rows.setdefault(y, set()).add(x)
    return diff, rows


def metric(
    coupled: set[tuple[int, int]],
    reference: set[tuple[int, int]],
    t: int,
) -> dict:
    diff, rows = diff_rows(coupled, reference)
    q = rows.get(2, set())
    vulnerable = vulnerable_row2_sites(q, reference, t)
    lower_diff = {(y, x) for y, x in diff if y >= 3}
    return {
        "tick": t,
        "coupled_mass": len(coupled),
        "reference_mass": len(reference),
        "difference_mass": len(diff),
        "row2_difference": sorted(q),
        "row2_difference_mass": len(q),
        "row3_equal": 3 not in rows,
        "lower_halfplane_equal": not lower_diff,
        "selected_row2_contamination": sorted(vulnerable),
        "selected_row2_contamination_mass": len(vulnerable),
        "coupled_sha256": canonical_digest(coupled),
        "reference_sha256": canonical_digest(reference),
    }


def failure_record(
    tick: int,
    previous: dict | None,
    current: dict,
    coupled: set[tuple[int, int]],
    reference: set[tuple[int, int]],
) -> dict:
    diff = coupled ^ reference
    row3 = sorted(x for y, x in diff if y == 3)
    return {
        "tick": tick,
        "kind": "row3-shielding-failure",
        "row3_difference": row3,
        "previous_metric": previous,
        "current_metric": current,
        "coupled_row2": row_support(coupled, 2),
        "reference_row2": row_support(reference, 2),
        "coupled_row3": row_support(coupled, 3),
        "reference_row3": row_support(reference, 3),
    }


def main() -> None:
    started = time.time()
    coupled_dense = seed_coupled()
    coupled_sparse = set(coupled_dense)
    lower_dense = seed_lower()
    lower_sparse = set(lower_dense)

    rows: list[dict] = []
    failure = None
    first_row2_difference = None
    max_row2_difference_mass = 0
    max_total_difference_mass = 0

    for t in range(HORIZON + 1):
        if coupled_dense != coupled_sparse:
            raise AssertionError(f"coupled dense/sparse mismatch at tick {t}")
        if lower_dense != lower_sparse:
            raise AssertionError(f"reference dense/sparse mismatch at tick {t}")

        m = metric(coupled_dense, lower_dense, t)
        rows.append(m)
        if m["row2_difference_mass"] and first_row2_difference is None:
            first_row2_difference = t
        max_row2_difference_mass = max(max_row2_difference_mass, m["row2_difference_mass"])
        max_total_difference_mass = max(max_total_difference_mass, m["difference_mass"])

        if not m["row3_equal"]:
            failure = failure_record(t, rows[-2] if len(rows) > 1 else None, m,
                                     coupled_dense, lower_dense)
            break
        if not m["lower_halfplane_equal"]:
            failure = {
                "tick": t,
                "kind": "lower-halfplane-failure-before-row3-failure",
                "metric": m,
            }
            break
        if m["selected_row2_contamination_mass"]:
            failure = {
                "tick": t,
                "kind": "selector-overlap-before-row3-failure",
                "metric": m,
            }
            break

        if t < HORIZON:
            coupled_dense = dense_step(coupled_dense, t)
            coupled_sparse = sparse_step(coupled_sparse, t)
            lower_dense = dense_step(lower_dense, t)
            lower_sparse = sparse_step(lower_sparse, t)

    direct_through = rows[-1]["tick"]
    result = {
        "protocol": PROTOCOL,
        "witness": {"A": sorted(A), "B": sorted(B)},
        "horizon": HORIZON,
        "directly_simulated_through": direct_through,
        "finite_horizon_survives": failure is None and direct_through == HORIZON,
        "failure": failure,
        "first_row2_difference": first_row2_difference,
        "max_row2_difference_mass": max_row2_difference_mass,
        "max_total_difference_mass": max_total_difference_mass,
        "all_row3_equal": all(r["row3_equal"] for r in rows),
        "all_lower_halfplane_equal": all(r["lower_halfplane_equal"] for r in rows),
        "all_selector_overlaps_empty": all(r["selected_row2_contamination_mass"] == 0 for r in rows),
        "ticks": rows,
        "seconds": round(time.time() - started, 3),
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
            "dense_kernel": hashlib.sha256((ROOT / "scripts/experiment_pulse_scattering.py").read_bytes()).hexdigest(),
            "sparse_kernel": hashlib.sha256((ROOT / "scripts/audit_pulse_scattering.py").read_bytes()).hexdigest(),
        },
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "finite_horizon_survives": result["finite_horizon_survives"],
        "directly_simulated_through": direct_through,
        "first_row2_difference": first_row2_difference,
        "max_row2_difference_mass": max_row2_difference_mass,
        "max_total_difference_mass": max_total_difference_mass,
        "all_row3_equal": result["all_row3_equal"],
        "all_lower_halfplane_equal": result["all_lower_halfplane_equal"],
        "all_selector_overlaps_empty": result["all_selector_overlaps_empty"],
        "failure": failure,
        "seconds": result["seconds"],
    }, indent=2))
    if failure is not None:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
