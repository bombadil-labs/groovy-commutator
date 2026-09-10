#!/usr/bin/env python3
"""Frozen full-gradient census; standard library, canonical JSON on stdout.

Local source bit x+4*y covers x,y=0..3 except (3,3). These coordinates
represent physical x-1,y-1. Local observed site x+3*y stores Jx at bit
2*(x+3*y), Jy at the next bit. Target site is (1,1).
"""
import hashlib
import itertools
import json

import verify_guard_free_axial_lift as axial

PROTOCOL_COMMIT = 'e1a1ef7002615977c1cbb5477dc051d38765009e'
RULES = [0, *range(128, 255, 2), 255]


def pack(values):
    return sum(int(value) << i for i, value in enumerate(values))


def reference_pack(values):
    return int(''.join('1' if value else '0' for value in values)[::-1], 2)


def primary_observation(word):
    return pack(value for y in range(3) for x in range(3)
                for value in (((word >> (x+4*y)) ^ (word >> (x+1+4*y))) & 1,
                              ((word >> (x+4*y)) ^ (word >> (x+4*(y+1)))) & 1))


def geometry():
    primary, reference = [], []
    for word in range(32768):
        windows = tuple(pack((word >> (x+dx+4*(y+dy))) & 1
                             for y in range(3) for x in range(3))
                        for dx, dy in ((0, 0), (1, 0), (0, 1)))
        primary.append((primary_observation(word), windows))
        bits = format(word, '015b')[::-1]
        field = {(x, y): bits[x+4*y] == '1' for y in range(4) for x in range(4)
                 if (x, y) != (3, 3)}
        ref_windows = tuple(tuple(field[x+dx, y+dy] for y in range(3) for x in range(3))
                            for dx, dy in ((0, 0), (1, 0), (0, 1)))
        observed = reference_pack(value for y in range(3) for x in range(3)
                                  for value in (field[x, y] != field[x+1, y],
                                                field[x, y] != field[x, y+1]))
        assert observed == primary[-1][0]
        reference.append((observed, ref_windows))
    anchor_index = {primary[2*i][0]: i for i in range(16384)}
    assert len(anchor_index) == 16384
    for word, (observed, _) in enumerate(primary):
        assert primary[word ^ 32767][0] == observed
        assert anchor_index[observed] == ((word ^ (32767 if word & 1 else 0)) >> 1)
        # Four independent plaquette constraints characterize this local image.
        for y in range(2):
            for x in range(2):
                edge_indices = (2*(x+3*y), 2*(x+1+3*y)+1,
                                2*(x+3*(y+1)), 2*(x+3*y)+1)
                assert sum((observed >> i) & 1 for i in edge_indices) % 2 == 0
    return primary, reference, anchor_index


def packed_cap(values):
    data = bytearray((len(values)+3)//4)
    for index, value in enumerate(values):
        data[index//4] |= value << (2*(index % 4))
    return data.hex()


def read_cap(encoded, index):
    return (encoded[index//4] >> (2*(index % 4))) & 3


def gradient(field, width, height):
    return pack(value for y in range(height) for x in range(width)
                for value in (field[x, y] ^ field[(x+1) % width, y],
                              field[x, y] ^ field[x, (y+1) % height]))


def reference_gradient(field, width, height):
    return reference_pack(value for y in range(height) for x in range(width)
                          for value in (field[x, y] != field[(x+1) % width, y],
                                        field[x, y] != field[x, (y+1) % height]))


def finite_step(rule, word, width, height):
    field = {(x, y): (word >> (x+width*y)) & 1 for y in range(height) for x in range(width)}
    text = format(word, f'0{width*height}b')[::-1]
    reference = {(x, y): text[x+width*y] == '1' for y in range(height) for x in range(width)}
    after = axial.lattice_passes(rule, field, (width, height))
    truth = axial.boolean_truth(rule)
    ref_after = {point: axial.local_tree(truth, reference, (width, height), point, 2)
                 for point in reference}
    assert after == ref_after
    actual = (gradient(field, width, height), gradient(after, width, height),
              pack(after[x, y] for y in range(height) for x in range(width)))
    ref = (reference_gradient(reference, width, height), reference_gradient(ref_after, width, height),
           reference_pack(ref_after[x, y] for y in range(height) for x in range(width)))
    assert actual == ref
    return actual, ref


def audit():
    primary, reference, anchor_index = geometry()
    affine = {sum((a*l ^ b*c ^ d*r ^ e) << (4*l+2*c+r)
                  for l, c, r in itertools.product(range(2), repeat=3))
              for a, b, d, e in itertools.product(range(2), repeat=4)}
    controls = sorted(affine.intersection(RULES))
    pairs = {name: [hashlib.sha256(), hashlib.sha256()]
             for name in ('local', 'complement', 'periodic', 'extension')}
    passing = [[], []]
    constant_response, self_dual, source_self_dual, finite_functional, obstructions = [], [], [], [], []
    records = []
    cap_sites = extended_cells = extended_updates = 0
    for rule in RULES:
        truth = axial.boolean_truth(rule)
        g = [axial.composite(rule, axial.unpack(p, 9)) for p in range(512)]
        # Memoization is keyed by Boolean arrays, independently of integer words.
        bool_g = {}
        for bits in itertools.product((False, True), repeat=9):
            field = {(x, y): bits[x+3*y] for y in range(3) for x in range(3)}
            bool_g[bits] = axial.shrinking(truth, field, 2, (0, 1))
        complement_values = []
        for p in range(512):
            bits = tuple(c == '1' for c in format(p, '09b')[::-1])
            a, b = g[p], g[p ^ 511]
            ra, rb = bool_g[bits], bool_g[tuple(not v for v in bits)]
            assert (a, b, a ^ b) == (ra, rb, int(ra != rb))
            pairs['complement'][0].update(bytes((a, b, a ^ b)))
            pairs['complement'][1].update(bytes((ra, rb, int(ra != rb))))
            complement_values.append(a ^ b)
        response = sorted(set(complement_values))
        complement_witness = next((p for p in range(512)
                                   if complement_values[p] != complement_values[0]), None)
        if len(response) == 1:
            constant_response.append(rule)
        if response == [1]:
            self_dual.append(rule)
        if all(axial.bit(rule, *bits) != axial.bit(rule, *(1-v for v in bits))
               for bits in itertools.product(range(2), repeat=3)):
            source_self_dual.append(rule)

        seen, witnesses, conflicts = [{}, {}], [None, None], [0, 0]
        targets = []
        for word in range(32768):
            observed, windows = primary[word]
            a, b, c = (g[p] for p in windows)
            target = (a ^ b) | ((a ^ c) << 1)
            ref_observed, ref_windows = reference[word]
            ra, rb, rc = (bool_g[bits] for bits in ref_windows)
            ref_target = int(ra != rb)+2*int(ra != rc)
            assert (observed, target, a, b, c) == (ref_observed, ref_target, ra, rb, rc)
            for checksum, values in zip(pairs['local'], ((observed, target, a, b, c),
                                                        (ref_observed, ref_target, ra, rb, rc))):
                checksum.update(values[0].to_bytes(3, 'little')+bytes(values[1:]))
            targets.append(target)
            if rule in affine:
                linear_rule = rule ^ (255*axial.bit(rule, 0, 0, 0))
                components = [axial.composite(linear_rule, [(observed >> (2*i+axis)) & 1 for i in range(9)])
                              for axis in range(2)]
                assert target == components[0]+2*components[1]
            for radius, key in enumerate(((observed >> 8) & 3, observed)):
                if key not in seen[radius]:
                    seen[radius][key] = (target, word)
                elif seen[radius][key][0] != target:
                    conflicts[radius] += 1
                    if witnesses[radius] is None:
                        old_target, old_word = seen[radius][key]
                        witnesses[radius] = {'observed_word': key, 'source_words': [old_word, word],
                                             'next_gradient_pairs': [old_target, target]}
        budgets = []
        for radius in (0, 1):
            assert len(seen[radius]) == (4 if radius == 0 else 16384)
            cap = None
            if witnesses[radius] is None:
                passing[radius].append(rule)
                values = [seen[0][i][0] for i in range(4)] if radius == 0 else targets[::2]
                cap = packed_cap(values)
            budgets.append({'radius': radius, 'passes': cap is not None,
                            'reachable_neighborhoods': len(seen[radius]),
                            'unreachable_neighborhoods': (4 if radius == 0 else 262144)-len(seen[radius]),
                            'conflicts_against_first_representative': conflicts[radius],
                            'first_conflict': witnesses[radius], 'reachable_cap_hex': cap})

        fibers = {}
        finite_witness = None
        finite_conflicts = 0
        decoded = [(b['radius'], bytes.fromhex(b['reachable_cap_hex'])) for b in budgets if b['passes']]
        for word in range(512):
            actual, ref = finite_step(rule, word, 3, 3)
            observed, target, after_word = actual
            for checksum, values in zip(pairs['periodic'], (actual, ref)):
                checksum.update(values[0].to_bytes(3, 'little')+values[1].to_bytes(3, 'little')
                                +values[2].to_bytes(2, 'little'))
            if observed not in fibers:
                fibers[observed] = {'first_source': word, 'first_target': target, 'targets': set(), 'size': 0}
            fiber = fibers[observed]
            fiber['size'] += 1
            fiber['targets'].add(target)
            if fiber['first_target'] != target:
                finite_conflicts += 1
                if finite_witness is None:
                    finite_witness = {'observed_full_word': observed,
                                      'source_words': [fiber['first_source'], word],
                                      'next_gradient_words': [fiber['first_target'], target]}
            for radius, encoded in decoded:
                for y in range(3):
                    for x in range(3):
                        if radius == 0:
                            index = (observed >> (2*(x+3*y))) & 3
                        else:
                            neighborhood = pack((observed >> (2*((x+dx) % 3+3*((y+dy) % 3))+axis)) & 1
                                                for dy in (-1, 0, 1) for dx in (-1, 0, 1) for axis in (0, 1))
                            index = anchor_index[neighborhood]
                        assert read_cap(encoded, index) == ((target >> (2*(x+3*y))) & 3)
                        cap_sites += 1
        assert len(fibers) == 256 and {v['size'] for v in fibers.values()} == {2}
        if finite_witness is None:
            finite_functional.append(rule)

        extension = None
        if witnesses[1] is not None:
            a, b = witnesses[1]['source_words']
            assert a ^ b == 32767
            # Fill omitted corner with 0 for A,1 for B; full tiles are complements.
            full_words = [a, b | (1 << 15)]
            assert full_words[0] ^ full_words[1] == 65535
            observations, next_fields = [], []
            for word in full_words:
                actual, ref = finite_step(rule, word, 4, 4)
                observations.append(actual[0])
                next_fields.append(actual[1])
                for checksum, values in zip(pairs['extension'], (actual, ref)):
                    checksum.update(values[0].to_bytes(4, 'little')+values[1].to_bytes(4, 'little')
                                    +values[2].to_bytes(2, 'little'))
                extended_updates += 1
                extended_cells += 16
            assert observations[0] == observations[1]
            assert next_fields[0] != next_fields[1]
            center_pairs = [(w >> 10) & 3 for w in next_fields]
            assert center_pairs == witnesses[1]['next_gradient_pairs']
            assert center_pairs[0] != center_pairs[1]
            extension = {'source_words_4_by_4': full_words, 'omitted_corner_values': [0, 1],
                         'observed_full_word': observations[0], 'next_gradient_words': next_fields,
                         'center_next_gradient_pairs': center_pairs}
            obstructions.append(rule)
        records.append({'rule': rule, 'local_budgets': budgets,
                        'complement_response_values': response,
                        'first_nonconstant_complement_response_patch': complement_witness,
                        'periodic': {'observed_fields': len(fibers), 'fiber_size': 2,
                                     'conflicting_fibers': sum(len(v['targets']) > 1 for v in fibers.values()),
                                     'conflicts_against_first_representative': finite_conflicts,
                                     'first_conflict': finite_witness},
                        'full_field_extension': extension})
    assert set(controls) <= set(passing[1])
    assert {0, 204, 255} <= set(passing[0])
    assert set(passing[0]) <= set(passing[1]) <= set(finite_functional)
    assert passing[1] == constant_response
    assert self_dual == source_self_dual
    assert sorted(set(passing[1]) | set(obstructions)) == RULES
    assert all(a.digest() == b.digest() for a, b in pairs.values())
    return {'protocol_commit': PROTOCOL_COMMIT, 'source_rules': RULES,
            'observation': 'J(X)=(X XOR next-x translate, X XOR next-y translate)',
            'local_source_convention': 'bit x+4*y, x,y=0..3 except (3,3); physical coordinates x-1,y-1',
            'local_gradient_convention': 'bits 2*(x+3*y),2*(x+3*y)+1 store Jx,Jy for x,y=0..2',
            'target_convention': 'bit0 is next Jx, bit1 is next Jy at local source coordinate (1,1)',
            'finite_convention': 'source bit x+width*y; gradient components at 2*(x+width*y), then +1',
            'reachable_cap_encoding': 'two-bit outputs packed four per byte, low pair first, hex bytes; R0 index=current center pair; R1 index=i means J of 15-bit source word 2*i, fixing source (0,0)=0',
            'reachability': {'radius_zero_patterns': 4, 'radius_one_total_patterns': 262144,
                             'radius_one_reachable_patterns': 16384, 'radius_one_unreachable_patterns': 245760,
                             'radius_one_criterion': 'XOR of oriented edges on each of four plaquettes with lower-left x,y=0,1 is zero',
                             'preimages_per_reachable_local_gradient': 2},
            'radius_zero_rules': passing[0], 'radius_one_rules': passing[1],
            'constant_complement_response_rules': constant_response,
            'self_dual_composite_rules': self_dual, 'self_dual_source_rules': source_self_dual,
            'finite_functional_rules': finite_functional, 'full_field_obstruction_rules': obstructions,
            'selected_affine_controls': controls,
            'counts': {'source_rules': len(RULES), 'local_source_windows': len(RULES)*32768,
                       'local_rule_budget_windows': len(RULES)*32768*2,
                       'memoized_boolean_G_windows': len(RULES)*512,
                       'complement_patch_pairs': len(RULES)*512,
                       'periodic_macro_updates': len(RULES)*512, 'periodic_output_cells': len(RULES)*512*9,
                       'passing_cap_site_checks': cap_sites, 'passing_cap_component_checks': 2*cap_sites,
                       'extended_macro_updates': extended_updates, 'extended_output_cells': extended_cells,
                       'radius_zero_rules': len(passing[0]), 'radius_one_rules': len(passing[1]),
                       'finite_functional_rules': len(finite_functional), 'full_field_obstructions': len(obstructions)},
            'checksum_conventions': {'order': 'source rules then source words ascending; all integers little endian',
                                     'local': 'observed J uint24; next center pair,G center,G right,G up as four bytes',
                                     'complement': 'G(p),G(complement p),their XOR as bytes',
                                     'periodic': 'observed J uint24,next J uint24,next source uint16',
                                     'extension': 'first then second source; observed J uint32,next J uint32,next source uint16'},
            'checksums': {name: {'primary': a.hexdigest(), 'independent': b.hexdigest()} for name, (a, b) in pairs.items()},
            'rules': records}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
