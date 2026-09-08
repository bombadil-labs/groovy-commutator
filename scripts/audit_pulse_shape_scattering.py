"""Independent Research021 classification audit over the frozen 1,600 cases."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import time

from audit_pulse_scattering import sparse_step

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "results/pulse_shape_scattering_20260908.json"
OUT = ROOT / "results/pulse_shape_scattering_20260908_audit.json"
PROTOCOL = "docs/research/protocols/pulse-shape-scattering-20260908.md"
HORIZON = 128


def bg(t: int, x: int) -> int:
    return (x % 2) ^ (t % 2)


def encode(row: int, support: set[int]) -> set[tuple[int, int]]:
    out = set()
    for i in support:
        out.add((row, 2 * i + 1))
        out.add((row + 1, 2 * i))
    return out


def initial(a: list[int], b: list[int], d: int) -> set[tuple[int, int]]:
    return encode(0, {i + d for i in a}) | encode(2, set(b))


def digest(delta: set[tuple[int, int]]) -> str:
    h = hashlib.sha256()
    for y, x in sorted(delta):
        h.update(f"{y},{x};".encode())
    return h.hexdigest()


def pair_support(delta: set[tuple[int, int]], row: int):
    top = {x for y, x in delta if y == row}
    bottom = {x for y, x in delta if y == row + 1}
    if bool(top) != bool(bottom):
        return None
    if not top:
        return set()
    if any(x % 2 != 1 for x in top) or any(x % 2 != 0 for x in bottom):
        return None
    a = {(x - 1) // 2 for x in top}
    b = {x // 2 for x in bottom}
    return a if a == b else None


def in_v0(delta: set[tuple[int, int]], t: int):
    if t % 2:
        return None
    if any(y < 0 or y > 3 for y, _ in delta):
        return False
    return pair_support(delta, 0) is not None and pair_support(delta, 2) is not None


def separated_union(delta: set[tuple[int, int]], t: int):
    if t % 2:
        return None
    if not delta:
        return []
    row_ids = sorted({y for y, _ in delta})
    out = []
    k = 0
    while k < len(row_ids):
        row = row_ids[k]
        if k + 1 >= len(row_ids) or row_ids[k + 1] != row + 1:
            return None
        support = pair_support(delta, row)
        if support is None or not support:
            return None
        out.append((row, tuple(sorted(support))))
        k += 2
        if k < len(row_ids) and row_ids[k] < row + 3:
            return None
    return out


def top_cert(delta: set[tuple[int, int]], t: int):
    if not delta:
        return None
    y = min(y for y, _ in delta)
    xs = sorted(x for yy, x in delta if yy == y)
    if xs and all(bg(t, x + 1) == 1 for x in xs):
        return (t, y, tuple(xs))
    return None


def bottom_cert(delta: set[tuple[int, int]], t: int):
    if not delta:
        return None
    y = max(y for y, _ in delta)
    xs = sorted(x for yy, x in delta if yy == y)
    if xs and all(bg(t, x - 1) == 0 for x in xs):
        return (t, y, tuple(xs))
    return None


def classify(row: dict) -> tuple[dict, int, int, list[dict]]:
    delta = initial(row["a"], row["b"], row["d"])
    departure = exterior = extinction = reconstitution = None
    top = bottom = None
    mismatches = []
    checked_ticks = checked_points = 0

    for t in range(row["last_simulated_tick"] + 1):
        primary_tick = row["ticks"][t]
        checked_ticks += 1
        checked_points += len(delta)
        dg = digest(delta)
        if len(delta) != primary_tick["mass"] or dg != primary_tick["coord_sha256"]:
            mismatches.append({"kind": "field", "tick": t, "mass": len(delta), "digest": dg})
            break

        prior = ((departure is not None and departure < t) or (exterior is not None and exterior < t))
        if not delta:
            extinction = t
            status = "annihilated"
            break
        if exterior is None and any(y < 0 or y > 3 for y, _ in delta):
            exterior = t
        if t > 0 and t % 2 == 0 and departure is None and in_v0(delta, t) is False:
            departure = t
        if t > 0 and t % 2 == 0 and prior:
            strips = separated_union(delta, t)
            if strips is not None:
                reconstitution = (t, strips)
                status = f"reconstituted-{len(strips)}"
                break
        if top is None:
            top = top_cert(delta, t)
        if bottom is None:
            bottom = bottom_cert(delta, t)
        if top is not None and bottom is not None:
            status = "escape-both"
            break
        if t < row["last_simulated_tick"]:
            delta = sparse_step(delta, t)
    else:
        status = "unresolved-through-128"

    observed = {
        "status": status,
        "departure": departure,
        "exterior": exterior,
        "top_persistent": top,
        "bottom_persistent": bottom,
        "extinction": extinction,
        "reconstitution": reconstitution,
    }
    return observed, checked_ticks, checked_points, mismatches


def main():
    started = time.time()
    primary = json.loads(PRIMARY.read_text())
    mismatches = []
    ticks = points = 0
    for row in primary["trajectories"]:
        observed, ct, cp, field_mismatches = classify(row)
        ticks += ct
        points += cp
        if field_mismatches:
            mismatches.append({"a": row["a"], "b": row["b"], "d": row["d"], "details": field_mismatches})
            continue
        p = row["first"]
        expected_top = None if p["top_persistent"] is None else (
            p["top_persistent"]["tick"], p["top_persistent"]["row"], tuple(p["top_persistent"]["support"])
        )
        expected_bottom = None if p["bottom_persistent"] is None else (
            p["bottom_persistent"]["tick"], p["bottom_persistent"]["row"], tuple(p["bottom_persistent"]["support"])
        )
        checks = {
            "status": observed["status"] == row["status"],
            "departure": observed["departure"] == p["departure"],
            "exterior": observed["exterior"] == p["exterior"],
            "top": observed["top_persistent"] == expected_top,
            "bottom": observed["bottom_persistent"] == expected_bottom,
            "extinction": observed["extinction"] == p["extinction"],
            "reconstitution": (observed["reconstitution"] is None) == (p["reconstitution"] is None),
        }
        if not all(checks.values()):
            mismatches.append({"a": row["a"], "b": row["b"], "d": row["d"], "checks": checks, "observed": observed})

    result = {
        "ok": not mismatches,
        "cases": len(primary["trajectories"]),
        "checked_ticks": ticks,
        "checked_changed_points": points,
        "mismatches": mismatches,
        "seconds": round(time.time() - started, 3),
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
            "primary": hashlib.sha256(PRIMARY.read_bytes()).hexdigest(),
            "sparse_kernel": hashlib.sha256((ROOT / "scripts/audit_pulse_scattering.py").read_bytes()).hexdigest(),
        },
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("ok", "cases", "checked_ticks", "checked_changed_points", "seconds")}, indent=2))
    if mismatches:
        print(json.dumps(mismatches[:5], indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
