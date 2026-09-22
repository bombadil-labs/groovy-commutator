#!/usr/bin/env python3
"""Independent certificate audit for the Rule-110 original-G result.

This verifier intentionally does not import the primary evaluator.  It uses
literal tuples for finite causal words and cyclic rings, checks only the
frozen local budgets and rings through the retained period-three witness, and
validates the result/execution manifests.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results/rule110_g_autonomy_20260922.json"
EXECUTION_PATH = ROOT / "experiments/rule110_g_autonomy_20260922/execution.json"
PROTOCOL_PATH = ROOT / "docs/research/protocols/rule110-g-autonomy-20260922.md"
PRIMARY_PATH = ROOT / "scripts/verify_rule110_g_autonomy.py"
PROTOCOL_COMMIT = "ad38b4937321501889b6b8a1caab4e4bfb54052e"
IMPLEMENTATION_COMMIT = "232662516b858eabb4743dce9f8ef2c76847bec6"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rule_output(rule: int, left: int, center: int, right: int) -> int:
    """Return one Wolfram-indexed ECA output bit."""
    return (rule >> (4 * left + 2 * center + right)) & 1


def finite_step(row: tuple[int, ...], rule: int) -> tuple[int, ...]:
    """Apply an ECA to every complete three-cell window, without wrapping."""
    return tuple(rule_output(rule, *row[i : i + 3]) for i in range(len(row) - 2))


def finite_g(row: tuple[int, ...], rule: int) -> tuple[int, ...]:
    """Compute original G on every complete radius-two causal window."""
    evolved = finite_step(row, rule)
    evolved_twice = finite_step(evolved, rule)
    derivative = tuple(row[i + 1] ^ evolved[i] for i in range(len(evolved)))
    evolved_derivative = finite_step(derivative, rule)
    return tuple(
        evolved[i + 1] ^ evolved_twice[i] ^ evolved_derivative[i]
        for i in range(len(evolved_twice))
    )


def cyclic_step(row: tuple[int, ...], rule: int) -> tuple[int, ...]:
    """Tuple-valued cyclic ECA update, including aliased n=1 and n=2 rings."""
    n = len(row)
    return tuple(
        rule_output(rule, row[(i - 1) % n], row[i], row[(i + 1) % n])
        for i in range(n)
    )


def cyclic_g(row: tuple[int, ...], rule: int) -> tuple[int, ...]:
    evolved = cyclic_step(row, rule)
    evolved_twice = cyclic_step(evolved, rule)
    derivative = tuple(source ^ target for source, target in zip(row, evolved))
    evolved_derivative = cyclic_step(derivative, rule)
    return tuple(
        a ^ b ^ c for a, b, c in zip(evolved, evolved_twice, evolved_derivative)
    )


def parse_word(value: str) -> tuple[int, ...]:
    return tuple(int(bit) for bit in value)


def format_word(row: tuple[int, ...]) -> str:
    return "".join(str(bit) for bit in row)


def int_word(value: int, width: int) -> tuple[int, ...]:
    return parse_word(f"{value:0{width}b}")


def tuple_trace(row: tuple[int, ...], rule: int) -> dict[str, str]:
    evolved = cyclic_step(row, rule)
    derivative = tuple(a ^ b for a, b in zip(row, evolved))
    return {
        "S": format_word(row),
        "E": format_word(evolved),
        "D": format_word(derivative),
        "G": format_word(cyclic_g(row, rule)),
        "next_G": format_word(cyclic_g(evolved, rule)),
    }


def reconstruct_local(radius: int) -> dict[str, object]:
    source_radius = max(radius + 2, 3)
    width = 2 * source_radius + 1
    first: dict[str, tuple[str, int]] = {}
    targets: dict[str, set[int]] = {}
    conflict = None

    for value in range(1 << width):
        source = int_word(value, width)
        g_word = finite_g(source, 110)
        start = source_radius - 2 - radius
        patch = format_word(g_word[start : start + 2 * radius + 1])
        target = finite_g(finite_step(source, 110), 110)[source_radius - 3]
        targets.setdefault(patch, set()).add(target)
        if patch not in first:
            first[patch] = (format_word(source), target)
        elif first[patch][1] != target and conflict is None:
            conflict = {
                "source_words": [first[patch][0], format_word(source)],
                "G_patch": patch,
                "next_G_center": [first[patch][1], target],
            }

    require(conflict is not None, f"expected a radius-{radius} conflict")
    return {
        "R": radius,
        "status": "conflict",
        "source_radius": source_radius,
        "source_windows": 1 << width,
        "realized_patches": len(targets),
        "required_targets": {key: sorted(value) for key, value in sorted(targets.items())},
        "table_zero_off_image": None,
        "conflict": conflict,
    }


def check_manifests(
    result: dict[str, object], execution: dict[str, object], verify_history: bool
) -> None:
    result_bytes = RESULT_PATH.read_bytes()
    require(execution["result_sha256"] == sha256(result_bytes), "result byte hash mismatch")
    require(execution["implementation_commit"] == IMPLEMENTATION_COMMIT,
            "unexpected implementation commit")
    require(result["protocol_reviewed_commit"] == PROTOCOL_COMMIT,
            "unexpected reviewed protocol commit")

    source_hashes = result["source_hashes"]
    protocol_hash = sha256(PROTOCOL_PATH.read_bytes())
    primary_hash = sha256(PRIMARY_PATH.read_bytes())
    require(source_hashes[str(PROTOCOL_PATH.relative_to(ROOT))] == protocol_hash,
            "current protocol hash differs from result manifest")
    require(source_hashes[str(PRIMARY_PATH.relative_to(ROOT))] == primary_hash,
            "current primary evaluator hash differs from result manifest")

    if not verify_history:
        return
    parent = subprocess.check_output(
        ["git", "show", "-s", "--format=%P", IMPLEMENTATION_COMMIT],
        cwd=ROOT,
        text=True,
    ).strip()
    require(parent == PROTOCOL_COMMIT, "implementation is not a child of the reviewed protocol")
    for relative, expected in source_hashes.items():
        committed = subprocess.check_output(
            ["git", "show", f"{IMPLEMENTATION_COMMIT}:{relative}"], cwd=ROOT
        )
        require(sha256(committed) == expected, f"committed source hash mismatch: {relative}")


def check_controls(result: dict[str, object]) -> None:
    rule32_ok = True
    for value in range(128):
        source = int_word(value, 7)
        left = finite_g(finite_step(source, 32), 32)
        right = finite_step(finite_g(source, 32), 128)
        rule32_ok &= left == right
    require(rule32_ok, "Rule-32 G-to-Rule-128 control failed")

    rule90_ok = all(finite_g(int_word(value, 5), 90) == (0,) for value in range(32))
    require(rule90_ok, "Rule-90 zero-G control failed")
    require(
        result["controls"]
        == {
            "C1_rule32_factor": {
                "identity": "G_32 E_32 = E_128 G_32",
                "source_windows": 128,
                "status": "pass",
            },
            "C2_rule90_constant": {
                "identity": "G_90 = 0",
                "source_windows": 32,
                "status": "pass",
            },
        },
        "canonical control records differ from independent checks",
    )


def ring_record(n: int) -> tuple[dict[str, object], dict[str, object] | None]:
    first: dict[tuple[int, ...], tuple[tuple[int, ...], tuple[int, ...]]] = {}
    visited = 0
    for value in range(1 << n):
        source = int_word(value, n)
        observed = cyclic_g(source, 110)
        successor = cyclic_g(cyclic_step(source, 110), 110)
        visited += 1
        if observed in first and first[observed][1] != successor:
            earlier = first[observed][0]
            return (
                {"n": n, "states_visited": visited, "status": "collision"},
                {"n": n, "sources": [tuple_trace(earlier, 110), tuple_trace(source, 110)]},
            )
        first.setdefault(observed, (source, successor))
    return (
        {
            "distinct_G_words": len(first),
            "n": n,
            "states_visited": visited,
            "status": "no_collision_on_this_ring",
        },
        None,
    )


def periodic_phase_values(period: tuple[int, ...]) -> tuple[str, str]:
    """Check one period using only explicit radius-three causal windows."""
    present = []
    successor = []
    for center in range(len(period)):
        window = tuple(period[offset % len(period)] for offset in range(center - 3, center + 4))
        present.append(finite_g(window, 110)[1])
        successor.append(finite_g(finite_step(window, 110), 110)[0])
    return format_word(tuple(present)), format_word(tuple(successor))


def check_target(result: dict[str, object]) -> dict[str, object]:
    require(result["local"] == [reconstruct_local(radius) for radius in (0, 1, 2)],
            "canonical local-factor records differ from independent reconstruction")

    ring_records = []
    witness = None
    for n in (1, 2, 3):
        record, collision = ring_record(n)
        ring_records.append(record)
        if collision is not None:
            witness = collision
            break
    require(ring_records == result["rings"][:3], "ring 1-3 records differ")
    require(witness == result["witness"], "period-three certificate traces differ")
    require(witness is not None, "period-three witness was not reconstructed")

    first, second = witness["sources"]
    require(first["S"] == "001" and second["S"] == "011", "unexpected witness sources")
    require(first["G"] == second["G"], "witness present G fields are unequal")
    require(first["next_G"] != second["next_G"], "witness next G fields are equal")

    first_periodic = periodic_phase_values(parse_word("001"))
    second_periodic = periodic_phase_values(parse_word("011"))
    require(first_periodic == (first["G"], first["next_G"]),
            "001 periodic finite-window extension differs from ring trace")
    require(second_periodic == (second["G"], second["next_G"]),
            "011 periodic finite-window extension differs from ring trace")
    require(first_periodic[0] == second_periodic[0],
            "periodic extensions do not have equal complete G fields")
    require(first_periodic[1] != second_periodic[1],
            "periodic extensions do not have unequal complete next-G fields")

    require(len(result["rings"]) == 16, "canonical result does not contain all 16 ring records")
    require(all(
        row == {"n": n, "states_visited": 0, "status": "not_run_after_witness"}
        for n, row in zip(range(4, 17), result["rings"][3:])
    ), "post-witness ring statuses differ from the frozen stopping rule")
    require(result["status"] == "no_full_shift_factor", "unexpected overall result status")
    require(result["predictions"] == {"P1_no_full_shift_factor": "supported_by_counterexample"},
            "unexpected prediction score")
    require(result["protocol_deviations"] == [], "result declares a protocol deviation")
    require(
        result["prediction_context"]
        == "001/011 collision candidate hand-derived after protocol freeze, before execution",
        "pre-execution candidate provenance is missing or altered",
    )
    return {
        "ring_1": ring_records[0],
        "ring_2": ring_records[1],
        "witness": witness,
        "periodic_finite_windows": {
            "001": {"G": first_periodic[0], "next_G": first_periodic[1]},
            "011": {"G": second_periodic[0], "next_G": second_periodic[1]},
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--history",
        action="store_true",
        help="also require Git ancestry and committed source-blob checks",
    )
    args = parser.parse_args()
    result = json.loads(RESULT_PATH.read_text())
    execution = json.loads(EXECUTION_PATH.read_text())
    check_manifests(result, execution, args.history)
    check_controls(result)
    evidence = check_target(result)
    print(json.dumps({
        "status": "independent_certificate_pass",
        "history_reverified": args.history,
        **evidence,
    }, indent=2))


if __name__ == "__main__":
    main()
