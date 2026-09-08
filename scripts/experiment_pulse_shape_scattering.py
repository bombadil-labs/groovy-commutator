"""Frozen Research021 finite pulse-shape scattering census.

See docs/research/protocols/pulse-shape-scattering-20260908.md before changing
any scientific domain, status, or certificate criterion.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import hashlib
import json
import time

from experiment_pulse_scattering import (
    background,
    canonical_digest,
    dense_step,
    v0_member,
)
from audit_pulse_scattering import sparse_step

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/pulse_shape_scattering_20260908.json"
PROTOCOL = "docs/research/protocols/pulse-shape-scattering-20260908.md"
D_MIN, D_MAX, HORIZON = -12, 12, 128

# Exact order frozen in the protocol.
SHAPES = [
    (0,),
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 1, 2),
    (0, 1, 3),
    (0, 2, 3),
    (0, 1, 2, 3),
]


def shape_id(shape: tuple[int, ...]) -> str:
    return "{" + ",".join(str(x) for x in shape) + "}"


def encode_strip(row: int, support: set[int]) -> set[tuple[int, int]]:
    delta: set[tuple[int, int]] = set()
    for i in support:
        delta.add((row, 2 * i + 1))
        delta.add((row + 1, 2 * i))
    return delta


def seed(a: tuple[int, ...], b: tuple[int, ...], d: int) -> set[tuple[int, int]]:
    upper = {i + d for i in a}
    lower = set(b)
    return encode_strip(0, upper) | encode_strip(2, lower)


def normalize_x(xs: list[int]) -> list[int]:
    if not xs:
        return []
    x0 = min(xs)
    return [x - x0 for x in xs]


def decode_separated(delta: set[tuple[int, int]], t: int):
    """Return exact separated-strip logical supports, [] for background, or None."""
    if t & 1:
        return None
    if not delta:
        return []
    rows: dict[int, set[int]] = {}
    for y, x in delta:
        rows.setdefault(y, set()).add(x)
    nonempty = sorted(rows)
    result: list[dict] = []
    k = 0
    while k < len(nonempty):
        j = nonempty[k]
        if k + 1 >= len(nonempty) or nonempty[k + 1] != j + 1:
            return None
        top, bottom = rows[j], rows[j + 1]
        if any((x & 1) != 1 for x in top) or any((x & 1) != 0 for x in bottom):
            return None
        logical_top = {(x - 1) // 2 for x in top}
        logical_bottom = {x // 2 for x in bottom}
        if not logical_top or logical_top != logical_bottom:
            return None
        result.append({"row": j, "logical_support": sorted(logical_top)})
        k += 2
        if k < len(nonempty) and nonempty[k] < j + 3:
            return None
    return result


def extreme_support(delta: set[tuple[int, int]], top: bool) -> tuple[int, list[int]]:
    ys = [y for y, _ in delta]
    row = min(ys) if top else max(ys)
    xs = sorted(x for y, x in delta if y == row)
    return row, xs


def persistent_top(delta: set[tuple[int, int]], t: int) -> dict | None:
    if not delta:
        return None
    row, xs = extreme_support(delta, True)
    if xs and all(background(t, x + 1) == 1 for x in xs):
        return {"tick": t, "row": row, "support": xs, "normalized_support": normalize_x(xs)}
    return None


def persistent_bottom(delta: set[tuple[int, int]], t: int) -> dict | None:
    if not delta:
        return None
    row, xs = extreme_support(delta, False)
    if xs and all(background(t, x - 1) == 0 for x in xs):
        return {"tick": t, "row": row, "support": xs, "normalized_support": normalize_x(xs)}
    return None


def bounds(delta: set[tuple[int, int]]):
    if not delta:
        return None
    ys = [y for y, _ in delta]
    xs = [x for _, x in delta]
    return [min(ys), max(ys), min(xs), max(xs)]


def metric(delta: set[tuple[int, int]], t: int) -> dict:
    box = bounds(delta)
    exterior = bool(box and (box[0] < 0 or box[1] > 3))
    return {
        "tick": t,
        "mass": len(delta),
        "bounds": box,
        "exterior": exterior,
        "v0": v0_member(delta, t),
        "coord_sha256": canonical_digest(delta),
    }


def run_one(a: tuple[int, ...], b: tuple[int, ...], d: int) -> dict:
    dense = seed(a, b, d)
    sparse = set(dense)
    ticks: list[dict] = []
    first_departure = first_exterior = None
    top_cert = bottom_cert = None
    extinction = None
    reconstitution = None
    stop_reason = "horizon"
    status = "unresolved-through-128"

    for t in range(HORIZON + 1):
        if dense != sparse:
            raise AssertionError(f"dense/sparse mismatch A={a} B={b} d={d} t={t}")

        prior_interaction = (
            (first_departure is not None and first_departure < t)
            or (first_exterior is not None and first_exterior < t)
        )
        m = metric(dense, t)
        ticks.append(m)

        # Exact extinction has highest precedence.
        if not dense:
            extinction = t
            status = "annihilated"
            stop_reason = "extinction-certificate"
            break

        if m["exterior"] and first_exterior is None:
            first_exterior = t
        if t > 0 and t % 2 == 0 and first_departure is None and m["v0"] is False:
            first_departure = t

        # Reconstitution is only admitted strictly after a previously observed
        # departure/exterior event, per the frozen protocol.
        if t > 0 and t % 2 == 0 and prior_interaction:
            strips = decode_separated(dense, t)
            if strips is not None:
                reconstitution = {"tick": t, "count": len(strips), "strips": strips}
                status = f"reconstituted-{len(strips)}"
                stop_reason = "separated-strip-certificate"
                break

        if top_cert is None:
            top_cert = persistent_top(dense, t)
        if bottom_cert is None:
            bottom_cert = persistent_bottom(dense, t)

        if top_cert is not None and bottom_cert is not None:
            status = "escape-both"
            stop_reason = "two-sided-persistent-support-certificate"
            break

        if t < HORIZON:
            dense = dense_step(dense, t)
            sparse = sparse_step(sparse, t)

    return {
        "a": list(a),
        "b": list(b),
        "a_id": shape_id(a),
        "b_id": shape_id(b),
        "d": d,
        "initial_mass": 2 * (len(a) + len(b)),
        "status": status,
        "stop_reason": stop_reason,
        "last_simulated_tick": ticks[-1]["tick"],
        "first": {
            "departure": first_departure,
            "exterior": first_exterior,
            "top_persistent": top_cert,
            "bottom_persistent": bottom_cert,
            "extinction": extinction,
            "reconstitution": reconstitution,
        },
        "ticks": ticks,
    }


def predicted_departure(d: int) -> int:
    if d > 0:
        return d if d % 2 == 0 else d + 1
    n = -d
    return n + 2 if n % 2 == 0 else n + 1


def predicted_exterior(d: int) -> int:
    if d > 0:
        return d + {0: 6, 1: 3, 2: 4, 3: 3}[d % 4]
    n = -d
    return n + 6 + (n % 2)


def predicted_supports(d: int) -> tuple[list[int], list[int]]:
    if d % 2 == 0:
        return [d + 4], [d - 3]
    if d > 0:
        return [d + 3], [d - 2]
    if d % 4 == 3:
        return [d + 1], [d]
    return [d + 3, d + 5], [d - 4, d - 2]


def check_singleton_controls(rows: list[dict]) -> dict:
    controls = [r for r in rows if r["a"] == [0] and r["b"] == [0]]
    failures = []
    for row in controls:
        d = row["d"]
        first = row["first"]
        top, bottom = predicted_supports(d)
        checks = {
            "status": row["status"] == "escape-both",
            "departure": first["departure"] == predicted_departure(d),
            "exterior": first["exterior"] == predicted_exterior(d),
            "top_support": first["top_persistent"] is not None and first["top_persistent"]["support"] == top,
            "bottom_support": first["bottom_persistent"] is not None and first["bottom_persistent"]["support"] == bottom,
            "no_extinction": first["extinction"] is None,
            "no_reconstitution": first["reconstitution"] is None,
        }
        if not all(checks.values()):
            failures.append({"d": d, "checks": checks, "first": first, "status": row["status"]})
    return {"cases": len(controls), "ok": not failures and len(controls) == 25, "failures": failures}


def minimal_witness(rows: list[dict], statuses: set[str]):
    matches = [r for r in rows if r["status"] in statuses]
    if not matches:
        return None
    return min(
        matches,
        key=lambda r: (
            len(r["a"]) + len(r["b"]),
            (max(r["a"]) - min(r["a"]) + 1) + (max(r["b"]) - min(r["b"]) + 1),
            r["a"], r["b"], abs(r["d"]), r["d"],
        ),
    )


def main():
    started = time.time()
    rows = [
        run_one(a, b, d)
        for a in SHAPES
        for b in SHAPES
        for d in range(D_MIN, D_MAX + 1)
    ]
    controls = check_singleton_controls(rows)
    if not controls["ok"]:
        raise AssertionError(f"Research020 singleton controls failed: {controls['failures'][:3]}")

    counts = Counter(row["status"] for row in rows)
    result = {
        "protocol": PROTOCOL,
        "domain": {
            "shapes": [list(s) for s in SHAPES],
            "ordered_shape_pairs": len(SHAPES) ** 2,
            "d_min": D_MIN,
            "d_max": D_MAX,
            "horizon": HORIZON,
            "cases": len(rows),
        },
        "summary": dict(sorted(counts.items())),
        "singleton_controls": controls,
        "minimal_witnesses": {
            "annihilated": minimal_witness(rows, {"annihilated"}),
            "fold_in": minimal_witness(rows, {"reconstituted-1"}),
            "transmission": minimal_witness(rows, {"reconstituted-2"}),
            "fan_out": minimal_witness(rows, {f"reconstituted-{k}" for k in range(3, 10)}),
            "escape_both": minimal_witness(rows, {"escape-both"}),
        },
        "trajectories": rows,
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
        "summary": result["summary"],
        "controls_ok": controls["ok"],
        "cases": len(rows),
        "seconds": result["seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
