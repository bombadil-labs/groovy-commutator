"""Independent sparse infinite-lattice audit for Research020 pulse scattering."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "results/pulse_scattering_20260908.json"
OUT = ROOT / "results/pulse_scattering_20260908_audit.json"
PROTOCOL = "docs/research/protocols/pulse-scattering-20260908.md"


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


def main():
    started = time.time()
    primary = json.loads(PRIMARY.read_text())
    checked_ticks = checked_points = 0
    mismatches = []
    classifications = []
    for row in primary["trajectories"]:
        d = row["d"]
        delta = initial(d)
        target_last = row["last_simulated_tick"]
        # Audit every directly simulated tick. This is stronger than the frozen
        # minimum and makes certificate-time agreement explicit.
        audit_last = target_last
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

    # Certificate first-times must agree whenever the primary event lies within
    # the independently audited interval. Unresolved trajectories are audited
    # through the full horizon by construction.
    for a, p in zip(classifications, primary["trajectories"]):
        last = a["audited_through"]
        for key, audit_key in (("top_tip", "top_tip_first_within_audit"),
                               ("bottom_tip", "bottom_tip_first_within_audit"),
                               ("extinction", "extinction_first_within_audit")):
            pt = p["first"][key]
            if pt is not None and pt <= last and pt != a[audit_key]:
                mismatches.append({"d": p["d"], "kind": key,
                                   "primary": pt, "audit": a[audit_key]})

    result = {
        "ok": not mismatches,
        "checked_ticks": checked_ticks,
        "checked_changed_points": checked_points,
        "mismatches": mismatches,
        "classifications": classifications,
        "seconds": round(time.time() - started, 3),
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
            "primary": hashlib.sha256(PRIMARY.read_bytes()).hexdigest(),
        },
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ("ok", "checked_ticks", "checked_changed_points", "seconds")}, indent=2))
    if mismatches:
        print(json.dumps(mismatches[:10], indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
