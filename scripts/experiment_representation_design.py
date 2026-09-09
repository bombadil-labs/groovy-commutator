"""Research027: constructive representation design on the local partition lattice.

The expensive n=12 census is intentionally shardable by ECA rule range so the
frozen experiment can run in CI without changing its scientific definition.

Example:
    python scripts/experiment_representation_design.py \
        --rule-start 0 --rule-end 32 --output artifacts/repdesign-0-32.json

`rule_end` is exclusive.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from experiment_history_lift_closure import FULL_CLASS, state_map, compress  # noqa:E402

TOL = 1e-10
PROTOCOLS = [
    "docs/research/protocols/representation-design-20260908.md",
    "docs/research/protocols/representation-design-tail-20260908.md",
]


def partitions4() -> list[tuple[int, int, int, int]]:
    out = []
    def rec(prefix):
        if len(prefix) == 4:
            out.append(tuple(prefix)); return
        hi = max(prefix) + 1 if prefix else 0
        for x in range(hi + 1): rec(prefix + [x])
    rec([0])
    assert len(out) == 15 and len(set(out)) == 15
    return sorted(out, key=lambda p: (len(set(p)), p))


PARTITIONS = partitions4()
IDENTITY = (0, 1, 2, 3)
CONSTANT = (0, 0, 0, 0)
BINARY_TARGETS = [p for p in PARTITIONS if len(set(p)) == 2]
assert len(BINARY_TARGETS) == 7


def pkey(p): return "".join(map(str, p))
def refines(fine, coarse): return all(fine[i] != fine[j] or coarse[i] == coarse[j] for i in range(4) for j in range(4))
def is_cover(fine, coarse): return refines(fine, coarse) and len(set(fine)) == len(set(coarse)) + 1


REFINE_COVERS = {c: sorted([f for f in PARTITIONS if is_cover(f, c)], key=pkey) for c in PARTITIONS}
COARSEN_COVERS = {f: sorted([c for c in PARTITIONS if is_cover(f, c)], key=pkey) for f in PARTITIONS}


def entropy(labels):
    _, counts = np.unique(labels, return_counts=True)
    p = counts.astype(float) / len(labels)
    return float(-(p * np.log2(p)).sum())


def combine(a, b):
    aa = compress(a); bb = compress(b); k = int(bb.max()) + 1
    return compress(aa.astype(np.uint64) * np.uint64(k) + bb.astype(np.uint64))


def block_codes(n):
    states = np.arange(2**n, dtype=np.uint32)
    bits = ((states[:, None] >> np.arange(n, dtype=np.uint32)) & 1).astype(np.uint8)
    blocks = bits.reshape(len(states), n // 2, 2)
    return (blocks[:, :, 0] + 2 * blocks[:, :, 1]).astype(np.uint8)


def observation_from_partition(codes, partition):
    lut = np.asarray(partition, dtype=np.uint8); macro = lut[codes]; base = len(set(partition))
    weights = np.asarray([base**i for i in range(codes.shape[1])], dtype=np.uint64)
    return (macro.astype(np.uint64) * weights).sum(axis=1).astype(np.uint32)


def target_future_equivalence(step, target_obs, max_steps):
    states = np.arange(len(step), dtype=np.uint32); s = states.copy()
    target_labels = compress(target_obs); k = int(target_labels.max()) + 1
    labels = target_labels.copy(); count = int(labels.max()) + 1; future = [target_labels.copy()]
    for t in range(1, max_steps + 1):
        s = step[s]; y = target_labels[s]
        new = compress(labels.astype(np.uint64) * np.uint64(k) + y.astype(np.uint64))
        if int(new.max()) + 1 == count: return {"labels": labels, "hstar": t - 1, "future": future}
        labels = new; count = int(labels.max()) + 1; future.append(y.copy())
    raise RuntimeError(f"target future partition did not stabilize by {max_steps}")


def encoder_metrics(z_obs, target):
    z = compress(z_obs); hz = entropy(z); cinf = target["labels"]
    joint = combine(z, cinf); w = entropy(joint) - hz; final_count = int(joint.max()) + 1
    if w <= TOL: return {"H_encoder": hz, "W": 0.0, "tail": 0}
    current = z.copy()
    for t, y in enumerate(target["future"][1:], start=1):
        current = combine(current, y)
        if int(current.max()) + 1 == final_count: return {"H_encoder": hz, "W": w, "tail": t}
    raise AssertionError("encoder did not reach its full target-future partition")


def diagonal_metrics(step, obs, max_steps, n):
    fut = target_future_equivalence(step, obs, max_steps); hp = entropy(compress(obs)); hc = entropy(fut["labels"])
    return {"visible_bits": hp, "forgotten_bits": n - hp, "future_repertoire_bits": hc - hp, "shielded_bits": n - hc, "hstar": fut["hstar"]}


def pareto_nodes(nodes, interval, n):
    keep = set()
    for p in interval:
        fp = n - nodes[p]["H_encoder"]; wp = nodes[p]["W"]
        dominated = False
        for q in interval:
            if q == p: continue
            fq = n - nodes[q]["H_encoder"]; wq = nodes[q]["W"]
            if fq <= fp + TOL and wq >= wp - TOL and (fq < fp - TOL or wq > wp + TOL): dominated = True; break
        if not dominated: keep.add(p)
    return keep


def choose_close(current, target_p, nodes):
    scored = []
    for child in [p for p in REFINE_COVERS[current] if refines(p, target_p)]:
        dh = nodes[child]["H_encoder"] - nodes[current]["H_encoder"]
        if dh <= TOL: continue
        g = (nodes[current]["W"] - nodes[child]["W"]) / dh
        scored.append((-g, pkey(child), child))
    if not scored: raise AssertionError("nonclosed encoder has no refinement cover")
    return min(scored)[2]


def choose_poss(current, target_p, nodes):
    scored = []
    for coarse in [p for p in COARSEN_COVERS[current] if refines(p, target_p)]:
        dh = nodes[current]["H_encoder"] - nodes[coarse]["H_encoder"]
        if dh <= TOL: continue
        g = (nodes[coarse]["W"] - nodes[current]["W"]) / dh
        scored.append((-g, pkey(coarse), coarse))
    return min(scored)[2] if scored else None


def target_record(rule, target_p, step, observations, max_steps, n):
    target = target_future_equivalence(step, observations[target_p], max_steps)
    interval = [p for p in PARTITIONS if refines(p, target_p)]
    ht = entropy(compress(observations[target_p])); nodes = {}
    for p in interval:
        m = encoder_metrics(observations[p], target); m["added_bits"] = m["H_encoder"] - ht; nodes[p] = m
    base = nodes[target_p]
    assert base["tail"] == target["hstar"] and nodes[IDENTITY]["W"] <= TOL and nodes[IDENTITY]["tail"] == 0
    for coarse in interval:
        for fine in REFINE_COVERS[coarse]:
            if fine in nodes and nodes[fine]["W"] > nodes[coarse]["W"] + 1e-9: raise AssertionError((rule, target_p, "W monotonicity", coarse, fine))

    path = [target_p]; current = target_p
    while nodes[current]["W"] > TOL:
        current = choose_close(current, target_p, nodes); path.append(current)
    greedy_cost = nodes[current]["added_bits"]
    global_cost = min(nodes[p]["added_bits"] for p in interval if nodes[p]["W"] <= TOL)

    frontier = pareto_nodes(nodes, interval, n); ppath = [IDENTITY]; current = IDENTITY
    while current != target_p:
        nxt = choose_poss(current, target_p, nodes)
        if nxt is None: break
        ppath.append(nxt); current = nxt
    greedy_frontier_hits = sum(p in frontier for p in ppath)

    first = [p for p in REFINE_COVERS[target_p] if p in nodes]; bulk_scores = {}
    for p in first:
        dh = nodes[p]["H_encoder"] - nodes[target_p]["H_encoder"]
        bulk_scores[p] = (nodes[target_p]["W"] - nodes[p]["W"]) / dh
    max_bulk = max(bulk_scores.values()) if bulk_scores else float("nan")
    bulk_set = sorted([p for p, g in bulk_scores.items() if abs(g - max_bulk) <= 1e-10], key=pkey)
    tail_choice = sorted(first, key=lambda p: (nodes[p]["tail"], nodes[p]["W"], pkey(p)))[0] if first else None

    def brief(p): return {"partition": pkey(p), "H_encoder": nodes[p]["H_encoder"], "added_bits": nodes[p]["added_bits"], "W": nodes[p]["W"], "tail": nodes[p]["tail"]}
    return {"rule": rule, "wclass": FULL_CLASS[rule], "target": pkey(target_p), "closed": base["W"] <= TOL,
            "target_hstar": target["hstar"], "target_W": base["W"], "interval_nodes": len(interval),
            "greedy_closure_path": [pkey(p) for p in path], "greedy_added_bits": greedy_cost,
            "global_min_added_bits": global_cost, "greedy_globally_optimal": abs(greedy_cost - global_cost) <= 1e-9,
            "possibility_path": [pkey(p) for p in ppath], "possibility_path_frontier_fraction": greedy_frontier_hits / len(ppath),
            "pareto_nodes": sorted(pkey(p) for p in frontier), "bulk_first_split_set": [pkey(p) for p in bulk_set],
            "tail_first_split": pkey(tail_choice) if tail_choice else None,
            "bulk_tail_agree": tail_choice in bulk_set if tail_choice is not None else True,
            "first_split_nodes": [brief(p) for p in sorted(first, key=pkey)]}


def scan_rule(rule, n, max_steps):
    if n % 2: raise ValueError("representation-design lattice needs an even ring width")
    codes = block_codes(n); observations = {p: observation_from_partition(codes, p) for p in PARTITIONS}
    e = state_map(rule, n); step = e[e]
    diagonal = {p: diagonal_metrics(step, observations[p], max_steps, n) for p in PARTITIONS}
    drift = 0; edges = []
    for coarse in PARTITIONS:
        for fine in REFINE_COVERS[coarse]:
            dl = diagonal[coarse]["forgotten_bits"] - diagonal[fine]["forgotten_bits"]
            dv = diagonal[coarse]["future_repertoire_bits"] - diagonal[fine]["future_repertoire_bits"]
            if diagonal[fine]["future_repertoire_bits"] > diagonal[coarse]["future_repertoire_bits"] + TOL: drift += 1
            edges.append({"coarse": pkey(coarse), "fine": pkey(fine), "delta_forgetting": dl, "delta_repertoire": dv})
    assert abs(diagonal[IDENTITY]["forgotten_bits"]) <= TOL and abs(diagonal[IDENTITY]["future_repertoire_bits"]) <= TOL
    assert abs(diagonal[CONSTANT]["forgotten_bits"] - n) <= TOL and abs(diagonal[CONSTANT]["future_repertoire_bits"]) <= TOL
    return {"rule": rule, "wclass": FULL_CLASS[rule], "diagonal_target_drift_increasing_edges": drift,
            "diagonal_edges": edges, "targets": [target_record(rule, t, step, observations, max_steps, n) for t in BINARY_TARGETS]}


def source_hashes():
    paths = [Path(__file__), *(ROOT / p for p in PROTOCOLS)]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rule-start", type=int, default=0); ap.add_argument("--rule-end", type=int, default=256, help="exclusive")
    ap.add_argument("--n", type=int, default=12); ap.add_argument("--max-steps", type=int, default=128); ap.add_argument("--output", type=Path, required=True); args = ap.parse_args()
    if not (0 <= args.rule_start < args.rule_end <= 256): raise SystemExit("rule range must satisfy 0 <= start < end <= 256")
    result = {"experiment": "representation-design", "schema": 1, "ring_width": args.n,
              "rule_start": args.rule_start, "rule_end": args.rule_end, "rule_count": args.rule_end - args.rule_start,
              "source_hashes": source_hashes(), "rows": [scan_rule(r, args.n, args.max_steps) for r in range(args.rule_start, args.rule_end)]}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))


if __name__ == "__main__": main()
