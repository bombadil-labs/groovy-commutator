#!/usr/bin/env python3
"""Frozen interface-factor audit for touching Rule90 strips.

Protocol: docs/research/protocols/interface-factor-20260911.md
Protocol integrated before this implementation.  Myk authorized execution without
cross-model Gate 1 on 2026-09-11 while Claude/Fable is unavailable; retrospective
review remains owed.

The complete census uses a vectorized implementation of the fixed 2D selector law
with vertical causal-window shrinking and horizontal periodic wrapping.  It does
not import Research018/019 saved result tables.  A separate scalar implementation
replays the scored controls and every canonical full-state conflict witness.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name == "scripts" else Path(__file__).resolve().parent
PROTOCOL_REL = "docs/research/protocols/interface-factor-20260911.md"
PROTOCOL = ROOT / PROTOCOL_REL
OUT = ROOT / "results/interface_factor_20260911.json"
RINGS = (6, 7)
COARSE_TRANSITIONS = tuple(range(7))
PRIMARY_TIMES = tuple(range(4))
STRESS_TIMES = COARSE_TRANSITIONS
RADII = (0, 1, 2)
MASKS = tuple(range(16))
Y0_MIN = -16
Y0_MAX = 19
BATCH = 1024
COORD_NAMES = ("A", "B", "E0", "E1", "E2", "E3")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_bits(ids: np.ndarray, n: int) -> np.ndarray:
    shifts = (n - 1 - np.arange(n, dtype=np.uint64))[None, :]
    return ((ids.astype(np.uint64)[:, None] >> shifts) & 1).astype(np.uint8)


def encode_batch(source_ids: np.ndarray, n: int) -> tuple[np.ndarray, int]:
    """Adjacent two-strip source on alternating background, periodic in x."""
    size = 1 << n
    a_ids = source_ids // size
    b_ids = source_ids % size
    a = source_bits(a_ids, n)
    b = source_bits(b_ids, n)
    width = 2 * n
    ys = np.arange(Y0_MIN, Y0_MAX + 1)
    background = (np.arange(width, dtype=np.uint8) & 1)[None, None, :]
    field = np.broadcast_to(background, (len(source_ids), len(ys), width)).copy()
    row = {y: int(y - Y0_MIN) for y in range(4)}
    field[:, row[0], 1::2] = 1 ^ a
    field[:, row[1], 0::2] = a
    field[:, row[2], 1::2] = 1 ^ b
    field[:, row[3], 0::2] = b
    return field, Y0_MIN


def step_vector(field: np.ndarray) -> np.ndarray:
    """One fine selector step: shrink only y, wrap x periodically."""
    batch, height, width = field.shape
    c = field[:, 1:-1, :].astype(np.int64)
    pop = np.roll(field[:, 1:-1, :], 1, axis=-1) + np.roll(field[:, 1:-1, :], -1, axis=-1)
    yy = np.arange(1, height - 1, dtype=np.int64)[None, :, None]
    xx = np.arange(width, dtype=np.int64)[None, None, :]
    yi = yy + 2 * c - 1
    xi = (xx + pop.astype(np.int64) - 1) % width
    bb = np.arange(batch, dtype=np.int64)[:, None, None]
    return field[bb, yi, xi]


def step_scalar(field: np.ndarray) -> np.ndarray:
    """Independent scalar one-fine-step implementation, shrink y / wrap x."""
    height, width = field.shape
    out = np.empty((height - 2, width), dtype=np.uint8)
    for oy in range(height - 2):
        y = oy + 1
        for x in range(width):
            c = int(field[y, x])
            pop = int(field[y, (x - 1) % width]) + int(field[y, (x + 1) % width])
            out[oy, x] = field[y + 2 * c - 1, (x + pop - 1) % width]
    return out


def raw_symbols(field: np.ndarray, y_min: int, n: int) -> np.ndarray:
    """Pack the six Research019 W cells as raw bits u0..u5 at each logical block."""
    rows = [y - y_min for y in range(4)]
    assert min(rows) >= 0 and max(rows) < field.shape[-2]
    u0 = field[:, rows[0], 1::2]
    u1 = field[:, rows[1], 0::2]
    u2 = field[:, rows[1], 1::2]
    u3 = field[:, rows[2], 0::2]
    u4 = field[:, rows[2], 1::2]
    u5 = field[:, rows[3], 0::2]
    return (u0 | (u1 << 1) | (u2 << 2) | (u3 << 3) | (u4 << 4) | (u5 << 5)).astype(np.uint8)


def typed_symbols_from_raw(raw: np.ndarray) -> np.ndarray:
    u0 = raw & 1
    u1 = (raw >> 1) & 1
    u2 = (raw >> 2) & 1
    u3 = (raw >> 3) & 1
    u4 = (raw >> 4) & 1
    u5 = (raw >> 5) & 1
    A = u1
    B = u5
    E0 = u0 ^ 1 ^ A
    E1 = u2 ^ 1
    E2 = u3
    E3 = u4 ^ 1 ^ B
    return (A | (B << 1) | (E0 << 2) | (E1 << 3) | (E2 << 4) | (E3 << 5)).astype(np.uint8)


def raw_from_typed(typed: np.ndarray) -> np.ndarray:
    A = typed & 1
    B = (typed >> 1) & 1
    E0 = (typed >> 2) & 1
    E1 = (typed >> 3) & 1
    E2 = (typed >> 4) & 1
    E3 = (typed >> 5) & 1
    u0 = E0 ^ 1 ^ A
    u1 = A
    u2 = E1 ^ 1
    u3 = E2
    u4 = E3 ^ 1 ^ B
    u5 = B
    return (u0 | (u1 << 1) | (u2 << 2) | (u3 << 3) | (u4 << 4) | (u5 << 5)).astype(np.uint8)


def background_rows(field: np.ndarray) -> np.ndarray:
    width = field.shape[-1]
    return np.broadcast_to((np.arange(width, dtype=np.uint8) & 1)[None, :], field.shape[-2:])


def outside_changed(field: np.ndarray, y_min: int) -> np.ndarray:
    """Per batch: any difference from coarse-phase background outside rows 0..3."""
    bg = background_rows(field)
    ys = np.arange(y_min, y_min + field.shape[-2])
    mask = (ys < 0) | (ys > 3)
    if not mask.any():
        return np.zeros(field.shape[0], dtype=bool)
    return (field[:, mask, :] != bg[mask][None, :, :]).any(axis=(1, 2))


def w_band_invalid(field: np.ndarray, y_min: int) -> np.ndarray:
    """Research019 W validity: background outside, row0/even=0, row3/odd=1."""
    bad = outside_changed(field, y_min)
    r0 = 0 - y_min; r3 = 3 - y_min
    bad = bad | (field[:, r0, 0::2] != 0).any(axis=1)
    bad = bad | (field[:, r3, 1::2] != 1).any(axis=1)
    return bad


def select_symbols(typed: np.ndarray, mask: int) -> tuple[np.ndarray, tuple[int, ...]]:
    coords = [0, 1] + [2 + j for j in range(4) if (mask >> j) & 1]
    out = np.zeros_like(typed, dtype=np.uint8)
    for dst, src in enumerate(coords):
        out |= (((typed >> src) & 1) << dst).astype(np.uint8)
    return out, tuple(coords)


def neighborhood_keys(symbols: np.ndarray, radius: int, symbol_bits: int) -> np.ndarray:
    key = np.zeros_like(symbols, dtype=np.uint64)
    for d in range(-radius, radius + 1):
        key = (key << symbol_bits) | np.roll(symbols, -d, axis=1).astype(np.uint64)
    return key


def source_pair_record(source: int, n: int) -> dict:
    size = 1 << n
    a, b = divmod(source, size)
    return {
        "source_index": int(source),
        "a": int(a),
        "b": int(b),
        "a_bits": format(a, f"0{n}b"),
        "b_bits": format(b, f"0{n}b"),
    }


def build_records(obs: dict[int, list[np.ndarray]], times: Iterable[int], mask: int, radius: int):
    current_parts = []
    output_parts = []
    meta_parts = []
    coord_count = 2 + mask.bit_count()
    for t in times:
        for n in RINGS:
            selected, _ = select_symbols(obs[n][t], mask)
            selected_next, _ = select_symbols(obs[n][t + 1], mask)
            keys = neighborhood_keys(selected, radius, coord_count).reshape(-1)
            vals = selected_next.reshape(-1).astype(np.uint16)
            sources = np.repeat(np.arange(selected.shape[0], dtype=np.int32), n)
            sites = np.tile(np.arange(n, dtype=np.int16), selected.shape[0])
            tt = np.full(len(keys), t, dtype=np.int8)
            nn = np.full(len(keys), n, dtype=np.int8)
            current_parts.append(keys)
            output_parts.append(vals)
            meta_parts.append((tt, nn, sources, sites))
    keys = np.concatenate(current_parts)
    vals = np.concatenate(output_parts)
    tarr = np.concatenate([m[0] for m in meta_parts])
    narr = np.concatenate([m[1] for m in meta_parts])
    sarr = np.concatenate([m[2] for m in meta_parts])
    iarr = np.concatenate([m[3] for m in meta_parts])
    return keys, vals, (tarr, narr, sarr, iarr), coord_count


def factor_check(keys: np.ndarray, vals: np.ndarray, meta_arrays) -> tuple[bool, dict | None, np.ndarray | None, np.ndarray | None]:
    """Check single-valuedness. Original record order is the protocol metadata order."""
    order = np.argsort(keys, kind="stable")
    sk = keys[order]
    sv = vals[order]
    if len(sk) == 0:
        return True, None, order, np.array([], dtype=np.int64)
    starts = np.r_[0, np.flatnonzero(sk[1:] != sk[:-1]) + 1]
    ends = np.r_[starts[1:], len(sk)]
    mins = np.minimum.reduceat(sv, starts)
    maxs = np.maximum.reduceat(sv, starts)
    bad_groups = np.flatnonzero(mins != maxs)
    if len(bad_groups) == 0:
        return True, None, order, starts

    first_record_indices = order[starts[bad_groups]]
    g = int(bad_groups[np.argmin(first_record_indices)])
    lo, hi = int(starts[g]), int(ends[g])
    group_order = order[lo:hi]
    first = int(group_order[0])
    first_out = int(vals[first])
    second = next(int(idx) for idx in group_order[1:] if int(vals[idx]) != first_out)
    tarr, narr, sarr, iarr = meta_arrays

    def rec(idx: int) -> dict:
        n = int(narr[idx]); source = int(sarr[idx])
        return {
            "t": int(tarr[idx]), "n": n, "site": int(iarr[idx]),
            **source_pair_record(source, n),
            "next_symbol": int(vals[idx]),
        }

    witness = {
        "current_neighborhood_key": int(keys[first]),
        "record_1": rec(first),
        "record_2": rec(second),
    }
    return False, witness, order, starts


def simulate_all() -> tuple[dict[int, list[np.ndarray]], dict, dict]:
    obs: dict[int, list[np.ndarray]] = {}
    controls = {"coarse_t1_exterior_changed": {}, "coarse_t1_W_invalid": {}, "coarse_t2_exterior_changed": {}}
    engine = {"sources": {}, "vector_scalar_checks": 0}
    for n in RINGS:
        total = 1 << (2 * n)
        engine["sources"][str(n)] = total
        obs_n = [np.empty((total, n), dtype=np.uint8) for _ in range(8)]
        ext1 = 0; invalid1 = 0; ext2 = 0
        for start in range(0, total, BATCH):
            ids = np.arange(start, min(start + BATCH, total), dtype=np.int64)
            field, y_min = encode_batch(ids, n)
            obs_n[0][start:start+len(ids)] = typed_symbols_from_raw(raw_symbols(field, y_min, n))
            for coarse in range(1, 8):
                field = step_vector(field); y_min += 1
                field = step_vector(field); y_min += 1
                obs_n[coarse][start:start+len(ids)] = typed_symbols_from_raw(raw_symbols(field, y_min, n))
                if coarse == 1:
                    ext1 += int(outside_changed(field, y_min).sum())
                    invalid1 += int(w_band_invalid(field, y_min).sum())
                if coarse == 2: ext2 += int(outside_changed(field, y_min).sum())
        obs[n] = obs_n
        controls["coarse_t1_exterior_changed"][str(n)] = ext1
        controls["coarse_t1_W_invalid"][str(n)] = invalid1
        controls["coarse_t2_exterior_changed"][str(n)] = ext2
    return obs, controls, engine


def simulate_one_vector(source: int, n: int, coarse_t: int) -> tuple[np.ndarray, int]:
    field, y_min = encode_batch(np.array([source], dtype=np.int64), n)
    for _ in range(2 * coarse_t):
        field = step_vector(field); y_min += 1
    return field[0], y_min


def simulate_one_scalar(source: int, n: int, coarse_t: int) -> tuple[np.ndarray, int]:
    field, y_min = encode_batch(np.array([source], dtype=np.int64), n)
    f = field[0]
    for _ in range(2 * coarse_t):
        f = step_scalar(f); y_min += 1
    return f, y_min


def scalar_replay(source: int, n: int, coarse_t: int) -> int:
    a, ya = simulate_one_vector(source, n, coarse_t)
    b, yb = simulate_one_scalar(source, n, coarse_t)
    assert ya == yb and np.array_equal(a, b)
    return int(a.size)


def scalar_typed_ring(source: int, n: int, coarse_t: int) -> tuple[np.ndarray, np.ndarray, int]:
    current, y_min = simulate_one_scalar(source, n, coarse_t)
    next_field, next_y = current.copy(), y_min
    next_field = step_scalar(next_field); next_y += 1
    next_field = step_scalar(next_field); next_y += 1
    cur_typed = typed_symbols_from_raw(raw_symbols(current[None], y_min, n))[0]
    nxt_typed = typed_symbols_from_raw(raw_symbols(next_field[None], next_y, n))[0]
    return cur_typed, nxt_typed, y_min


def full_key_at(typed: np.ndarray, site: int, radius: int) -> int:
    key = 0
    n = len(typed)
    for d in range(-radius, radius + 1):
        key = (key << 6) | int(typed[(site + d) % n])
    return key


def hidden_cause(witness: dict, radius: int) -> dict:
    records = []
    fields = []
    for name in ("record_1", "record_2"):
        r = witness[name]
        f, y_min = simulate_one_scalar(r["source_index"], r["n"], r["t"])
        scalar_replay(r["source_index"], r["n"], r["t"])
        cur_typed, nxt_typed, _ = scalar_typed_ring(r["source_index"], r["n"], r["t"])
        assert full_key_at(cur_typed, r["site"], radius) == witness["current_neighborhood_key"]
        assert int(nxt_typed[r["site"]]) == int(r["next_symbol"])
        fields.append((f, y_min, r))
        records.append({"record": name, "physical_cells_replayed": int(f.size), "factor_replay": True})
    f1, y1, r1 = fields[0]; f2, y2, r2 = fields[1]
    diffs = []
    for y in (-2, -1, 4, 5):
        iy1, iy2 = y - y1, y - y2
        for dx in range(-2, 4):
            x1 = (2 * r1["site"] + dx) % (2 * r1["n"])
            x2 = (2 * r2["site"] + dx) % (2 * r2["n"])
            if int(f1[iy1, x1]) != int(f2[iy2, x2]):
                diffs.append([y, dx])
    return {
        "comparable_patch": True,
        "outside_rows_current_causal_patch_diff": bool(diffs),
        "outside_difference_coordinates_relative": diffs,
        "replays": records,
    }


def essential_edges(keys: np.ndarray, vals: np.ndarray, radius: int) -> list[dict]:
    table: dict[int, int] = {}
    for k, v in zip(keys.tolist(), vals.tolist()):
        table.setdefault(int(k), int(v))
    total_bits = 6 * (2 * radius + 1)
    edges = set()
    for key, out in table.items():
        for packed_bit in range(total_bits):
            other = key ^ (1 << packed_bit)
            if other not in table or key > other:
                continue
            diff = out ^ table[other]
            if not diff:
                continue
            rev_site = packed_bit // 6
            coord = packed_bit % 6
            d = radius - rev_site
            for out_coord in range(6):
                if (diff >> out_coord) & 1:
                    edges.add((d, coord, out_coord))
    return [
        {"input_offset": int(d), "input_coord": COORD_NAMES[ci], "output_coord": COORD_NAMES[co]}
        for d, ci, co in sorted(edges)
    ]


def is_cross_edge(edge: dict) -> bool:
    inp = edge["input_coord"]; out = edge["output_coord"]
    if inp.startswith("E") != out.startswith("E"):
        return True
    if out == "A" and (inp == "B" or inp.startswith("E")):
        return True
    if out == "B" and (inp == "A" or inp.startswith("E")):
        return True
    return False


def main() -> None:
    obs, controls, engine = simulate_all()
    assert all(v == 0 for v in controls["coarse_t1_exterior_changed"].values()), controls
    assert all(v == 0 for v in controls["coarse_t1_W_invalid"].values()), controls
    assert any(v > 0 for v in controls["coarse_t2_exterior_changed"].values()), controls

    j1_initial = {}
    for n in RINGS:
        j1_initial[str(n)] = bool(np.all((obs[n][0] >> 2) == 0))
        for t in range(8):
            typed = obs[n][t]
            raw = raw_from_typed(typed)
            assert np.array_equal(typed_symbols_from_raw(raw), typed)
    assert all(j1_initial.values())

    results = {"primary": {}, "stress": {}}
    full_pass_data = {}
    for horizon_name, times in (("primary", PRIMARY_TIMES), ("stress", STRESS_TIMES)):
        for mask in MASKS:
            mrec = {}
            for radius in RADII:
                keys, vals, meta, coord_count = build_records(obs, times, mask, radius)
                passed, witness, _, _ = factor_check(keys, vals, meta)
                rec = {"pass": bool(passed), "radius": radius, "selected_interface_bits": mask.bit_count(), "records": int(len(keys))}
                if witness is not None:
                    rec["witness"] = witness
                mrec[str(radius)] = rec
                if mask == 15 and passed:
                    full_pass_data[(horizon_name, radius)] = (keys, vals)
            results[horizon_name][str(mask)] = mrec

    def passing_summary(h: str):
        pass_masks = {}
        for mask in MASKS:
            rs = [r for r in RADII if results[h][str(mask)][str(r)]["pass"]]
            if rs: pass_masks[mask] = min(rs)
        if not pass_masks:
            return {"passing_masks": [], "minimum_interface_bits": None, "inclusion_minimal_masks": []}
        min_bits = min(m.bit_count() for m in pass_masks)
        minimal = []
        for m in pass_masks:
            if not any(o != m and (o & m) == o for o in pass_masks):
                minimal.append(m)
        return {
            "passing_masks": [{"mask": m, "minimum_radius": pass_masks[m], "interface_bits": m.bit_count()} for m in sorted(pass_masks)],
            "minimum_interface_bits": min_bits,
            "inclusion_minimal_masks": sorted(minimal),
        }

    summaries = {h: passing_summary(h) for h in ("primary", "stress")}
    p15_primary = [r for r in RADII if results["primary"]["15"][str(r)]["pass"]]
    p15_stress = [r for r in RADII if results["stress"]["15"][str(r)]["pass"]]
    j3 = bool(p15_primary)

    conflicts_detail = {}
    for h, rs in (("primary", p15_primary), ("stress", p15_stress)):
        if rs:
            continue
        w = results[h]["15"][str(max(RADII))].get("witness")
        if w:
            conflicts_detail[h] = {"radius": max(RADII), "witness": w, "hidden_cause": hidden_cause(w, max(RADII))}

    dependency = {}
    for h, rs in (("primary", p15_primary), ("stress", p15_stress)):
        if not rs:
            dependency[h] = None
            continue
        r = min(rs)
        keys, vals = full_pass_data[(h, r)]
        edges = essential_edges(keys, vals, r)
        dependency[h] = {
            "minimum_passing_radius": r,
            "essential_edges": edges,
            "transverse_interface_edges": [e for e in edges if is_cross_edge(e)],
            "bounded_two_channel_interacting_closure_witness": any(is_cross_edge(e) for e in edges),
        }

    scalar_cells = 0; scalar_cases = 0
    for n in RINGS:
        for t in range(8):
            scalar_cells += scalar_replay(0, n, t); scalar_cases += 1
    for h in conflicts_detail.values():
        for recname in ("record_1", "record_2"):
            r = h["witness"][recname]
            scalar_cells += scalar_replay(r["source_index"], r["n"], r["t"]); scalar_cases += 1
    engine["vector_scalar_checks"] = scalar_cases
    engine["vector_scalar_cells"] = scalar_cells

    j2_scalar = []
    for n in RINGS:
        f1, y1 = simulate_one_scalar(0, n, 1)
        j2_scalar.append({"n": n, "source": 0, "coarse_t": 1, "outside_changed": bool(outside_changed(f1[None], y1)[0]), "W_invalid": bool(w_band_invalid(f1[None], y1)[0])})
        assert not j2_scalar[-1]["outside_changed"] and not j2_scalar[-1]["W_invalid"]
        first = None
        for src in range(1 << (2*n)):
            f2, y2 = simulate_one_vector(src, n, 2)
            if outside_changed(f2[None], y2)[0]: first = src; break
        assert first is not None
        fs, ys = simulate_one_scalar(first, n, 2)
        j2_scalar.append({"n": n, "source": first, "coarse_t": 2, "outside_changed": bool(outside_changed(fs[None], ys)[0])})
        assert j2_scalar[-1]["outside_changed"]

    report = {
        "protocol": "interface-factor-20260911",
        "schema": 1,
        "scope": {
            "rings": list(RINGS), "source_pairs": {str(n): 1 << (2*n) for n in RINGS},
            "coarse_transitions": list(COARSE_TRANSITIONS), "primary_times": list(PRIMARY_TIMES),
            "stress_times": list(STRESS_TIMES), "masks": list(MASKS), "radii": list(RADII),
            "batch_size": BATCH,
        },
        "source_hashes": {"script": sha(Path(__file__)), "protocol": sha(PROTOCOL)},
        "controls": {
            "J1_initial_interface_zero": j1_initial,
            "J1_coordinate_bijection": True,
            "J2_exterior_counts": controls,
            "J2_scalar_replay": j2_scalar,
            "J8_engine_replay": engine,
        },
        "factor_census": results,
        "factor_summary": summaries,
        "full_state": {
            "J3_primary_prediction_pass": j3,
            "primary_minimum_radius": min(p15_primary) if p15_primary else None,
            "J4_stress_pass": bool(p15_stress),
            "stress_minimum_radius": min(p15_stress) if p15_stress else None,
            "conflict_details": conflicts_detail,
            "typed_dependency": dependency,
        },
        "summary": {
            "J1": True,
            "J2": True,
            "J3": j3,
            "J4": "pass" if p15_stress else "conflict",
            "J5_primary_passing_masks": len(summaries["primary"]["passing_masks"]),
            "J5_stress_passing_masks": len(summaries["stress"]["passing_masks"]),
            "J7_primary_interacting": bool(dependency["primary"] and dependency["primary"]["bounded_two_channel_interacting_closure_witness"]),
            "J7_stress_interacting": bool(dependency["stress"] and dependency["stress"]["bounded_two_channel_interacting_closure_witness"]),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["summary"], sort_keys=True))
    print("written", OUT)


if __name__ == "__main__":
    main()
