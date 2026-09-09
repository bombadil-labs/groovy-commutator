"""Research035 recovery: exact sofic slices with lazy nondeterministic accumulated union."""
from __future__ import annotations
import argparse, hashlib, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from experiment_window3_reachable_language import scan_rule as scan_research034  # noqa:E402
from experiment_reachable_context_invariants import DIAGONAL, FULL_CLASS, TARGETS, paired_table  # noqa:E402
from experiment_causal_witness_horizon import macro_rule  # noqa:E402
from sofic_graph import (  # noqa:E402
    ResourceCeiling,
    compress_block_language,
    disjoint_union,
    image_compressed,
    initial_one_seed_graph,
    language_inclusion,
)

PROTOCOL = "docs/research/protocols/sofic-defect-orbit-20260909.md"
RESOURCE_ADDENDUM = "docs/research/protocols/sofic-defect-orbit-resource-addendum-20260909.md"
RECOVERY_PROTOCOL = "docs/research/protocols/sofic-defect-orbit-lazy-union-recovery-20260909.md"
HMAX = 12
LIMITS = {
    "max_states": 200_000,
    "max_edges": 2_000_000,
    "max_subset_states": 500_000,
    "max_pretrim_edges": 5_000_000,
    "max_image_pair_states": 1_000_000,
}
MAX_INCLUSION_PAIRS = 2_000_000
MAX_LAZY_UNION_STATES = 1_000_000
MAX_LAZY_UNION_EDGES = 10_000_000

VISIBLE_TARGET_MASK = []
for p in range(64):
    a, b = divmod(p, 8)
    m = 0
    for tid, target in enumerate(TARGETS):
        if target[a] != target[b]:
            m |= 1 << tid
    VISIBLE_TARGET_MASK.append(m)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label_set(graph):
    return {label for _, label, _ in graph.edges}


def graph_visible_mask(graph) -> int:
    m = 0
    for label in label_set(graph):
        m |= VISIBLE_TARGET_MASK[label]
    return m


def bit_ids(mask: int):
    out = []
    while mask:
        bit = mask & -mask
        out.append(bit.bit_length() - 1)
        mask ^= bit
    return out


def target_mask(ids_) -> int:
    m = 0
    for tid in ids_:
        m |= 1 << int(tid)
    return m


def graph_stats(graph):
    return {"states": graph.n_states, "edges": graph.n_edges, "labels": len(label_set(graph))}


def build_lazy_union(slices):
    states = sum(g.n_states for g in slices)
    edges = sum(g.n_edges for g in slices)
    if states > MAX_LAZY_UNION_STATES:
        raise ResourceCeiling("lazy-union-states", MAX_LAZY_UNION_STATES, states)
    if edges > MAX_LAZY_UNION_EDGES:
        raise ResourceCeiling("lazy-union-edges", MAX_LAZY_UNION_EDGES, edges)
    return disjoint_union(slices), {"component_slices": len(slices), "pretrim_states": states, "pretrim_edges": edges}


def run_seed_recovery(rule: int, seed: int, incoming_target_ids: list[int]):
    ph = paired_table(macro_rule(rule))
    incoming = target_mask(incoming_target_ids)
    try:
        x, init_stats = compress_block_language(initial_one_seed_graph(DIAGONAL, seed), **LIMITS)
    except ResourceCeiling as exc:
        return {
            "incoming_target_ids": list(incoming_target_ids),
            "statuses": [{"target_id": tid, "status": "censored", "horizon": 0, "reason": exc.kind, "stage": "initial-slice"} for tid in incoming_target_ids],
            "censoring": {"horizon": 0, "stage": "initial-slice", "kind": exc.kind, "limit": exc.limit, "observed": exc.observed},
            "closure_horizon": None,
            "initial_compression": None,
            "slices": [],
        }

    slices = [x]
    first_witness = {}
    closure_at = None
    censoring = None
    records = []

    for t in range(HMAX + 1):
        visible = graph_visible_mask(x) & incoming
        for tid in bit_ids(visible):
            first_witness.setdefault(tid, t)
        if t <= 6 and visible:
            raise AssertionError((rule, seed, t, "Research032 h<=6 visibility regression", bit_ids(visible)))
        rec = {
            "horizon": t,
            "slice": graph_stats(x),
            "visible_target_ids": bit_ids(visible),
            "first_witness_target_ids_so_far": sorted(first_witness),
            "slice_count": len(slices),
        }
        if len(first_witness) == len(incoming_target_ids):
            records.append(rec)
            break
        if t == HMAX:
            records.append(rec)
            break

        try:
            nxt, image_stats = image_compressed(x, ph, **LIMITS)
            rec["next_image"] = {**graph_stats(nxt), **image_stats}
        except ResourceCeiling as exc:
            censoring = {"horizon": t, "stage": "image", "kind": exc.kind, "limit": exc.limit, "observed": exc.observed}
            rec["censored"] = censoring
            records.append(rec)
            break

        try:
            lazy, lazy_stats = build_lazy_union(slices)
            rec["lazy_union"] = {**graph_stats(lazy), **lazy_stats}
        except ResourceCeiling as exc:
            censoring = {"horizon": t, "stage": "lazy-union-size", "kind": exc.kind, "limit": exc.limit, "observed": exc.observed}
            rec["censored"] = censoring
            records.append(rec)
            break

        try:
            inclusion = language_inclusion(nxt, lazy, MAX_INCLUSION_PAIRS)
            rec["next_subset_lazy_union"] = inclusion[0]
            rec["inclusion_subset_pairs"] = inclusion[2]
            rec["inclusion_counterexample_length"] = len(inclusion[1]) if inclusion[1] else None
        except ResourceCeiling as exc:
            censoring = {"horizon": t, "stage": "inclusion", "kind": exc.kind, "limit": exc.limit, "observed": exc.observed}
            rec["censored"] = censoring
            records.append(rec)
            break

        records.append(rec)
        if inclusion[0]:
            closure_at = t
            break

        slices.append(nxt)
        x = nxt

    statuses = []
    for tid in incoming_target_ids:
        if tid in first_witness:
            statuses.append({"target_id": tid, "status": "finite-witness", "horizon": first_witness[tid]})
        elif closure_at is not None:
            statuses.append({"target_id": tid, "status": "finite-sofic-closure", "horizon": closure_at})
        elif censoring is not None:
            statuses.append({"target_id": tid, "status": "censored", "horizon": censoring["horizon"], "reason": censoring["kind"], "stage": censoring["stage"]})
        else:
            statuses.append({"target_id": tid, "status": "unresolved-through-12", "horizon": HMAX})

    return {
        "incoming_target_ids": list(incoming_target_ids),
        "initial_compression": init_stats,
        "closure_horizon": closure_at,
        "censoring": censoring,
        "statuses": statuses,
        "slices": records,
    }


def scan_rule(rule: int):
    base = scan_research034(rule)
    languages = []
    for lang in base["languages"]:
        incoming = list(lang["width3_unresolved_target_ids"])
        if not incoming:
            continue
        result = run_seed_recovery(rule, int(lang["seed_symbol"]), incoming)
        languages.append({
            "pair_index": lang["pair_index"],
            "pair": lang["pair"],
            "seed_symbol": lang["seed_symbol"],
            "width3_word_count": lang["width3_word_count"],
            "width3_rounds": lang["width3_rounds"],
            "is_r122_161_sentinel": lang["is_r122_161_sentinel"],
            **result,
        })
    counts = Counter(s["status"] for lang in languages for s in lang["statuses"])
    return {
        "rule": rule,
        "wclass": FULL_CLASS[rule],
        "research034_survivors": sum(len(l["width3_unresolved_target_ids"]) for l in base["languages"]),
        "survivor_seed_languages": len(languages),
        "status_counts": dict(counts),
        "languages": languages,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule-start", type=int, default=0)
    ap.add_argument("--rule-end", type=int, default=256)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if not (0 <= args.rule_start < args.rule_end <= 256):
        raise SystemExit("bad rule range")
    rows = [scan_rule(rule) for rule in range(args.rule_start, args.rule_end)]
    out = {
        "experiment": "sofic-defect-orbit-lazy-recovery",
        "schema": 1,
        "rule_start": args.rule_start,
        "rule_end": args.rule_end,
        "hmax": HMAX,
        "block_size": 3,
        "cadence": 3,
        "resource_limits": {
            **LIMITS,
            "max_inclusion_subset_pairs": MAX_INCLUSION_PAIRS,
            "max_lazy_union_states": MAX_LAZY_UNION_STATES,
            "max_lazy_union_edges": MAX_LAZY_UNION_EDGES,
        },
        "source_hashes": {
            "scripts/experiment_sofic_defect_orbit_lazy.py": file_hash(Path(__file__)),
            PROTOCOL: file_hash(ROOT / PROTOCOL),
            RESOURCE_ADDENDUM: file_hash(ROOT / RESOURCE_ADDENDUM),
            RECOVERY_PROTOCOL: file_hash(ROOT / RECOVERY_PROTOCOL),
        },
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    counts = Counter(s["status"] for r in rows for l in r["languages"] for s in l["statuses"])
    print(json.dumps({"rules": len(rows), "survivors": sum(r["research034_survivors"] for r in rows), "statuses": dict(counts)}, indent=2))


if __name__ == "__main__":
    main()
