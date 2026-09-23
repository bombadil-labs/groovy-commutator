#!/usr/bin/env python3
"""Complete-cone verification of the constant-row follow-up to PR #295.

The one-separator construction is evaluated on unpacked Boolean source
cones independently of its packed history table. The zero separator gets
the frozen complete 13-by-4 table test and an independent certificate/replay.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import signal
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
from groovy.separator_lift import (SOURCE_BITS, MASK, history_table, local_step,
                                   pack_rows, source_history_words, sorted_table,
                                   table_digest)  # noqa: E402
from groovy_four_row_separator import enforce_budget, verify_graph  # noqa: E402

IMAGE_RECORD = "results/groovy_four_row_separator_20260922.json"
RECORD = ROOT / "results/groovy_separator_lift_20260922.json"
PINNED = ("docs/research/protocols/groovy-four-row-separator-20260922.md",
          IMAGE_RECORD, "results/groovy_field_20260922/review_audit.json",
          "scripts/verify_groovy_separator_lift.py", "src/groovy/separator_lift.py",
          "scripts/groovy_four_row_separator.py", "scripts/groovy_three_row_geometry.py",
          "src/groovy/groovy_field.py", "src/groovy/ca.py")


def stencil_rows(history, separator, phase):
    rows = history + [np.full_like(history[0], int(MASK) * separator)]
    return [rows[(phase + dy) % 4] for dy in (-2, -1, 0, 1)]


def zero_table():
    size = 1 << SOURCE_BITS
    rows, centers = source_history_words(np.arange(size, dtype=np.uint64))
    keys = np.empty(4 * size, np.uint64)
    outputs = np.empty(4 * size, np.uint8)
    for phase in range(4):
        region = slice(phase * size, (phase + 1) * size)
        keys[region] = pack_rows(stencil_rows(rows, 0, phase))
        outputs[region] = centers[phase + 1] if phase < 3 else 0
    unique_keys, values, conflict = sorted_table(keys, outputs)
    if conflict is not None:
        examples = []
        for index in conflict:
            phase, word = divmod(index, size)
            patch = stencil_rows([row[word:word+1] for row in rows], 0, phase)
            examples.append({"source_window": format(word, "021b"), "phase": phase,
                             "patch_rows": [format(int(r[0]), "013b") for r in patch],
                             "output": int(outputs[index])})
        return {"separator": 0, "status": "local_stencil_conflict",
                "source_bits": 21, "phase_cases": 4 * size,
                "examples": examples, "scope": "13-by-4 stencil only"}
    return {"separator": 0, "status": "local_law", "source_bits": 21,
            "phase_cases": 4 * size, "forced_patterns": len(unique_keys),
            "table_sha256": table_digest(unique_keys, values)}


def unpacked_history(source):
    """Independent Boolean Rule-30 matrix computation, no packed CA arithmetic."""
    matrix = ((source[:, None] >> np.arange(20, -1, -1, dtype=np.uint32)) & 1).astype(np.uint8)

    def evolve(w):
        return w[:, :-2] ^ (w[:, 1:-1] | w[:, 2:])

    rows, centers = [], []
    for j in range(4):
        e = evolve(matrix)
        g = e[:, 1:-1] ^ evolve(e) ^ evolve(matrix[:, 1:-1] ^ e)
        c = g.shape[1] // 2
        centers.append(g[:, c])
        if j < 3:
            # Pack only at the interface to the binary local rule.
            row = np.zeros(len(source), dtype=np.uint64)
            for x in range(c - 6, c + 7):
                row = (row << np.uint64(1)) | g[:, x]
            rows.append(row)
            matrix = e
    return rows, centers


def verify_local_conflict(record):
    outputs = []
    for example in record["examples"]:
        w, phase = example["source_window"], example["phase"]
        assert len(w) == 21 and not (set(w) - {"0", "1"}) and phase in range(4)
        s = tuple(map(int, w))

        def evolve(v):
            return tuple(a ^ (b | c) for a, b, c in zip(v, v[1:], v[2:]))

        fields = []
        for j in range(4):
            e = evolve(s)
            g = tuple(a ^ b ^ c for a, b, c in zip(e[1:-1], evolve(e),
                      evolve(tuple(a ^ b for a, b in zip(s[1:-1], e)))))
            fields.append(g)
            s = e
        local = ["".join(map(str, row[len(row)//2-6:len(row)//2+7])) for row in fields[:3]] + ["0" * 13]
        patch = [local[(phase + dy) % 4] for dy in (-2, -1, 0, 1)]
        output = fields[phase + 1][len(fields[phase + 1])//2] if phase < 3 else 0
        assert patch == example["patch_rows"] and output == example["output"]
        outputs.append(output)
    assert record["examples"][0]["patch_rows"] == record["examples"][1]["patch_rows"]
    assert outputs[0] != outputs[1]
    return True


def independent_cone_replay(table, verify_zero):
    size = 1 << SOURCE_BITS
    keys = np.empty(4 * size, np.uint64) if verify_zero else None
    values = np.empty(4 * size, np.uint8) if verify_zero else None
    per_phase = [0] * 4
    for lo in range(0, size, 65536):
        hi = min(lo + 65536, size)
        rows, centers = unpacked_history(np.arange(lo, hi, dtype=np.uint32))
        for phase in range(4):
            patch = stencil_rows(rows, 1, phase)
            expected = centers[phase + 1] if phase < 3 else np.ones(hi-lo, np.uint8)
            actual = local_step(patch, table)
            if not np.array_equal(actual, expected):
                bad = int(np.flatnonzero(actual != expected)[0]) + lo
                raise ValueError(f"one-separator construction failed at {phase=}, source={bad}")
            per_phase[phase] += hi - lo
            if verify_zero:
                # Independent row ordering/key assembly for the zero table.
                all_rows = rows + [np.zeros(hi-lo, np.uint64)]
                key = np.zeros(hi-lo, np.uint64)
                for offset in (-2, -1, 0, 1):
                    key = key * np.uint64(8192) + all_rows[(phase + offset) % 4]
                region = slice(phase * size + lo, phase * size + hi)
                keys[region] = key
                values[region] = centers[phase + 1] if phase < 3 else 0
    zero = None
    if verify_zero:
        # Use a separate grouping expression rather than the primary helper.
        order = np.lexsort((values, keys))
        k, v = keys[order], values[order]
        eq = k[:-1] == k[1:]
        if np.any(eq & (v[:-1] != v[1:])):
            raise ValueError("independent zero-table replay found a conflict")
        first = np.r_[True, ~eq]
        raw = k[first].astype("<u8").tobytes() + v[first].tobytes()
        zero = {"forced_patterns": int(first.sum()), "table_sha256": hashlib.sha256(raw).hexdigest()}
    return {"one_separator_cases_by_phase": per_phase, "zero_table": zero}


def evidence():
    image = json.loads((ROOT / IMAGE_RECORD).read_text())
    assert verify_graph(image["image_graph"])
    one = next(x for x in image["image_graph"]["output_subgraphs"] if x["bit"] == 1)
    assert one["status"] == "acyclic" and one["max_run"] == 3
    table = history_table()
    digest = table_digest(*table)
    prior = json.loads((ROOT / "results/groovy_field_20260922/review_audit.json").read_text())
    known = next(x for x in prior["independent_laws"] if x["rule"] == 30)
    assert len(table[0]) == known["realized_patterns"] and digest == known["table_sha256"]
    zero = zero_table()
    if zero["status"] == "local_stencil_conflict":
        assert verify_local_conflict(zero)
    independent = independent_cone_replay(table, zero["status"] == "local_law")
    if zero["status"] == "local_law":
        assert independent["zero_table"] == {k: zero[k] for k in ("forced_patterns", "table_sha256")}
    return {"one_separator": {"status": "certified_constructive_law", "source_bits": 21,
                              "cases_by_phase": independent["one_separator_cases_by_phase"],
                              "history_patterns": len(table[0]), "history_table_sha256": digest,
                              "forbidden_data_word": "1111", "stencil": {"x": [-6, 6], "y": [-2, 1]},
                              "completion": "zero for invalid marker or absent history key"},
            "zero_separator": zero, "independent_zero_table": independent["zero_table"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--record", action="store_true")
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--integrity", action="store_true")
    args = parser.parse_args()
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in PINNED}
    if args.record:
        if RECORD.exists():
            raise FileExistsError(f"refusing to overwrite {RECORD}")
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        for p in PINNED:
            assert subprocess.check_output(["git", "show", f"{head}:{p}"], cwd=ROOT) == (ROOT / p).read_bytes()
        result = {"schema_version": 1, "implementation_commit": head, "source_hashes": hashes}
        enforce_budget()
        try:
            result.update(evidence())
        except (TimeoutError, MemoryError) as exc:
            result["evaluation_error"] = {"status": "resource_limit", "reason": str(exc)}
        finally:
            signal.alarm(0)
        with RECORD.open("x") as file:
            json.dump(result, file, indent=2)
            file.write("\n")
        print(json.dumps(result, indent=2))
    else:
        result = json.loads(RECORD.read_text())
        assert result["source_hashes"] == hashes
        if args.check:
            enforce_budget()
            assert evidence() == {k: result[k] for k in ("one_separator", "zero_separator", "independent_zero_table")}
            signal.alarm(0)
        print("PASS: separator-lift integrity" + (" and independent complete-cone replay" if args.check else ""))


if __name__ == "__main__":
    main()
