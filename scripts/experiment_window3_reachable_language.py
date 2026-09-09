"""Research034: exact width-3 reachable paired-language invariant for Research033 survivors."""
from __future__ import annotations
import argparse, hashlib, json, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from experiment_reachable_context_invariants import (  # noqa:E402
    DIAGONAL,
    FULL_CLASS,
    PAIR_LIST,
    TARGETS,
    paired_table,
    scan as scan_research033,
    visible_mask,
)
from experiment_causal_witness_horizon import macro_rule  # noqa:E402

B = 64
PROTOCOL = "docs/research/protocols/window3-reachable-language-20260909.md"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_bits(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def initial_window3(seed: int) -> list[int]:
    rows = [0] * (B * B)
    d = DIAGONAL
    for a in d:
        for b in d:
            idx = B * a + b
            m = rows[idx]
            for c in d:
                m |= 1 << c
            rows[idx] = m
    for b in d:
        idx = B * seed + b
        m = rows[idx]
        for c in d:
            m |= 1 << c
        rows[idx] = m
    for a in d:
        idx = B * a + seed
        m = rows[idx]
        for c in d:
            m |= 1 << c
        rows[idx] = m
    bit = 1 << seed
    for a in d:
        for b in d:
            rows[B * a + b] |= bit
    assert sum(m.bit_count() for m in rows) == 704
    return rows


def window3_step(ph, rows: list[int]) -> list[int]:
    """One exact monotone closure step over admitted length-5 de Bruijn paths."""
    pred_out = [0] * (B * B)
    succ_out = [0] * (B * B)

    for c in range(B):
        base = B * c
        for d in range(B):
            idx = base + d
            mask = rows[idx]
            out = 0
            for e in iter_bits(mask):
                out |= 1 << int(ph[4096 * c + 64 * d + e])
            succ_out[idx] = out

    for a in range(B):
        abase = B * a
        for b in range(B):
            mask = rows[abase + b]
            if not mask:
                continue
            for c in iter_bits(mask):
                q0 = int(ph[4096 * a + 64 * b + c])
                pred_out[B * b + c] |= 1 << q0

    new = list(rows)
    buckets = [0] * B
    for b in range(B):
        bbase = B * b
        for c in range(B):
            idx = bbase + c
            dmask = rows[idx]
            q0mask = pred_out[idx]
            if not dmask or not q0mask:
                continue
            touched = []
            for d in iter_bits(dmask):
                q1 = int(ph[4096 * b + 64 * c + d])
                if buckets[q1] == 0:
                    touched.append(q1)
                buckets[q1] |= succ_out[B * c + d]
            for q1 in touched:
                q2mask = buckets[q1]
                for q0 in iter_bits(q0mask):
                    new[B * q0 + q1] |= q2mask
                buckets[q1] = 0
    return new


def window3_closure(ph, seed: int):
    rows = initial_window3(seed)
    rounds = 0
    while True:
        nxt = window3_step(ph, rows)
        rounds += 1
        if nxt == rows:
            return rows, rounds
        rows = nxt


def language_vertices(rows: list[int]) -> list[int]:
    vertices = set()
    for ab, mask in enumerate(rows):
        if not mask:
            continue
        a, b = divmod(ab, B)
        vertices.add(a)
        vertices.add(b)
        vertices.update(iter_bits(mask))
    return sorted(vertices)


def target_mask(ids_) -> int:
    m = 0
    for tid in ids_:
        m |= 1 << int(tid)
    return m


def mask_ids(mask: int):
    return list(iter_bits(mask))


def scan_rule(rule: int):
    base = scan_research033(rule)
    edge_survivors = sum(len(l["unresolved_target_ids"]) for l in base["languages"])
    ph = paired_table(macro_rule(rule))
    languages = []
    new_certificates = 0
    remaining = 0

    for lang in base["languages"]:
        if not lang["unresolved_target_ids"]:
            continue
        seed = int(lang["seed_symbol"])
        rows, rounds = window3_closure(ph, seed)
        count = sum(m.bit_count() for m in rows)
        assert 704 <= count <= B**3
        vertices = language_vertices(rows)
        visible = visible_mask(vertices)
        incoming = target_mask(lang["unresolved_target_ids"])
        certified = incoming & ~visible
        left = incoming & visible
        if certified & left:
            raise AssertionError((rule, seed, "classification overlap"))
        if certified | left != incoming:
            raise AssertionError((rule, seed, "classification loss"))
        occ = [m.bit_count() for m in rows]
        rec = {
            "pair_index": lang["pair_index"],
            "pair": lang["pair"],
            "seed_symbol": seed,
            "edge_count": lang["generated_edge_count"],
            "edge_rounds": lang["edge_rounds"],
            "incoming_target_ids": list(lang["unresolved_target_ids"]),
            "width3_certified_target_ids": mask_ids(certified),
            "width3_unresolved_target_ids": mask_ids(left),
            "width3_word_count": count,
            "width3_rounds": rounds,
            "width3_vertex_count": len(vertices),
            "max_row_occupancy": max(occ),
            "median_row_occupancy": statistics.median(occ),
            "is_r122_161_sentinel": rule in (122, 161),
        }
        languages.append(rec)
        new_certificates += certified.bit_count()
        remaining += left.bit_count()

    return {
        "rule": rule,
        "wclass": FULL_CLASS[rule],
        "research032_noncongruence_residual": base["noncongruence_residual"],
        "research033_edge_certificates": base["edge_certificates"],
        "research033_edge_survivors": edge_survivors,
        "survivor_seed_languages": len(languages),
        "width3_certificates": new_certificates,
        "remaining_after_width3": remaining,
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
        "experiment": "window3-reachable-language",
        "schema": 1,
        "rule_start": args.rule_start,
        "rule_end": args.rule_end,
        "block_size": 3,
        "cadence": 3,
        "window_width": 3,
        "source_hashes": {
            "scripts/experiment_window3_reachable_language.py": file_hash(Path(__file__)),
            PROTOCOL: file_hash(ROOT / PROTOCOL),
        },
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "rules": len(rows),
        "r033_survivors": sum(r["research033_edge_survivors"] for r in rows),
        "width3_certificates": sum(r["width3_certificates"] for r in rows),
        "remaining": sum(r["remaining_after_width3"] for r in rows),
        "languages": sum(r["survivor_seed_languages"] for r in rows),
    }, indent=2))


if __name__ == "__main__":
    main()
