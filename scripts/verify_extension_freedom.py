#!/usr/bin/env python3
"""Frozen extension census; data-image agreement is not ambient uniqueness."""
import hashlib
import json

import verify_local_correction_caps as caps
import verify_editable_routing_tables as base
import verify_finite_routing_boundaries as finite
import verify_rule32_physical_cap as physical32

FREEZE = "f4caa22f762bc4df47a0f777b85abbd13e38bdb1"


def pack(row):
    out = 0
    for value in row:
        out = 2*out + value
    return out


def source_cases():
    tables = caps.tables(32)
    a0, a1 = tables["K"][:2]
    b1 = tables["O"][1]
    cases = []
    for word in range(128):
        u = [a0[(word >> shift) & 7] for shift in (3, 2, 1)]
        v = [a1[(word >> shift) & 31] for shift in (2, 1, 0)]
        evolved = pack((32 >> ((word >> shift) & 7)) & 1 for shift in range(4, -1, -1))
        cases.append((pack(u+v), (b1[(word >> 1) & 31], a1[evolved])))
    return cases


def independent_cases():
    def f(row):
        return tuple(l and not c and r for l, c, r in zip(row, row[1:], row[2:]))

    def d(row):
        return int(row[1] != f(row)[0])

    def correction(row):
        return int(d(f(row)) != f(tuple(d(row[i:i+3]) for i in range(3)))[0])

    out = []
    for word in range(128):
        row = tuple(c == '1' for c in format(word, '07b'))
        u = [d(row[i:i+3]) for i in (1, 2, 3)]
        v = [correction(row[i:i+5]) for i in (0, 1, 2)]
        next_row = f(row)
        out.append((int(''.join(str(x) for x in u+v), 2),
                    (d(next_row[1:4]), correction(next_row))))
    return out


def signature(q, h):
    return sum(((h >> (4*((q >> (context >> 1)) & 1)+(context & 1))) & 1) << context
               for context in range(16))


def independent_signature(q, h):
    # A separate two-level selection tree with the positive guard fixed to0.
    qbits = [int(x) for x in format(q, '08b')[::-1]]
    hbits = [int(x) for x in format(h, '08b')[::-1]]
    values = []
    for context in range(16):
        left, center, right, below = [int(x) for x in format(context, '04b')]
        leaves = list(qbits)
        for selector in (right, center, left):
            leaves = [leaves[i+selector] for i in range(0, len(leaves), 2)]
        pairs = [hbits[i+below] for i in range(0, 8, 2)]
        on_zero_north = [pairs[0], pairs[2]]
        values.append(on_zero_north[leaves[0]])
    return sum(bit << i for i, bit in enumerate(values))


def encode_with_top(state, width, q=128, lambdas=None, copy=False):
    native = physical32.prepare(state, width)
    for x in range(width):
        word = q if lambdas is None else 128+32*((lambdas >> x) & 1)
        native[x, 1] = (word, 240), native[x, 1][1]
    return native, finite.MaskedField.encode(native, 2, (width,), copy)


def native_copy_step(native, width):
    after = physical32.native_step(native, width)
    return {(x, y): (native[(x-1) % width, y][0] if value else program, after[x, y][1])
            for (x, y), (program, value) in native.items()}


def audit():
    cases, independent = source_cases(), independent_cases()
    assert cases == independent
    forced, top_forced, quad_forced = {}, {}, {}
    for patch, pair in cases:
        for mapping, key, value in ((forced, patch, pair), (top_forced, patch & 7, pair[1]),
                                    (quad_forced, 2*(patch & 7)+((patch >> 4) & 1), pair[1])):
            if key in mapping:
                assert mapping[key] == value
            mapping[key] = value
    free = [p for p in range(64) if p not in forced]
    top_pass, top_witnesses = [], []
    for q in range(256):
        witness = next((word for word, (patch, pair) in enumerate(cases)
                        if ((q >> (patch & 7)) & 1) != pair[1]), None)
        if witness is None:
            top_pass.append(q)
        else:
            patch, pair = independent[witness]
            assert int(format(q, '08b')[::-1][patch & 7]) != pair[1]
            top_witnesses.append({"q": q, "source_word": witness,
                                  "V_patch": patch & 7, "expected": pair[1],
                                  "actual": (q >> (patch & 7)) & 1})
    assert top_pass == [128, 160]
    for p in range(8):
        l, c, r = (p >> 2) & 1, (p >> 1) & 1, p & 1
        assert (((128 ^ 160) >> p) & 1) == l*(1-c)*r
    assert set(top_forced) == set(range(8))-{5}

    witnesses, functions, checksums = [], {}, [hashlib.sha256(), hashlib.sha256()]
    native_passes = 0
    mask = sum(1 << p for p in quad_forced)
    required = sum(v << p for p, v in quad_forced.items())
    for q in range(256):
        row = []
        for h in range(256):
            sig, ref = signature(q, h), independent_signature(q, h)
            assert sig == ref
            checksums[0].update(sig.to_bytes(2, 'little'))
            checksums[1].update(ref.to_bytes(2, 'little'))
            witness = next((word for word, (patch, pair) in enumerate(cases)
                            if ((sig >> (2*(patch & 7)+((patch >> 4) & 1))) & 1) != pair[1]), -1)
            independent_witness = next((word for word, (patch, pair) in enumerate(independent)
                                        if ((ref >> (2*(patch % 8)+((patch // 16) % 2))) & 1) != pair[1]), -1)
            assert witness == independent_witness
            assert (witness == -1) == (((sig ^ required) & mask) == 0)
            row.append(witness)
            if witness == -1:
                native_passes += 1
                functions.setdefault(sig, []).append([q, h])
        witnesses.append(row)
    assert checksums[0].hexdigest() == checksums[1].hexdigest()

    counts = {"physical_timepoints": 0, "compared_stored_symbols": 0,
              "remote_absorbing_blank_checks": 0, "neutral_program_bit_changes": 0}

    def compare(field, native, width):
        assert field.symbols == physical32.reference_symbols(native)
        assert len(field.symbols) == 68*width
        assert base.physical_value(2, (0, 1000), field.get, field.copy) == base.B
        counts["physical_timepoints"] += 1
        counts["compared_stored_symbols"] += len(field.symbols)
        counts["remote_absorbing_blank_checks"] += 1

    holds = []
    for width in (4, 6):
        for q in top_pass:
            checksum = hashlib.sha256()
            for initial in range(1 << width):
                state = initial
                native, field = encode_with_top(state, width, q)
                for tick in range(9):
                    compare(field, native, width)
                    expected, _ = encode_with_top(state, width, q)
                    assert native == expected
                    checksum.update(bytes(physical32.active_pair(native, width)))
                    if tick < 8:
                        native = physical32.native_step(native, width)
                        field = field.step()
                        state = physical32.evolve(state, width)
            holds.append({"width": width, "top_word": q, "cases": 1 << width,
                          "ticks": 8, "active_pair_trace_sha256": checksum.hexdigest()})
    for width in (4, 6):
        assert len({r["active_pair_trace_sha256"] for r in holds if r["width"] == width}) == 1

    defects = []
    for q in top_pass:
        width = 21
        native, field = encode_with_top(0, width, q)
        for x in range(width):
            native[x, 0] = (32, 60), 1
            native[x, 1] = (q, 240), int(x != 0)
        field = finite.MaskedField.encode(native, 2, (width,))
        trace = []
        for tick in range(9):
            compare(field, native, width)
            zeros = sorted(x if x <= width//2 else x-width
                           for x in range(width) if native[x, 1][1] == 0)
            trace.append({"tick": tick, "top_zero_positions": zeros,
                          "active_pair_words": physical32.active_pair(native, width)})
            if tick < 8:
                native = physical32.native_step(native, width)
                field = field.step()
        defects.append({"top_word": q, "width": width, "trace": trace})

    transports = []
    width = 4
    for initial in range(16):
        for initial_lambda in range(16):
            state, lam = initial, initial_lambda
            native, field = encode_with_top(state, width, lambdas=lam, copy=True)
            trace = []
            for tick in range(5):
                compare(field, native, width)
                expected, _ = encode_with_top(state, width, lambdas=lam, copy=True)
                assert native == expected
                trace.append({"tick": tick, "lambda": lam,
                              "active_pair": physical32.active_pair(native, width)})
                if tick < 4:
                    v = physical32.active_pair(physical32.prepare(state, width), width)[1]
                    next_lambda = sum(((lam >> ((x-1) % width if (v >> x) & 1 else x)) & 1) << x
                                      for x in range(width))
                    counts["neutral_program_bit_changes"] += (lam ^ next_lambda).bit_count()
                    lam, state = next_lambda, physical32.evolve(state, width)
                    native, field = native_copy_step(native, width), field.step()
            transports.append({"initial": initial, "initial_lambda": initial_lambda, "trace": trace})
    assert counts["neutral_program_bit_changes"] > 0
    return {"schema": 1, "protocol": "extension-freedom-20260910", "protocol_freeze_commit": FREEZE,
            "protocol_deviations": [], "implementation_corrections": [],
            "packing": "source and six-bit U/V patches MSB left-to-right; target pair=[U_next,V_next]; ring bit x has weight2**x",
            "source_window_cases": 128,
            "pair_radius_one": {"forced_map": [{"patch": p, "target": list(v)} for p, v in sorted(forced.items())],
                                "realized_patterns": len(forced), "free_patterns": free,
                                "free_table_bits": 2*len(free), "ambient_map_count": str(1 << (2*len(free)))},
            "top_eca": {"compatible_words": top_pass, "forced_map": [{"patch": p, "target": v} for p, v in sorted(top_forced.items())],
                        "rejections": top_witnesses, "difference_polynomial": "V_left*(1+V_center)*V_right over GF(2)"},
            "native_top": {"candidate_tuples": 65536, "passing_tuples": native_passes,
                           "distinct_effective_functions": len(functions), "realized_four_bit_contexts": len(quad_forced),
                           "signature_packing": "output bit at context=2*V_triple+U_center; positive guard fixed0",
                           "all_candidate_signatures_sha256": checksums[0].hexdigest(),
                           "functions": [{"signature": sig, "multiplicity": len(programs), "programs": programs}
                                         for sig, programs in sorted(functions.items())],
                           "rejection_matrix": witnesses,
                           "rejection_matrix_format": "[q][h] is first conflicting source word0..127, or-1 for a pass"},
            "physical_counts": counts, "hold_controls": holds,
            "defect_controls": defects, "neutral_transport": {"cases": 256, "width": 4, "ticks": 4, "records": transports},
            "scope": "Logical pair and guarded native-strip extensions, not all raw 2D states or a canonical dimension-raising law. Compatible physical encodings carry different program words."}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
