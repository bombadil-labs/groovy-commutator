#!/usr/bin/env python3
"""Exact image-graph and phase tests for one constant Groovy separator row.

--record pins this implementation before evaluation and refuses overwrite.
--check replays the bounded evidence and independently checks certificates.
An unsettled candidate remains explicit; no larger search is started here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
from groovy.groovy_field import g_word  # noqa: E402
from groovy_three_row_geometry import field_rows, scalar_rows  # noqa: E402

PROTOCOL = "docs/research/protocols/groovy-four-row-separator-20260922.md"
PROTOCOL_COMMIT = "28475d0de55491f86299cbcd704c9538d5805db2"
RECORD = ROOT / "results/groovy_four_row_separator_20260922.json"
PINNED = (PROTOCOL, "scripts/groovy_four_row_separator.py",
          "scripts/groovy_three_row_geometry.py", "src/groovy/ca.py",
          "src/groovy/groovy_field.py")


def scalar_g_window(word):
    def step(s):
        return tuple(a ^ (b | c) for a, b, c in zip(s, s[1:], s[2:]))
    s = tuple(map(int, word))
    e = step(s)
    return e[1] ^ step(e)[0] ^ step(tuple(a ^ b for a, b in zip(s[1:-1], e)))[0]


def image_graph():
    labels = g_word(np.arange(32, dtype=np.uint64), 5, 30).astype(int).tolist()
    assert labels == [scalar_g_window(format(w, "05b")) for w in range(32)]
    answers = []
    for bit in (0, 1):
        edges = [w for w in range(32) if labels[w] == bit]
        adjacency = [[w for w in edges if w >> 1 == u] for u in range(16)]
        colors = [0] * 16
        nodes, path_edges, cycle = [], [], None

        def visit(u):
            nonlocal cycle
            colors[u] = 1
            nodes.append(u)
            for w in adjacency[u]:
                v = w & 15
                if colors[v] == 1:
                    cycle = path_edges[nodes.index(v):] + [w]
                    return True
                if colors[v] == 0:
                    path_edges.append(w)
                    if visit(v):
                        return True
                    path_edges.pop()
            nodes.pop()
            colors[u] = 2
            return False

        for u in range(16):
            if colors[u] == 0 and visit(u):
                break
        if cycle is not None:
            source = "".join(str(w >> 4) for w in cycle)
            assert scalar_rows(source)[0] == str(bit) * len(source)
            answers.append({"bit": bit, "status": "cycle",
                            "edges": edges, "cycle_edges": cycle,
                            "periodic_source": source})
        else:
            rank = {}

            def depth(u):
                if u not in rank:
                    rank[u] = max((1 + depth(w & 15) for w in adjacency[u]), default=0)
                return rank[u]

            longest = max(depth(u) for u in range(16))
            start = next(u for u in range(16) if depth(u) == longest)
            path, u = [], start
            while depth(u):
                w = next(w for w in adjacency[u] if depth(w & 15) == depth(u) - 1)
                path.append(w)
                u = w & 15
            answers.append({"bit": bit, "status": "acyclic", "edges": edges,
                            "rank": [depth(u) for u in range(16)],
                            "max_run": longest, "longest_path_edges": path})
    record = {"truth_table_00000_to_11111": labels, "output_subgraphs": answers}
    verify_graph(record)
    return record


def verify_graph(record):
    labels = [scalar_g_window(format(w, "05b")) for w in range(32)]
    assert record["truth_table_00000_to_11111"] == labels
    for item in record["output_subgraphs"]:
        c = item["bit"]
        edges = [w for w, b in enumerate(labels) if b == c]
        assert item["edges"] == edges
        if item["status"] == "cycle":
            cycle = item["cycle_edges"]
            assert cycle and all(w in edges for w in cycle)
            assert all((a & 15) == (b >> 1) for a, b in zip(cycle, cycle[1:] + cycle[:1]))
            assert scalar_rows(item["periodic_source"])[0] == str(c) * len(item["periodic_source"])
        else:
            rank = item["rank"]
            assert len(rank) == 16 and all(type(r) is int and r >= 0 for r in rank)
            assert all(rank[w >> 1] >= 1 + rank[w & 15] for w in edges)
            path = item["longest_path_edges"]
            assert len(path) == item["max_run"] == max(rank)
            assert all(w in edges for w in path)
            assert all((a & 15) == (b >> 1) for a, b in zip(path, path[1:]))
    return True


def periodic_search(bit, max_period=12):
    counts = []
    for n in range(1, max_period + 1):
        seen, cases = {}, 0
        for value in range(1 << n):
            word = format(value, f"0{n}b")
            rows = field_rows(word)
            before = rows[:3] + [str(bit) * n]
            after = rows[1:] + [str(bit) * n]
            for phase in range(4):
                cases += 1
                key = tuple(before[(y + phase) % 4] for y in range(4))
                target = tuple(after[(y + phase) % 4] for y in range(4))
                old = seen.get(key)
                if old is not None and old["target"] != target:
                    example = {"source": word, "phase": phase, "g_rows": rows}
                    defect = next([x, y] for y in range(4) for x in range(n)
                                  if old["target"][y][x] != target[y][x])
                    cert = {"separator": bit, "horizontal_period": n,
                            "examples": [old["example"], example],
                            "input_rows": list(key),
                            "output_rows": [list(old["target"]), list(target)],
                            "defect_xy": defect}
                    counts.append({"period": n, "source_words_visited": value + 1,
                                   "phase_cases": cases, "complete": False})
                    assert verify_collision(cert)
                    return {"status": "whole_plane_collision", "counts": counts,
                            "certificate": cert}
                if old is None:
                    seen[key] = {"target": target,
                                 "example": {"source": word, "phase": phase,
                                             "g_rows": rows}}
        counts.append({"period": n, "source_words_visited": 1 << n,
                       "phase_cases": cases, "complete": True})
    return {"status": "local_test_pending", "counts": counts,
            "certificate": None}


def verify_collision(cert):
    n, bit = cert["horizontal_period"], cert["separator"]
    assert type(n) is int and 1 <= n <= 12 and bit in (0, 1)
    inputs, outputs = [], []
    assert len(cert["examples"]) == 2
    for example in cert["examples"]:
        word, p = example["source"], example["phase"]
        assert isinstance(word, str) and len(word) == n and not (set(word) - {"0", "1"})
        assert type(p) is int and 0 <= p < 4
        rows = scalar_rows(word)
        assert rows == example["g_rows"]
        inputs.append([rows[(y + p) % 4] if (y + p) % 4 < 3 else str(bit) * n
                       for y in range(4)])
        outputs.append([rows[1 + (y + p) % 4] if (y + p) % 4 < 3 else str(bit) * n
                        for y in range(4)])
    assert inputs[0] == inputs[1] == cert["input_rows"]
    assert outputs == cert["output_rows"] and outputs[0] != outputs[1]
    x, y = cert["defect_xy"]
    assert type(x) is int and type(y) is int and 0 <= x < n and 0 <= y < 4
    assert outputs[0][y][x] != outputs[1][y][x]
    return True


def evidence():
    graph = image_graph()
    candidates = []
    for item in graph["output_subgraphs"]:
        bit = item["bit"]
        if item["status"] == "acyclic":
            candidates.append({"separator": bit, "status": "recognizable_separator",
                               "max_data_run": item["max_run"],
                               "marker_detection_width": item["max_run"] + 1,
                               "construction_verification": "pending",
                               "periodic_search": "not_evaluated: marker construction applies",
                               "local_table_test": "not_evaluated: marker construction applies"})
        else:
            result = periodic_search(bit)
            result["separator"] = bit
            result["local_table_test"] = ("not_evaluated: whole-plane obstruction"
                                           if result["status"] == "whole_plane_collision"
                                           else "pending")
            candidates.append(result)
    return {"image_graph": graph, "candidates": candidates}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enforce_budget():
    resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))

    def expired(signum, frame):
        raise TimeoutError("120-second evaluation budget exhausted")

    signal.signal(signal.SIGALRM, expired)
    signal.alarm(120)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--record", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    hashes = {p: sha(ROOT / p) for p in PINNED}
    if args.record:
        if RECORD.exists():
            raise FileExistsError(f"refusing to overwrite {RECORD}")
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        for p in PINNED:
            assert subprocess.check_output(["git", "show", f"{head}:{p}"], cwd=ROOT) == (ROOT / p).read_bytes()
        result = {"schema_version": 1, "rule": 30, "memory": 3,
                  "source_cadence": 1, "vertical_period": 4,
                  "protocol_commit": PROTOCOL_COMMIT, "implementation_commit": head,
                  "source_hashes": hashes}
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
        record = json.loads(RECORD.read_text())
        assert record["source_hashes"] == hashes
        enforce_budget()
        actual = evidence()
        assert actual == {k: record[k] for k in ("image_graph", "candidates")}
        signal.alarm(0)
        print("PASS: source hashes, exact graph, bounded search and scalar certificates")


if __name__ == "__main__":
    main()
