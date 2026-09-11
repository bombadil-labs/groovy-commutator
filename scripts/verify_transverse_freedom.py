#!/usr/bin/env python3
"""Finite-width packing and transverse-freedom diagnostic (frozen 2026-09-11).

The theorem controls T1-T3 are analytic. The bounded primary diagnostic T4
measures full-ring image/fiber counts for the inherited Rule32 correction
family on n=6..12 and h=0..4. ``--controls-only`` deliberately avoids every
T4 count so it is safe on an implementation-only commit before evaluation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import subprocess
from collections import Counter

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "results/transverse_freedom_20260911.json"
PROTOCOL = ROOT / "docs/research/protocols/transverse-freedom-20260911.md"
RINGS = tuple(range(6, 13))
COMPLETIONS = (128, 160)
KINDS = ("K", "O")
DEPTHS = tuple(range(5))


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def truth(rule: int) -> np.ndarray:
    return np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)


TRUTH = {r: truth(r) for r in (32, 128, 160)}


def decode_binary_states(n: int) -> np.ndarray:
    vals = np.arange(1 << n, dtype=np.uint64)
    shifts = np.arange(n - 1, -1, -1, dtype=np.uint64)
    return ((vals[:, None] >> shifts) & 1).astype(np.uint8)


def ring_step(bits: np.ndarray, rule: int, ref: bool = False) -> np.ndarray:
    l = np.roll(bits, 1, axis=1)
    c = bits
    r = np.roll(bits, -1, axis=1)
    if ref:
        if rule == 32:
            return l & (1 ^ c) & r
        if rule == 128:
            return l & c & r
        if rule == 160:
            return l & r
        raise ValueError(rule)
    return TRUTH[rule][4 * l + 2 * c + r]


def encode_first_image(source: np.ndarray, ref: bool = False) -> tuple[np.ndarray, np.ndarray]:
    f = ring_step(source, 32, ref=ref)
    d = source ^ f
    g = (f ^ ring_step(f, 32, ref=ref)) ^ ring_step(d, 32, ref=ref)
    return d, g


def H(pair: tuple[np.ndarray, np.ndarray], top: int, ref: bool = False) -> tuple[np.ndarray, np.ndarray]:
    u, v = pair
    return ring_step(u, 32, ref=ref) ^ v, ring_step(v, top, ref=ref)


def xor_pair(a: tuple[np.ndarray, np.ndarray], b: tuple[np.ndarray, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    return a[0] ^ b[0], a[1] ^ b[1]


def pair_equal(a: tuple[np.ndarray, np.ndarray], b: tuple[np.ndarray, np.ndarray]) -> bool:
    return bool(np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1]))


def A(pair: tuple[np.ndarray, np.ndarray], top: int, j: int, ref: bool = False) -> tuple[np.ndarray, np.ndarray]:
    if j == 0:
        return xor_pair(pair, H(pair, top, ref=ref))
    return xor_pair(
        A(H(pair, top, ref=ref), top, j - 1, ref=ref),
        H(A(pair, top, j - 1, ref=ref), top, ref=ref),
    )


def O(pair: tuple[np.ndarray, np.ndarray], top: int, j: int, ref: bool = False) -> tuple[np.ndarray, np.ndarray]:
    cur = pair
    for _ in range(j):
        cur = H(cur, top, ref=ref)
    return A(cur, top, 0, ref=ref)


def pair_state_keys(pair: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
    symbols = (2 * pair[0] + pair[1]).astype(np.uint64)
    keys = np.zeros(symbols.shape[0], dtype=np.uint64)
    for x in range(symbols.shape[1]):
        keys = (keys << np.uint64(2)) | symbols[:, x]
    return keys


def tuple_symbols(rows: list[tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
    return np.concatenate([(2 * u + v).astype(np.uint8) for u, v in rows], axis=1)


def partition_stats(symbols: np.ndarray) -> tuple[int, np.ndarray, dict[str, int], str, str]:
    arr = np.ascontiguousarray(symbols, dtype=np.uint8)
    width_bytes = arr.dtype.itemsize * arr.shape[1]
    raw = arr.view(np.dtype((np.void, width_bytes))).reshape(-1)
    _, inverse = np.unique(raw, return_inverse=True)
    image_count = int(inverse.max()) + 1 if len(inverse) else 0
    first = np.full(image_count, len(inverse), dtype=np.uint32)
    if image_count:
        np.minimum.at(first, inverse, np.arange(len(inverse), dtype=np.uint32))
    signature = first[inverse] if image_count else np.empty(0, dtype=np.uint32)
    sizes = np.bincount(inverse, minlength=image_count) if image_count else np.empty(0, dtype=np.int64)
    hist = Counter(int(x) for x in sizes.tolist())
    return (
        image_count,
        signature,
        {str(size): int(hist[size]) for size in sorted(hist)},
        sha_bytes(signature.astype("<u4", copy=False).tobytes()),
        sha_bytes(arr.tobytes()),
    )


def T_from_K_rows(
    krows: list[tuple[np.ndarray, np.ndarray]], top: int, ref: bool = False
) -> list[tuple[np.ndarray, np.ndarray]]:
    current = krows
    out: list[tuple[np.ndarray, np.ndarray]] = []
    while current:
        out.append(current[0])
        if len(current) == 1:
            break
        current = [
            xor_pair(H(current[j], top, ref=ref), current[j + 1])
            for j in range(len(current) - 1)
        ]
    return out


def inverse_T_from_O_rows(
    orows: list[tuple[np.ndarray, np.ndarray]], top: int, ref: bool = False
) -> list[tuple[np.ndarray, np.ndarray]]:
    current = orows
    out: list[tuple[np.ndarray, np.ndarray]] = []
    while current:
        out.append(current[0])
        if len(current) == 1:
            break
        current = [
            xor_pair(current[j + 1], H(current[j], top, ref=ref))
            for j in range(len(current) - 1)
        ]
    return out


def rows_equal(
    a: list[tuple[np.ndarray, np.ndarray]], b: list[tuple[np.ndarray, np.ndarray]]
) -> bool:
    return len(a) == len(b) and all(pair_equal(x, y) for x, y in zip(a, b))


def round_metric(x: float) -> float:
    return round(float(x), 12)


def t1_indexing_control() -> dict:
    n, w = 3, 3
    total = 1 << (n * w)
    bits = decode_binary_states(n * w).reshape(total, n, w)
    packed = np.zeros((total, n), dtype=np.uint8)
    for y in range(w):
        packed = (packed << 1) | bits[:, :, y]
    unpacked = np.empty_like(bits)
    for y in range(w):
        shift = w - 1 - y
        unpacked[:, :, y] = (packed >> shift) & 1
    if not np.array_equal(bits, unpacked):
        raise AssertionError("T1 column packing roundtrip failed")
    shifted_packed = np.roll(packed, -1, axis=1)
    shifted_bits = np.roll(bits, -1, axis=1)
    repacked_shifted = np.zeros_like(packed)
    for y in range(w):
        repacked_shifted = (repacked_shifted << 1) | shifted_bits[:, :, y]
    if not np.array_equal(shifted_packed, repacked_shifted):
        raise AssertionError("T1 horizontal shift conjugacy failed")
    if len(np.unique(packed, axis=0)) != total:
        raise AssertionError("T1 packed states are not injective")
    return {
        "alphabet_size": 2,
        "n": n,
        "width": w,
        "states_checked": total,
        "roundtrip": True,
        "horizontal_shift_commutes": True,
        "injective": True,
    }


def t2_capacity_controls() -> list[dict]:
    samples = [
        {"source_alphabet": 4, "q": 2, "K": 2, "n": 3, "widths": (1, 2, 3)},
        {"source_alphabet": 4, "q": 4, "K": 2, "n": 5, "widths": (1, 2, 3)},
        {"source_alphabet": 4, "q": 8, "K": 2, "n": 4, "widths": (2, 3, 4)},
        {"source_alphabet": 2, "q": 2, "K": 3, "n": 7, "widths": (2, 3, 4)},
    ]
    out = []
    for sample in samples:
        rows = []
        for w in sample["widths"]:
            source_count = sample["source_alphabet"] ** (w * sample["n"])
            target_count = sample["q"] ** (sample["K"] * sample["n"])
            rows.append(
                {
                    "width": w,
                    "source_count": source_count,
                    "target_count": target_count,
                    "capacity_allows_injection": bool(source_count <= target_count),
                }
            )
        if not any(r["capacity_allows_injection"] for r in rows) or not any(
            not r["capacity_allows_injection"] for r in rows
        ):
            raise AssertionError(("T2 sample must straddle capacity threshold", sample))
        out.append({**{k: v for k, v in sample.items() if k != "widths"}, "cases": rows})
    return out


def strip_count_controls() -> dict:
    # Small exhaustive enumeration checks the closed forms used for the large
    # diagnostic table; the theorem itself is just product counting.
    checks = []
    n = 2
    for w in (1, 2, 3):
        total = 4 ** (w * n)
        vals = np.arange(total, dtype=np.uint64)
        digits = np.empty((total, w * n), dtype=np.uint8)
        cur = vals.copy()
        for j in range(w * n - 1, -1, -1):
            digits[:, j] = (cur & 3).astype(np.uint8)
            cur >>= 2
        independent = len(np.unique(digits, axis=0))
        base_total = 4**n
        base_vals = np.arange(base_total, dtype=np.uint64)
        base = np.empty((base_total, n), dtype=np.uint8)
        cur = base_vals.copy()
        for j in range(n - 1, -1, -1):
            base[:, j] = (cur & 3).astype(np.uint8)
            cur >>= 2
        duplicated = np.tile(base, (1, w))
        duplicate_count = len(np.unique(duplicated, axis=0))
        if independent != 4 ** (w * n) or duplicate_count != 4**n:
            raise AssertionError(("strip count control", w, independent, duplicate_count))
        checks.append(
            {
                "n": n,
                "width": w,
                "independent_enumerated": independent,
                "independent_closed_form": 4 ** (w * n),
                "duplicated_enumerated": duplicate_count,
                "duplicated_closed_form": 4**n,
            }
        )
    return {"small_exhaustive": checks}


def truth_formula_control() -> dict:
    neighborhoods = decode_binary_states(3)
    for rule in (32, 128, 160):
        l, c, r = neighborhoods[:, 0], neighborhoods[:, 1], neighborhoods[:, 2]
        codes = 4 * l + 2 * c + r
        table = TRUTH[rule][codes]
        if rule == 32:
            formula = l & (1 ^ c) & r
        elif rule == 128:
            formula = l & c & r
        else:
            formula = l & r
        if not np.array_equal(table, formula):
            raise AssertionError(("truth formula", rule))
    return {"rules": [32, 128, 160], "neighborhoods_per_rule": 8, "agreement": True}


def controls_only() -> dict:
    return {
        "truth_formula": truth_formula_control(),
        "T1_column_packing": t1_indexing_control(),
        "T2_capacity_samples": t2_capacity_controls(),
        "strip_closed_forms": strip_count_controls(),
        "note": "Analytic theorem controls and indexing checks only; no n=6..12 Rule32 tuple image count is computed here.",
    }


def git_last_change(path: pathlib.Path) -> str | None:
    resolved = path.resolve()
    env_key = None
    if resolved == pathlib.Path(__file__).resolve():
        env_key = "TRANSVERSE_FREEDOM_IMPLEMENTATION_COMMIT"
    elif resolved == PROTOCOL.resolve():
        env_key = "TRANSVERSE_FREEDOM_PROTOCOL_COMMIT"
    if env_key and os.environ.get(env_key):
        return os.environ[env_key]
    try:
        rel = str(resolved.relative_to(ROOT.resolve()))
        return (
            subprocess.check_output(
                ["git", "-C", str(ROOT), "log", "-1", "--format=%H", "--", rel],
                text=True,
            ).strip()
            or None
        )
    except Exception:
        return None


def full_ring_diagnostic() -> tuple[list[dict], list[dict], dict]:
    cells: list[dict] = []
    ring_summaries: list[dict] = []
    total_reference_row_arrays = 0
    total_recoding_state_checks = 0

    for n in RINGS:
        source = decode_binary_states(n)
        xp = encode_first_image(source, ref=False)
        xr = encode_first_image(source, ref=True)
        if not pair_equal(xp, xr):
            raise AssertionError(("first image reference mismatch", n))

        keys = pair_state_keys(xp)
        unique_keys, first = np.unique(keys, return_index=True)
        order = np.argsort(unique_keys)
        first = first[order]
        X = (xp[0][first], xp[1][first])
        b_count = int(len(first))
        if b_count > (1 << n):
            raise AssertionError(("B source bound", n, b_count))

        rows_by_top: dict[int, dict[str, list[tuple[np.ndarray, np.ndarray]]]] = {}
        rows_ref_by_top: dict[int, dict[str, list[tuple[np.ndarray, np.ndarray]]]] = {}
        stats: dict[
            tuple[int, str, int], tuple[int, np.ndarray, dict[str, int], str, str]
        ] = {}

        for top in COMPLETIONS:
            krows = [A(X, top, j, ref=False) for j in DEPTHS]
            orows = [O(X, top, j, ref=False) for j in DEPTHS]
            krows_ref = [A(X, top, j, ref=True) for j in DEPTHS]
            orows_ref = [O(X, top, j, ref=True) for j in DEPTHS]
            for primary_rows, reference_rows, kind in (
                (krows, krows_ref, "K"),
                (orows, orows_ref, "O"),
            ):
                for j, (p, r) in enumerate(zip(primary_rows, reference_rows)):
                    if not pair_equal(p, r):
                        raise AssertionError(("reference tuple row mismatch", n, top, kind, j))
                    total_reference_row_arrays += 1
            rows_by_top[top] = {"K": krows, "O": orows}
            rows_ref_by_top[top] = {"K": krows_ref, "O": orows_ref}

            for h in DEPTHS:
                direct_k = krows[: h + 1]
                direct_o = orows[: h + 1]
                if not rows_equal(T_from_K_rows(direct_k, top), direct_o):
                    raise AssertionError(("K->O recoding", n, top, h))
                if not rows_equal(inverse_T_from_O_rows(direct_o, top), direct_k):
                    raise AssertionError(("O->K recoding", n, top, h))
                total_recoding_state_checks += 2 * b_count

        for j in DEPTHS:
            if not pair_equal(rows_by_top[128]["O"][j], rows_by_top[160]["O"][j]):
                raise AssertionError(("O pointwise completion equality", n, j))

        for h in DEPTHS:
            o128 = rows_by_top[128]["O"][: h + 1]
            o160 = rows_by_top[160]["O"][: h + 1]
            k128 = rows_by_top[128]["K"][: h + 1]
            k160 = rows_by_top[160]["K"][: h + 1]
            if not rows_equal(inverse_T_from_O_rows(o128, 160), k160):
                raise AssertionError(("H128->H160 recoding", n, h))
            if not rows_equal(inverse_T_from_O_rows(o160, 128), k128):
                raise AssertionError(("H160->H128 recoding", n, h))
            total_recoding_state_checks += 2 * b_count

        for top in COMPLETIONS:
            for kind in KINDS:
                rows = rows_by_top[top][kind]
                rows_ref = rows_ref_by_top[top][kind]
                for h in DEPTHS:
                    symbols = tuple_symbols(rows[: h + 1])
                    symbols_ref = tuple_symbols(rows_ref[: h + 1])
                    if not np.array_equal(symbols, symbols_ref):
                        raise AssertionError(("reference tuple mismatch", n, top, kind, h))
                    image_count, signature, fiber_hist, sig_sha, tuple_sha = partition_stats(symbols)
                    ref_count, ref_sig, ref_hist, ref_sig_sha, ref_tuple_sha = partition_stats(
                        symbols_ref
                    )
                    if (
                        image_count,
                        fiber_hist,
                        sig_sha,
                        tuple_sha,
                    ) != (ref_count, ref_hist, ref_sig_sha, ref_tuple_sha) or not np.array_equal(
                        signature, ref_sig
                    ):
                        raise AssertionError(("reference partition mismatch", n, top, kind, h))
                    if image_count > b_count:
                        raise AssertionError(
                            ("T3 source bound", n, top, kind, h, image_count, b_count)
                        )
                    log_c = math.log2(image_count) if image_count else 0.0
                    log_b = math.log2(b_count) if b_count else 0.0
                    cell = {
                        "n": n,
                        "completion": top,
                        "kind": kind,
                        "h": h,
                        "B_n_states": b_count,
                        "tuple_image_states": image_count,
                        "tuple_information_rate_bits_per_longitudinal_site": round_metric(
                            log_c / n
                        ),
                        "nominal_represented_bits_per_site": 2 * (h + 1),
                        "fraction_of_B_log_capacity_exposed": round_metric(log_c / log_b)
                        if log_b
                        else None,
                        "source_bound_margin_states": b_count - image_count,
                        "fiber_histogram_over_distinct_B_states": fiber_hist,
                        "fiber_signature_sha256": sig_sha,
                        "tuple_symbols_sha256": tuple_sha,
                    }
                    cells.append(cell)
                    stats[(top, kind, h)] = (
                        image_count,
                        signature,
                        fiber_hist,
                        sig_sha,
                        tuple_sha,
                    )

        for h in DEPTHS:
            base_sig = stats[(128, "K", h)][1]
            for top in COMPLETIONS:
                for kind in KINDS:
                    if not np.array_equal(base_sig, stats[(top, kind, h)][1]):
                        raise AssertionError(("fiber control", n, h, top, kind))

        common_counts = [stats[(128, "K", h)][0] for h in DEPTHS]
        if any(b < a for a, b in zip(common_counts, common_counts[1:])):
            raise AssertionError(("depth monotonicity", n, common_counts))
        terminal_plateau_start = None
        for h in range(len(DEPTHS) - 1):
            if all(x == common_counts[h] for x in common_counts[h:]):
                terminal_plateau_start = h
                break
        ring_summaries.append(
            {
                "n": n,
                "binary_source_states": 1 << n,
                "B_n_states": b_count,
                "B_n_information_rate_bits_per_longitudinal_site": round_metric(
                    math.log2(b_count) / n
                ),
                "source_aliases_under_E": (1 << n) - b_count,
                "tuple_image_states_by_depth": common_counts,
                "tuple_image_increments": [common_counts[0]]
                + [common_counts[j] - common_counts[j - 1] for j in range(1, len(common_counts))],
                "terminal_plateau_start_within_h0_to_h4": terminal_plateau_start,
                "all_four_completion_coordinate_partitions_identical": True,
                "O_pointwise_identical_across_completions": True,
                "K_O_recoding_both_directions": True,
                "cross_completion_recoding_both_directions": True,
                "source_bound_holds": all(c <= b_count for c in common_counts),
                "closed_form_controls": [
                    {
                        "h": h,
                        "width": h + 1,
                        "independent_strip_states": 4 ** ((h + 1) * n),
                        "independent_strip_information_rate_bits_per_site": 2 * (h + 1),
                        "duplicated_row_states": 4**n,
                        "duplicated_row_information_rate_bits_per_site": 2,
                    }
                    for h in DEPTHS
                ],
            }
        )

    summary = {
        "rings": list(RINGS),
        "depths": list(DEPTHS),
        "completions": list(COMPLETIONS),
        "coordinate_systems": list(KINDS),
        "diagnostic_cells": len(cells),
        "all_source_bounds_hold": True,
        "all_fixed_depth_fiber_controls_hold": True,
        "all_K_O_recoding_controls_hold": True,
        "all_cross_completion_recoding_controls_hold": True,
        "all_primary_reference_rows_agree": True,
        "reference_tuple_row_arrays_compared": total_reference_row_arrays,
        "recoding_state_checks": total_recoding_state_checks,
        "claim_scope": "bounded n=6..12, h=0..4 inherited Rule32 diagnostic; theorem T3 is analytic for every finite h; no intrinsic-dimension claim",
    }
    return cells, ring_summaries, summary


def run_full() -> dict:
    theorem_controls = controls_only()
    cells, rings, summary = full_ring_diagnostic()
    result = {
        "protocol": "transverse-freedom-20260911",
        "scope": {
            "ring_sizes": list(RINGS),
            "completions": list(COMPLETIONS),
            "coordinates": list(KINDS),
            "depths": list(DEPTHS),
            "domain": "distinct Rule32 first-image pair states B_n on periodic rings",
            "primary_question": "independent transverse state capacity under a fixed representation budget",
        },
        "source_hashes": {
            "script": sha_file(pathlib.Path(__file__)),
            "protocol": sha_file(PROTOCOL),
        },
        "implementation_commit": git_last_change(pathlib.Path(__file__)),
        "protocol_commit": git_last_change(PROTOCOL),
        "theorem_and_indexing_controls": theorem_controls,
        "ring_summaries": rings,
        "cells": cells,
        "summary": summary,
        "interpretation_limit": "Finite-width packing and fixed-budget capacity are representation/resource statements. The bounded Rule32 diagnostic does not define intrinsic spatial dimension, establish a new spatial axis, or extrapolate the measured h<=4 pattern to h->infinity.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls-only", action="store_true")
    args = parser.parse_args()
    if args.controls_only:
        print(json.dumps(controls_only(), indent=2, sort_keys=True))
        return 0
    result = run_full()
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
