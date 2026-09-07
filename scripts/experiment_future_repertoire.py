#!/usr/bin/env python3
"""Exact finite-ring continuation repertoires after two operation orders.

AB means chronologically A then B, hence X=B(A(S)); Y=A(B(S)).
For a declared open-loop alphabet {A,B}, R_h(S) contains endpoints of all
words of exactly h ticks. The recurrence R_h(S)=R_(h-1)(A(S)) union
R_(h-1)(B(S)) computes sets, while a separate word table preserves which
word reaches each endpoint. No fitted predictor or random sampling is used.

Run from any directory: python scripts/experiment_future_repertoire.py
Outputs are aggregates over every initial state, plus independently replayed
witnesses. They are exact only for the configured rings/panel/horizons.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import platform
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from groovy.ca import apply_rule, apply_rule_int  # noqa: E402

DEFAULT_PROTOCOL = ROOT / "docs/research/protocols/future-repertoire-20260907.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vector_step(value: int, n: int, rule: int) -> int:
    bits = np.array([(value >> i) & 1 for i in range(n)], dtype=np.uint8)
    return sum(int(bit) << i for i, bit in enumerate(apply_rule(bits, rule)))


def rule_map(n: int, rule: int) -> np.ndarray:
    # Existing integer engine is designed for exhaustive finite-state work.
    return np.fromiter((apply_rule_int(s, n, rule) for s in range(1 << n)),
                       dtype=np.uint16, count=1 << n)


def observe(values: np.ndarray, observation: str, popcounts: np.ndarray) -> np.ndarray:
    return values if observation == "identity" else popcounts[values]


def selected_witness(n, a, b, h, s, observation, x, y, rx, ry,
                     word_maps, popcounts, category):
    words = ["".join(w) for w in itertools.product("AB", repeat=h)]
    responses_x = observe(word_maps[:, x], observation, popcounts)
    responses_y = observe(word_maps[:, y], observation, popcounts)
    return {
        "category": category, "observation": observation,
        "n": n, "A": a, "B": b, "h": h, "initial_state": s,
        "prepared_AB": x, "prepared_BA": y,
        "outcomes_AB": np.flatnonzero(rx).tolist(),
        "outcomes_BA": np.flatnonzero(ry).tolist(),
        "responses": [{"word": w, "AB": int(u), "BA": int(v)}
                      for w, u, v in zip(words, responses_x, responses_y)],
    }


def replay_witness(witness):
    n, a, b, s = (witness[k] for k in ("n", "A", "B", "initial_state"))
    x = vector_step(vector_step(s, n, a), n, b)
    y = vector_step(vector_step(s, n, b), n, a)
    assert (x, y) == (witness["prepared_AB"], witness["prepared_BA"])
    outputs = [set(), set()]
    for response in witness["responses"]:
        for k, (state, label) in enumerate(((x, "AB"), (y, "BA"))):
            for letter in response["word"]:
                state = vector_step(state, n, a if letter == "A" else b)
            result = state if witness["observation"] == "identity" else state.bit_count()
            assert result == response[label]
            outputs[k].add(result)
    assert sorted(outputs[0]) == witness["outcomes_AB"]
    assert sorted(outputs[1]) == witness["outcomes_BA"]
    if witness["category"] == "strict_containment":
        assert outputs[0] < outputs[1] or outputs[1] < outputs[0]
    elif witness["category"] == "equal_size_different_sets":
        assert len(outputs[0]) == len(outputs[1]) and outputs[0] != outputs[1]
    else:
        assert outputs[0] == outputs[1]
        assert any(r["AB"] != r["BA"] for r in witness["responses"])


def run(protocol):
    assert protocol["observations"] == ["identity", "population_count"]
    assert protocol["horizons"] == list(range(7))
    assert all(1 <= n <= 15 for n in protocol["ring_widths"])
    assert protocol["rules"] == sorted(set(protocol["rules"]))
    rows, witnesses = [], {}
    checks = {"vector_engine_states_checked": 0,
              "direct_word_repertoires_checked": 0,
              "same_present_cases_checked": 0, "zero_horizon_cases_checked": 0,
              "identity_constant_word_endpoints_checked": 0}
    for n in protocol["ring_widths"]:
        count = 1 << n
        states = np.arange(count, dtype=np.uint16)
        popcounts = np.array([s.bit_count() for s in range(count)], dtype=np.uint8)
        maps = {r: rule_map(n, r) for r in protocol["rules"]}
        if n == 6:
            for rule, mapping in maps.items():
                assert all(int(mapping[s]) == vector_step(s, n, rule) for s in range(count))
                checks["vector_engine_states_checked"] += count
        for a, b in itertools.combinations(protocol["rules"], 2):
            x, y = maps[b][maps[a]], maps[a][maps[b]]
            noncommuting = x != y
            hamming = popcounts[x ^ y]
            word_maps = states[None, :]
            repertoires = {}
            for observation in protocol["observations"]:
                columns = count if observation == "identity" else n + 1
                r = np.zeros((count, columns), dtype=bool)
                r[states, observe(states, observation, popcounts)] = True
                repertoires[observation] = r
            for h in protocol["horizons"]:
                if h:
                    word_maps = np.stack((maps[a][word_maps], maps[b][word_maps]),
                                         axis=1).reshape(-1, count)
                    for observation, previous in list(repertoires.items()):
                        repertoires[observation] = previous[maps[a]] | previous[maps[b]]
                # Independent closed form for all words in the 0/identity control.
                if (a, b) == (0, 204):
                    for i, word in enumerate(itertools.product("AB", repeat=h)):
                        expected = np.zeros_like(states) if "A" in word else states
                        assert np.array_equal(word_maps[i], expected)
                        checks["identity_constant_word_endpoints_checked"] += count
                for observation, repertoire in repertoires.items():
                    if n == 6:
                        direct = np.zeros_like(repertoire)
                        endpoints = observe(word_maps, observation, popcounts)
                        direct[states[:, None], endpoints.T] = True
                        assert np.array_equal(repertoire, direct)
                        checks["direct_word_repertoires_checked"] += count
                    rx, ry = repertoire[x], repertoire[y]
                    size_x, size_y = rx.sum(axis=1), ry.sum(axis=1)
                    intersection = (rx & ry).sum(axis=1)
                    union = size_x + size_y - intersection
                    equal = intersection == union
                    x_subset = (intersection == size_x) & (size_x < size_y)
                    y_subset = (intersection == size_y) & (size_y < size_x)
                    unequal_size = size_x != size_y
                    changed_words = (observe(word_maps[:, x], observation, popcounts)
                                     != observe(word_maps[:, y], observation, popcounts))
                    changed_response = changed_words.any(axis=0)
                    same_set_changed_response = equal & changed_response
                    assert np.all(equal[~noncommuting])
                    assert not changed_response[~noncommuting].any()
                    assert np.all(size_x >= 1) and np.all(size_x <= 2 ** h)
                    assert np.all(size_y >= 1) and np.all(size_y <= 2 ** h)
                    checks["same_present_cases_checked"] += int((~noncommuting).sum())
                    if h == 0 and observation == "identity":
                        assert np.array_equal(~equal, noncommuting)
                        checks["zero_horizon_cases_checked"] += count
                    if (a, b) == (0, 204):
                        expected_sets = np.zeros_like(repertoire)
                        expected_sets[states, observe(states, observation, popcounts)] = True
                        if h: expected_sets[:, 0] = True
                        assert np.array_equal(repertoire, expected_sets)
                    row = {
                        "n": n, "A": a, "B": b, "h": h,
                        "observation": observation, "initial_states": count,
                        "action_words": 2 ** h,
                        "noncommuting_states": int(noncommuting.sum()),
                        "sum_prepared_hamming": int(hamming.sum()),
                        "different_sets": int((~equal).sum()),
                        "equal_sets": int(equal.sum()),
                        "unequal_sizes": int(unequal_size.sum()),
                        "equal_size_different_sets": int(((size_x == size_y) & ~equal).sum()),
                        "AB_strict_subset_BA": int(x_subset.sum()),
                        "BA_strict_subset_AB": int(y_subset.sum()),
                        "incomparable_sets": int((~equal & ~x_subset & ~y_subset).sum()),
                        "changed_response_maps": int(changed_response.sum()),
                        "equal_sets_different_maps": int(same_set_changed_response.sum()),
                        "different_prepared_equal_sets": int((noncommuting & equal).sum()),
                        "different_word_endpoints": int(changed_words.sum()),
                        "sum_repertoire_AB": int(size_x.sum()),
                        "sum_repertoire_BA": int(size_y.sum()),
                        "min_repertoire_AB": int(size_x.min()),
                        "max_repertoire_AB": int(size_x.max()),
                        "min_repertoire_BA": int(size_y.min()),
                        "max_repertoire_BA": int(size_y.max()),
                        "mean_jaccard_distance": float(np.mean(1 - intersection / union)),
                    }
                    assert row["equal_sets"] + row["different_sets"] == count
                    assert (row["equal_sets"] + row["AB_strict_subset_BA"]
                            + row["BA_strict_subset_AB"] + row["incomparable_sets"]) == count
                    rows.append(row)
                    if h:
                        candidates = {
                            "strict_containment": x_subset | y_subset,
                            "equal_size_different_sets": (size_x == size_y) & ~equal,
                            "equal_sets_different_response_map": same_set_changed_response,
                        }
                        for category, mask in candidates.items():
                            key = observation + ":" + category
                            matches = np.flatnonzero(mask & noncommuting)
                            if key not in witnesses and len(matches):
                                s = int(matches[0])
                                witnesses[key] = selected_witness(
                                    n, a, b, h, s, observation, int(x[s]), int(y[s]),
                                    rx[s], ry[s], word_maps, popcounts, category)
        print(f"Completed n={n}: all {count} states, 66 pairs, 7 horizons, 2 views", flush=True)
    for witness in witnesses.values(): replay_witness(witness)
    checks["witnesses_replayed"] = len(witnesses)
    checks["all_passed"] = True
    return rows, list(witnesses.values()), checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output-prefix", type=Path,
                        default=ROOT / "results/future_repertoire_20260907")
    args = parser.parse_args()
    protocol = json.loads(args.protocol.read_text())
    rows, witnesses, checks = run(protocol)
    prefix = args.output_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    with prefix.with_suffix(".csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    metadata = {
        "protocol": protocol, "protocol_sha256": digest(args.protocol),
        "script_sha256": digest(Path(__file__)),
        "ca_engine_sha256": digest(ROOT / "src/groovy/ca.py"),
        "python": platform.python_version(), "numpy": np.__version__,
        "aggregate_rows": len(rows),
        "cases_per_observation": sum(r["initial_states"] for r in rows if r["observation"] == "identity"),
        "checks": checks,
        "interpretation": "Exact bounded enumeration; shared cases are not independent replicates.",
    }
    Path(str(prefix) + "_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    Path(str(prefix) + "_witnesses.json").write_text(json.dumps(witnesses, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
