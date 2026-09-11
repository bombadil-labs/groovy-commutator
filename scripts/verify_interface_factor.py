#!/usr/bin/env python3
"""Verifier for the frozen touching-strip interface-factor protocol.

Protocol: docs/research/protocols/interface-factor-20260911.md
Authorization: Myk authorized execution on 2026-09-11 under the recorded
temporary retrospective-review exception while Claude/Fable is unavailable.

This file is the implementation-only stage.  Committing it does not execute
the frozen primary/stress censuses and does not create a canonical result.
Running without --self-test performs the complete frozen evaluation and writes
results/interface_factor_20260911.json.  --self-test is a non-scientific
implementation check on an out-of-domain three-site ring and writes nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from dataclasses import dataclass

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/interface-factor-20260911.md"
OUT = ROOT / "results/interface_factor_20260911.json"

RINGS = (6, 7)
RADII = (0, 1, 2)
MASKS = tuple(range(16))
PRIMARY_TIMES = (0, 1, 2, 3)
STRESS_TIMES = (0, 1, 2, 3, 4, 5, 6)
COARSE_STATES = 8
COORDINATES = ("A", "B", "E0", "E1", "E2", "E3")


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def step2(grid: np.ndarray, shrink: bool = False) -> np.ndarray:
    """Exact fixed Research-012 2D selector law; final axes are y,x."""
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
    return np.take_along_axis(flat, index, axis=-1).reshape(c.shape).astype(np.uint8)


def fine_step_ring(field: np.ndarray) -> np.ndarray:
    """One fine tick: periodic horizontal ring, shrinking exact vertical cone."""
    padded = np.pad(field, [(0, 0)] * (field.ndim - 1) + [(1, 1)], mode="wrap")
    return step2(padded, shrink=True)


def row_bits(value: int, n: int) -> np.ndarray:
    """Big-endian bitstring order, so integer order equals lexicographic order."""
    shifts = np.arange(n - 1, -1, -1, dtype=np.uint64)
    return ((np.uint64(value) >> shifts) & np.uint64(1)).astype(np.uint8)


def all_source_pairs(n: int) -> tuple[np.ndarray, np.ndarray]:
    values = np.arange(1 << n, dtype=np.uint64)
    shifts = np.arange(n - 1, -1, -1, dtype=np.uint64)
    rows = ((values[:, None] >> shifts) & np.uint64(1)).astype(np.uint8)
    a = np.repeat(rows, 1 << n, axis=0)
    b = np.tile(rows, (1 << n, 1))
    return a, b


def encode_adjacent(a: np.ndarray, b: np.ndarray, ys: np.ndarray, xs: np.ndarray) -> np.ndarray:
    """Vectorized V_0(a,b) in alternating background on a physical x-ring."""
    a = np.asarray(a, dtype=np.uint8)
    b = np.asarray(b, dtype=np.uint8)
    if a.shape != b.shape or a.ndim != 2:
        raise AssertionError("a and b must have shape (sources, logical_width)")
    sources, n = a.shape
    if len(xs) != 2 * n:
        raise AssertionError("physical ring must have width 2*n")
    background = (xs % 2).astype(np.uint8)
    out = np.broadcast_to(background, (sources, len(ys), len(xs))).copy()
    y_index = {int(y): j for j, y in enumerate(ys)}
    for y in (0, 1, 2, 3):
        if y not in y_index:
            raise AssertionError("vertical window omits the four interface rows")
    even = np.flatnonzero((xs % 2) == 0)
    odd = np.flatnonzero((xs % 2) == 1)
    blocks_even = (xs[even] // 2) % n
    blocks_odd = (xs[odd] // 2) % n
    out[:, y_index[0], odd] = 1 ^ a[:, blocks_odd]
    out[:, y_index[1], even] = a[:, blocks_even]
    out[:, y_index[2], odd] = 1 ^ b[:, blocks_odd]
    out[:, y_index[3], even] = b[:, blocks_even]
    return out


def observe_symbols(field: np.ndarray, ys: np.ndarray, *, assert_roundtrip: bool = True) -> np.ndarray:
    """Return (A,B,E0,E1,E2,E3) packed as six fixed-position bits."""
    y_index = {int(y): j for j, y in enumerate(ys)}
    for y in (0, 1, 2, 3):
        if y not in y_index:
            raise AssertionError("observation rows not present")
    u0 = field[:, y_index[0], 1::2]
    u1 = field[:, y_index[1], 0::2]
    u2 = field[:, y_index[1], 1::2]
    u3 = field[:, y_index[2], 0::2]
    u4 = field[:, y_index[2], 1::2]
    u5 = field[:, y_index[3], 0::2]
    A = u1
    B = u5
    E0 = u0 ^ 1 ^ A
    E1 = u2 ^ 1
    E2 = u3
    E3 = u4 ^ 1 ^ B
    symbol = (A | (B << 1) | (E0 << 2) | (E1 << 3) | (E2 << 4) | (E3 << 5)).astype(np.uint8)
    if assert_roundtrip:
        recovered = (E0 ^ 1 ^ A, A, E1 ^ 1, E2, E3 ^ 1 ^ B, B)
        for raw, check in zip((u0, u1, u2, u3, u4, u5), recovered):
            if not np.array_equal(raw, check):
                raise AssertionError("J1 coordinate map is not invertible")
    return symbol


def exterior_changed(field: np.ndarray, ys: np.ndarray, xs: np.ndarray) -> np.ndarray:
    """Per-source exterior-row departure from even-coarse-time background."""
    exterior_rows = np.flatnonzero((ys < 0) | (ys > 3))
    if len(exterior_rows) == 0:
        return np.zeros(field.shape[0], dtype=bool)
    background = (xs % 2).astype(np.uint8)
    return np.any(field[:, exterior_rows, :] != background[None, None, :], axis=(1, 2))


@dataclass
class RingOrbit:
    n: int
    symbols: list[np.ndarray]
    j2_t1_any_exterior: bool
    j2_t2_first_source: int | None


def build_ring_orbit(n: int) -> RingOrbit:
    """Exhaust every source pair and retain only symbolic coarse states."""
    a, b = all_source_pairs(n)
    xs = np.arange(2 * n, dtype=int)
    margin = 2 * (COARSE_STATES - 1)
    ys = np.arange(-margin, 4 + margin, dtype=int)
    field = encode_adjacent(a, b, ys, xs)
    symbols = [observe_symbols(field, ys)]
    if np.any(symbols[0] & np.uint8(0b111100)):
        raise AssertionError("J1 initial interface coordinates are not all zero")
    t1_any = False
    t2_first: int | None = None
    current_ys = ys
    for coarse in range(1, COARSE_STATES):
        field = fine_step_ring(field)
        field = fine_step_ring(field)
        current_ys = current_ys[2:-2]
        symbols.append(observe_symbols(field, current_ys))
        if coarse == 1:
            t1_any = bool(np.any(exterior_changed(field, current_ys, xs)))
        elif coarse == 2:
            changed = np.flatnonzero(exterior_changed(field, current_ys, xs))
            t2_first = int(changed[0]) if len(changed) else None
    return RingOrbit(n=n, symbols=symbols, j2_t1_any_exterior=t1_any, j2_t2_first_source=t2_first)


def local_key(symbols: np.ndarray, radius: int) -> np.ndarray:
    """Pack full six-bit symbols at offsets -R..+R into one uint64 key."""
    key = np.zeros(symbols.shape, dtype=np.uint64)
    for j, d in enumerate(range(-radius, radius + 1)):
        key |= np.roll(symbols, -d, axis=1).astype(np.uint64) << np.uint64(6 * j)
    return key


@dataclass
class RecordArrays:
    keys: np.ndarray
    outputs: np.ndarray
    t: np.ndarray
    n: np.ndarray
    source: np.ndarray
    site: np.ndarray
    primary_len: int


def build_records(orbits: dict[int, RingOrbit], radius: int) -> RecordArrays:
    """Canonical record order: t, n, source_pair_lex, logical_site."""
    keys_parts: list[np.ndarray] = []
    out_parts: list[np.ndarray] = []
    t_parts: list[np.ndarray] = []
    n_parts: list[np.ndarray] = []
    source_parts: list[np.ndarray] = []
    site_parts: list[np.ndarray] = []
    primary_len = 0
    for t in STRESS_TIMES:
        for n in RINGS:
            current = orbits[n].symbols[t]
            nxt = orbits[n].symbols[t + 1]
            sources = current.shape[0]
            keys = local_key(current, radius).reshape(-1)
            outputs = nxt.reshape(-1).astype(np.uint8)
            keys_parts.append(keys)
            out_parts.append(outputs)
            t_parts.append(np.full(keys.size, t, dtype=np.uint8))
            n_parts.append(np.full(keys.size, n, dtype=np.uint8))
            source_parts.append(np.repeat(np.arange(sources, dtype=np.uint32), n))
            site_parts.append(np.tile(np.arange(n, dtype=np.uint8), sources))
        if t in PRIMARY_TIMES:
            primary_len = sum(len(x) for x in keys_parts)
    return RecordArrays(
        keys=np.concatenate(keys_parts), outputs=np.concatenate(out_parts),
        t=np.concatenate(t_parts), n=np.concatenate(n_parts),
        source=np.concatenate(source_parts), site=np.concatenate(site_parts),
        primary_len=primary_len,
    )


def field_mask(mask: int) -> int:
    return 0b11 | (mask << 2)


def expanded_neighborhood_mask(mask: int, radius: int) -> np.uint64:
    selected = field_mask(mask)
    result = 0
    for j in range(2 * radius + 1):
        result |= selected << (6 * j)
    return np.uint64(result)


@dataclass
class FactorVerdict:
    passed: bool
    canonical_pair: tuple[int, int] | None
    neighborhood_key: int | None
    next_symbols: tuple[int, int] | None


def factor_verdict(full_keys: np.ndarray, full_outputs: np.ndarray, *, mask: int, radius: int) -> FactorVerdict:
    """Single-valuedness plus the protocol's canonical conflict pair."""
    selected = np.uint8(field_mask(mask))
    keys = full_keys & expanded_neighborhood_mask(mask, radius)
    outputs = full_outputs & selected
    order = np.argsort(keys, kind="stable")
    sorted_keys = keys[order]
    sorted_outputs = outputs[order]
    if len(order) == 0:
        return FactorVerdict(True, None, None, None)
    new_group = np.empty(len(order), dtype=bool)
    new_group[0] = True
    new_group[1:] = sorted_keys[1:] != sorted_keys[:-1]
    starts = np.flatnonzero(new_group)
    group_id = np.cumsum(new_group, dtype=np.int64) - 1
    first_outputs = sorted_outputs[starts]
    differs = sorted_outputs != first_outputs[group_id]
    diff_pos = np.flatnonzero(differs)
    if len(diff_pos) == 0:
        return FactorVerdict(True, None, None, None)
    diff_groups = group_id[diff_pos]
    first_for_group = np.r_[True, diff_groups[1:] != diff_groups[:-1]]
    first_diff_pos = diff_pos[first_for_group]
    conflict_group_ids = group_id[first_diff_pos]
    first_pos = starts[conflict_group_ids]
    first_record = order[first_pos]
    second_record = order[first_diff_pos]
    chosen = int(np.argmin(first_record))
    p1 = int(first_record[chosen])
    p2 = int(second_record[chosen])
    return FactorVerdict(False, (p1, p2), int(keys[p1]), (int(outputs[p1]), int(outputs[p2])))


def record_json(records: RecordArrays, position: int) -> dict:
    n = int(records.n[position])
    source = int(records.source[position])
    width = 1 << n
    a_int, b_int = divmod(source, width)
    return {
        "t": int(records.t[position]), "n": n,
        "source_pair_lex": [format(a_int, f"0{n}b"), format(b_int, f"0{n}b")],
        "source_index": source, "logical_site": int(records.site[position]),
    }


def factor_entry(records: RecordArrays, verdict: FactorVerdict) -> dict:
    entry = {"pass": verdict.passed}
    if verdict.canonical_pair is None:
        entry["canonical_conflict"] = None
        return entry
    p1, p2 = verdict.canonical_pair
    entry["canonical_conflict"] = {
        "local_neighborhood_key": verdict.neighborhood_key,
        "next_center_symbols": list(verdict.next_symbols or ()),
        "records": [record_json(records, p1), record_json(records, p2)],
    }
    return entry


def horizon_census(entries: dict[int, dict[int, dict]]) -> dict:
    passing_masks: dict[int, int] = {}
    for mask in MASKS:
        passing = [r for r in RADII if entries[mask][r]["pass"]]
        if passing:
            passing_masks[mask] = min(passing)
    if passing_masks:
        min_bits = min(mask.bit_count() for mask in passing_masks)
        inclusion_minimal = [
            mask for mask in passing_masks
            if not any(other != mask and (other & mask) == other and other in passing_masks for other in passing_masks)
        ]
    else:
        min_bits = None
        inclusion_minimal = []
    return {
        "minimum_retained_interface_bit_count": min_bits,
        "inclusion_minimal_passing_masks": inclusion_minimal,
        "minimum_passing_radius_by_mask": {str(mask): radius for mask, radius in sorted(passing_masks.items())},
    }


def factor_table(keys: np.ndarray, outputs: np.ndarray) -> dict[int, int]:
    order = np.argsort(keys, kind="stable")
    sk = keys[order]
    so = outputs[order]
    table: dict[int, int] = {}
    if len(order) == 0:
        return table
    starts = np.r_[0, np.flatnonzero(sk[1:] != sk[:-1]) + 1]
    ends = np.r_[starts[1:], len(sk)]
    for start, end in zip(starts, ends):
        values = so[start:end]
        if np.any(values != values[0]):
            raise AssertionError("essential-dependency audit requested on conflicting factor")
        table[int(sk[start])] = int(values[0])
    return table


def essential_dependencies(table: dict[int, int], radius: int) -> dict:
    edges: set[tuple[int, str, str]] = set()
    bits = 6 * (2 * radius + 1)
    for key, output in table.items():
        for bit in range(bits):
            other_key = key ^ (1 << bit)
            if other_key not in table or other_key < key:
                continue
            changed_outputs = output ^ table[other_key]
            if not changed_outputs:
                continue
            chunk, coord_index = divmod(bit, 6)
            offset = chunk - radius
            input_coord = COORDINATES[coord_index]
            for out_index, output_coord in enumerate(COORDINATES):
                if (changed_outputs >> out_index) & 1:
                    edges.add((offset, input_coord, output_coord))
    def transverse(inp: str, out: str) -> bool:
        inp_interface = inp.startswith("E")
        out_interface = out.startswith("E")
        return inp_interface != out_interface or (out == "A" and inp == "B") or (out == "B" and inp == "A")
    rows = [
        {"offset": offset, "input_coordinate": inp, "output_coordinate": out,
         "transverse_interface_edge": transverse(inp, out)}
        for offset, inp, out in sorted(edges, key=lambda x: (x[0], COORDINATES.index(x[1]), COORDINATES.index(x[2])))
    ]
    return {"edges": rows, "has_transverse_interface_edge": any(row["transverse_interface_edge"] for row in rows)}


def scalar_encode_adjacent(a_int: int, b_int: int, n: int, ys: np.ndarray) -> np.ndarray:
    xs = np.arange(2 * n, dtype=int)
    field = np.tile((xs % 2).astype(np.uint8), (len(ys), 1))
    y_index = {int(y): j for j, y in enumerate(ys)}
    a = row_bits(a_int, n)
    b = row_bits(b_int, n)
    for i in range(n):
        field[y_index[0], 2 * i + 1] = 1 ^ int(a[i])
        field[y_index[1], 2 * i] = int(a[i])
        field[y_index[2], 2 * i + 1] = 1 ^ int(b[i])
        field[y_index[3], 2 * i] = int(b[i])
    return field


def scalar_fine_step_ring(field: np.ndarray) -> np.ndarray:
    """Independent scalar coordinate implementation of one fine tick."""
    h, w = field.shape
    out = np.empty((h - 2, w), dtype=np.uint8)
    for y in range(1, h - 1):
        for x in range(w):
            center = int(field[y, x])
            left = int(field[y, (x - 1) % w])
            right = int(field[y, (x + 1) % w])
            source_y = y + 2 * center - 1
            source_x = (x + left + right - 1) % w
            out[y - 1, x] = field[source_y, source_x]
    return out


def replay_source(n: int, source: int, max_coarse: int) -> tuple[list[np.ndarray], list[np.ndarray]]:
    width = 1 << n
    a_int, b_int = divmod(source, width)
    margin = 2 * max_coarse
    ys = np.arange(-margin, 4 + margin, dtype=int)
    scalar = scalar_encode_adjacent(a_int, b_int, n, ys)
    a = row_bits(a_int, n)[None, :]
    b = row_bits(b_int, n)[None, :]
    vector = encode_adjacent(a, b, ys, np.arange(2 * n, dtype=int))[0]
    scalar_states = [scalar.copy()]
    ys_states = [ys.copy()]
    if not np.array_equal(scalar, vector):
        raise AssertionError("independent initial encoders disagree")
    current_ys = ys
    for _ in range(max_coarse):
        scalar = scalar_fine_step_ring(scalar)
        scalar = scalar_fine_step_ring(scalar)
        vector = fine_step_ring(vector[None, ...])[0]
        vector = fine_step_ring(vector[None, ...])[0]
        current_ys = current_ys[2:-2]
        if not np.array_equal(scalar, vector):
            raise AssertionError("J8 scalar/vector physical replay mismatch")
        scalar_states.append(scalar.copy())
        ys_states.append(current_ys.copy())
    return scalar_states, ys_states


def causal_patch(field: np.ndarray, ys: np.ndarray, site: int, n: int) -> np.ndarray:
    """Two-fine-tick light-cone rectangle for the six observed center cells."""
    y_index = {int(y): j for j, y in enumerate(ys)}
    patch = np.empty((8, 6), dtype=np.uint8)
    center_x = 2 * site
    width = 2 * n
    for ry, y in enumerate(range(-2, 6)):
        if y not in y_index:
            raise AssertionError("replay window does not contain conflict causal patch")
        for rx, dx in enumerate(range(-2, 4)):
            patch[ry, rx] = field[y_index[y], (center_x + dx) % width]
    return patch


def hidden_cause_replay(conflict: dict) -> dict:
    r1, r2 = conflict["records"]
    states1, ys1 = replay_source(r1["n"], r1["source_index"], r1["t"] + 1)
    states2, ys2 = replay_source(r2["n"], r2["source_index"], r2["t"] + 1)
    patch1 = causal_patch(states1[r1["t"]], ys1[r1["t"]], r1["logical_site"], r1["n"])
    patch2 = causal_patch(states2[r2["t"]], ys2[r2["t"]], r2["logical_site"], r2["n"])
    differences = []
    for iy, y in enumerate(range(-2, 6)):
        for ix, dx in enumerate(range(-2, 4)):
            if y in (0, 1, 2, 3):
                continue
            if int(patch1[iy, ix]) != int(patch2[iy, ix]):
                differences.append({"relative_y": y, "relative_x": dx,
                                    "first": int(patch1[iy, ix]), "second": int(patch2[iy, ix])})
    return {
        "causal_patch_rows": [-2, 5], "causal_patch_relative_x": [-2, 3],
        "differs_outside_rows_0_3": bool(differences), "exterior_differences": differences,
        "scalar_replay_matches_vectorized": True,
    }


def scalar_j2_t1_exhaustive(n: int) -> bool:
    """Independent scalar replay of J2's universal t=1 no-exterior control."""
    margin = 4
    initial_ys = np.arange(-margin, 4 + margin, dtype=int)
    after_ys = initial_ys[2:-2]
    exterior_rows = np.flatnonzero((after_ys < 0) | (after_ys > 3))
    background = (np.arange(2 * n, dtype=int) % 2).astype(np.uint8)
    for source in range(1 << (2 * n)):
        width = 1 << n
        a_int, b_int = divmod(source, width)
        field = scalar_encode_adjacent(a_int, b_int, n, initial_ys)
        field = scalar_fine_step_ring(field)
        field = scalar_fine_step_ring(field)
        if len(exterior_rows) and np.any(field[exterior_rows, :] != background[None, :]):
            return False
    return True


def j8_controls(orbits: dict[int, RingOrbit], full_conflicts: list[tuple[str, int, dict]]) -> dict:
    passing_source_replays = []
    for n in RINGS:
        states, _ = replay_source(n, 0, 7)
        passing_source_replays.append({
            "n": n, "source_pair_lex": [format(0, f"0{n}b"), format(0, f"0{n}b")],
            "coarse_states_checked": list(range(len(states))), "scalar_replay_matches_vectorized": True,
        })
    j2_witnesses = []
    j2_t1_scalar = {}
    for n in RINGS:
        j2_t1_scalar[str(n)] = scalar_j2_t1_exhaustive(n)
        source = orbits[n].j2_t2_first_source
        if source is not None:
            replay_source(n, source, 2)
            j2_witnesses.append({"n": n, "first_t2_exterior_source_index": source,
                                 "scalar_replay_matches_vectorized": True})
    if not all(j2_t1_scalar.values()):
        raise AssertionError("J8 independent scalar replay disagrees with J2 t=1 control")
    conflict_replays = []
    for horizon, radius, conflict in full_conflicts:
        conflict_replays.append({"horizon": horizon, "radius": radius,
                                 "conflict_records": conflict["records"], **hidden_cause_replay(conflict)})
    return {
        "deterministic_source_replays": passing_source_replays,
        "j2_t1_no_exterior_exhaustive_scalar_by_ring": j2_t1_scalar,
        "j2_t2_exterior_witness_replays": j2_witnesses,
        "p15_conflict_replays": conflict_replays,
        "all_scalar_replays_match_vectorized": True,
    }


def evaluate() -> dict:
    orbits = {n: build_ring_orbit(n) for n in RINGS}
    j2 = {
        "t1_no_exterior_change_for_every_source": not any(o.j2_t1_any_exterior for o in orbits.values()),
        "t2_exterior_change_exists": any(o.j2_t2_first_source is not None for o in orbits.values()),
        "first_t2_exterior_source_by_ring": {str(n): orbits[n].j2_t2_first_source for n in RINGS},
    }
    if not j2["t1_no_exterior_change_for_every_source"]:
        raise AssertionError("J2 first-step physical control failed")
    if not j2["t2_exterior_change_exists"]:
        raise AssertionError("J2 expected reachable exterior change at t=2 was not found")
    primary_entries: dict[int, dict[int, dict]] = {m: {} for m in MASKS}
    stress_entries: dict[int, dict[int, dict]] = {m: {} for m in MASKS}
    full_conflicts: list[tuple[str, int, dict]] = []
    p15_pass: dict[str, list[int]] = {"primary": [], "stress": []}
    records_by_radius: dict[int, RecordArrays] = {}
    for radius in RADII:
        records = build_records(orbits, radius)
        records_by_radius[radius] = records
        for mask in MASKS:
            primary_verdict = factor_verdict(records.keys[:records.primary_len], records.outputs[:records.primary_len], mask=mask, radius=radius)
            stress_verdict = factor_verdict(records.keys, records.outputs, mask=mask, radius=radius)
            primary_entries[mask][radius] = factor_entry(records, primary_verdict)
            stress_entries[mask][radius] = factor_entry(records, stress_verdict)
            if mask == 15:
                if primary_verdict.passed:
                    p15_pass["primary"].append(radius)
                else:
                    full_conflicts.append(("primary", radius, primary_entries[mask][radius]["canonical_conflict"]))
                if stress_verdict.passed:
                    p15_pass["stress"].append(radius)
                else:
                    full_conflicts.append(("stress", radius, stress_entries[mask][radius]["canonical_conflict"]))
    dependencies: dict[str, dict | None] = {}
    for horizon in ("primary", "stress"):
        passing = p15_pass[horizon]
        if not passing:
            dependencies[horizon] = None
            continue
        radius = min(passing)
        records = records_by_radius[radius]
        length = records.primary_len if horizon == "primary" else len(records.keys)
        table = factor_table(records.keys[:length], records.outputs[:length])
        dependencies[horizon] = {"minimum_passing_radius": radius, "reachable_local_words": len(table),
                                 **essential_dependencies(table, radius)}
    return {
        "protocol": "interface-factor-20260911", "schema": 1,
        "parameters": {
            "rings": list(RINGS), "source_pairs_by_ring": {str(n): 1 << (2 * n) for n in RINGS},
            "scored_transition_times_primary": list(PRIMARY_TIMES), "scored_transition_times_stress": list(STRESS_TIMES),
            "interface_masks": list(MASKS), "longitudinal_radii": list(RADII),
            "symbol_bit_order": list(COORDINATES),
            "canonical_record_order": ["t", "n", "source_pair_lex", "logical_site"],
        },
        "source_hashes": {"script": sha(pathlib.Path(__file__)), "protocol": sha(PROTOCOL)},
        "controls": {
            "J1_coordinate_bijection_all_recorded_symbols": True,
            "J1_initial_interface_bits_all_zero": True, "J2": j2,
            "J8": j8_controls(orbits, full_conflicts),
        },
        "factor_census": {
            "primary": {"entries": {str(m): {str(r): primary_entries[m][r] for r in RADII} for m in MASKS},
                        "summary": horizon_census(primary_entries)},
            "stress": {"entries": {str(m): {str(r): stress_entries[m][r] for r in RADII} for m in MASKS},
                       "summary": horizon_census(stress_entries)},
        },
        "P15": {
            "primary_prediction_J3_passes_some_R_le_2": bool(p15_pass["primary"]),
            "primary_passing_radii": p15_pass["primary"], "stress_passing_radii": p15_pass["stress"],
            "essential_dependency_audits": dependencies,
        },
        "interpretation_scope": {
            "primary": "exhaustive declared adjacent-strip reachable domain through coarse transition 3 only",
            "stress": "same declared family through coarse transition 6 only",
            "nonclaims": ["no arbitrary-width causal grid", "no recursive 2D-to-3D lift", "no all-time closure conclusion",
                          "no claim of natural/minimal/unique state outside the frozen mask census"],
        },
    }


def self_test() -> None:
    """Out-of-domain implementation check; no frozen scientific verdict is scored."""
    n = 3
    a_int, b_int = 0b101, 0b011
    ys = np.arange(-4, 8, dtype=int)
    scalar = scalar_encode_adjacent(a_int, b_int, n, ys)
    a = row_bits(a_int, n)[None, :]
    b = row_bits(b_int, n)[None, :]
    vector = encode_adjacent(a, b, ys, np.arange(2 * n, dtype=int))[0]
    assert np.array_equal(scalar, vector)
    initial_symbol = observe_symbols(vector[None, ...], ys)
    assert np.all((initial_symbol & np.uint8(0b111100)) == 0)
    for _ in range(2):
        scalar = scalar_fine_step_ring(scalar)
        vector = fine_step_ring(vector[None, ...])[0]
        ys = ys[1:-1]
        assert np.array_equal(scalar, vector)
    observe_symbols(vector[None, ...], ys)
    print("implementation self-test passed (out-of-domain n=3; no canonical result written)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true",
                        help="run non-scientific implementation checks only; do not execute frozen census")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = evaluate()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"J3": result["P15"]["primary_prediction_J3_passes_some_R_le_2"],
                      "primary_passing_radii": result["P15"]["primary_passing_radii"],
                      "stress_passing_radii": result["P15"]["stress_passing_radii"]}, sort_keys=True))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
