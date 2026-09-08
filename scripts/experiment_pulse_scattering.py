"""Frozen Research020 pulse-scattering census. See protocol before changing."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import hashlib
import json
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/pulse_scattering_20260908.json"
PROTOCOL = "docs/research/protocols/pulse-scattering-20260908.md"
D_MIN, D_MAX, HORIZON = -64, 64, 192


def background(t: int, x: int) -> int:
    return (x & 1) ^ (t & 1)


def seed(d: int) -> set[tuple[int, int]]:
    return {(0, 2 * d + 1), (1, 2 * d), (2, 1), (3, 0)}


def dense_step(delta: set[tuple[int, int]], t: int) -> set[tuple[int, int]]:
    """Exact one-tick update on a cropped rectangle padded by analytic background."""
    if not delta:
        return set()
    ys0 = [p[0] for p in delta]
    xs0 = [p[1] for p in delta]
    y0, y1 = min(ys0) - 2, max(ys0) + 2
    x0, x1 = min(xs0) - 2, max(xs0) + 2
    ys = np.arange(y0, y1 + 1, dtype=np.int64)
    xs = np.arange(x0, x1 + 1, dtype=np.int64)
    grid = np.broadcast_to(((xs & 1) ^ (t & 1)).astype(np.uint8),
                           (len(ys), len(xs))).copy()
    points = np.asarray([(y - y0, x - x0) for y, x in delta], dtype=np.int64)
    grid[points[:, 0], points[:, 1]] ^= 1

    c = grid[1:-1, 1:-1]
    h = grid[1:-1, :-2] + grid[1:-1, 2:]
    up = np.where(h == 0, grid[:-2, :-2],
                  np.where(h == 1, grid[:-2, 1:-1], grid[:-2, 2:]))
    down = np.where(h == 0, grid[2:, :-2],
                    np.where(h == 1, grid[2:, 1:-1], grid[2:, 2:]))
    out = np.where(c == 0, up, down).astype(np.uint8)

    out_xs = xs[1:-1]
    diff = out ^ (((out_xs & 1) ^ ((t + 1) & 1)).astype(np.uint8))[None, :]
    points = np.argwhere(diff)
    oy0, ox0 = y0 + 1, x0 + 1
    return {(int(y + oy0), int(x + ox0)) for y, x in points}


def canonical_digest(delta: set[tuple[int, int]]) -> str:
    h = hashlib.sha256()
    for y, x in sorted(delta):
        h.update(f"{y},{x};".encode())
    return h.hexdigest()


def paired_strip(rows: dict[int, set[int]], j: int) -> tuple[bool, int]:
    top, bottom = rows.get(j, set()), rows.get(j + 1, set())
    if not top or not bottom:
        return False, 0
    if any((x & 1) != 1 for x in top) or any((x & 1) != 0 for x in bottom):
        return False, 0
    a = {(x - 1) // 2 for x in top}
    b = {x // 2 for x in bottom}
    return (a == b), len(a)


def separated_strips(delta: set[tuple[int, int]], t: int):
    if t & 1:
        return None
    if not delta:
        return []
    rows: dict[int, set[int]] = {}
    for y, x in delta:
        rows.setdefault(y, set()).add(x)
    nonempty = sorted(rows)
    result = []
    k = 0
    while k < len(nonempty):
        j = nonempty[k]
        if k + 1 >= len(nonempty) or nonempty[k + 1] != j + 1:
            return None
        ok, mass = paired_strip(rows, j)
        if not ok:
            return None
        result.append({"row": j, "logical_mass": mass})
        k += 2
        if k < len(nonempty) and nonempty[k] < j + 3:
            return None
    return result


def v0_member(delta: set[tuple[int, int]], t: int) -> bool | None:
    if t & 1:
        return None
    if any(y < 0 or y > 3 for y, _ in delta):
        return False
    rows: dict[int, set[int]] = {}
    for y, x in delta:
        rows.setdefault(y, set()).add(x)
    for j in (0, 2):
        top, bottom = rows.get(j, set()), rows.get(j + 1, set())
        if bool(top) != bool(bottom):
            return False
        if top:
            ok, _ = paired_strip(rows, j)
            if not ok:
                return False
    return True


def metric(delta: set[tuple[int, int]], t: int) -> dict:
    if not delta:
        return {
            "tick": t, "mass": 0, "bounds": None, "vertical_span": 0,
            "horizontal_span": 0, "exterior": False, "v0": v0_member(delta, t),
            "separated_strips": separated_strips(delta, t),
            "top_tip": False, "bottom_tip": False,
            "coord_sha256": canonical_digest(delta),
        }
    ys = [y for y, _ in delta]
    xs = [x for _, x in delta]
    ymin, ymax, xmin, xmax = min(ys), max(ys), min(xs), max(xs)
    top = sorted((y, x) for y, x in delta if y == ymin)
    bottom = sorted((y, x) for y, x in delta if y == ymax)
    top_tip = len(top) == 1 and background(t, top[0][1] + 1) == 1
    bottom_tip = len(bottom) == 1 and background(t, bottom[0][1] - 1) == 0
    return {
        "tick": t, "mass": len(delta),
        "bounds": [ymin, ymax, xmin, xmax],
        "vertical_span": ymax - ymin + 1,
        "horizontal_span": xmax - xmin + 1,
        "exterior": ymin < 0 or ymax > 3,
        "v0": v0_member(delta, t),
        "separated_strips": separated_strips(delta, t),
        "top_tip": top_tip, "bottom_tip": bottom_tip,
        "top": top, "bottom": bottom,
        "coord_sha256": canonical_digest(delta),
    }


def run_one(d: int) -> dict:
    delta = seed(d)
    ticks = []
    first = {
        "extinction": None, "departure": None, "exterior": None,
        "top_tip": None, "bottom_tip": None, "two_sided_tip": None,
        "reconstitution": None,
    }
    top_seen = bottom_seen = False
    departed = False
    stop_reason = "horizon"
    for t in range(HORIZON + 1):
        was_departed = departed
        m = metric(delta, t)
        ticks.append(m)
        if m["mass"] == 0:
            first["extinction"] = t
            stop_reason = "extinction-certificate"
            break
        if m["exterior"] and first["exterior"] is None:
            first["exterior"] = t
        if t > 0 and (m["exterior"] or (m["v0"] is False)):
            if first["departure"] is None:
                first["departure"] = t
            departed = True
        if m["top_tip"] and first["top_tip"] is None:
            first["top_tip"] = t
            top_seen = True
        if m["bottom_tip"] and first["bottom_tip"] is None:
            first["bottom_tip"] = t
            bottom_seen = True
        if top_seen and bottom_seen and first["two_sided_tip"] is None:
            first["two_sided_tip"] = t
        strips = m["separated_strips"]
        if t % 2 == 0 and t > 0 and was_departed and strips is not None:
            first["reconstitution"] = {
                "tick": t, "count": len(strips), "strips": strips,
            }
            # Do not terminate: the frozen protocol only permits early stop on
            # extinction or persistent-tip certificates.
        if top_seen and bottom_seen:
            stop_reason = "two-sided-tip-certificate"
            break
        if t < HORIZON:
            delta = dense_step(delta, t)

    if first["extinction"] is not None:
        status = "annihilated"
    elif first["reconstitution"] is not None:
        status = f"reconstituted-{first['reconstitution']['count']}"
    elif top_seen and bottom_seen:
        status = "escape-both"
    elif top_seen:
        status = "escape-top"
    elif bottom_seen:
        status = "escape-bottom"
    else:
        status = "unresolved-through-192"
    return {
        "d": d, "seed": sorted(seed(d)), "status": status,
        "stop_reason": stop_reason, "last_simulated_tick": ticks[-1]["tick"],
        "first": first, "ticks": ticks,
    }


def main():
    started = time.time()
    trajectories = [run_one(d) for d in range(D_MIN, D_MAX + 1)]
    summary = Counter(row["status"] for row in trajectories)
    result = {
        "protocol": PROTOCOL,
        "domain": {"d_min": D_MIN, "d_max": D_MAX, "horizon": HORIZON},
        "summary": dict(sorted(summary.items())),
        "trajectories": trajectories,
        "seconds": round(time.time() - started, 3),
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
        },
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))
    for row in trajectories:
        f = row["first"]
        print(row["d"], row["status"], row["last_simulated_tick"],
              "depart", f["departure"], "ext", f["exterior"],
              "tips", f["top_tip"], f["bottom_tip"],
              "recon", f["reconstitution"])


if __name__ == "__main__":
    main()
