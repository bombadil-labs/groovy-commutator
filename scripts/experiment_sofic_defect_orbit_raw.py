"""Note 036 / sofic-defect-orbit recovery: exact raw-NFA sofic slices with lazy accumulated union."""
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
from experiment_sofic_defect_orbit import target_id  # noqa:E402
from sofic_graph import (  # noqa:E402
    Graph,
    ResourceCeiling,
    disjoint_union,
    image_compressed,
    initial_one_seed_graph,
    language_inclusion,
    normalize_graph,
    trim_biinfinite,
)

PROTOCOL = "docs/research/protocols/sofic-defect-orbit-20260909.md"
RECOVERY_PROTOCOL = "docs/research/protocols/sofic-defect-orbit-raw-slice-recovery-20260909.md"
HMAX = 12
MAX_RAW_PAIR_STATES = 1_000_000
MAX_RAW_TRANSITIONS = 5_000_000
MAX_LAZY_UNION_STATES = 1_000_000
MAX_LAZY_UNION_EDGES = 10_000_000
MAX_INCLUSION_PAIRS = 2_000_000
CONTROL_COMPRESS_LIMITS = {
    "max_states": 200_000,
    "max_edges": 2_000_000,
    "max_subset_states": 500_000,
    "max_pretrim_edges": 5_000_000,
    "max_image_pair_states": 1_000_000,
}

VISIBLE_TARGET_MASK = []
for p in range(64):
    a, b = divmod(p, 8)
    mask = 0
    for tid, target in enumerate(TARGETS):
        if target[a] != target[b]:
            mask |= 1 << tid
    VISIBLE_TARGET_MASK.append(mask)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label_set(graph):
    return {label for _, label, _ in graph.edges}


def graph_visible_mask(graph) -> int:
    out = 0
    for label in label_set(graph):
        out |= VISIBLE_TARGET_MASK[label]
    return out


def graph_stats(graph):
    return {"states": graph.n_states, "edges": graph.n_edges, "labels": len(label_set(graph))}


def bit_ids(mask: int):
    out = []
    while mask:
        bit = mask & -mask
        out.append(bit.bit_length() - 1)
        mask ^= bit
    return out


def target_mask(ids_) -> int:
    out = 0
    for tid in ids_:
        out |= 1 << int(tid)
    return out


def raw_image_limited(graph, paired_rule):
    graph = trim_biinfinite(graph)
    source_edges = list(graph.edges)
    incoming = [[] for _ in range(graph.n_states)]
    outgoing = [[] for _ in range(graph.n_states)]
    for i, (a, _, b) in enumerate(source_edges):
        outgoing[a].append(i)
        incoming[b].append(i)

    pair_count = sum(len(incoming[m]) * len(outgoing[m]) for m in range(graph.n_states))
    if pair_count > MAX_RAW_PAIR_STATES:
        raise ResourceCeiling("raw-image-pair-states", MAX_RAW_PAIR_STATES, pair_count)

    pairs = []
    pair_id = {}
    for middle in range(graph.n_states):
        for e0 in incoming[middle]:
            for e1 in outgoing[middle]:
                pair_id[(e0, e1)] = len(pairs)
                pairs.append((e0, e1))

    transition_count = sum(len(outgoing[source_edges[e1][2]]) for e0, e1 in pairs)
    if transition_count > MAX_RAW_TRANSITIONS:
        raise ResourceCeiling("raw-image-transitions", MAX_RAW_TRANSITIONS, transition_count)

    edges = []
    for sid, (e0, e1) in enumerate(pairs):
        for e2 in outgoing[source_edges[e1][2]]:
            label = int(paired_rule[
                4096 * source_edges[e0][1]
                + 64 * source_edges[e1][1]
                + source_edges[e2][1]
            ])
            edges.append((sid, label, pair_id[(e1, e2)]))
    result = trim_biinfinite(normalize_graph(len(pairs), edges))
    return result, {
        "raw_pair_states": pair_count,
        "raw_pre_normalization_transitions": transition_count,
        "trimmed_states": result.n_states,
        "trimmed_edges": result.n_edges,
    }


def build_lazy_union(slices):
    states = sum(g.n_states for g in slices)
    edges = sum(g.n_edges for g in slices)
    if states > MAX_LAZY_UNION_STATES:
        raise ResourceCeiling("lazy-union-states", MAX_LAZY_UNION_STATES, states)
    if edges > MAX_LAZY_UNION_EDGES:
        raise ResourceCeiling("lazy-union-edges", MAX_LAZY_UNION_EDGES, edges)
    return disjoint_union(slices), {
        "component_slices": len(slices),
        "pretrim_states": states,
        "pretrim_edges": edges,
    }


def exact_equivalent(g1, g2):
    a = language_inclusion(g1, g2, MAX_INCLUSION_PAIRS, return_word=False)
    b = language_inclusion(g2, g1, MAX_INCLUSION_PAIRS, return_word=False)
    return a[0] and b[0], {"a_subset_b": a[2], "b_subset_a": b[2]}


def run_controls():
    rows = []
    specs = [
        (35, "00000001", (2, 6), 3),
        (5, "01001100", (0, 2), None),
    ]
    for rule, key, pair, expected in specs:
        tid = target_id(key)
        seed = 8 * pair[0] + pair[1]
        ph = paired_table(macro_rule(rule))
        x = initial_one_seed_graph(DIAGONAL, seed)
        first = None
        slices = []
        for t in range(4):
            visible = bool((graph_visible_mask(x) >> tid) & 1)
            if visible and first is None:
                first = t
            rec = {"horizon": t, **graph_stats(x), "target_visible": visible}
            if t < 3:
                raw, raw_stats = raw_image_limited(x, ph)
                compressed, comp_stats = image_compressed(x, ph, **CONTROL_COMPRESS_LIMITS)
                eq, eq_stats = exact_equivalent(raw, compressed)
                if not eq:
                    raise AssertionError((rule, t + 1, "raw/compressed mismatch"))
                rec["next_raw"] = {**graph_stats(raw), **raw_stats}
                rec["equivalence"] = {**eq_stats, "compressed": comp_stats}
                x = raw
            slices.append(rec)
        if expected is None:
            assert first is None, (rule, first)
        else:
            assert first == expected, (rule, first)
        rows.append({"rule": rule, "target": key, "pair": f"{pair[0]}-{pair[1]}", "first_visible": first, "slices": slices})

    rule = 5
    tid = target_id("01001100")
    seed = 2
    ph = paired_table(macro_rule(rule))
    x = initial_one_seed_graph(DIAGONAL, seed)
    slices = [x]
    closure_at = None
    orbit = []
    for t in range(4):
        assert not ((graph_visible_mask(x) >> tid) & 1)
        nxt, stats = raw_image_limited(x, ph)
        lazy, lazy_stats = build_lazy_union(slices)
        inc = language_inclusion(nxt, lazy, MAX_INCLUSION_PAIRS)
        orbit.append({
            "horizon": t,
            "next_subset_lazy_union": inc[0],
            "inclusion_pairs": inc[2],
            "counterexample_length": len(inc[1]) if inc[1] else None,
            "next": stats,
            "lazy": lazy_stats,
        })
        if inc[0]:
            closure_at = t
            break
        slices.append(nxt)
        x = nxt
    assert closure_at == 2, closure_at
    return {"ok": True, "cases": rows, "rule5_control_closure_horizon": closure_at, "rule5_orbit": orbit}


def run_seed(rule: int, seed: int, incoming_target_ids: list[int]):
    ph = paired_table(macro_rule(rule))
    incoming = target_mask(incoming_target_ids)
    x = initial_one_seed_graph(DIAGONAL, seed)
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
            nxt, image_stats = raw_image_limited(x, ph)
            rec["next_image"] = {**graph_stats(nxt), **image_stats}
        except ResourceCeiling as exc:
            censoring = {"horizon": t, "stage": "raw-image", "kind": exc.kind, "limit": exc.limit, "observed": exc.observed}
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
            inc = language_inclusion(nxt, lazy, MAX_INCLUSION_PAIRS)
            rec["next_subset_lazy_union"] = inc[0]
            rec["inclusion_subset_pairs"] = inc[2]
            rec["inclusion_counterexample_length"] = len(inc[1]) if inc[1] else None
        except ResourceCeiling as exc:
            censoring = {"horizon": t, "stage": "inclusion", "kind": exc.kind, "limit": exc.limit, "observed": exc.observed}
            rec["censored"] = censoring
            records.append(rec)
            break
        records.append(rec)
        if inc[0]:
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
    return {"incoming_target_ids": list(incoming_target_ids), "closure_horizon": closure_at, "censoring": censoring, "statuses": statuses, "slices": records}


def scan_rule(rule: int):
    base = scan_research034(rule)
    languages = []
    for lang in base["languages"]:
        incoming = list(lang["width3_unresolved_target_ids"])
        if not incoming:
            continue
        result = run_seed(rule, int(lang["seed_symbol"]), incoming)
        languages.append({
            "pair_index": lang["pair_index"],
            "pair": lang["pair"],
            "seed_symbol": lang["seed_symbol"],
            "width3_word_count": lang["width3_word_count"],
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
    ap.add_argument("--controls-only", action="store_true")
    args = ap.parse_args()
    if args.controls_only:
        out = {"experiment": "sofic-defect-orbit-raw-controls", "schema": 1, "controls": run_controls(), "source_hashes": {RECOVERY_PROTOCOL: file_hash(ROOT / RECOVERY_PROTOCOL), "scripts/experiment_sofic_defect_orbit_raw.py": file_hash(Path(__file__))}}
    else:
        if not (0 <= args.rule_start < args.rule_end <= 256):
            raise SystemExit("bad rule range")
        rows = [scan_rule(rule) for rule in range(args.rule_start, args.rule_end)]
        out = {
            "experiment": "sofic-defect-orbit-raw-recovery",
            "schema": 1,
            "rule_start": args.rule_start,
            "rule_end": args.rule_end,
            "hmax": HMAX,
            "block_size": 3,
            "cadence": 3,
            "resource_limits": {
                "max_raw_pair_states": MAX_RAW_PAIR_STATES,
                "max_raw_transitions": MAX_RAW_TRANSITIONS,
                "max_lazy_union_states": MAX_LAZY_UNION_STATES,
                "max_lazy_union_edges": MAX_LAZY_UNION_EDGES,
                "max_inclusion_subset_pairs": MAX_INCLUSION_PAIRS,
            },
            "source_hashes": {RECOVERY_PROTOCOL: file_hash(ROOT / RECOVERY_PROTOCOL), "scripts/experiment_sofic_defect_orbit_raw.py": file_hash(Path(__file__))},
            "rows": rows,
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    if args.controls_only:
        print(json.dumps({"ok": out["controls"]["ok"], "rule5_closure": out["controls"]["rule5_control_closure_horizon"]}, indent=2))
    else:
        counts = Counter(s["status"] for r in out["rows"] for l in r["languages"] for s in l["statuses"])
        print(json.dumps({"rules": len(out["rows"]), "survivors": sum(r["research034_survivors"] for r in out["rows"]), "statuses": dict(counts)}, indent=2))


if __name__ == "__main__":
    main()
