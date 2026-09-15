#!/usr/bin/env python3
"""Independent full-offset audit of the partial-rule commutator census.

This reviewer does not import the new production keyer or analysis code.
It reconstructs physical neighborhoods with the earlier seven-offset DAG,
and derives native successors directly from recovered elementary source words.
Scientific replay belongs outside GitHub Actions.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import sys
import tarfile
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "experiments/commutator_completion_20260915"
PILOT = ROOT.parent / "gc-pilot"
sys.path.insert(0, str(PILOT / "scripts"))
from uniform_jet6_cache import PhysicalKeys

ARCHIVE = PILOT / "experiments/uniform_jet6_cache_20260914/run/uniform_jet6_rules.tar.gz"
FULL_D2 = ROOT / "experiments/beam_discriminator_loop_20260915/round01/tables.npz"


def sha(path):
    with Path(path).open("rb") as stream:
        h = hashlib.file_digest(stream, "sha256")
    return h.hexdigest()


def unpack(text, shape):
    raw = base64.b64decode(text, validate=True)
    n = int(np.prod(shape))
    assert len(raw) == (n + 7) // 8
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))
    assert not bits[n:].any()
    return bits[:n].reshape(shape)


def direct_patch(grid, flat, radius):
    source, *pos = np.unravel_index(flat, grid.shape)
    return tuple(int(grid[(source,) + tuple((p + a) % n for p, a, n in
                    zip(pos, offsets, grid.shape[1:]))])
                 for offsets in itertools.product(*(range(-r, r + 1) for r in radius)))


def scalar_eca(words, rule):
    out = np.zeros_like(words)
    # Truth-table summands provide a separate implementation from bit-index lookup.
    for left, center, right in itertools.product((0, 1), repeat=3):
        if (rule >> (4 * left + 2 * center + right)) & 1:
            out |= ((np.roll(words, 1, -1) == left) & (words == center)
                    & (np.roll(words, -1, -1) == right)).astype(np.uint8)
    return out


def bit_integer(bits):
    result = 0
    for b in bits:
        result = (result << 1) | int(b)
    return result


def summarize(variables, constant):
    """Variable -1 denotes a forced cell; IDs otherwise have no numerical meaning."""
    free = variables >= 0
    active, inverse, counts = np.unique(variables[free], return_inverse=True, return_counts=True)
    per_state = []
    state_occurrences = {}
    for row in variables:
        ids = np.unique(row[row >= 0])
        per_state.append(len(ids))
        for q in ids:
            state_occurrences[int(q)] = state_occurrences.get(int(q), 0) + 1
    zeros = np.bincount(inverse[constant[free] == 0], minlength=len(active)).astype(np.int64)
    ones = counts - zeros
    same = sum(int(a) * (int(a) - 1) // 2 + int(b) * (int(b) - 1) // 2 for a, b in zip(zeros, ones))
    opposite = sum(int(a) * int(b) for a, b in zip(zeros, ones))
    phases = []
    for phase in itertools.product(range(6), repeat=variables.ndim - 2):
        f = free[(slice(None),) + phase + (slice(None),)]
        c = constant[(slice(None),) + phase + (slice(None),)]
        phases.append({"phase": list(phase), "fixed_zero": int(np.count_nonzero(~f & (c == 0))),
                       "fixed_one": int(np.count_nonzero(~f & (c == 1))), "free": int(f.sum())})
    return {"cells": int(free.size), "fixed_zero": int(np.count_nonzero(~free & (constant == 0))),
            "fixed_one": int(np.count_nonzero(~free & (constant == 1))), "free": int(free.sum()),
            "variables": int(len(active)), "per_state_variables": per_state,
            "variables_shared_across_states": sum(n > 1 for n in state_occurrences.values()),
            "same_pairs": same, "opposite_pairs": opposite, "phases": phases,
            "occurrences_sorted": sorted(int(n) for n in counts)}


def decode_record(record):
    g = unpack(record["grid_bits_big"], record["grid_shape"])
    width, rule, dim = record["width"], record["rule"], record["dimension"]
    assert g.shape == (1 << width,) + (6,) * (dim - 1) + (width,)
    count = record["forced_root_count"]
    flips = unpack(record["forced_derivative_bits_big"], (count,))
    dec = unpack(record["forced_decoder_bits_big"], (count,))
    assert hashlib.sha256(flips.tobytes() + dec.tobytes()).hexdigest() == record["native_table_sha256"]
    representatives = np.frombuffer(base64.b64decode(record["representative_flat_indices_u32le"], validate=True), dtype="<u4")
    assert len(representatives) == count
    keyer = PhysicalKeys(record["radii_array_order"])
    keys = keyer.keys(g)
    forced_keys = keys.ravel()[representatives]
    assert len(np.unique(forced_keys)) == count
    assert np.array_equal(np.sort(forced_keys), np.unique(keys))
    assert np.array_equal(representatives, np.unique(keys.ravel(), return_index=True)[1])
    table = np.full(int(keys.max()) + 1, -1, dtype=np.int8)
    table[forced_keys] = flips
    assert (table[keys] >= 0).all()

    root_words = g
    while root_words.ndim > 2:
        root_words = root_words[:, 4] ^ root_words[:, 5]
    expected_words = ((np.arange(1 << width)[:, None] >> np.arange(width - 1, -1, -1)) & 1).astype(np.uint8)
    assert np.array_equal(root_words, expected_words)
    next_root = scalar_eca(root_words, rule)
    successor = next_root @ (1 << np.arange(width - 1, -1, -1))
    assert np.array_equal(g ^ table[keys], g[successor])
    # Decoder values must recover the immediate parent at every physical phase.
    decode_table = np.empty(len(table), dtype=np.uint8)
    decode_table[forced_keys] = dec
    parent = g[:, 4] ^ g[:, 5]
    assert np.array_equal(decode_table[keys], np.broadcast_to(parent[:, None], g.shape))

    difference = g ^ g[successor]
    two_step = g ^ g[successor[successor]]
    dkeys = keyer.keys(difference)
    alltable = np.full(len(keyer.nodes[-1]), -1, dtype=np.int8)
    alltable[forced_keys] = flips
    pinned = alltable[dkeys]
    free = pinned < 0
    constants = two_step.copy()
    constants[~free] ^= pinned[~free].astype(np.uint8)
    variables = np.where(free, dkeys.astype(np.int64), -1)
    family = {row.tobytes(): i for i, row in enumerate(g)}
    assert len(family) == len(g)
    difference_index = np.array([family.get(row.tobytes(), -1) for row in difference], dtype=np.int64)
    for event in sorted({0, g.size // 3, g.size // 2, g.size - 1}):
        assert keyer.expand(keys.ravel()[event]) == direct_patch(g, event, record["radii_array_order"])
        assert keyer.expand(dkeys.ravel()[event]) == direct_patch(difference, event, record["radii_array_order"])
    return {"grid": g, "keyer": keyer, "keys": keys, "forced_keys": forced_keys,
            "flips": flips, "successor": successor, "difference": difference,
            "two_step": two_step, "dkeys": dkeys, "variables": variables,
            "constant": constants, "difference_index": difference_index}


def full_input(record, info, tables):
    assert record["dimension"] == 2
    rule = record["rule"]
    keys = tables[f"r{rule:03d}_keys"]
    masks = tables[f"r{rule:03d}_native"]
    assert np.isin(masks, (1, 2)).all()
    lookup = {int(k): int(m == 2) for k, m in zip(keys, masks)}
    keyer = info["keyer"]
    physical = np.array([bit_integer(keyer.expand(i)) for i in range(len(keyer.nodes[-1]))], dtype=np.uint64)
    assert len(np.unique(physical)) == len(physical)
    for k, value in zip(info["forced_keys"], info["flips"]):
        assert lookup[int(physical[k])] == int(value)
    lut = np.array([lookup.get(int(q), -1) for q in physical], dtype=np.int8)
    pinned = lut[info["dkeys"]]
    free = pinned < 0
    constant = info["two_step"].copy()
    constant[~free] ^= pinned[~free].astype(np.uint8)
    variables = np.where(free, info["dkeys"].astype(np.int64), -1)
    return {"variables": variables, "constant": constant, "physical": physical}


def physical_remap(info, arrays):
    """Map each production DAG identifier to the separately rebuilt seven-child DAG."""
    old = info["keyer"].nodes
    leaf = {}
    for ident, children in enumerate(old[0]):
        assert children[-1] == children[0]
        packed = 0
        for child in children[:-1]:
            packed = (packed << 5) | child
        assert packed not in leaf
        leaf[packed] = ident
    previous = None
    for depth in range(len(old) - 1):
        nodes = arrays[f"dag_{depth}"]
        assert nodes.ndim == 2 and nodes.shape[1] == 6
        expected = {tuple(children): ident for ident, children in enumerate(old[depth + 1])}
        mapped = np.empty(len(nodes), dtype=np.int64)
        for ident, children in enumerate(nodes):
            expanded = tuple(leaf[int(q)] if depth == 0 else int(previous[q]) for q in children)
            mapped[ident] = expected[expanded + expanded[:1]]
        assert len(np.unique(mapped)) == len(mapped)
        previous = mapped
    if previous is None:
        return lambda q: np.array([leaf[int(k)] for k in np.asarray(q).ravel()], dtype=np.int64).reshape(np.asarray(q).shape)
    return lambda q: previous[np.asarray(q)]


def compare_contract(record, info, contract, expected, arrays, meta, remap):
    prefix = contract + "_"
    labels = arrays[prefix + "g_symbol"]
    assert labels.shape == info["grid"].shape
    variables, constant = expected["variables"], expected["constant"]
    assert np.array_equal(labels == 0, variables < 0)
    packed = arrays[prefix + "g_constant_bits"]
    bits = np.unpackbits(packed)
    assert not bits[constant.size:].any()
    assert np.array_equal(bits[:constant.size].reshape(constant.shape), constant)
    free_ids = remap(arrays[prefix + "free_keys"])
    assert len(np.unique(free_ids)) == len(free_ids)
    assert np.array_equal(np.sort(free_ids), np.unique(variables[variables >= 0]))
    assert labels.max(initial=0) == len(free_ids)
    active = labels > 0
    assert np.array_equal(free_ids[labels[active] - 1], variables[active])

    counts = np.bincount(labels.ravel(), minlength=len(free_ids) + 1)[1:]
    ones = np.bincount(labels[constant == 1], minlength=len(free_ids) + 1)[1:]
    state_uses = np.zeros(len(free_ids), dtype=np.int64)
    for row in labels:
        at = np.unique(row)
        state_uses[at[at > 0] - 1] += 1
    assert np.array_equal(counts, arrays[prefix + "variable_occurrences"])
    assert np.array_equal(ones, arrays[prefix + "variable_one_constants"])
    assert np.array_equal(state_uses, arrays[prefix + "variable_state_uses"])

    summary = summarize(variables, constant)
    target = meta["contracts"][contract]
    mapping = {"cells": "cells", "fixed_zero": "fixed_zero", "fixed_one": "fixed_one", "free": "free_cells",
               "variables": "free_keys", "per_state_variables": "per_state_free_keys",
               "variables_shared_across_states": "variables_shared_across_states",
               "same_pairs": "equal_G_pairs_from_shared_variable", "opposite_pairs": "opposite_G_pairs_from_shared_variable"}
    for our, their in mapping.items():
        assert summary[our] == target[their], (meta["id"], contract, our, summary[our], target[their])
    assert target["log2_distinct_joint_G_fields"] == len(free_ids)
    assert target["free_fraction"] == float(active.mean())
    assert target["per_state_free_cells"] == active.sum(axis=tuple(range(1, active.ndim))).tolist()
    assert target["free_cells_by_newest_phase"] == active.sum(axis=(0,) + tuple(range(2, active.ndim))).tolist()
    no_free = np.array(summary["per_state_variables"]) == 0
    in_family = info["difference_index"] >= 0
    assert np.all(no_free[in_family])
    assert target["fully_fixed_states"] == int(no_free.sum())
    assert target["difference_in_family_states"] == int(in_family.sum())
    assert target["fully_fixed_off_family_states"] == int((no_free & ~in_family).sum())
    assert target["variable_state_uses_sum"] == int(state_uses.sum())
    assert target["mean_variable_occurrences"] == (float(counts.mean()) if len(counts) else 0.0)
    assert target["max_variable_occurrences"] == (int(counts.max()) if len(counts) else 0)

    # Construct the origin and single-bit alternative completion explicitly on
    # every query used by the native commutator definition.
    pinned_delta = constant ^ info["two_step"]
    h_difference = info["difference"] ^ pinned_delta
    next_state = info["grid"][info["successor"]]
    next_next = info["grid"][info["successor"][info["successor"]]]
    assert np.array_equal((next_state ^ next_next) ^ h_difference, constant)
    witness = target["witness"]
    if len(free_ids):
        chosen = int(free_ids[0])
        occurrence = info["dkeys"] == chosen
        event = int(np.flatnonzero(occurrence)[0])
        assert not np.any(info["keys"] == chosen)
        assert np.array_equal((next_state ^ next_next) ^ (h_difference ^ occurrence), constant ^ occurrence)
        assert witness["query_key_id"] == int(arrays[prefix + "free_keys"][0])
        assert witness["symbol"] == 1
        assert witness["event"] == list(map(int, np.unravel_index(event, constant.shape)))
        literal = direct_patch(info["difference"], event, record["radii_array_order"])
        assert witness["physical_bits"] == "".join(map(str, literal))
        assert literal == info["keyer"].expand(chosen)
        assert witness["origin_G"] == int(constant.ravel()[event])
        assert witness["flipped_G"] == int(constant.ravel()[event] ^ 1)
        assert witness["changed_cells"] == int(occurrence.sum())
    else:
        assert witness is None
    if record["rule"] in (0, 204):
        assert not active.any() and not constant.any()
    return {k: summary[k] for k in ("cells", "fixed_zero", "fixed_one", "free", "variables",
                                    "variables_shared_across_states", "same_pairs", "opposite_pairs")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=ARCHIVE)
    parser.add_argument("--follow", action="store_true", help="Review completed atomic records while the primary census runs")
    args = parser.parse_args()
    started = time.perf_counter()
    primary_path = UNIT / "result.json"
    wait_seconds = 0.0
    def await_path(path):
        nonlocal wait_seconds
        before = time.perf_counter()
        while not path.exists():
            if not args.follow or time.perf_counter() - before > 1200:
                raise FileNotFoundError(path)
            time.sleep(0.5)
        wait_seconds += time.perf_counter() - before
    freeze_path = UNIT / "freeze.json"
    await_path(freeze_path)
    freeze = json.loads(freeze_path.read_text())
    assert sha(args.archive) == freeze["raw_input_hashes"]["uniform_jet6_rules.tar.gz"] == "766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1"
    assert sha(FULL_D2) == freeze["raw_input_hashes"][str(FULL_D2.relative_to(ROOT))]
    for name, digest in freeze["source_hashes"].items():
        assert sha(ROOT / name) == digest
    expected = {f"w{w}/rule{r:03d}/d{d}.json": f"w{w}_r{r:03d}_d{d}" for w in (7, 8) for r in range(256) for d in (2, 3, 4)}
    assert len(expected) == 1536
    evidence, metadata = [], []
    with np.load(FULL_D2) as full, tarfile.open(args.archive, "r|gz") as archive:
        for member in archive:
            if member.name not in expected:
                continue
            saved_meta = UNIT / "records" / (expected[member.name] + ".json")
            await_path(saved_meta)
            meta = json.loads(saved_meta.read_text())
            assert meta["id"] == expected[member.name] and meta["archive_member"] == member.name
            raw = archive.extractfile(member).read()
            assert hashlib.sha256(raw).hexdigest() == meta["archive_member_sha256"]
            record = json.loads(raw)
            assert [record[k] for k in ("width", "rule", "dimension")] == [meta[k] for k in ("width", "rule", "dimension")]
            path = ROOT / meta["arrays_file"]
            assert sha(path) == meta["arrays_sha256"]
            assert path.stat().st_size == meta["arrays_bytes"]
            info = decode_record(record)
            with np.load(path) as arrays:
                assert np.array_equal(arrays["next_index"], info["successor"])
                assert np.array_equal(arrays["difference_in_family"], info["difference_index"] >= 0)
                remap = physical_remap(info, arrays)
                pinned = remap(arrays["pinned_keys"])
                lut = {int(k): int(v) for k, v in zip(info["forced_keys"], info["flips"])}
                assert len(pinned) == len(lut) == meta["forced_keys"]
                assert np.array_equal(np.sort(pinned), np.sort(info["forced_keys"]))
                assert np.array_equal(arrays["pinned_values"], [lut[int(k)] for k in pinned])
                contracts = {"finite": compare_contract(record, info, "finite", info, arrays, meta, remap)}
                if record["dimension"] == 2:
                    independent_full = full_input(record, info, full)
                    contracts["full_input_d2"] = compare_contract(record, info, "full_input_d2", independent_full, arrays, meta, remap)
                    resolved = contracts["finite"]["free"] - contracts["full_input_d2"]["free"]
                    assert resolved == meta["finite_free_cells_resolved_by_full_input"] >= 0
            evidence.append({"id": meta["id"], "contracts": contracts})
            metadata.append(meta)
            if len(evidence) % 24 == 0:
                print(json.dumps({"reviewed_records": len(evidence), "last": meta["id"],
                                  "seconds": round(time.perf_counter() - started, 3)}), flush=True)
    assert len(evidence) == 1536
    await_path(primary_path)
    primary = json.loads(primary_path.read_text())
    assert primary["completed_records"] == primary["expected_records"] == 1536
    assert primary["censored_records"] == 0 and not primary["budget_expired"]
    assert primary["source_hashes"] == freeze["source_hashes"]
    assert primary["raw_input_hashes"] == freeze["raw_input_hashes"]
    assert primary["controls"] == {"enumerated_completions": 4, "distinct_G_fields": 4, "scalar_identity_cases": 16}
    assert primary["records"] == metadata
    assert primary["raw_arrays_bytes"] == sum(r["arrays_bytes"] for r in metadata)
    result = {"reviewer": "Codex (OpenAI), independent agent /root/g_completion_review",
              "method": "Original full seven-offset PhysicalKeys; independently recovered native root successors; all saved physical-key DAGs, symbolic cells, counts and two-completion witnesses replayed",
              "primary_result_sha256": sha(primary_path), "review_source_sha256": sha(__file__),
              "archive_sha256": sha(args.archive), "full_d2_tables_sha256": sha(FULL_D2),
              "keyer_source_sha256": sha(PILOT / "scripts/uniform_jet6_cache.py"),
              "reviewed_records": len(evidence), "reviewed_contracts": sum(len(r["contracts"]) for r in evidence),
              "python": platform.python_version(), "numpy": np.__version__,
              "seconds": time.perf_counter() - started,
              "waiting_for_primary_record_seconds": wait_seconds,
              "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "all_checks_passed": True, "records": evidence}
    output = ROOT / "review/commutator_completion_independent.json"
    output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"}), flush=True)


if __name__ == "__main__":
    main()
