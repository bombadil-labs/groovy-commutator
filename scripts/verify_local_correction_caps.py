#!/usr/bin/env python3
"""Exact full-shift cap census; frozen protocol local-correction-caps-20260910.

Source words and tuple patches are packed left-to-right, most significant
bit first. Tuple components are concatenated in increasing j. No torus.
The second evaluator uses tuples, shrinking evolution, and recursive operators,
not the integer truth-table composition used to construct certificates.
"""
import hashlib
import json
from functools import lru_cache


def pack(bits):
    value = 0
    for bit in bits:
        value = 2 * value + bit
    return value


def bits(word, width):
    return tuple((word >> i) & 1 for i in range(width - 1, -1, -1))


def tables(rule):
    f = [(rule >> i) & 1 for i in range(8)]
    a = [[((i >> 1) & 1) ^ f[i] for i in range(8)]]
    b = [a[0][:]]
    for j in range(3):
        width = 2 * (j + 2) + 1
        mask = (1 << (width - 2)) - 1
        aa, bb = [], []
        for word in range(1 << width):
            evolved = 0
            for shift in range(width - 3, -1, -1):
                evolved = (evolved << 1) | f[(word >> shift) & 7]
            transformed = (a[j][word >> 2] << 2
                           | a[j][(word >> 1) & mask] << 1
                           | a[j][word & mask])
            aa.append(a[j][evolved] ^ f[transformed])
            bb.append(b[j][evolved])
        a.append(aa)
        b.append(bb)
    return {"K": a, "O": b}


def direct_evaluator(rule):
    def step(row):
        # Deliberately use tuple neighborhoods and a string truth word here.
        truth = format(rule, "08b")[::-1]
        return tuple(int(truth[4*l + 2*c + r])
                     for l, c, r in zip(row, row[1:], row[2:]))

    @lru_cache(None)
    def evaluate(kind, j, row):
        assert len(row) == 2*j + 3
        if kind == "O":
            evolved = row
            for _ in range(j):
                evolved = step(evolved)
            return evolved[1] ^ step(evolved)[0]
        if j == 0:
            return row[1] ^ step(row)[0]
        left_path = evaluate("K", j-1, step(row))
        right_row = tuple(evaluate("K", j-1, row[i:i+len(row)-2])
                          for i in range(3))
        return left_path ^ step(right_row)[0]

    return evaluate


def audit():
    records, minima, controls = [], [], {}
    counts = {"truth_entries": 0, "source_windows": 0,
              "independent_source_windows": 0, "conflicts": 0}
    for rule in range(256):
        ts = tables(rule)
        direct = direct_evaluator(rule)
        for kind in ("K", "O"):
            for j, table in enumerate(ts[kind]):
                for word, value in enumerate(table):
                    assert direct(kind, j, bits(word, 2*j+3)) == value
                    counts["truth_entries"] += 1
        rule_minima = {"rule": rule}
        for kind in ("K", "O"):
            rule_minima[kind] = []
            for h in range(3):
                minimum = None
                for radius in range(3):
                    m = max(h+1+radius, h+2)
                    width = 2*m+1
                    patch_bits = (h+1)*(2*radius+1)
                    mapping, witness = {}, None
                    target_table = ts[kind][h+1]
                    for word in range(1 << width):
                        patch = 0
                        for j in range(h+1):
                            mask = (1 << (2*j+3))-1
                            for x in range(-radius, radius+1):
                                local = (word >> (m-x-j-1)) & mask
                                patch = (patch << 1) | ts[kind][j][local]
                        target = target_table[(word >> (m-h-2))
                                              & ((1 << (2*h+5))-1)]
                        if patch not in mapping:
                            mapping[patch] = (target, word)
                        elif mapping[patch][0] != target and witness is None:
                            witness = {"patch": patch,
                                       "words": [mapping[patch][1], word],
                                       "targets": [mapping[patch][0], target]}
                        counts["source_windows"] += 1

                    # Reconstruct all fibers independently, not only witnesses.
                    independent, independent_witness = {}, None
                    for word in range(1 << width):
                        row = bits(word, width)
                        patch = pack(direct(kind, j,
                                            row[m+x-j-1:m+x+j+2])
                                     for j in range(h+1)
                                     for x in range(-radius, radius+1))
                        target = direct(kind, h+1, row[m-h-2:m+h+3])
                        if patch not in independent:
                            independent[patch] = (target, word)
                        elif independent[patch][0] != target and independent_witness is None:
                            independent_witness = {
                                "patch": patch,
                                "words": [independent[patch][1], word],
                                "targets": [independent[patch][0], target]}
                        counts["independent_source_windows"] += 1
                    assert mapping == independent
                    assert witness == independent_witness
                    record = {"rule": rule, "kind": kind, "h": h, "R": radius,
                              "source_radius": m, "represented_bits": h+1,
                              "preparation_radius_bound": h+1,
                              "patch_bits": patch_bits,
                              "dense_table_bits": 1 << patch_bits,
                              "realized_patterns": len(mapping),
                              "pass": witness is None}
                    if witness is None:
                        if minimum is None:
                            minimum = radius
                        dense = bytearray(1 << patch_bits)
                        for patch, (target, _) in mapping.items():
                            dense[patch] = target
                        record.update({
                            "complete_update_radius_bound": max(1, radius) if kind == "K" else radius,
                            "cap_sha256": hashlib.sha256(dense).hexdigest(),
                            "cap_constant_on_image": len({v[0] for v in mapping.values()}) == 1})
                        if h == 0 and radius == 1:
                            record["eca_cap_zero_extension"] = sum(v << i for i, v in enumerate(dense))
                    else:
                        record["conflict"] = witness
                        counts["conflicts"] += 1
                    if rule == 232 and h == 0 and radius == 1:
                        expected = 104 if kind == "K" else 128
                        assert witness is None
                        assert all(target == ((expected >> patch) & 1)
                                   for patch, (target, _) in mapping.items())
                        controls[kind+"_232"] = {"expected_cap_on_image": expected,
                                                  "realized_patterns": len(mapping)}
                    records.append(record)
                rule_minima[kind].append(minimum)
        minima.append(rule_minima)
        constant = rule & 1
        coefficients = [((rule >> (1 << i)) & 1) ^ constant for i in range(3)]
        affine = all(((rule >> x) & 1) == (constant ^ (sum(coefficients[i] * ((x >> i) & 1)
                                                                          for i in range(3)) % 2))
                     for x in range(8))
        if affine:
            assert all(len(set(table)) == 1 for table in ts["K"][1:])
            controls.setdefault("affine_rules", []).append(rule)
    assert len(controls["affine_rules"]) == 16
    assert len(records) == 4608
    summary = []
    for h in range(3):
        for radius in range(3):
            summary.append({"h": h, "R": radius,
                            **{kind: sum(r["pass"] for r in records
                                         if (r["kind"], r["h"], r["R"]) == (kind, h, radius))
                               for kind in ("K", "O")}})
    return {"schema": 1, "protocol": "local-correction-caps-20260910",
            "implementation_corrections": [], "protocol_deviations": [],
            "domain": "all 256 homogeneous ECA on the full infinite binary lattice",
            "packing": "source left-to-right MSB first; patch component-major j increasing then x=-R..R",
            "cap_hash": "SHA256 of one byte (0 or 1) per dense table output, ascending patch; unseen inputs zero",
            "source_baseline": {"bits_per_site": 1, "update_radius": 1,
                                "readout_radius_bound": "j+1 for A_j and B_j"},
            "counts": counts, "controls": controls, "summary": summary,
            "minimum_passing_radius": minima, "records": records}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
