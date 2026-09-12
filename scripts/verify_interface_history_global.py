#!/usr/bin/env python3
"""Verifier for full-field determinism of frozen interface history.

Protocol: docs/research/protocols/interface-history-global-20260912.md
Binding Gate-1 witness-order supplement:
docs/research/protocols/interface-history-global-gate1-clarification-20260912.md

Claude/Fable approved the protocol-only gathering head
651ba1f574fcc2dca6bc8b130e11cbe7e5efac6c on 2026-09-12, requiring only the
canonical witness-order clarification recorded before this verifier commit.
This implementation stage must not create the canonical result. Running without
--self-test performs the frozen n=6,7 census and writes the canonical result;
--self-test is strictly outside the frozen scientific domain and writes nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from dataclasses import dataclass
from typing import Iterable

import numpy as np

from verify_interface_factor import (
    RINGS,
    MASKS,
    COORDINATES,
    build_ring_orbit,
    field_mask,
    replay_source,
    observe_symbols,
)
from verify_interface_history import (
    DOMAINS,
    DEPTHS,
    build_records as build_local_records,
    verdict as local_verdict,
    entry as local_entry,
    pack_chunks,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs/research/protocols/interface-history-global-20260912.md"
CLARIFICATION = ROOT / "docs/research/protocols/interface-history-global-gate1-clarification-20260912.md"
PREV_PROTOCOL = ROOT / "docs/research/protocols/interface-history-20260911.md"
PREV_SCRIPT = ROOT / "scripts/verify_interface_history.py"
PREV_RESULT = ROOT / "results/interface_history_20260911.json"
FACTOR_SCRIPT = ROOT / "scripts/verify_interface_factor.py"
FACTOR_RESULT = ROOT / "results/interface_factor_20260911.json"
OUT = ROOT / "results/interface_history_global_20260912.json"
DOMAINS_GLOBAL = ("D0", "D1", "D2")


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pack_field(symbols: np.ndarray) -> np.ndarray:
    """Pack a complete retained ring field; n<=7 so 42 bits fit in uint64."""
    if symbols.ndim != 2:
        raise AssertionError("field must have shape (sources, ring_sites)")
    out = np.zeros(symbols.shape[0], dtype=np.uint64)
    for site in range(symbols.shape[1]):
        out |= symbols[:, site].astype(np.uint64) << np.uint64(6 * site)
    return out


def repeat_mask(selected: int, chunks: int) -> tuple[np.uint64, np.uint64]:
    lo = 0
    hi = 0
    for j in range(chunks):
        value = selected << (6 * j)
        if 6 * j < 64:
            lo |= value & ((1 << 64) - 1)
            if 6 * j + 6 > 64:
                hi |= value >> 64
        else:
            hi |= selected << (6 * j - 64)
    return np.uint64(lo), np.uint64(hi)


def output_mask(selected: int, n: int) -> np.uint64:
    value = 0
    for site in range(n):
        value |= selected << (6 * site)
    return np.uint64(value)


@dataclass
class GlobalRecords:
    n: int
    domain: str
    h: int
    lo: np.ndarray
    hi: np.ndarray
    out: np.ndarray
    t: np.ndarray
    source: np.ndarray


def build_global_records(orbit, domain: str, h: int) -> GlobalRecords:
    """Canonical record order: (t, source_pair_lex), no site component."""
    if orbit.n not in RINGS or domain not in DOMAINS_GLOBAL or h not in DEPTHS[domain]:
        raise AssertionError((orbit.n, domain, h))
    los = []
    his = []
    outs = []
    ts = []
    sources = []
    for t in DOMAINS[domain]:
        if t < h:
            raise AssertionError((domain, h, t))
        chunks = []
        for tt in range(t - h, t + 1):
            for site in range(orbit.n):
                chunks.append(orbit.symbols[tt][:, site])
        lo, hi = pack_chunks(chunks)
        nxt = pack_field(orbit.symbols[t + 1])
        count = lo.shape[0]
        los.append(lo)
        his.append(hi)
        outs.append(nxt)
        ts.append(np.full(count, t, dtype=np.uint8))
        sources.append(np.arange(count, dtype=np.uint32))
    return GlobalRecords(
        n=orbit.n,
        domain=domain,
        h=h,
        lo=np.concatenate(los),
        hi=np.concatenate(his),
        out=np.concatenate(outs),
        t=np.concatenate(ts),
        source=np.concatenate(sources),
    )


@dataclass(frozen=True)
class GlobalVerdict:
    passed: bool
    pair: tuple[int, int] | None
    key: tuple[int, int] | None
    outputs: tuple[int, int] | None


def primary_verdict(records: GlobalRecords, mask: int) -> GlobalVerdict:
    """Hash complete packed history fields and keep the frozen canonical pair."""
    selected = field_mask(mask)
    mlo, mhi = repeat_mask(selected, records.n * (records.h + 1))
    omask = output_mask(selected, records.n)
    lo = records.lo & mlo
    hi = records.hi & mhi
    out = records.out & omask
    first: dict[tuple[int, int], tuple[int, int]] = {}
    best: tuple[int, int] | None = None
    best_key: tuple[int, int] | None = None
    best_outputs: tuple[int, int] | None = None
    for i in range(len(out)):
        key = (int(lo[i]), int(hi[i]))
        value = int(out[i])
        old = first.get(key)
        if old is None:
            first[key] = (i, value)
            continue
        j, old_value = old
        if value == old_value:
            continue
        candidate = (j, i)
        if best is None or candidate < best:
            best = candidate
            best_key = key
            best_outputs = (old_value, value)
    return GlobalVerdict(best is None, best, best_key, best_outputs)


def explicit_history_key(orbit, source: int, t: int, h: int, selected: int) -> tuple:
    return tuple(
        tuple(int(x) & selected for x in orbit.symbols[tt][source])
        for tt in range(t - h, t + 1)
    )


def explicit_next_field(orbit, source: int, t: int, selected: int) -> tuple[int, ...]:
    return tuple(int(x) & selected for x in orbit.symbols[t + 1][source])


def reference_verdict(orbit, records: GlobalRecords, mask: int) -> GlobalVerdict:
    """Independent explicit-tuple path; no packed history key is used."""
    selected = field_mask(mask)
    first: dict[tuple, tuple[int, tuple[int, ...]]] = {}
    best: tuple[int, int] | None = None
    best_key: tuple | None = None
    best_outputs: tuple[tuple[int, ...], tuple[int, ...]] | None = None
    for i in range(len(records.t)):
        t = int(records.t[i])
        source = int(records.source[i])
        key = explicit_history_key(orbit, source, t, records.h, selected)
        value = explicit_next_field(orbit, source, t, selected)
        old = first.get(key)
        if old is None:
            first[key] = (i, value)
            continue
        j, old_value = old
        if value == old_value:
            continue
        candidate = (j, i)
        if best is None or candidate < best:
            best = candidate
            best_key = key
            best_outputs = (old_value, value)
    if best is None:
        return GlobalVerdict(True, None, None, None)
    # Normalize tuple data only for verdict/pair agreement; entry() reconstructs it.
    return GlobalVerdict(False, best, None, None)


def source_pair_lex(n: int, source: int) -> list[str]:
    width = 1 << n
    a, b = divmod(source, width)
    return [format(a, f"0{n}b"), format(b, f"0{n}b")]


def record_json(records: GlobalRecords, position: int) -> dict:
    source = int(records.source[position])
    return {
        "t": int(records.t[position]),
        "source_index": source,
        "source_pair_lex": source_pair_lex(records.n, source),
    }


def field_json(orbit, source: int, t: int, mask: int) -> list[int]:
    selected = field_mask(mask)
    return [int(x) & selected for x in orbit.symbols[t][source]]


def history_json(orbit, source: int, t: int, h: int, mask: int) -> list[list[int]]:
    return [field_json(orbit, source, tt, mask) for tt in range(t - h, t + 1)]


def first_differing_output(a: Iterable[int], b: Iterable[int], h: int, mask: int) -> dict | None:
    selected = field_mask(mask)
    aa = list(a)
    bb = list(b)
    for site, (x, y) in enumerate(zip(aa, bb)):
        if x == y:
            continue
        for c, name in enumerate(COORDINATES):
            if ((selected >> c) & 1) and ((x >> c) & 1) != ((y >> c) & 1):
                # Equal histories imply all copied lag coordinates of the next
                # history agree; the first difference is at its newest field.
                return {
                    "site": site,
                    "history_index_oldest_first": h,
                    "coordinate": name,
                }
        raise AssertionError("masked fields differ but no retained coordinate differs")
    return None


def entry(orbit, records: GlobalRecords, mask: int, value: GlobalVerdict) -> dict:
    if value.passed:
        return {"pass": True, "canonical_conflict": None}
    if value.pair is None:
        raise AssertionError("conflict missing pair")
    a, b = value.pair
    sa = int(records.source[a])
    sb = int(records.source[b])
    ta = int(records.t[a])
    tb = int(records.t[b])
    ha = history_json(orbit, sa, ta, records.h, mask)
    hb = history_json(orbit, sb, tb, records.h, mask)
    if ha != hb:
        raise AssertionError("canonical pair does not have equal complete retained history")
    oa = field_json(orbit, sa, ta + 1, mask)
    ob = field_json(orbit, sb, tb + 1, mask)
    if oa == ob:
        raise AssertionError("canonical conflict next fields are equal")
    return {
        "pass": False,
        "canonical_conflict": {
            "records": [record_json(records, a), record_json(records, b)],
            "equal_complete_history_oldest_to_newest": ha,
            "next_complete_retained_fields": [oa, ob],
            "first_differing_output_coordinate": first_differing_output(oa, ob, records.h, mask),
        },
    }


def check_predecessor_provenance(old: dict) -> None:
    expected = {
        "script": PREV_SCRIPT,
        "protocol": PREV_PROTOCOL,
        "interface_factor_result": FACTOR_RESULT,
        "interface_factor_script": FACTOR_SCRIPT,
    }
    for key, path in expected.items():
        recorded = old["source_hashes"].get(key)
        actual = sha(path)
        if recorded != actual:
            raise AssertionError(f"G1 predecessor provenance mismatch: {key}")


def check_local_regression(orbits, old: dict) -> None:
    """Replay every accepted full-state D0/D1/D2 local verdict/witness."""
    for domain in DOMAINS_GLOBAL:
        for h in DEPTHS[domain]:
            for radius in (0, 1, 2):
                rr = build_local_records(orbits, domain, h, radius)
                now = local_entry(rr, 15, local_verdict(rr, 15))
                accepted = old["census"][domain][str(h)][str(radius)]["15"]
                if now != accepted:
                    raise AssertionError(("G1 local regression mismatch", domain, h, radius))


def observe_replayed(states: list[np.ndarray], ys: list[np.ndarray], t: int) -> np.ndarray:
    return observe_symbols(states[t][None, ...], ys[t], assert_roundtrip=True)[0]


def replay_global_conflict(orbit, records: GlobalRecords, mask: int, conflict: dict) -> dict:
    rec1, rec2 = conflict["records"]
    max_t = max(rec1["t"], rec2["t"]) + 1
    states1, ys1 = replay_source(records.n, rec1["source_index"], max_t)
    states2, ys2 = replay_source(records.n, rec2["source_index"], max_t)
    selected = field_mask(mask)
    hist1 = [
        [int(x) & selected for x in observe_replayed(states1, ys1, tt)]
        for tt in range(rec1["t"] - records.h, rec1["t"] + 1)
    ]
    hist2 = [
        [int(x) & selected for x in observe_replayed(states2, ys2, tt)]
        for tt in range(rec2["t"] - records.h, rec2["t"] + 1)
    ]
    if hist1 != hist2 or hist1 != conflict["equal_complete_history_oldest_to_newest"]:
        raise AssertionError("G7 scalar/reference history replay mismatch")
    next1 = [int(x) & selected for x in observe_replayed(states1, ys1, rec1["t"] + 1)]
    next2 = [int(x) & selected for x in observe_replayed(states2, ys2, rec2["t"] + 1)]
    if next1 == next2 or [next1, next2] != conflict["next_complete_retained_fields"]:
        raise AssertionError("G7 scalar/reference next-field replay mismatch")
    current1 = states1[rec1["t"]]
    current2 = states2[rec2["t"]]
    physical_diff = bool(np.any(current1 != current2))
    if not physical_diff:
        raise AssertionError("G7 conflict has identical complete current physical fields")
    full1 = observe_replayed(states1, ys1, rec1["t"])
    full2 = observe_replayed(states2, ys2, rec2["t"])
    masked_out_symbol_difference = bool(np.any((full1 ^ full2) & np.uint8(~selected & 63)))
    exterior_or_other_physical_difference = physical_diff and not np.array_equal(current1, current2)
    return {
        "scalar_vector_complete_field_agreement_through_t_plus_1": True,
        "retained_histories_equal": True,
        "next_retained_fields_differ": True,
        "current_complete_physical_fields_identical": False,
        "unretained_current_difference_exists": bool(masked_out_symbol_difference or exterior_or_other_physical_difference),
        "masked_out_symbol_difference_exists": masked_out_symbol_difference,
    }


def pareto_rows(census_ring: dict, domain: str) -> list[dict]:
    points = []
    for h in DEPTHS[domain]:
        for mask in MASKS:
            if census_ring[domain][str(h)][str(mask)]["pass"]:
                points.append((mask.bit_count(), h, mask))
    minimal = []
    for p in points:
        if any(
            q != p and q[0] <= p[0] and q[1] <= p[1] and (q[0] < p[0] or q[1] < p[1])
            for q in points
        ):
            continue
        minimal.append(p)
    return [
        {"interface_bit_count": bits, "history_depth": h, "mask": mask}
        for bits, h, mask in sorted(minimal)
    ]


def evaluate() -> dict:
    old = json.loads(PREV_RESULT.read_text())
    check_predecessor_provenance(old)
    orbits = {n: build_ring_orbit(n) for n in RINGS}
    check_local_regression(orbits, old)

    census: dict[str, dict] = {}
    records_by_cell: dict[tuple[int, str, int], GlobalRecords] = {}
    reference_agreement = 0
    conflict_replays = []
    monotonicity_violations = []

    for n in RINGS:
        ring_key = str(n)
        census[ring_key] = {}
        orbit = orbits[n]
        for domain in DOMAINS_GLOBAL:
            census[ring_key][domain] = {}
            for h in DEPTHS[domain]:
                rr = build_global_records(orbit, domain, h)
                records_by_cell[(n, domain, h)] = rr
                census[ring_key][domain][str(h)] = {}
                for mask in MASKS:
                    primary = primary_verdict(rr, mask)
                    reference = reference_verdict(orbit, rr, mask)
                    if primary.passed != reference.passed or primary.pair != reference.pair:
                        raise AssertionError(("primary/reference verdict mismatch", n, domain, h, mask, primary, reference))
                    reference_agreement += 1
                    item = entry(orbit, rr, mask, primary)
                    census[ring_key][domain][str(h)][str(mask)] = item
                    if not item["pass"]:
                        conflict_replays.append(
                            {
                                "ring": n,
                                "domain": domain,
                                "history_depth": h,
                                "mask": mask,
                                **replay_global_conflict(orbit, rr, mask, item["canonical_conflict"]),
                            }
                        )

        for domain in ("D1", "D2"):
            depths = DEPTHS[domain]
            for mask in MASKS:
                for low in depths:
                    for high in depths:
                        if high <= low:
                            continue
                        if census[ring_key][domain][str(low)][str(mask)]["pass"] and not census[ring_key][domain][str(high)][str(mask)]["pass"]:
                            monotonicity_violations.append([n, domain, mask, low, high])
    if monotonicity_violations:
        raise AssertionError(f"G3 violations: {monotonicity_violations[:3]}")

    ladders = {}
    pareto = {}
    g8 = {}
    for n in RINGS:
        rk = str(n)
        ladders[rk] = [
            {
                "domain": domain,
                "history_depth": h,
                "pass": census[rk][domain][str(h)]["15"]["pass"],
            }
            for domain, h in (("D0", 0), ("D1", 0), ("D1", 1), ("D2", 0), ("D2", 1), ("D2", 2))
        ]
        pareto[rk] = {domain: pareto_rows(census[rk], domain) for domain in DOMAINS_GLOBAL}
        g8[rk] = {}
        for domain in DOMAINS_GLOBAL:
            g8[rk][domain] = {}
            for h in DEPTHS[domain]:
                g8[rk][domain][str(h)] = {}
                for mask in MASKS:
                    global_pass = census[rk][domain][str(h)][str(mask)]["pass"]
                    g8[rk][domain][str(h)][str(mask)] = (
                        "global-information present; bounded locality unresolved"
                        if global_pass
                        else "information-loss certified on this finite ring/domain"
                    )

    g4_by_ring = {str(n): not census[str(n)]["D2"]["2"]["15"]["pass"] for n in RINGS}
    return {
        "protocol": "interface-history-global-20260912",
        "schema": 1,
        "source_hashes": {
            "script": sha(pathlib.Path(__file__)),
            "protocol": sha(PROTOCOL),
            "gate1_clarification": sha(CLARIFICATION),
            "predecessor_protocol": sha(PREV_PROTOCOL),
            "predecessor_script": sha(PREV_SCRIPT),
            "predecessor_result": sha(PREV_RESULT),
            "interface_factor_script": sha(FACTOR_SCRIPT),
            "interface_factor_result": sha(FACTOR_RESULT),
        },
        "parameters": {
            "rings": list(RINGS),
            "domains": {d: list(DOMAINS[d]) for d in DOMAINS_GLOBAL},
            "history_depths_by_domain": {d: list(DEPTHS[d]) for d in DOMAINS_GLOBAL},
            "masks": list(MASKS),
            "record_order": ["t", "source_pair_lex"],
            "history_order": "oldest-to-newest, then site index",
            "symbol_coordinate_order": list(COORDINATES),
            "primary_cells": 2 * 6 * 16,
        },
        "controls": {
            "G1_predecessor_source_hashes_and_full_state_local_regression": True,
            "G3_history_refinement_monotonicity": True,
            "G7_primary_reference_verdict_agreement_cells": reference_agreement,
            "G7_canonical_global_conflict_replays": conflict_replays,
        },
        "census": census,
        "G4_P15_h2_D2_global_conflict_by_ring": g4_by_ring,
        "G4_primary_bet_holds_both_rings": all(g4_by_ring.values()),
        "G5_P15_ladders": ladders,
        "G6_pareto_minimal": pareto,
        "G8_local_failure_classification": g8,
        "scope": "finite rings n=6,7; frozen source family; coarse transitions through t=6; h<=2; frozen masks; complete retained ring fields; no infinite-lattice/local-factor claim",
    }


def self_test() -> None:
    """Out-of-domain implementation checks only; no frozen n=6,7 census."""
    # Pure packing/masking check on synthetic data.
    x = np.array([[0, 1, 2], [3, 4, 5]], dtype=np.uint8)
    lo, hi = pack_chunks([x[:, 0], x[:, 1], x[:, 2]])
    assert lo.shape == (2,) and hi.shape == (2,)
    assert int(output_mask(63, 3)) != 0
    # Independent scalar/vector replay control on n=3, outside the scientific domain.
    replay_source(3, 0, 1)
    assert PROTOCOL.exists() and CLARIFICATION.exists() and PREV_RESULT.exists()
    print("interface-history-global implementation self-test passed (out-of-domain n=3; no canonical result written)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = evaluate()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "G4": result["G4_primary_bet_holds_both_rings"],
        "G4_by_ring": result["G4_P15_h2_D2_global_conflict_by_ring"],
        "P15_ladders": result["G5_P15_ladders"],
    }, sort_keys=True))
    print("written", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
