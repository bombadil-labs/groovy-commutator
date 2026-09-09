"""Fresh tick-256 check of the post-discovery dyadic shielding template."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import time

from experiment_pulse_scattering import background, canonical_digest, dense_step
from audit_pulse_scattering import sparse_step

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/selector_shielding_dyadic_20260908.json"
PROTOCOL = "docs/research/protocols/selector-shielding-dyadic-20260908.md"
T = 256
A = {-5, 0}
B = {0, 1, 3, 4, 6}


def encode_strip(row: int, support: set[int]) -> set[tuple[int, int]]:
    out = set()
    for i in support:
        out.add((row, 2*i + 1))
        out.add((row + 1, 2*i))
    return out


def value(delta: set[tuple[int, int]], t: int, y: int, x: int) -> int:
    return background(t, x) ^ int((y, x) in delta)


def expected_normalized(t: int) -> dict[int, set[int]]:
    row2 = set(range(2, 2*t + 1, 2))
    row2.remove(8)
    row2.add(13)

    row1 = {-10, 0, 1, 4, 6, 11}
    row1 |= {u for u in range(12, 2*t - 3) if u % 8 in {0, 4, 6}}

    row0 = {-9, 1, 6, 9, 12, 14, 16, 18}
    row0 |= {u for u in range(24, 2*t - 5) if u % 8 in {0, 2}}
    row0 |= {2*t - 4, 2*t - 2, 2*t + 1}
    return {0: row0, 1: row1, 2: row2}


def main() -> None:
    started = time.time()
    coupled_d = encode_strip(0, A) | encode_strip(2, B)
    coupled_s = set(coupled_d)
    lower_d = encode_strip(2, B)
    lower_s = set(lower_d)

    complete_field_ticks = 0
    changed_points_compared = 0
    first_negative_row2 = None
    first_lower_failure = None

    for t in range(T + 1):
        if coupled_d != coupled_s:
            raise AssertionError(f"coupled dense/sparse mismatch at {t}")
        if lower_d != lower_s:
            raise AssertionError(f"lower dense/sparse mismatch at {t}")
        complete_field_ticks += 2
        changed_points_compared += len(coupled_d) + len(lower_d)

        diff = coupled_d ^ lower_d
        if first_lower_failure is None and any(y >= 3 for y, _ in diff):
            first_lower_failure = t
        if first_negative_row2 is None:
            for y, x in diff:
                if y == 2 and value(lower_d, t, 2, x) == 1 and value(coupled_d, t, 2, x) == 0:
                    first_negative_row2 = {"tick": t, "x": x}
                    break

        if t < T:
            coupled_d = dense_step(coupled_d, t)
            coupled_s = sparse_step(coupled_s, t)
            lower_d = dense_step(lower_d, t)
            lower_s = sparse_step(lower_s, t)

    diff = coupled_d ^ lower_d
    observed = {
        y: {x + T for yy, x in diff if yy == y}
        for y in (0, 1, 2)
    }
    expected = expected_normalized(T)
    row_checks = {}
    for y in (0, 1, 2):
        row_checks[str(y)] = {
            "ok": observed[y] == expected[y],
            "observed_mass": len(observed[y]),
            "expected_mass": len(expected[y]),
            "extra": sorted(observed[y] - expected[y]),
            "missing": sorted(expected[y] - observed[y]),
        }

    result = {
        "ok": all(v["ok"] for v in row_checks.values()) and first_negative_row2 is None and first_lower_failure is None,
        "tick": T,
        "row_checks": row_checks,
        "first_negative_row2": first_negative_row2,
        "first_lower_failure": first_lower_failure,
        "complete_field_ticks": complete_field_ticks,
        "changed_points_compared": changed_points_compared,
        "coupled_mass_at_256": len(coupled_d),
        "reference_mass_at_256": len(lower_d),
        "coupled_sha256": canonical_digest(coupled_d),
        "reference_sha256": canonical_digest(lower_d),
        "seconds": round(time.time() - started, 3),
        "source_sha256": {
            "script": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "protocol": hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
            "dense_kernel": hashlib.sha256((ROOT / "scripts/experiment_pulse_scattering.py").read_bytes()).hexdigest(),
            "sparse_kernel": hashlib.sha256((ROOT / "scripts/audit_pulse_scattering.py").read_bytes()).hexdigest(),
        },
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
