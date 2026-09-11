#!/usr/bin/env python3
"""Verifier for the frozen uniform-local-intervention-axis protocol.

Protocol: docs/research/protocols/intervention-axis-20260911.md
Gate 1: Claude Code / Fable 5.1 approved integrated revision dc363745 on
2026-09-11 with the two binding clarifications recorded in Section 11.
This verifier is committed before the first primary run.

The all-m statements I1-I3 are analytic or inherited theorem controls.  The
finite computation below is only the bounded I4/I5 implementation replay plus
small exact examples of the I3 endpoint-count inequality.  It imports no saved
research result table.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/intervention-axis-20260911.md"
OUT = ROOT / "results/intervention_axis_20260911.json"

CHANNEL_COUNTS = (1, 2, 3, 4, 5, 6)
RINGS = (5, 7)
GAP = 1
ACTION_COORDINATE = 0
COARSE_UPDATES = 2
SEEDED_ROW_SEED = 20260911
BASE_KINDS = ("zero", "one", "seeded")
I3_EXAMPLES = ((2, 1, 0), (2, 2, 1), (4, 1, 1), (3, 2, 2))


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def step2(grid: np.ndarray, shrink: bool = False) -> np.ndarray:
    """Exact fixed Research-012 2D update; last axes are y,x.

    This is the same local law used by the coupled-strips instruments, written
    here directly so the present verifier has no dependency on saved results.
    """
    m, n = grid.shape[-2:]
    if shrink:
        c = grid[..., 1:-1, 1:-1].astype(np.int64)
        population = grid[..., 1:-1, :-2] + grid[..., 1:-1, 2:]
        yy, xx = np.indices((m - 2, n - 2)) + 1
    else:
        c = grid.astype(np.int64)
        population = np.roll(grid, 1, axis=-1) + np.roll(grid, -1, axis=-1)
        yy, xx = np.indices((m, n))
    yi = (yy + 2 * c - 1) % m
    xi = (xx + population.astype(np.int64) - 1) % n
    index = (yi * n + xi).reshape(grid.shape[:-2] + (-1,))
    flat = grid.reshape(grid.shape[:-2] + (-1,))
    return np.take_along_axis(flat, index, axis=-1).reshape(c.shape)


def fine_step_ring(field: np.ndarray) -> np.ndarray:
    """One fine tick with horizontal wrap and open/shrinking vertical edges."""
    padded = np.pad(field, ((0, 0), (0, 0), (1, 1)), mode="wrap")
    return step2(padded, shrink=True)


def rule90(states: np.ndarray) -> np.ndarray:
    """Independent literal Rule-90 reference: left XOR right."""
    return np.roll(states, 1, axis=-1) ^ np.roll(states, -1, axis=-1)


def encode_many(states: np.ndarray, ys: np.ndarray, xs: np.ndarray, gap: int) -> np.ndarray:
    """Encode arbitrary aligned logical rows as separated/touching strips.

    states has shape (..., channels, logical_width).  Strip r starts at
    y=(2+gap)r.  The untouched background is B(y,2i)=0, B(y,2i+1)=1.
    """
    states = np.asarray(states, dtype=np.uint8)
    channels, n = states.shape[-2:]
    batch_shape = states.shape[:-2]
    background = np.asarray(xs % 2, dtype=np.uint8)
    out = np.broadcast_to(background, batch_shape + (len(ys), len(xs))).copy()
    y_to_index = {int(y): j for j, y in enumerate(ys)}
    for r in range(channels):
        start = (2 + gap) * r
        if start not in y_to_index or start + 1 not in y_to_index:
            raise AssertionError("vertical window does not contain complete strip")
        top = y_to_index[start]
        bottom = y_to_index[start + 1]
        for k, x in enumerate(xs):
            data = states[..., r, (int(x) // 2) % n]
            if int(x) % 2:
                out[..., top, k] = 1 ^ data
            else:
                out[..., bottom, k] = data
    return out


def seeded_rows(channels: int, n: int) -> np.ndarray:
    rows = []
    for r in range(channels):
        rng = np.random.default_rng(SEEDED_ROW_SEED + 1000 * n + r)
        rows.append(rng.integers(0, 2, size=n, dtype=np.uint8))
    return np.stack(rows, axis=0)


def base_rows(kind: str, channels: int, n: int) -> np.ndarray:
    if kind == "zero":
        return np.zeros((channels, n), dtype=np.uint8)
    if kind == "one":
        return np.ones((channels, n), dtype=np.uint8)
    if kind == "seeded":
        return seeded_rows(channels, n)
    raise ValueError(kind)


def logical_endpoints(base: np.ndarray, action_coordinate: int = ACTION_COORDINATE) -> np.ndarray:
    channels = base.shape[0]
    endpoints = np.repeat(base[None, ...], 1 << channels, axis=0)
    for mask in range(1 << channels):
        for r in range(channels):
            if (mask >> r) & 1:
                endpoints[mask, r, action_coordinate] ^= 1
    return endpoints


def physical_endpoints(base_field: np.ndarray, ys: np.ndarray, channels: int) -> np.ndarray:
    endpoints = np.repeat(base_field[None, ...], 1 << channels, axis=0)
    y_to_index = {int(y): j for j, y in enumerate(ys)}
    # At logical i=0 the matched action flips physical x=1 on the top row
    # and x=0 on the bottom row of the selected strip.
    for mask in range(1 << channels):
        for r in range(channels):
            if (mask >> r) & 1:
                start = 3 * r
                endpoints[mask, y_to_index[start], 1] ^= 1
                endpoints[mask, y_to_index[start + 1], 0] ^= 1
    return endpoints


def support_coordinates(a: np.ndarray, b: np.ndarray, ys: np.ndarray, xs: np.ndarray) -> list[list[int]]:
    diff = np.argwhere(a != b)
    return [[int(ys[y]), int(xs[x])] for y, x in diff]


def replay_separated() -> tuple[list[dict], bool, bool]:
    records: list[dict] = []
    all_rank_controls = True
    all_replay_controls = True
    xs_by_n = {n: np.arange(2 * n, dtype=int) for n in RINGS}

    for m in CHANNEL_COUNTS:
        for n in RINGS:
            xs = xs_by_n[n]
            ys = np.arange(-6, 3 * m + 8, dtype=int)
            for kind in BASE_KINDS:
                base = base_rows(kind, m, n)
                base_field = encode_many(base, ys, xs, GAP)
                logical = logical_endpoints(base)
                physical = physical_endpoints(base_field, ys, m)
                expected = encode_many(logical, ys, xs, GAP)
                endpoints_valid = bool(np.array_equal(physical, expected))
                endpoint_count = len({row.tobytes() for row in physical})

                generator_supports = []
                support_sets = []
                for r in range(m):
                    coords = support_coordinates(base_field, physical[1 << r], ys, xs)
                    generator_supports.append(coords)
                    support_sets.append({tuple(c) for c in coords})
                support_sizes = [len(s) for s in support_sets]
                supports_disjoint = all(
                    support_sets[a].isdisjoint(support_sets[b])
                    for a in range(m)
                    for b in range(a + 1, m)
                )

                evolution_pass = True
                field = physical.copy()
                current_logical = logical.copy()
                current_ys = ys.copy()
                coarse_records = []
                for coarse in range(1, COARSE_UPDATES + 1):
                    field = fine_step_ring(field)
                    field = fine_step_ring(field)
                    current_ys = current_ys[2:-2]
                    current_logical = rule90(current_logical)
                    expected_field = encode_many(current_logical, current_ys, xs, GAP)
                    matches = bool(np.array_equal(field, expected_field))
                    evolution_pass &= matches
                    coarse_records.append({"coarse_step": coarse, "matches_rule90_product": matches})

                rank_ok = endpoints_valid and endpoint_count == (1 << m) and all(s == 2 for s in support_sizes) and supports_disjoint
                replay_ok = rank_ok and evolution_pass
                all_rank_controls &= rank_ok
                all_replay_controls &= replay_ok
                records.append(
                    {
                        "m": m,
                        "n": n,
                        "base": kind,
                        "endpoint_count": endpoint_count,
                        "expected_endpoint_count": 1 << m,
                        "all_action_endpoints_valid": endpoints_valid,
                        "generator_support_sizes": support_sizes,
                        "generator_supports": generator_supports,
                        "supports_disjoint": supports_disjoint,
                        "coarse_replay": coarse_records,
                        "pass": replay_ok,
                    }
                )
    return records, all_rank_controls, all_replay_controls


def replay_copied_width() -> tuple[list[dict], bool]:
    records: list[dict] = []
    all_ok = True
    for m in CHANNEL_COUNTS:
        for n in RINGS:
            xs = np.arange(2 * n, dtype=int)
            ys = np.arange(-6, 3 * m + 8, dtype=int)
            for kind in BASE_KINDS:
                shared = base_rows(kind, 1, n)[0]
                base = np.repeat(shared[None, :], m, axis=0)
                base_field = encode_many(base, ys, xs, GAP)
                logical = logical_endpoints(base)
                physical = physical_endpoints(base_field, ys, m)
                inside_masks = [
                    mask
                    for mask in range(1 << m)
                    if bool(np.all(logical[mask] == logical[mask, 0][None, :]))
                ]
                expected_masks = [0, (1 << m) - 1] if m > 0 else [0]
                full_support = len(support_coordinates(base_field, physical[(1 << m) - 1], ys, xs))
                ok = inside_masks == expected_masks and full_support == 2 * m
                all_ok &= ok
                records.append(
                    {
                        "m": m,
                        "n": n,
                        "base": kind,
                        "image_preserving_subset_masks_at_edit_time": inside_masks,
                        "expected_masks": expected_masks,
                        "full_channel_flip_support": full_support,
                        "expected_full_support": 2 * m,
                        "pass": ok,
                    }
                )
    return records, all_ok


def touching_control() -> dict:
    # VARIABLE order matches the archived local census: aL,aC,aR,bL,bC,bR.
    inputs = ((np.arange(64)[:, None] >> np.arange(6)) & 1).astype(np.uint8)
    a = inputs[:, [1, 2, 0]]  # logical ring indices center,right,left
    b = inputs[:, [4, 5, 3]]
    states = np.stack([a, b], axis=1)
    ys = np.arange(-4, 8, dtype=int)
    xs = np.arange(-2, 4, dtype=int)
    initial = encode_many(states, ys, xs, gap=0)
    first = step2(initial, shrink=True)
    output = step2(first, shrink=True)
    rows = ys[2:-2]
    out_xs = xs[2:-2]
    row_to_index = {int(y): j for j, y in enumerate(rows)}
    decoded_a = output[:, row_to_index[1], 0]
    decoded_b = output[:, row_to_index[3], 0]
    decoded = np.stack([decoded_a, decoded_b], axis=1)[..., None]
    reconstructed = encode_many(decoded, rows, out_xs, gap=0)
    valid = np.all(output == reconstructed, axis=(1, 2))
    failed = np.flatnonzero(~valid)
    witness = None
    if len(failed):
        q = int(failed[0])
        invalid = np.argwhere(output[q] != reconstructed[q])
        witness = {
            "input_index": q,
            "input_bits_aL_aC_aR_bL_bC_bR": [int(x) for x in inputs[q]],
            "decoded_pair": [int(decoded_a[q]), int(decoded_b[q])],
            "invalid_cells": [
                {"y": int(rows[y]), "x": int(out_xs[x])} for y, x in invalid
            ],
        }
    valid_count = int(valid.sum())
    return {
        "total_inputs": 64,
        "valid_inputs": valid_count,
        "invalid_inputs": 64 - valid_count,
        "expected_valid": 17,
        "expected_invalid": 47,
        "first_invalid_witness": witness,
        "pass": valid_count == 17 and (64 - valid_count) == 47 and witness is not None,
    }


def i3_examples() -> tuple[list[dict], bool]:
    records = []
    all_ok = True
    for q, k, r in I3_EXAMPLES:
        s = k + 2 * r
        capacity = q**s
        max_m = 0
        while 2 ** (max_m + 1) <= capacity:
            max_m += 1
        first_failure = max_m + 1
        ok = (2**max_m <= capacity) and (2**first_failure > capacity)
        all_ok &= ok
        records.append(
            {
                "q": q,
                "K": k,
                "R": r,
                "endpoint_window_sites": s,
                "endpoint_capacity": capacity,
                "max_m_satisfying_2^m_le_q^S": max_m,
                "first_failing_m": first_failure,
                "fixed_total_length_special_case_capacity_per_coordinate": q**k,
                "pass": ok,
            }
        )
    return records, all_ok


def main() -> None:
    separated, i1_ok, i5_ok = replay_separated()
    copied, i2_ok = replay_copied_width()
    touching = touching_control()
    i3, i3_ok = i3_examples()

    summary = {
        "I1_prior_theorem_rank_controls": i1_ok,
        "I2_copied_width_control": i2_ok,
        "I3_local_endpoint_count_examples": i3_ok,
        "I4_touching_strip_control": bool(touching["pass"]),
        "I5_bounded_separated_replay": i5_ok,
    }
    result = {
        "protocol": "intervention-axis-20260911",
        "schema": 1,
        "parameters": {
            "channel_counts": list(CHANNEL_COUNTS),
            "rings": list(RINGS),
            "gap_background_rows": GAP,
            "action_coordinate": ACTION_COORDINATE,
            "coarse_updates_after_action": COARSE_UPDATES,
            "base_kinds": list(BASE_KINDS),
            "seeded_row_seed_formula": "20260911 + 1000*n + channel",
            "i3_examples_q_K_R": [list(x) for x in I3_EXAMPLES],
        },
        "source_hashes": {
            "script": sha(pathlib.Path(__file__)),
            "protocol": sha(PROTOCOL),
        },
        "analytic_status": {
            "I1": "inherited all-m theorem repackaged as a rank lower bound; finite replay is implementation control only",
            "I2": "declared-layout instantaneous support statement; finite replay is implementation control only",
            "I3": "counting theorem for unbounded total target length with fixed common local endpoint window; numeric rows are examples only",
        },
        "separated_strip_replay": separated,
        "copied_width_replay": copied,
        "i3_endpoint_count_examples": i3,
        "touching_strip_control": touching,
        "summary": summary,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
