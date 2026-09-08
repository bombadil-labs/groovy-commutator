"""Independent sparse infinite-lattice audit for Research020 pulse scattering.

The fixed shards are an execution-only response to a first full audit timing out
before producing a result. They do not change the frozen domain or checks.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "results/pulse_scattering_20260908.json"
OUT = ROOT / "results/pulse_scattering_20260908_audit.json"
PROTOCOL = "docs/research/protocols/pulse-scattering-20260908.md"
SHARDS = [(-64, -49), (-48, -33), (-32, -17), (-16, -1), (0, 31), (32, 64)]


def b(t: int, x: int) -> int:
    return (x % 2) ^ (t % 2)


def initial(d: int) -> set[tuple[int, int]]:
    return {(0, 2*d + 1), (1, 2*d), (2, 1), (3, 0)}


def value(delta: set[tuple[int, int]], t: int, y: int, x: int) -> int:
    return b(t, x) ^ int((y, x) in delta)


def sparse_step(delta: set[tuple[int, int]], t: int) -> set[tuple[int, int]]:
    if not delta:
        return set()
    candidates = set()
    for y, x in delta:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                candidates.add((y + dy, x + dx))
    nxt = set()
    for y, x in candidates:
        c = value(delta, t, y, x)
        left = value(delta, t, y, x - 1)
        right = value(delta, t, y, x + 1)
        sy = y + 1 if c else y - 1
        sx = x + left + right - 1
        actual = value(delta, t, sy, sx)
        if actual != b(t + 1, x):
            nxt.add((y, x))
    return nxt


def digest(delta: set[tuple[int, int]]) -> str:
    h = hashlib.sha256()
    for y, x in sorted(delta):
        h.update(f"{y},{x};".encode())
    return h.hexdigest()


def top_bottom_tips(delta: set[tuple[int, int]], t: int) -> tuple[bool, bool]:
    if not delta:
        return False, False
    ymin = min(y for y, _ in delta)
    ymax = max(y for y, _ in delta)
    top = [(y, x) for y, x in delta if y == ymin]
    bottom = [(y, x) for y, x in delta if y == ymax]
    top_tip = len(top) == 1 and b(t, top[0][1] + 1) == 1
    bottom_tip = len(bottom) == 1 and b(t, bottom[0][1] - 1) == 0
    return top_tip, bottom_tip


def audit_range(primary: dict, d_min: int, d_max: int) -> dict:
    started = time.time()
    checked_ticks = checked_points = 0
    mismatches = []
    classifications = []
    selected = [row for row in primary["trajectories"] if d_min <= row["d"] <= d_max]
    for row in selected:
        d = row["d"]
        delta = initial(d)
        audit_last = row["last_simulated_tick"]
        top_first = bottom_first = extinction_first = None
        primary_ticks = {m["tick"]: m for m in row["ticks"]}
        for t in range(audit_last + 1):
            m = primary_ticks[t]
            dg = digest(delta)
            checked_ticks += 1
            checked_points += len(delta)
            if dg != m["coord_sha256"] or len(delta) != m["mass"]:
                mismatches.append({"d": d, "tick": t, "kind": "field",
                                   "primary_mass": m["mass"], "audit_mass": len(delta),
                                   "primary_digest": m["coord_sha256"], "audit_digest": dg})
                break
            tt, bt = top_bottom_tips(delta, t)
            if tt and top_first is None:
                top_first = t
            if bt and bottom_first is None:
                bottom_first = t
            if not delta and extinction_first is None:
                extinction_first = t
            if t < audit_last:
                delta = sparse_step(delta, t)
        classifications.append({
            "d": d, "audited_through": audit_last,
            "top_tip_first_within_audit": top_first,
            "bottom_tip_first_within_audit": bottom_first,
            "extinction_first_within_audit": extinction_first,
            "primary_status": row["status"],
        })

    for a in classifications:
        p = next(row for row in selected if row["d"] == a["d"])
        last = a["audited_through"]
        for key, audit_key in (("top_tip", "top_tip_first_within_audit"),
                               ("bottom_tip", "bottom_tip_first_within_audit"),
                               ("extinction", "extinction_first_within_audit")):
            pt = p["first"][key]
            if pt is not None and pt <= last and pt != a[audit_key]:
                mismatches.append({"d": p["d"], "kind": key,
                                   "primary": pt, "audit": a[audit_key]})
    return {
        "d_min": d_min, "d_max": d_max, "ok": not mismatches,
        "checked_ticks": checked_ticks,
        "checked_changed_points": checked_points,
        "mismatches": mismatches,
        "classifications": classifications,
        "seconds": round(time.time() - started, 3),
    }


def aggregate(primary: dict) -> dict:
    parts = []
    for i in range(len(SHARDS)):
        p = ROOT / f"results/pulse_scattering_20260908_audit_shard_{i}.json"
        parts.append(json.loads(p.read_text()))
    ds = [c["d"] for part in parts for c in part["classifications"]]
    expected = list(range(primary["domain"]["d_min"], primary["domain"]["d_max"] + 1))
    if sorted(ds) != expected or len(ds) != len(set(ds)):
        raise AssertionError("Audit shards do not form the exact frozen displacement domain")
    mismatches = [m for part in parts for m in part["mismatches"]]
    result = {
        "ok": all(part["ok"] for part in parts) and not mismatches,
        "shards": SHARDS,
        "checked_ticks": sum(part["checked_ticks"] for part in parts),
        "checked_changed_points": sum(part["checked_changed_points"] for part in parts),
        "mismatches": mismatches,
        "classifications": sorted(
            [c for part in parts for c in part["classifications"]], key=lambda x: x["d"]),
        "shard_seconds": [part["seconds"] for part in parts],
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
            "primary": hashlib.sha256(PRIMARY.read_bytes()).hexdigest(),
        },
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("ok", "checked_ticks", "checked_changed_points", "shard_seconds")}, indent=2))
    if not result["ok"]:
        raise SystemExit(1)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", type=int, choices=range(len(SHARDS)))
    parser.add_argument("--aggregate", action="store_true")
    args = parser.parse_args()
    primary = json.loads(PRIMARY.read_text())
    if args.aggregate:
        aggregate(primary)
        return
    if args.shard is None:
        # Full one-process mode remains available outside constrained runners.
        part = audit_range(primary, primary["domain"]["d_min"], primary["domain"]["d_max"])
        path = OUT
    else:
        d_min, d_max = SHARDS[args.shard]
        part = audit_range(primary, d_min, d_max)
        path = ROOT / f"results/pulse_scattering_20260908_audit_shard_{args.shard}.json"
    part["source_sha256"] = {
        "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
        "primary": hashlib.sha256(PRIMARY.read_bytes()).hexdigest(),
    }
    path.write_text(json.dumps(part, indent=2) + "\n")
    print(json.dumps({k: part[k] for k in ("d_min", "d_max", "ok", "checked_ticks", "checked_changed_points", "seconds")}, indent=2))
    if not part["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
