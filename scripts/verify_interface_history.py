#!/usr/bin/env python3
"""Verifier for finite interface history (2026-09-11 frozen protocol).

Gate 1: Claude/Fable approved the protocol on the integrated gathering head
36f20aa89889bb884af4ec07785d1611158d6b28, with the K8 causal-patch
clarification recorded before this implementation. This implementation stage
must not create the canonical result until it is integrated and evaluation is
opened separately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from dataclasses import dataclass

import numpy as np

from verify_interface_factor import (
    RINGS,
    RADII,
    MASKS,
    COORDINATES,
    build_ring_orbit,
    field_mask,
    replay_source,
    causal_patch,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/interface-history-20260911.md"
OLD_RESULT = ROOT / "results/interface_factor_20260911.json"
INTERFACE_FACTOR_SCRIPT = ROOT / "scripts/verify_interface_factor.py"
OUT = ROOT / "results/interface_history_20260911.json"
DOMAINS = {
    "D0": (0, 1, 2, 3, 4, 5, 6),
    "D1": (1, 2, 3, 4, 5, 6),
    "D2": (2, 3, 4, 5, 6),
    "P0": (0, 1, 2, 3),
}
DEPTHS = {"D0": (0,), "D1": (0, 1), "D2": (0, 1, 2), "P0": (0,)}


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repeat_mask(selected: int, count: int) -> tuple[np.uint64, np.uint64]:
    lo = hi = 0
    for j in range(count):
        bit = selected << (6 * j)
        if 6 * j < 64:
            lo |= bit & ((1 << 64) - 1)
            if 6 * j + 6 > 64:
                hi |= bit >> 64
        else:
            hi |= selected << (6 * j - 64)
    return np.uint64(lo), np.uint64(hi)


def pack_chunks(chunks: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    lo = np.zeros(chunks[0].shape, dtype=np.uint64)
    hi = np.zeros(chunks[0].shape, dtype=np.uint64)
    for j, array in enumerate(chunks):
        shift = 6 * j
        x = array.astype(np.uint64)
        if shift <= 58:
            lo |= x << np.uint64(shift)
        elif shift < 64:
            lo |= x << np.uint64(shift)
            hi |= x >> np.uint64(64 - shift)
        else:
            hi |= x << np.uint64(shift - 64)
    return lo, hi


def pack_output(chunks: list[np.ndarray]) -> np.ndarray:
    out = np.zeros(chunks[0].shape, dtype=np.uint32)
    for j, array in enumerate(chunks):
        out |= array.astype(np.uint32) << np.uint32(6 * j)
    return out


@dataclass
class Records:
    lo: np.ndarray
    hi: np.ndarray
    out: np.ndarray
    newp: np.ndarray
    t: np.ndarray
    n: np.ndarray
    source: np.ndarray
    site: np.ndarray
    h: int
    radius: int
    domain: str


def build_records(orbits, domain: str, h: int, radius: int) -> Records:
    los = []
    his = []
    outs = []
    newps = []
    ts = []
    ns = []
    srcs = []
    sites = []
    for t in DOMAINS[domain]:
        if t < h:
            raise AssertionError((domain, h, t))
        for n in RINGS:
            orbit = orbits[n]
            chunks = []
            for d in range(-radius, radius + 1):
                for tt in range(t - h, t + 1):
                    chunks.append(np.roll(orbit.symbols[tt], -d, axis=1))
            lo, hi = pack_chunks(chunks)
            next_hist = [orbit.symbols[tt] for tt in range(t - h + 1, t + 2)]
            out = pack_output(next_hist)
            newp = orbit.symbols[t + 1].astype(np.uint8)
            total = lo.size
            sources = lo.shape[0]
            los.append(lo.reshape(-1))
            his.append(hi.reshape(-1))
            outs.append(out.reshape(-1))
            newps.append(newp.reshape(-1))
            ts.append(np.full(total, t, np.uint8))
            ns.append(np.full(total, n, np.uint8))
            srcs.append(np.repeat(np.arange(sources, dtype=np.uint32), n))
            sites.append(np.tile(np.arange(n, dtype=np.uint8), sources))
    return Records(
        *(np.concatenate(x) for x in (los, his, outs, newps, ts, ns, srcs, sites)),
        h=h,
        radius=radius,
        domain=domain,
    )


@dataclass
class Verdict:
    passed: bool
    pair: tuple[int, int] | None
    key: tuple[int, int] | None
    outputs: tuple[int, int] | None


def verdict(records: Records, mask: int) -> Verdict:
    selected = field_mask(mask)
    count = (2 * records.radius + 1) * (records.h + 1)
    mlo, mhi = repeat_mask(selected, count)
    olo = records.lo & mlo
    ohi = records.hi & mhi
    omask = sum(selected << (6 * j) for j in range(records.h + 1))
    out = records.out.astype(np.uint64) & np.uint64(omask)
    order = np.lexsort((ohi, olo))
    slo, shi, sout = olo[order], ohi[order], out[order]
    if not len(order):
        return Verdict(True, None, None, None)
    new = np.empty(len(order), bool)
    new[0] = True
    new[1:] = (slo[1:] != slo[:-1]) | (shi[1:] != shi[:-1])
    starts = np.flatnonzero(new)
    gid = np.cumsum(new, dtype=np.int64) - 1
    first = sout[starts]
    pos = np.flatnonzero(sout != first[gid])
    if not len(pos):
        return Verdict(True, None, None, None)
    dg = gid[pos]
    pos = pos[np.r_[True, dg[1:] != dg[:-1]]]
    groups = gid[pos]
    p1 = order[starts[groups]]
    p2 = order[pos]
    choose = int(np.argmin(p1))
    a, b = int(p1[choose]), int(p2[choose])
    return Verdict(False, (a, b), (int(olo[a]), int(ohi[a])), (int(out[a]), int(out[b])))


def record_meta(records: Records, position: int) -> dict:
    n = int(records.n[position])
    source = int(records.source[position])
    width = 1 << n
    a, b = divmod(source, width)
    return {
        "t": int(records.t[position]),
        "n": n,
        "source_index": source,
        "source_pair_lex": [format(a, f"0{n}b"), format(b, f"0{n}b")],
        "logical_site": int(records.site[position]),
    }


def selected_neighborhood(records: Records, position: int, mask: int) -> list:
    count = (2 * records.radius + 1) * (records.h + 1)
    value = int(records.lo[position]) | (int(records.hi[position]) << 64)
    selected = field_mask(mask)
    chunks = [(value >> (6 * j)) & 63 for j in range(count)]
    rows = []
    k = 0
    for d in range(-records.radius, records.radius + 1):
        hist = []
        for _ in range(records.h + 1):
            hist.append(chunks[k] & selected)
            k += 1
        rows.append({"offset": d, "history_oldest_to_newest": hist})
    return rows


def first_diff_coordinate(a: int, b: int, h: int, mask: int) -> dict | None:
    selected = field_mask(mask)
    for j in range(h + 1):
        for c, name in enumerate(COORDINATES):
            if ((selected >> c) & 1) and ((a >> (6 * j + c)) & 1) != ((b >> (6 * j + c)) & 1):
                return {"history_index_oldest_first": j, "coordinate": name}
    return None


def entry(records: Records, mask: int, value: Verdict) -> dict:
    if value.passed:
        return {"pass": True, "canonical_conflict": None}
    a, b = value.pair
    oa, ob = value.outputs
    return {
        "pass": False,
        "canonical_conflict": {
            "local_key_low_high": list(value.key),
            "records": [record_meta(records, a), record_meta(records, b)],
            "selected_history_neighborhoods": [
                selected_neighborhood(records, a, mask),
                selected_neighborhood(records, b, mask),
            ],
            "complete_next_history_symbols": [oa, ob],
            "first_differing_output_coordinate": first_diff_coordinate(oa, ob, records.h, mask),
        },
    }


def check_shift_control(orbits) -> bool:
    for h in (1, 2):
        for t in range(h, 7):
            for n in RINGS:
                cur = [orbits[n].symbols[x] for x in range(t - h, t + 1)]
                nxt = [orbits[n].symbols[x] for x in range(t - h + 1, t + 2)]
                for j in range(h):
                    if not np.array_equal(nxt[j], cur[j + 1]):
                        return False
    return True


def current_patch_partition(conflict: dict, radius: int) -> dict:
    patches = []
    for rec in conflict["records"]:
        states, ys = replay_source(rec["n"], rec["source_index"], rec["t"] + 1)
        patches.append(causal_patch(states[rec["t"]], ys[rec["t"]], rec["logical_site"], rec["n"]))
    diffs = [[], [], []]
    retained = {(0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0)}
    for iy, y in enumerate(range(-2, 6)):
        for ix, dx in enumerate(range(-2, 4)):
            if int(patches[0][iy, ix]) == int(patches[1][iy, ix]):
                continue
            cat = 2
            if 0 <= y <= 3:
                cat = 1
                for d in range(-radius, radius + 1):
                    if (y, dx - 2 * d) in retained:
                        cat = 0
                        break
            diffs[cat].append(
                {
                    "relative_y": y,
                    "relative_x": dx,
                    "first": int(patches[0][iy, ix]),
                    "second": int(patches[1][iy, ix]),
                }
            )
    return {
        "patch_rows_relative": [-2, 5],
        "patch_columns_relative": [-2, 3],
        "retained_W_differences": diffs[0],
        "other_rows_0_3_differences": diffs[1],
        "outside_rows_0_3_differences": diffs[2],
        "complete_patches_identical": not any(diffs),
        "scalar_replay_matches_vectorized": True,
    }


def old_normalized(old_entry: dict) -> tuple:
    conflict = old_entry.get("canonical_conflict")
    if conflict is None:
        return (old_entry["pass"], None)
    records = tuple(
        (x["t"], x["n"], tuple(x["source_pair_lex"]), x["logical_site"])
        for x in conflict["records"]
    )
    return (old_entry["pass"], records, tuple(conflict["next_center_symbols"]))


def new_normalized(new_entry: dict) -> tuple:
    conflict = new_entry.get("canonical_conflict")
    if conflict is None:
        return (new_entry["pass"], None)
    records = tuple(
        (x["t"], x["n"], tuple(x["source_pair_lex"]), x["logical_site"])
        for x in conflict["records"]
    )
    return (new_entry["pass"], records, tuple(conflict["complete_next_history_symbols"]))


def essential_dependencies(records: Records) -> dict:
    keys = [int(lo) | (int(hi) << 64) for lo, hi in zip(records.lo, records.hi)]
    table = {}
    for key, output in zip(keys, records.newp):
        output = int(output)
        if key in table and table[key] != output:
            raise AssertionError("dependency audit on conflicting factor")
        table[key] = output
    edges = set()
    chunks = (2 * records.radius + 1) * (records.h + 1)
    for key, output in table.items():
        for bit in range(6 * chunks):
            other = key ^ (1 << bit)
            if other not in table or other < key:
                continue
            delta = output ^ table[other]
            if not delta:
                continue
            chunk, c = divmod(bit, 6)
            offset_index, hist_index = divmod(chunk, records.h + 1)
            offset = offset_index - records.radius
            lag = records.h - hist_index
            inp = COORDINATES[c]
            for oc, outname in enumerate(COORDINATES):
                if (delta >> oc) & 1:
                    edges.add((offset, lag, inp, outname))
    rows = []
    for d, lag, inp, outname in sorted(
        edges, key=lambda x: (x[0], x[1], COORDINATES.index(x[2]), COORDINATES.index(x[3]))
    ):
        cross = (
            inp.startswith("E") != outname.startswith("E")
            or (outname == "A" and inp == "B")
            or (outname == "B" and inp == "A")
        )
        rows.append(
            {
                "offset": d,
                "history_lag": lag,
                "input_coordinate": inp,
                "output_coordinate": outname,
                "cross_interface": cross,
            }
        )
    return {
        "reachable_local_words": len(table),
        "edges": rows,
        "has_historical_predictive_dependency": any(x["history_lag"] > 0 for x in rows),
        "has_cross_interface_predictive_dependency": any(x["cross_interface"] for x in rows),
        "has_both": any(x["history_lag"] > 0 for x in rows)
        and any(x["cross_interface"] for x in rows),
    }


def replay_record(record: dict) -> dict:
    """Run the imported independent scalar/vector physical replay through t+1.

    verify_interface_factor.replay_source asserts cell-for-cell equality of the
    complete scalar and vector physical fields at every coarse state, which is
    stronger than K10's requested equality on observation/causal-patch cells.
    """
    replay_source(record["n"], record["source_index"], record["t"] + 1)
    return {
        "t": record["t"],
        "n": record["n"],
        "source_index": record["source_index"],
        "logical_site": record["logical_site"],
        "scalar_vector_complete_field_agreement_through_t_plus_1": True,
    }


def k10_controls(old: dict, census: dict, k8_rows: list[dict]) -> dict:
    deterministic = []
    for n in RINGS:
        replay_source(n, 0, 7)
        for t in range(7):
            deterministic.append(
                {
                    "n": n,
                    "t": t,
                    "source_index": 0,
                    "scalar_vector_complete_field_agreement_through_t_plus_1": True,
                }
            )

    accepted_k1 = []
    for horizon in ("primary", "stress"):
        entries = old["factor_census"][horizon]["entries"]
        for mask in MASKS:
            for radius in RADII:
                old_entry = entries[str(mask)][str(radius)]
                conflict = old_entry.get("canonical_conflict")
                if conflict is None:
                    continue
                replays = [replay_record(record) for record in conflict["records"]]
                accepted_k1.append(
                    {
                        "horizon": horizon,
                        "mask": mask,
                        "radius": radius,
                        "records": replays,
                    }
                )

    full_state = []
    for row in k8_rows:
        full_state.append(
            {
                "domain": row["domain"],
                "history_depth": row["history_depth"],
                "radius": row["radius"],
                "records": [replay_record(record) for record in row["records"]],
            }
        )

    return {
        "pass": True,
        "comparison_strength": "replay_source asserts complete physical-field scalar/vector equality at every coarse state, stronger than the requested observation/causal-patch subset",
        "deterministic_source_time_controls": deterministic,
        "accepted_K1_memoryless_conflict_replays": accepted_k1,
        "canonical_full_state_conflict_replays": full_state,
    }


def evaluate() -> dict:
    old = json.loads(OLD_RESULT.read_text())
    orbits = {n: build_ring_orbit(n) for n in RINGS}
    if not check_shift_control(orbits):
        raise AssertionError("K2 history shift failed")

    records = {}
    census = {}
    for domain in ("P0", "D0", "D1", "D2"):
        census[domain] = {}
        for h in DEPTHS[domain]:
            census[domain][str(h)] = {}
            for radius in RADII:
                rr = build_records(orbits, domain, h, radius)
                records[(domain, h, radius)] = rr
                census[domain][str(h)][str(radius)] = {
                    str(mask): entry(rr, mask, verdict(rr, mask)) for mask in MASKS
                }

    k1 = []
    for label, oldlabel in (("P0", "primary"), ("D0", "stress")):
        for radius in RADII:
            for mask in MASKS:
                if new_normalized(census[label]["0"][str(radius)][str(mask)]) != old_normalized(
                    old["factor_census"][oldlabel]["entries"][str(mask)][str(radius)]
                ):
                    k1.append([label, radius, mask])
    if k1:
        raise AssertionError(f"K1 regression mismatches: {k1[:3]}")

    k3 = []
    for domain in ("D1", "D2"):
        for h in DEPTHS[domain][:-1]:
            for radius in RADII:
                for mask in MASKS:
                    if census[domain][str(h)][str(radius)][str(mask)]["pass"] and not census[domain][str(h + 1)][str(radius)][str(mask)]["pass"]:
                        k3.append([domain, h, h + 1, radius, mask])
    if k3:
        raise AssertionError(f"K3 violations {k3[:3]}")

    p15 = {}
    k8 = []
    dependencies = {}
    for domain in ("P0", "D0", "D1", "D2"):
        p15[domain] = {}
        for h in DEPTHS[domain]:
            passes = [
                radius
                for radius in RADII
                if census[domain][str(h)][str(radius)]["15"]["pass"]
            ]
            p15[domain][str(h)] = {"passing_radii": passes}
            for radius in RADII:
                item = census[domain][str(h)][str(radius)]["15"]
                if not item["pass"]:
                    conflict = item["canonical_conflict"]
                    part = current_patch_partition(conflict, radius)
                    if part["retained_W_differences"] or part["complete_patches_identical"]:
                        raise AssertionError("K8 invalid full-state conflict replay")
                    k8.append(
                        {
                            "domain": domain,
                            "history_depth": h,
                            "radius": radius,
                            "records": conflict["records"],
                            **part,
                        }
                    )
            if domain in ("D1", "D2") and passes:
                radius = min(passes)
                dependencies[f"{domain}_h{h}"] = {
                    "minimum_passing_radius": radius,
                    **essential_dependencies(records[(domain, h, radius)]),
                }

    k4 = bool(p15["D1"]["1"]["passing_radii"]) and not p15["D1"]["0"]["passing_radii"]
    h1 = bool(p15["D2"]["1"]["passing_radii"])
    h2 = bool(p15["D2"]["2"]["passing_radii"])
    k5 = (
        "two-lag resolution"
        if h2 and not h1
        else "both pass"
        if h2 and h1
        else "both conflict"
        if not h2 and not h1
        else "shallower-only anomaly"
    )

    pareto = {}
    for domain in ("D0", "D1", "D2"):
        points = []
        for h in DEPTHS[domain]:
            for radius in RADII:
                for mask in MASKS:
                    if census[domain][str(h)][str(radius)][str(mask)]["pass"]:
                        points.append((mask.bit_count(), h, radius, mask))
        mins = [
            p
            for p in points
            if not any(
                q != p
                and q[0] <= p[0]
                and q[1] <= p[1]
                and q[2] <= p[2]
                and (q[0] < p[0] or q[1] < p[1] or q[2] < p[2])
                for q in points
            )
        ]
        pareto[domain] = [
            {
                "interface_bit_count": a,
                "history_depth": h,
                "radius": radius,
                "mask": mask,
            }
            for a, h, radius, mask in mins
        ]

    k10 = k10_controls(old, census, k8)

    return {
        "protocol": "interface-history-20260911",
        "schema": 1,
        "source_hashes": {
            "script": sha(pathlib.Path(__file__)),
            "protocol": sha(PROTOCOL),
            "interface_factor_result": sha(OLD_RESULT),
            "interface_factor_script": sha(INTERFACE_FACTOR_SCRIPT),
        },
        "parameters": {
            "rings": list(RINGS),
            "domains": {k: list(v) for k, v in DOMAINS.items()},
            "history_depths": [0, 1, 2],
            "radii": list(RADII),
            "masks": list(MASKS),
            "history_order": "oldest-to-newest",
            "key_chunk_order": "offset outer, history oldest-to-newest",
            "output_coordinate_order": "history oldest-to-newest, then A,B,E0,E1,E2,E3",
            "causal_patch": {"rows_relative": [-2, 5], "columns_relative": [-2, 3]},
        },
        "controls": {
            "K1_memoryless_regression": True,
            "K2_history_shift": True,
            "K3_refinement_monotonicity": True,
            "K8_full_state_conflict_replays": k8,
            "K10_scalar_vector_replay": k10,
        },
        "census": census,
        "P15": p15,
        "K4_one_lag_constructive_bet": k4,
        "K5_depth_two_outcome": k5,
        "K6_pareto_minimal": pareto,
        "K9_dependency_audits": dependencies,
        "scope": "bounded n=6,7; t<7; h<=2; R<=2; frozen masks; no arbitrary-width or all-time claim",
    }


def self_test() -> None:
    x = np.arange(24, dtype=np.uint8).reshape(4, 6) & 63
    lo, hi = pack_chunks([x, x ^ 1, x ^ 2])
    assert lo.shape == x.shape and hi.shape == x.shape
    mlo, mhi = repeat_mask(63, 15)
    assert int(mlo) != 0 and int(mhi) != 0
    assert INTERFACE_FACTOR_SCRIPT.exists()
    print("interface-history implementation self-test passed (no frozen source-domain run)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        result = evaluate()
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(
            json.dumps(
                {
                    "K4": result["K4_one_lag_constructive_bet"],
                    "K5": result["K5_depth_two_outcome"],
                    "P15": result["P15"],
                    "dependencies": result["K9_dependency_audits"],
                },
                sort_keys=True,
            )
        )