#!/usr/bin/env python3
"""Verifier for cross-width locality of complete interface history.

Protocol: docs/research/protocols/interface-history-cross-width-20260912.md
Gate 1: Claude/Fable approved exact gathering head
7cc4bbae2eb5af50e133b8a8eaf44fb55db358a8 on 2026-09-12, with the
near-whole-ring null recorded before this verifier.

This is the implementation-only stage. Running without --self-test performs
the frozen n=6,7,8,9 census and writes the canonical result. --self-test uses
only out-of-domain widths 3 and 4 and writes nothing.
"""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import pathlib
from dataclasses import dataclass

import numpy as np

from verify_interface_factor import (
    COARSE_STATES,
    COORDINATES,
    all_source_pairs,
    build_ring_orbit,
    field_mask,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/interface-history-cross-width-20260912.md"
HISTORY_PROTOCOL = ROOT / "docs/research/protocols/interface-history-20260911.md"
HISTORY_SCRIPT = ROOT / "scripts/verify_interface_history.py"
HISTORY_RESULT = ROOT / "results/interface_history_20260911.json"
GLOBAL_PROTOCOL = ROOT / "docs/research/protocols/interface-history-global-20260912.md"
GLOBAL_SCRIPT = ROOT / "scripts/verify_interface_history_global.py"
GLOBAL_RESULT = ROOT / "results/interface_history_global_20260912.json"
FACTOR_SCRIPT = ROOT / "scripts/verify_interface_factor.py"
OUT = ROOT / "results/interface_history_cross_width_20260912.json"

WIDTHS = (6, 7, 8, 9)
FRESH_WIDTHS = (8, 9)
MASKS = (11, 13, 15)
TIMES = (2, 3, 4, 5, 6)
HISTORY_DEPTH = 2
RADIUS = 3
OFFSETS = tuple(range(-RADIUS, RADIUS + 1))


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class ReferenceOrbit:
    n: int
    symbols: list[np.ndarray]


def _reference_encode_adjacent(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Independent explicit encoder for the frozen adjacent-strip family."""
    if a.shape != b.shape or a.ndim != 2:
        raise AssertionError((a.shape, b.shape))
    sources, n = a.shape
    xs = np.arange(2 * n, dtype=int)
    margin = 2 * (COARSE_STATES - 1)
    ys = np.arange(-margin, 4 + margin, dtype=int)
    background = (xs % 2).astype(np.uint8)
    out = np.broadcast_to(background, (sources, len(ys), len(xs))).copy()
    yidx = {int(y): i for i, y in enumerate(ys)}
    for site in range(n):
        even = 2 * site
        odd = even + 1
        out[:, yidx[0], odd] = 1 ^ a[:, site]
        out[:, yidx[1], even] = a[:, site]
        out[:, yidx[2], odd] = 1 ^ b[:, site]
        out[:, yidx[3], even] = b[:, site]
    return out, ys


def _reference_fine_step(field: np.ndarray) -> np.ndarray:
    """Independent site-explicit selector step; periodic x and shrinking y."""
    if field.ndim != 3 or field.shape[1] < 3:
        raise AssertionError(field.shape)
    sources, height, width = field.shape
    out = np.empty((sources, height - 2, width), dtype=np.uint8)
    src = np.arange(sources, dtype=np.int64)
    for y in range(height - 2):
        cy = y + 1
        for x in range(width):
            c = field[:, cy, x].astype(np.int64)
            left = field[:, cy, (x - 1) % width].astype(np.int64)
            right = field[:, cy, (x + 1) % width].astype(np.int64)
            sy = y + 2 * c
            sx = (x + left + right - 1) % width
            out[:, y, x] = field[src, sy, sx]
    return out


def _reference_observe(field: np.ndarray, ys: np.ndarray) -> np.ndarray:
    """Independent explicit six-coordinate observer."""
    yidx = {int(y): i for i, y in enumerate(ys)}
    u0 = field[:, yidx[0], 1::2]
    u1 = field[:, yidx[1], 0::2]
    u2 = field[:, yidx[1], 1::2]
    u3 = field[:, yidx[2], 0::2]
    u4 = field[:, yidx[2], 1::2]
    u5 = field[:, yidx[3], 0::2]
    A = u1
    B = u5
    E0 = u0 ^ 1 ^ A
    E1 = u2 ^ 1
    E2 = u3
    E3 = u4 ^ 1 ^ B
    return (A | (B << 1) | (E0 << 2) | (E1 << 3) | (E2 << 4) | (E3 << 5)).astype(np.uint8)


def build_reference_orbit(n: int) -> ReferenceOrbit:
    """Independent physical trajectory/observer path for every retained field."""
    a, b = all_source_pairs(n)
    field, ys = _reference_encode_adjacent(a, b)
    symbols = [_reference_observe(field, ys)]
    for _ in range(1, COARSE_STATES):
        field = _reference_fine_step(field)
        field = _reference_fine_step(field)
        ys = ys[2:-2]
        symbols.append(_reference_observe(field, ys))
    return ReferenceOrbit(n=n, symbols=symbols)


def compare_orbits(primary, reference: ReferenceOrbit) -> None:
    if primary.n != reference.n or len(primary.symbols) != len(reference.symbols):
        raise AssertionError("primary/reference orbit shape mismatch")
    for t, (a, b) in enumerate(zip(primary.symbols, reference.symbols)):
        if not np.array_equal(a, b):
            raise AssertionError(("primary/reference retained-field mismatch", primary.n, t))


@dataclass(frozen=True)
class Verdict:
    passed: bool
    pair: tuple[int, int] | None


@dataclass(frozen=True)
class Segment:
    n: int
    t: int
    start: int
    stop: int
    local: bool


@dataclass
class PackedArrays:
    limbs: tuple[np.ndarray, ...]
    outputs: np.ndarray
    raw_keys: tuple[np.ndarray, ...]
    raw_outputs: tuple[np.ndarray, ...]
    segments: list[Segment]


def _pack_chunks(chunks: list[np.ndarray], limb_count: int) -> tuple[np.ndarray, ...]:
    """Pack six-bit chunks into fixed uint64 limbs, exact through 192 bits."""
    if not chunks:
        raise AssertionError("no chunks")
    shape = chunks[0].shape
    limbs = [np.zeros(shape, dtype=np.uint64) for _ in range(limb_count)]
    for j, chunk in enumerate(chunks):
        if chunk.shape != shape:
            raise AssertionError("chunk shape mismatch")
        shift = 6 * j
        limb = shift // 64
        offset = shift % 64
        values = chunk.astype(np.uint64)
        if limb >= limb_count:
            raise AssertionError((j, limb_count))
        limbs[limb] |= values << np.uint64(offset)
        if offset > 58:
            if limb + 1 >= limb_count:
                raise AssertionError("cross-limb overflow")
            limbs[limb + 1] |= values >> np.uint64(64 - offset)
    return tuple(limbs)


def _group_verdict_packed(limbs: tuple[np.ndarray, ...], outputs: np.ndarray) -> Verdict:
    n = len(outputs)
    if n == 0:
        return Verdict(True, None)
    idx = np.arange(n, dtype=np.int64)
    order = np.lexsort((idx, *limbs))
    sorted_limbs = [x[order] for x in limbs]
    sorted_outputs = outputs[order]
    change = np.zeros(n - 1, dtype=bool)
    for x in sorted_limbs:
        change |= x[1:] != x[:-1]
    starts = np.concatenate((np.array([0], dtype=np.int64), np.flatnonzero(change).astype(np.int64) + 1))
    stops = np.concatenate((starts[1:], np.array([n], dtype=np.int64)))
    first_outputs = sorted_outputs[starts]
    repeated = np.repeat(first_outputs, stops - starts)
    different = sorted_outputs != repeated
    positions = np.arange(n, dtype=np.int64)
    candidates = np.where(different, positions, n)
    first_diff = np.minimum.reduceat(candidates, starts)
    conflict = first_diff < stops
    if not np.any(conflict):
        return Verdict(True, None)
    a = order[starts[conflict]]
    b = order[first_diff[conflict]]
    pairs = np.column_stack((a, b))
    pick = np.lexsort((pairs[:, 1], pairs[:, 0]))[0]
    return Verdict(False, (int(pairs[pick, 0]), int(pairs[pick, 1])))


def _group_verdict_raw(keys: tuple[np.ndarray, ...], outputs: tuple[np.ndarray, ...]) -> Verdict:
    """Explicit un-packed tuple-column grouping, independent of bit packing."""
    if not keys or not outputs:
        raise AssertionError("raw grouping requires keys and outputs")
    n = len(outputs[0])
    if any(len(x) != n for x in (*keys, *outputs)):
        raise AssertionError("raw grouping length mismatch")
    if n == 0:
        return Verdict(True, None)
    idx = np.arange(n, dtype=np.int64)
    order = np.lexsort((idx, *keys))
    sorted_keys = [x[order] for x in keys]
    change = np.zeros(n - 1, dtype=bool)
    for x in sorted_keys:
        change |= x[1:] != x[:-1]
    starts = np.concatenate((np.array([0], dtype=np.int64), np.flatnonzero(change).astype(np.int64) + 1))
    stops = np.concatenate((starts[1:], np.array([n], dtype=np.int64)))
    different = np.zeros(n, dtype=bool)
    for output in outputs:
        so = output[order]
        first = so[starts]
        different |= so != np.repeat(first, stops - starts)
    positions = np.arange(n, dtype=np.int64)
    candidates = np.where(different, positions, n)
    first_diff = np.minimum.reduceat(candidates, starts)
    conflict = first_diff < stops
    if not np.any(conflict):
        return Verdict(True, None)
    a = order[starts[conflict]]
    b = order[first_diff[conflict]]
    pairs = np.column_stack((a, b))
    pick = np.lexsort((pairs[:, 1], pairs[:, 0]))[0]
    return Verdict(False, (int(pairs[pick, 0]), int(pairs[pick, 1])))


def _masked(orbit, t: int, selected: int) -> np.ndarray:
    return np.bitwise_and(orbit.symbols[t], np.uint8(selected))


def build_w1_arrays(orbit, mask: int) -> PackedArrays:
    selected = field_mask(mask)
    limb_parts = [[], [], []]
    out_parts: list[np.ndarray] = []
    raw_key_parts: list[list[np.ndarray]] = [[] for _ in range(3 * orbit.n)]
    raw_out_parts: list[list[np.ndarray]] = [[] for _ in range(orbit.n)]
    segments: list[Segment] = []
    start = 0
    for t in TIMES:
        chunks = [_masked(orbit, tt, selected)[:, site] for tt in range(t - 2, t + 1) for site in range(orbit.n)]
        limbs = _pack_chunks(chunks, 3)
        nxt = _masked(orbit, t + 1, selected)
        out_limb = _pack_chunks([nxt[:, site] for site in range(orbit.n)], 1)[0]
        for i in range(3):
            limb_parts[i].append(limbs[i])
        out_parts.append(out_limb)
        for j, chunk in enumerate(chunks):
            raw_key_parts[j].append(chunk.copy())
        for site in range(orbit.n):
            raw_out_parts[site].append(nxt[:, site].copy())
        stop = start + nxt.shape[0]
        segments.append(Segment(orbit.n, t, start, stop, False))
        start = stop
    return PackedArrays(
        tuple(np.concatenate(x) for x in limb_parts),
        np.concatenate(out_parts),
        tuple(np.concatenate(x) for x in raw_key_parts),
        tuple(np.concatenate(x) for x in raw_out_parts),
        segments,
    )


def build_w2_arrays(orbit, mask: int) -> PackedArrays:
    selected = field_mask(mask)
    limb_parts = [[], []]
    out_parts: list[np.ndarray] = []
    raw_key_parts: list[list[np.ndarray]] = [[] for _ in range(3 * len(OFFSETS))]
    raw_out_parts: list[np.ndarray] = []
    segments: list[Segment] = []
    start = 0
    for t in TIMES:
        chunks: list[np.ndarray] = []
        for tt in range(t - 2, t + 1):
            state = _masked(orbit, tt, selected)
            for d in OFFSETS:
                chunks.append(np.roll(state, -d, axis=1))
        limbs = _pack_chunks(chunks, 2)
        nxt = _masked(orbit, t + 1, selected).reshape(-1)
        for i in range(2):
            limb_parts[i].append(limbs[i].reshape(-1))
        out_parts.append(nxt)
        for j, chunk in enumerate(chunks):
            raw_key_parts[j].append(chunk.reshape(-1).copy())
        raw_out_parts.append(nxt.copy())
        stop = start + nxt.size
        segments.append(Segment(orbit.n, t, start, stop, True))
        start = stop
    return PackedArrays(
        tuple(np.concatenate(x) for x in limb_parts),
        np.concatenate(out_parts),
        tuple(np.concatenate(x) for x in raw_key_parts),
        (np.concatenate(raw_out_parts),),
        segments,
    )


def decode_record(segments: list[Segment], index: int) -> dict:
    stops = [s.stop for s in segments]
    pos = bisect.bisect_right(stops, index)
    seg = segments[pos]
    local = index - seg.start
    if seg.local:
        source, site = divmod(local, seg.n)
        return {"n": seg.n, "t": seg.t, "source_index": source, "site": site}
    return {"n": seg.n, "t": seg.t, "source_index": local}


def source_pair_lex(n: int, source: int) -> list[str]:
    width = 1 << n
    a, b = divmod(source, width)
    return [format(a, f"0{n}b"), format(b, f"0{n}b")]


def _record_json(record: dict) -> dict:
    out = dict(record)
    out["source_pair_lex"] = source_pair_lex(record["n"], record["source_index"])
    return out


def w1_key_explicit(orbit, record: dict, mask: int) -> tuple[tuple[int, ...], ...]:
    selected = field_mask(mask)
    return tuple(tuple(int(x) & selected for x in orbit.symbols[tt][record["source_index"]]) for tt in range(record["t"] - 2, record["t"] + 1))


def w1_target_explicit(orbit, record: dict, mask: int) -> tuple[int, ...]:
    selected = field_mask(mask)
    return tuple(int(x) & selected for x in orbit.symbols[record["t"] + 1][record["source_index"]])


def w2_key_explicit(orbit, record: dict, mask: int) -> tuple[tuple[int, ...], ...]:
    selected = field_mask(mask)
    source = record["source_index"]
    site = record["site"]
    return tuple(
        tuple(int(orbit.symbols[tt][source, (site + d) % orbit.n]) & selected for d in OFFSETS)
        for tt in range(record["t"] - 2, record["t"] + 1)
    )


def w2_target_explicit(orbit, record: dict, mask: int) -> int:
    selected = field_mask(mask)
    return int(orbit.symbols[record["t"] + 1][record["source_index"], record["site"]]) & selected


def first_differing_coordinate(a: int, b: int, mask: int) -> str:
    selected = field_mask(mask)
    for bit, name in enumerate(COORDINATES):
        if ((selected >> bit) & 1) and (((a >> bit) & 1) != ((b >> bit) & 1)):
            return name
    raise AssertionError("targets differ without a retained differing coordinate")


def w1_entry(orbit, arrays: PackedArrays, mask: int, verdict: Verdict) -> dict:
    if verdict.passed:
        return {"pass": True, "canonical_conflict": None}
    assert verdict.pair is not None
    r1 = decode_record(arrays.segments, verdict.pair[0])
    r2 = decode_record(arrays.segments, verdict.pair[1])
    k1 = w1_key_explicit(orbit, r1, mask)
    k2 = w1_key_explicit(orbit, r2, mask)
    y1 = w1_target_explicit(orbit, r1, mask)
    y2 = w1_target_explicit(orbit, r2, mask)
    if k1 != k2 or y1 == y2:
        raise AssertionError("W1 canonical conflict replay failed")
    site = next(i for i, (a, b) in enumerate(zip(y1, y2)) if a != b)
    return {"pass": False, "canonical_conflict": {"records": [_record_json(r1), _record_json(r2)], "equal_complete_history_oldest_to_newest": [list(x) for x in k1], "next_complete_retained_fields": [list(y1), list(y2)], "first_differing_output": {"site": site, "coordinate": first_differing_coordinate(y1[site], y2[site], mask)}}}


def w2_entry(orbits: dict[int, object], arrays: PackedArrays, mask: int, verdict: Verdict) -> dict:
    if verdict.passed:
        return {"pass": True, "canonical_conflict": None}
    assert verdict.pair is not None
    r1 = decode_record(arrays.segments, verdict.pair[0])
    r2 = decode_record(arrays.segments, verdict.pair[1])
    o1 = orbits[r1["n"]]
    o2 = orbits[r2["n"]]
    k1 = w2_key_explicit(o1, r1, mask)
    k2 = w2_key_explicit(o2, r2, mask)
    y1 = w2_target_explicit(o1, r1, mask)
    y2 = w2_target_explicit(o2, r2, mask)
    if k1 != k2 or y1 == y2:
        raise AssertionError("W2/W3 canonical conflict replay failed")
    return {"pass": False, "canonical_conflict": {"records": [_record_json(r1), _record_json(r2)], "equal_radius_three_history_oldest_to_newest": [list(x) for x in k1], "next_center_retained_symbols": [y1, y2], "first_differing_target_coordinate": first_differing_coordinate(y1, y2, mask)}}


def _verdict_pair(arrays: PackedArrays) -> tuple[Verdict, Verdict]:
    p = _group_verdict_packed(arrays.limbs, arrays.outputs)
    r = _group_verdict_raw(arrays.raw_keys, arrays.raw_outputs)
    if p != r:
        raise AssertionError(("primary/reference verdict mismatch", p, r))
    return p, r


def _rotate_word_right(values: np.ndarray, n: int) -> np.ndarray:
    mask = np.uint64((1 << n) - 1)
    return ((values >> np.uint64(1)) | ((values & np.uint64(1)) << np.uint64(n - 1))) & mask


def check_translation_covariance(orbit) -> None:
    width = 1 << orbit.n
    source = np.arange(width * width, dtype=np.uint64)
    a = source // np.uint64(width)
    b = source % np.uint64(width)
    shifted = (_rotate_word_right(a, orbit.n) * np.uint64(width) + _rotate_word_right(b, orbit.n)).astype(np.int64)
    for t in range(COARSE_STATES):
        expected = np.roll(orbit.symbols[t], 1, axis=1)
        actual = orbit.symbols[t][shifted]
        if not np.array_equal(actual, expected):
            raise AssertionError(("translation covariance failed", orbit.n, t))


def predecessor_controls() -> tuple[dict, dict]:
    history = json.loads(HISTORY_RESULT.read_text())
    global_result = json.loads(GLOBAL_RESULT.read_text())
    for radius in (0, 1, 2):
        for mask in MASKS:
            if history["census"]["D2"]["2"][str(radius)][str(mask)]["pass"]:
                raise AssertionError(("P1 predecessor local verdict unexpectedly passes", radius, mask))
    for n in (6, 7):
        for mask in MASKS:
            if not global_result["census"][str(n)]["D2"]["2"][str(mask)]["pass"]:
                raise AssertionError(("P1 predecessor W1 verdict unexpectedly conflicts", n, mask))
    return history, global_result


def _concat_local(parts: list[PackedArrays]) -> PackedArrays:
    limbs = tuple(np.concatenate([p.limbs[i] for p in parts]) for i in range(2))
    outputs = np.concatenate([p.outputs for p in parts])
    raw_keys = tuple(np.concatenate([p.raw_keys[i] for p in parts]) for i in range(len(parts[0].raw_keys)))
    raw_outputs = tuple(np.concatenate([p.raw_outputs[i] for p in parts]) for i in range(len(parts[0].raw_outputs)))
    segments: list[Segment] = []
    offset = 0
    for p in parts:
        for s in p.segments:
            length = s.stop - s.start
            segments.append(Segment(s.n, s.t, offset, offset + length, True))
            offset += length
    return PackedArrays(limbs, outputs, raw_keys, raw_outputs, segments)


def evaluate(widths: tuple[int, ...] = WIDTHS, masks: tuple[int, ...] = MASKS, *, write_scope: bool = True) -> dict:
    if write_scope:
        predecessor_controls()
    orbits = {}
    reference_orbits = {}
    for n in widths:
        primary = build_ring_orbit(n)
        reference = build_reference_orbit(n)
        compare_orbits(primary, reference)
        orbits[n] = primary
        reference_orbits[n] = reference
        check_translation_covariance(primary)

    census: dict[str, dict] = {str(n): {} for n in widths}
    pooled: dict[str, dict] = {}
    agreement = 0
    replay_count = 0

    for mask in masks:
        local_parts: list[PackedArrays] = []
        for n in widths:
            orbit = orbits[n]
            w1 = build_w1_arrays(orbit, mask)
            v1, _ = _verdict_pair(w1)
            agreement += 1
            e1 = w1_entry(reference_orbits[n], w1, mask, v1)
            if not e1["pass"]:
                replay_count += 1

            w2 = build_w2_arrays(orbit, mask)
            v2, _ = _verdict_pair(w2)
            agreement += 1
            e2 = w2_entry(reference_orbits, w2, mask, v2)
            if not e2["pass"]:
                replay_count += 1
            census[str(n)][str(mask)] = {"W1": e1, "W2_R3": e2}
            local_parts.append(w2)

        w3_arrays = _concat_local(local_parts)
        v3, _ = _verdict_pair(w3_arrays)
        agreement += 1
        e3 = w2_entry(reference_orbits, w3_arrays, mask, v3)
        if not e3["pass"]:
            replay_count += 1
        pooled[str(mask)] = e3

    if write_scope:
        for n in (6, 7):
            for mask in MASKS:
                if not census[str(n)][str(mask)]["W1"]["pass"] or not census[str(n)][str(mask)]["W2_R3"]["pass"]:
                    raise AssertionError(("P1 predecessor width control failed", n, mask))

    p2 = all(census[str(n)][str(mask)]["W1"]["pass"] for n in FRESH_WIDTHS if n in widths for mask in masks)
    p3 = all(census[str(n)]["15"]["W2_R3"]["pass"] for n in FRESH_WIDTHS if n in widths) if 15 in masks else None
    p4 = pooled.get("15", {}).get("pass") if 15 in masks else None

    return {
        "protocol": "interface-history-cross-width-20260912",
        "schema": 1,
        "source_hashes": ({
            "script": sha(pathlib.Path(__file__)),
            "protocol": sha(PROTOCOL),
            "interface_history_protocol": sha(HISTORY_PROTOCOL),
            "interface_history_script": sha(HISTORY_SCRIPT),
            "interface_history_result": sha(HISTORY_RESULT),
            "interface_history_global_protocol": sha(GLOBAL_PROTOCOL),
            "interface_history_global_script": sha(GLOBAL_SCRIPT),
            "interface_history_global_result": sha(GLOBAL_RESULT),
            "interface_factor_script": sha(FACTOR_SCRIPT),
        } if write_scope else {}),
        "parameters": {"widths": list(widths), "fresh_widths": [n for n in FRESH_WIDTHS if n in widths], "masks": list(masks), "history_depth": HISTORY_DEPTH, "domain": "D2", "times": list(TIMES), "radius": RADIUS, "offsets": list(OFFSETS), "W3_key_includes_width": False},
        "controls": {"P1_predecessor_regression": bool(write_scope), "P6_translation_covariance": True, "P6_primary_reference_retained_fields": True, "P6_primary_reference_agreement_verdicts": agreement, "canonical_conflicts_independently_replayed": replay_count},
        "census": census,
        "W3_pooled": pooled,
        "predictions": {"P2_common_masks_W1_fresh_widths": p2, "P3_P15_W2_R3_fresh_widths": p3, "P4_P15_W3_pooled_widths": p4},
        "scope": "finite widths 6-9; fresh exhaustive widths 8,9; frozen touching-strip reachable family; D2,h=2; masks 11,13,15; R=3 only; near-whole-ring finite-family test; no arbitrary-width/full-shift/infinite-lattice or intrinsic-dimension claim",
    }


def self_test() -> None:
    result = evaluate((3, 4), (15,), write_scope=False)
    assert result["controls"]["P6_translation_covariance"]
    assert result["controls"]["P6_primary_reference_agreement_verdicts"] == 5
    if OUT.exists():
        raise AssertionError("implementation-only self-test found canonical result")
    print("interface-history-cross-width implementation self-test passed (out-of-domain widths 3,4; no canonical result written)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = evaluate()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["predictions"], sort_keys=True))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
