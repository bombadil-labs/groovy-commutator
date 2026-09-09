"""Research035: exact sofic orbit closure for one-defect paired block-3 ECA dynamics."""
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
    raw_image_graph,
)

PROTOCOL = "docs/research/protocols/sofic-defect-orbit-20260909.md"
RESOURCE_ADDENDUM = "docs/research/protocols/sofic-defect-orbit-resource-addendum-20260909.md"
HMAX = 12
LIMITS = {
    "max_states": 200_000,
    "max_edges": 2_000_000,
    "max_subset_states": 500_000,
    "max_pretrim_edges": 5_000_000,
    "max_image_pair_states": 1_000_000,
}
MAX_INCLUSION_PAIRS = 2_000_000

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


def target_id(key: str) -> int:
    target = tuple(map(int, key))
    return list(TARGETS).index(target)


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
        b = mask & -mask
        out.append(b.bit_length() - 1)
        mask ^= b
    return out


def target_mask(ids_) -> int:
    m = 0
    for tid in ids_:
        m |= 1 << int(tid)
    return m


def graph_stats(graph):
    return {"states": graph.n_states, "edges": graph.n_edges, "labels": len(label_set(graph))}


def exact_equivalent(g1, g2):
    a = language_inclusion(g1, g2, MAX_INCLUSION_PAIRS, return_word=False)
    b = language_inclusion(g2, g1, MAX_INCLUSION_PAIRS, return_word=False)
    return a[0] and b[0], {"a_subset_b_states": a[2], "b_subset_a_states": b[2]}


def run_compression_controls():
    cases = [
        {"rule": 35, "target": "00000001", "pair": (2, 6), "expected_first_visible": 3},
        {"rule": 5, "target": "01001100", "pair": (0, 2), "expected_first_visible": None},
    ]
    rows = []
    for spec in cases:
        rule = spec["rule"]
        tid = target_id(spec["target"])
        seed = 8 * spec["pair"][0] + spec["pair"][1]
        ph = paired_table(macro_rule(rule))
        x, init_stats = compress_block_language(initial_one_seed_graph(DIAGONAL, seed), **LIMITS)
        slices = []
        first_visible = None
        for t in range(4):
            visible = bool((graph_visible_mask(x) >> tid) & 1)
            if visible and first_visible is None:
                first_visible = t
            rec = {"horizon": t, **graph_stats(x), "target_visible": visible}
            if t < 3:
                raw = raw_image_graph(x, ph)
                direct, direct_stats = image_compressed(x, ph, **LIMITS)
                via, via_stats = compress_block_language(raw, **LIMITS)
                eq_raw_direct, ed1 = exact_equivalent(raw, direct)
                eq_raw_via, ed2 = exact_equivalent(raw, via)
                eq_direct_via, ed3 = exact_equivalent(direct, via)
                if not (eq_raw_direct and eq_raw_via and eq_direct_via):
                    raise AssertionError((rule, t + 1, "image/compression language mismatch"))
                rec["next_raw"] = graph_stats(raw)
                rec["next_compressed"] = graph_stats(direct)
                rec["equivalence_guard"] = {
                    "raw_direct": ed1,
                    "raw_via": ed2,
                    "direct_via": ed3,
                    "direct_compression": direct_stats,
                    "raw_compression": via_stats,
                }
                x = direct
            slices.append(rec)
        if spec["expected_first_visible"] is not None:
            assert first_visible == spec["expected_first_visible"], (spec, first_visible)
        else:
            assert first_visible is None, (spec, first_visible)
        rows.append({**spec, "seed_symbol": seed, "first_visible": first_visible, "initial_compression": init_stats, "slices": slices})

    rule = 5
    seed = 2
    tid = target_id("01001100")
    ph = paired_table(macro_rule(rule))
    x, _ = compress_block_language(initial_one_seed_graph(DIAGONAL, seed), **LIMITS)
    u = x
    orbit = []
    closure_at = None
    for t in range(3):
        assert not ((graph_visible_mask(x) >> tid) & 1)
        nxt, istats = image_compressed(x, ph, **LIMITS)
        inc = language_inclusion(nxt, u, MAX_INCLUSION_PAIRS)
        orbit.append({"horizon": t, "next_subset_accumulated": inc[0], "counterexample_length": len(inc[1]) if inc[1] else None, "inclusion_subset_pairs": inc[2], "image": istats})
        if inc[0]:
            closure_at = t
            break
        u_raw = disjoint_union([u, nxt])
        u, _ = compress_block_language(u_raw, **LIMITS)
        x = nxt
    if closure_at is None:
        raise AssertionError("Rule-5 sofic control failed to stabilize in bounded implementation control")
    return {"ok": True, "cases": rows, "rule5_control_closure_horizon": closure_at, "rule5_orbit": orbit}


def run_seed_orbit(rule: int, seed: int, incoming_target_ids: list[int], hmax: int = HMAX):
    ph = paired_table(macro_rule(rule))
    incoming = target_mask(incoming_target_ids)
    x, init_comp = compress_block_language(initial_one_seed_graph(DIAGONAL, seed), **LIMITS)
    u = x
    first_witness = {}
    closure_at = None
    censored = None
    slices = []

    for t in range(hmax + 1):
        visible = graph_visible_mask(x) & incoming
        for tid in bit_ids(visible):
            first_witness.setdefault(tid, t)
        if t <= 6 and visible:
            raise AssertionError((rule, seed, t, "Research032 h<=6 visibility regression", bit_ids(visible)))
        u_visible = graph_visible_mask(u) & incoming
        if set(bit_ids(u_visible)) != set(first_witness):
            raise AssertionError((rule, seed, t, "accumulated visibility mismatch", bit_ids(u_visible), first_witness))
        rec = {
            "horizon": t,
            "slice": graph_stats(x),
            "accumulated": graph_stats(u),
            "visible_target_ids": bit_ids(visible),
            "first_witness_target_ids_so_far": sorted(first_witness),
        }
        if len(first_witness) == len(incoming_target_ids):
            rec["all_targets_witnessed"] = True
            slices.append(rec)
            break
        if t == hmax:
            slices.append(rec)
            break
        try:
            nxt, image_stats = image_compressed(x, ph, **LIMITS)
            inclusion = language_inclusion(nxt, u, MAX_INCLUSION_PAIRS)
            rec["next_image"] = {**graph_stats(nxt), **image_stats}
            rec["next_subset_accumulated"] = inclusion[0]
            rec["inclusion_subset_pairs"] = inclusion[2]
            rec["inclusion_counterexample_length"] = len(inclusion[1]) if inclusion[1] else None
            if inclusion[0]:
                closure_at = t
                slices.append(rec)
                break
            u_raw = disjoint_union([u, nxt])
            u, union_stats = compress_block_language(u_raw, **LIMITS)
            rec["union_compression"] = union_stats
            x = nxt
            slices.append(rec)
        except ResourceCeiling as exc:
            censored = {"horizon": t, "kind": exc.kind, "limit": exc.limit, "observed": exc.observed}
            rec["censored"] = censored
            slices.append(rec)
            break

    statuses = []
    for tid in incoming_target_ids:
        if tid in first_witness:
            statuses.append({"target_id": tid, "status": "finite-witness", "horizon": first_witness[tid]})
        elif closure_at is not None:
            statuses.append({"target_id": tid, "status": "finite-sofic-closure", "horizon": closure_at})
        elif censored is not None:
            statuses.append({"target_id": tid, "status": "censored", "horizon": censored["horizon"], "reason": censored["kind"]})
        else:
            statuses.append({"target_id": tid, "status": f"unresolved-through-{hmax}", "horizon": hmax})

    return {
        "incoming_target_ids": list(incoming_target_ids),
        "initial_compression": init_comp,
        "closure_horizon": closure_at,
        "censoring": censored,
        "statuses": statuses,
        "slices": slices,
    }


def scan_rule(rule: int):
    base = scan_research034(rule)
    languages = []
    for lang in base["languages"]:
        incoming = list(lang["width3_unresolved_target_ids"])
        if not incoming:
            continue
        result = run_seed_orbit(rule, int(lang["seed_symbol"]), incoming)
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
    ap.add_argument("--controls-only", action="store_true")
    args = ap.parse_args()

    if args.controls_only:
        out = {
            "experiment": "sofic-defect-orbit-controls",
            "schema": 1,
            "controls": run_compression_controls(),
            "source_hashes": {
                "scripts/experiment_sofic_defect_orbit.py": file_hash(Path(__file__)),
                PROTOCOL: file_hash(ROOT / PROTOCOL),
                RESOURCE_ADDENDUM: file_hash(ROOT / RESOURCE_ADDENDUM),
            },
        }
    else:
        if not (0 <= args.rule_start < args.rule_end <= 256):
            raise SystemExit("bad rule range")
        rows = [scan_rule(rule) for rule in range(args.rule_start, args.rule_end)]
        out = {
            "experiment": "sofic-defect-orbit",
            "schema": 1,
            "rule_start": args.rule_start,
            "rule_end": args.rule_end,
            "hmax": HMAX,
            "block_size": 3,
            "cadence": 3,
            "resource_limits": {**LIMITS, "max_inclusion_subset_pairs": MAX_INCLUSION_PAIRS},
            "source_hashes": {
                "scripts/experiment_sofic_defect_orbit.py": file_hash(Path(__file__)),
                PROTOCOL: file_hash(ROOT / PROTOCOL),
                RESOURCE_ADDENDUM: file_hash(ROOT / RESOURCE_ADDENDUM),
            },
            "rows": rows,
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    if args.controls_only:
        print(json.dumps({"ok": out["controls"]["ok"], "rule5_control_closure_horizon": out["controls"]["rule5_control_closure_horizon"]}, indent=2))
    else:
        counts = Counter(s["status"] for r in out["rows"] for l in r["languages"] for s in l["statuses"])
        print(json.dumps({"rules": len(out["rows"]), "survivors": sum(r["research034_survivors"] for r in out["rows"]), "statuses": dict(counts)}, indent=2))


if __name__ == "__main__":
    main()
