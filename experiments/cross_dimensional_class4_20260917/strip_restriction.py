#!/usr/bin/env python3
"""Exact periodic-strip restriction of outer-totalistic Life-like rules.

For strip height k, each vertical column is a symbol in an alphabet of size 2^k.
The 2D Moore rule becomes a 1D radius-one CA on those column symbols.
"""
from __future__ import annotations

import json
from pathlib import Path

PANEL = {
    "life": ((3,), (2,3)),
    "highlife": ((3,6), (2,3)),
    "day-night": ((3,6,7,8), (3,4,6,7,8)),
    "b35s236": ((3,5), (2,3,6)),
}


def bit(col: int, y: int, k: int) -> int:
    return (col >> (y % k)) & 1


def local_condition(L: int, C: int, R: int, y: int, k: int) -> tuple[int,int]:
    c = bit(C,y,k)
    n = 0
    for dy in (-1,0,1):
        for dx,col in ((-1,L),(0,C),(1,R)):
            if dx == 0 and dy == 0:
                continue
            n += bit(col,y+dy,k)
    return c,n


def reachable_conditions(k: int):
    witnesses = {}
    a = 1 << k
    for L in range(a):
        for C in range(a):
            for R in range(a):
                for y in range(k):
                    cond = local_condition(L,C,R,y,k)
                    witnesses.setdefault(cond, (L,C,R,y))
    return witnesses


def rule_output(births, survives, c, n):
    return int(n in (survives if c else births))


def strip_table(births, survives, k: int):
    a=1<<k
    table=[]
    for L in range(a):
        for C in range(a):
            for R in range(a):
                out=0
                for y in range(k):
                    c,n=local_condition(L,C,R,y,k)
                    out |= rule_output(births,survives,c,n)<<y
                table.append(out)
    return table


def eca_from_height1(births, survives):
    table=strip_table(births,survives,1)
    # table iteration order L,C,R binary equals code 4L+2C+R
    rule=0
    for code,out in enumerate(table):
        rule |= int(out)<<code
    return rule


def main():
    w1=reachable_conditions(1)
    w2=reachable_conditions(2)
    allconds={(c,n) for c in (0,1) for n in range(9)}
    assert set(w1)=={(0,0),(0,3),(0,6),(1,2),(1,5),(1,8)}
    assert set(w2)==allconds

    # k=1 depends on exactly six rule-table bits and is necessarily reflection symmetric.
    images={}
    for mask in range(1<<18):
        births=tuple(n for n in range(9) if (mask>>n)&1)
        survives=tuple(n for n in range(9) if (mask>>(9+n))&1)
        r=eca_from_height1(births,survives)
        images[r]=images.get(r,0)+1
    assert len(images)==64
    assert set(images.values())=={4096}
    assert all(((r>>1)&1)==((r>>4)&1) and ((r>>3)&1)==((r>>6)&1) for r in images)

    panel={}
    for name,(b,s) in PANEL.items():
        panel[name]={
            "births":list(b),"survives":list(s),
            "height1_eca":eca_from_height1(b,s),
            "height2_table_sha256": __import__('hashlib').sha256(bytes(strip_table(b,s,2))).hexdigest(),
        }

    life2 = strip_table(*PANEL["life"], 2)
    b352 = strip_table(*PANEL["b35s236"], 2)
    pair_cell_diffs = {}
    differing_triples = 0
    for idx, (a, b) in enumerate(zip(life2, b352)):
        if a == b:
            continue
        differing_triples += 1
        L, rem = divmod(idx, 16)
        C, R = divmod(rem, 4)
        for y in range(2):
            if ((a >> y) & 1) != ((b >> y) & 1):
                c, n = local_condition(L, C, R, y, 2)
                key = f"{'S' if c else 'B'}{n}"
                pair_cell_diffs[key] = pair_cell_diffs.get(key, 0) + 1

    payload={
        "height1":{
            "eca_rule_formula":"r = B0 + 18*B3 + 32*B6 + 4*S2 + 72*S5 + 128*S8",
            "linear_rank_over_gf2":6,
            "kernel_dimension_over_gf2":12,
            "reachable_conditions":[{"center":c,"neighbors":n} for c,n in sorted(w1)],
            "depends_on_rule_bits":["B0","B3","B6","S2","S5","S8"],
            "image_size":len(images),
            "image_characterization":"all 64 left-right-reflection-symmetric ECAs",
            "preimages_per_image":4096,
            "free_rule_bits":12,
        },
        "height2":{
            "reachable_condition_count":len(w2),
            "all_18_birth_survival_conditions_reachable":set(w2)==allconds,
            "therefore_restriction_is_injective_on_lifelike_rules":True,
            "witnesses":{
                f"{'S' if c else 'B'}{n}":{"L":L,"C":C,"R":R,"row":y}
                for (c,n),(L,C,R,y) in sorted(w2.items())
            },
        },
        "panel":panel,
        "pair_distinction_valuation": {
            "definition":"nu(F,G)=min{k in {1,2}: Res_k(F) != Res_k(G)} for distinct Life-like rules",
            "possible_values":[1,2],
            "height1_same_fiber_pair_count": 64 * ((4096 * 4095) // 2),
            "all_unordered_distinct_pair_count": ((1 << 18) * ((1 << 18) - 1)) // 2,
            "life_vs_b35s236": {
                "nu":2,
                "height2_differing_column_triples": differing_triples,
                "height2_differing_cell_outputs_by_hidden_rule_bit": pair_cell_diffs,
            },
        },
        "interpretation":(
            "Height 1 is a 12-bit-forgetting quotient from 18-bit Life-like rules to 64 symmetric ECAs. "
            "Height 2 already exposes every birth/survival condition, so the induced 4-state radius-one strip CA determines the full 2D outer-totalistic rule."
        ),
    }
    out=Path(__file__).resolve().parents[2]/"results/cross_dimensional_class4_20260917/strip_restriction_exact.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps(payload,indent=2,sort_keys=True))

if __name__=='__main__': main()
