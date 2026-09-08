"""Fresh, preregistered validation of the Research020 arithmetic scattering law."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import time

from experiment_pulse_scattering import (
    background, canonical_digest, dense_step, seed, v0_member,
)
from audit_pulse_scattering import sparse_step

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/pulse_scattering_20260908_fresh_range.json"
PROTOCOL = "docs/research/protocols/pulse-scattering-residue-20260908.md"
DOMAIN = list(range(-256, -64)) + list(range(65, 257))
MAX_TICK = 320


def predicted_departure(d: int) -> int:
    if d > 0:
        return d if d % 2 == 0 else d + 1
    n = -d
    return n + 2 if n % 2 == 0 else n + 1


def predicted_exterior(d: int) -> int:
    if d > 0:
        r = d % 4
        return d + {0: 6, 1: 3, 2: 4, 3: 3}[r]
    n = -d
    return n + 6 + (n % 2)


def predicted_mass(d: int) -> int:
    return 2 if d < 0 and d % 4 == 1 else 1


def extreme_data(delta: set[tuple[int, int]], t: int) -> dict:
    ymin = min(y for y, _ in delta)
    ymax = max(y for y, _ in delta)
    top = sorted((y, x) for y, x in delta if y == ymin)
    bottom = sorted((y, x) for y, x in delta if y == ymax)
    top_cert = bool(top) and all(background(t, x + 1) == 1 for _, x in top)
    bottom_cert = bool(bottom) and all(background(t, x - 1) == 0 for _, x in bottom)
    return {
        "top": top, "bottom": bottom,
        "top_mass": len(top), "bottom_mass": len(bottom),
        "top_persistent_parity": top_cert,
        "bottom_persistent_parity": bottom_cert,
    }


def run_one(d: int) -> tuple[dict, int, int]:
    dense = seed(d)
    sparse = seed(d)
    departure = None
    digest_checks = point_checks = 0
    for t in range(MAX_TICK + 1):
        if dense != sparse:
            raise AssertionError(f"dense/sparse field mismatch at d={d}, t={t}")
        digest_checks += 1
        point_checks += len(dense)
        if t > 0 and t % 2 == 0 and departure is None and v0_member(dense, t) is False:
            departure = t
        exterior = any(y < 0 or y > 3 for y, _ in dense)
        if exterior:
            ext = extreme_data(dense, t)
            pd, pe, pm = predicted_departure(d), predicted_exterior(d), predicted_mass(d)
            observed = {
                "d": d,
                "predicted_departure": pd,
                "observed_departure": departure,
                "predicted_exterior": pe,
                "observed_exterior": t,
                "predicted_extreme_mass": pm,
                **ext,
                "field_mass": len(dense),
                "field_sha256": canonical_digest(dense),
            }
            observed["passes"] = (
                departure == pd and t == pe and
                ext["top_mass"] == pm and ext["bottom_mass"] == pm and
                ext["top_persistent_parity"] and ext["bottom_persistent_parity"]
            )
            return observed, digest_checks, point_checks
        if t == MAX_TICK:
            raise AssertionError(f"no exterior change by frozen guard tick {MAX_TICK} for d={d}")
        dense = dense_step(dense, t)
        sparse = sparse_step(sparse, t)
    raise AssertionError("unreachable")


def main():
    started = time.time()
    rows = []
    digest_checks = point_checks = 0
    for d in DOMAIN:
        row, dc, pc = run_one(d)
        rows.append(row)
        digest_checks += dc
        point_checks += pc
    failures = [row for row in rows if not row["passes"]]
    counts = {}
    for row in rows:
        key = str(row["predicted_extreme_mass"])
        counts[key] = counts.get(key, 0) + 1
    result = {
        "ok": not failures,
        "domain": {"negative": [-256, -65], "positive": [65, 256], "cases": len(DOMAIN)},
        "extreme_mass_counts": counts,
        "complete_field_agreement_ticks": digest_checks,
        "changed_points_compared": point_checks,
        "failures": failures,
        "rows": rows,
        "seconds": round(time.time() - started, 3),
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
            "primary_instrument": hashlib.sha256((ROOT / "scripts/experiment_pulse_scattering.py").read_bytes()).hexdigest(),
            "audit_instrument": hashlib.sha256((ROOT / "scripts/audit_pulse_scattering.py").read_bytes()).hexdigest(),
        },
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "ok": result["ok"], "cases": len(DOMAIN),
        "extreme_mass_counts": counts,
        "complete_field_agreement_ticks": digest_checks,
        "changed_points_compared": point_checks,
        "seconds": result["seconds"],
    }, indent=2))
    if failures:
        print(json.dumps(failures[:10], indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
