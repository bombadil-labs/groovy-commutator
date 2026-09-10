#!/usr/bin/env python3
"""Frozen exhaustive one-shot flat-mask intervention audit; canonical JSON stdout.

Run from the repository root. Standard library only. Reuses the separately
audited native-edge and Boolean twisted-potential evaluators without changing
their laws. Budgets charge stored edge flips, not elapsed time or a controller.
"""
import hashlib
import itertools
import json
import struct
import sys
from collections import Counter

from verify_gradient_loops import (RULES, SHAPES, embed, encode, inspect,
                                   native_step, pack, points, recover,
                                   reference_step, topology)

PROTOCOL_COMMIT = 'f69b156ccc5fb7ff75ab4c2db95924dc87cc5d90'
HORIZONS = (0, 1, 4)


def reference_kernel(shape):
    """Coordinate-set equations, low-pivot RREF, and explicit nullspace span.

    This enumeration does not use potentials, loop labels, or topology().
    A set symmetric difference handles coincident edges on small tori.
    """
    pts, d = points(shape), len(shape)
    edges = [(p, a) for p in pts for a in range(d)]
    rows = []
    for p in pts:
        for a, b in itertools.combinations(range(d), 2):
            pa = tuple((x + (i == a)) % n for i, (x, n) in enumerate(zip(p, shape)))
            pb = tuple((x + (i == b)) % n for i, (x, n) in enumerate(zip(p, shape)))
            row = set()
            for edge in ((p, a), (pa, b), (pb, a), (p, b)):
                row.symmetric_difference_update((edges.index(edge),))
            if row:
                rows.append(row)
    rank, pivots = 0, []
    for col in range(len(edges)):
        chosen = next((i for i in range(rank, len(rows)) if col in rows[i]), None)
        if chosen is None:
            continue
        rows[rank], rows[chosen] = rows[chosen], rows[rank]
        for i in range(len(rows)):
            if i != rank and col in rows[i]:
                rows[i] ^= rows[rank]
        pivots.append(col)
        rank += 1
    basis = []
    for free in sorted(set(range(len(edges))) - set(pivots)):
        vector = {free}
        vector.update(pivot for pivot, row in zip(pivots, rows[:rank]) if free in row)
        basis.append(sum(2**i for i in vector))
    words = [0]
    for vector in basis:
        words += [word ^ vector for word in words]
    return rank, sorted(words)


def touched(word, d, n):
    return sum(bool((word >> (d*s)) & ((1 << d)-1)) for s in range(n))


def minima(profiles):
    result = []
    for h in sorted({p['loop_word'] for p in profiles}):
        group = [p for p in profiles if p['loop_word'] == h]
        record = {'loop_word': h, 'masks': len(group)}
        for cost in ('edge_cost', 'site_cost'):
            value = min(p[cost] for p in group)
            winners = [p['word'] for p in group if p[cost] == value]
            record[cost] = {'minimum': value, 'minimizers': len(winners),
                            'first_mask_word': min(winners)}
        result.append(record)
    return result


def census(shape):
    d, n = len(shape), len(points(shape))
    potentials = range(0, 1 << n, 2)
    words = sorted(encode(tuple((p >> i) & 1 for i in range(n)),
                          tuple((h >> a) & 1 for a in range(d)), shape)
                   for p in potentials for h in range(1 << d))
    rank, independent = reference_kernel(shape)
    assert rank == topology(shape)[2]
    assert words == independent and len(set(words)) == 1 << (d*n-rank)
    profiles, reference_costs = [], {}
    for word in words:
        potential, loops = recover(word, shape)
        assert encode(potential, loops, shape) == word
        bits = [bool(word & (2**i)) for i in range(d*n)]
        owners = {i//d for i, bit in enumerate(bits) if bit}
        reference_costs[word] = sum(bits)
        edge_cost, site_cost = word.bit_count(), touched(word, d, n)
        assert edge_cost == sum(bits) and site_cost == len(owners)
        profiles.append({'word': word, 'loop_word': pack(loops),
                         'edge_cost': edge_cost, 'site_cost': site_cost})
    minimum = minima(profiles)
    for record in minimum:
        h = record['loop_word']
        prediction = sum(n//side for a, side in enumerate(shape) if (h >> a) & 1)
        seam = encode((0,)*n, tuple((h >> a) & 1 for a in range(d)), shape)
        assert record['edge_cost']['minimum'] == prediction == seam.bit_count()
        record.update(predicted_minimum_edge_cost=prediction, seam_mask_word=seam)
    return words, profiles, reference_costs, {
        'shape': shape, 'sites': n, 'stored_edge_bits': d*n, 'plaquette_rank': rank,
        'flat_masks': len(words), 'nullspace_enumeration_matches': True,
        'no_op_masks': 1, 'nonzero_zero_loop_masks': (1 << (n-1))-1,
        'profiles': profiles, 'loop_minima': minimum}


def digest_row(pair, prefix, primary, reference):
    """One ASCII compact JSON header + newline, then little-endian uint32 words."""
    header = json.dumps(prefix, separators=(',', ':')).encode('ascii') + b'\n'
    for digest, values in zip(pair, (primary, reference)):
        digest.update(header)
        digest.update(struct.pack('<' + 'I'*len(values), *values))


def tables(shape, words, rule, hashes, counts, interface=False):
    primary, reference = {}, {}
    label = 'interface' if interface else 'base'
    for word in words:
        potential, loops = recover(word, shape)
        native = native_step(rule, word, shape)
        other, _, ref_loops = reference_step(rule, potential, loops, shape)
        assert native == other, ('transition', shape, rule, word, native, other)
        assert inspect(native, shape) == ref_loops
        assert ref_loops == ((0,)*len(shape) if rule in (0, 255) else loops)
        primary[word], reference[word] = native, other
    assert set(primary.values()) <= set(words)
    assert set(reference.values()) <= set(words)
    digest_row(hashes['transitions'], [label, shape, rule, len(words)],
               [primary[w] for w in words], [reference[w] for w in words])
    counts[label + '_one_step_comparisons'] += len(words)
    pt, rt = {0: dict(zip(words, words))}, {0: dict(zip(words, words))}
    for t in range(1, max(HORIZONS)+1):
        pt[t] = {w: primary[pt[t-1][w]] for w in words}
        rt[t] = {w: reference[rt[t-1][w]] for w in words}
    return pt, rt


def cumulative_minima(endpoints, costs, loop_words, maximum):
    fields, loops = {}, {}
    for endpoint, cost in zip(endpoints, costs):
        fields[endpoint] = min(fields.get(endpoint, maximum+1), cost)
        h = loop_words[endpoint]
        loops[h] = min(loops.get(h, maximum+1), cost)
    result = []
    for mapping in (fields, loops):
        histogram = Counter(mapping.values())
        result.append(list(itertools.accumulate(histogram[b] for b in range(maximum+1))))
    return result


def direct_counts(endpoints, action_order, reference_costs, loop_words, maximum):
    """Grow actual endpoint sets as each hard budget admits more actions.

    Uses the reference endpoints and independently counted mask bits, and never
    constructs the primary evaluator's minimum-cost-to-endpoint dictionary.
    """
    fields, loops, at = set(), set(), 0
    field_counts, loop_counts = [], []
    for budget in range(maximum+1):
        while at < len(action_order) and reference_costs[action_order[at]] <= budget:
            endpoint = endpoints[action_order[at]]
            fields.add(endpoint)
            loops.add(loop_words[endpoint])
            at += 1
        field_counts.append(len(fields))
        loop_counts.append(len(loops))
    assert at == len(action_order)
    return [field_counts, loop_counts]


def distribution(values, words):
    counts = Counter(values)
    low, high = min(counts), max(counts)
    return {'histogram': [[k, counts[k]] for k in sorted(counts)],
            'minimum': low, 'maximum': high,
            'first_minimum_state': words[values.index(low)],
            'first_maximum_state': words[values.index(high)]}


def audit():
    hashes = {key: [hashlib.sha256(), hashlib.sha256()]
              for key in ('transitions', 'endpoints', 'budget_counts', 'interfaces')}
    counts, geometry, records = Counter(), [], []
    ensembles, profiles_by_shape, all_tables, frontiers = {}, {}, {}, {}
    for shape in SHAPES:
        words, profiles, rcost, geom = census(shape)
        ensembles[shape], profiles_by_shape[shape] = words, profiles
        geometry.append(geom)
        maximum = len(shape)*len(points(shape))
        loop_words = {p['word']: p['loop_word'] for p in profiles}
        costs = [p['edge_cost'] for p in profiles]
        order = sorted(words, key=lambda w: (rcost[w], w))
        for rule in RULES:
            print('audit', shape, rule, file=sys.stderr, flush=True)
            pt, rt = tables(shape, words, rule, hashes, counts)
            all_tables[shape, rule] = pt, rt
            counts['initial_rule_state_action_combinations'] += len(words)**2
            for t in HORIZONS:
                per_state = []
                for state in words:
                    endpoints = [pt[t][state ^ mask] for mask in words]
                    reference = {mask: rt[t][state ^ mask] for mask in words}
                    refs = [reference[mask] for mask in words]
                    assert endpoints == refs, ('endpoints', shape, rule, t, state)
                    calculated = cumulative_minima(endpoints, costs, loop_words, maximum)
                    checked = direct_counts(reference, order, rcost, loop_words, maximum)
                    assert calculated == checked, ('budget counts', shape, rule, t, state)
                    assert calculated[0][0] == calculated[1][0] == 1
                    if rule in (0, 255) and t > 0:
                        assert calculated == [[1]*(maximum+1)]*2
                    else:
                        predicted = [sum(m['predicted_minimum_edge_cost'] <= b
                                         for m in geom['loop_minima']) for b in range(maximum+1)]
                        assert calculated[1] == predicted
                    digest_row(hashes['endpoints'], [shape, rule, t, state, len(words)], endpoints, refs)
                    digest_row(hashes['budget_counts'], [shape, rule, t, state, maximum],
                               calculated[0]+calculated[1], checked[0]+checked[1])
                    counts['endpoint_queries'] += len(words)
                    counts['state_budget_observation_comparisons'] += 2*(maximum+1)
                    per_state.append(calculated)
                frontiers[shape, rule, t] = dict(zip(words, per_state))
                image = set(pt[t].values())
                records.append({'shape': shape, 'rule': rule, 'horizon': t,
                    'unlimited_full_fields_by_terminal_loop': [
                        [h, sum(loop_words[w] == h for w in image)] for h in range(1 << len(shape))],
                    'budgets': [{'edge_budget': b,
                        'full_fields': distribution([v[0][b] for v in per_state], words),
                        'loop_vectors': distribution([v[1][b] for v in per_state], words)}
                        for b in range(maximum+1)]})

    interfaces = []
    for shape in SHAPES[:2]:
        target = shape+(2,)
        words = ensembles[shape]
        embedded = {w: embed(w, shape) for w in words}
        target_words = sorted(embedded.values())
        assert len(set(target_words)) == len(words)
        target_profiles = []
        for p in profiles_by_shape[shape]:
            w = embedded[p['word']]
            loops = inspect(w, target)
            assert loops == inspect(p['word'], shape)+(0,)
            ec, sc = w.bit_count(), touched(w, len(target), len(points(target)))
            assert ec == 2*p['edge_cost'] and sc == 2*p['site_cost']
            target_profiles.append({'word': w, 'loop_word': pack(loops),
                                    'edge_cost': ec, 'site_cost': sc})
            counts['interface_mask_cost_checks'] += 1
        report = {'source_shape': shape, 'target_shape': target,
                  'inherited_masks': len(words), 'edge_cost_multiplier': 2,
                  'site_cost_multiplier': 2, 'inherited_loop_minima': minima(target_profiles),
                  'native_target_census': target in ensembles,
                  'lifted_masks': [{'source_mask': w, 'target_mask': embedded[w]} for w in words]}
        if target in ensembles:
            native = profiles_by_shape[target]
            report['native_action_classes'] = dict(Counter(
                'inherited' if p['word'] in target_words else
                'outside_image_new_loop' if p['loop_word'] >> len(shape) else
                'outside_image_zero_new_loop' for p in native))
            report['native_loop_minima'] = minima(native)
            report['capability_comparison'] = []
        for rule in RULES:
            source_pt, source_rt = all_tables[shape, rule]
            target_pt, target_rt = tables(target, target_words, rule, hashes, counts, interface=True)
            for t in HORIZONS:
                for state in words:
                    left, right = [], []
                    for mask in words:
                        edited = embedded[state] ^ embedded[mask]
                        assert edited == embedded[state ^ mask]
                        primary = target_pt[t][edited]
                        reference = target_rt[t][edited]
                        inherited = embed(source_pt[t][state ^ mask], shape)
                        assert primary == reference == inherited
                        left.append(inherited)
                        right.append(reference)
                        counts['interface_endpoint_checks'] += 1
                    digest_row(hashes['interfaces'], [shape, rule, t, state, len(words)], left, right)
                if target in ensembles:
                    source_maximum = len(shape)*len(points(shape))
                    for b in range(source_maximum+1):
                        item = {'rule': rule, 'horizon': t, 'source_edge_budget': b,
                                'target_edge_budget': 2*b}
                        for obs, index in (('full_fields', 0), ('loop_vectors', 1)):
                            inherited_counts = [frontiers[shape, rule, t][s][index][b] for s in words]
                            native_counts = [frontiers[target, rule, t][embedded[s]][index][2*b] for s in words]
                            differences = [n-i for n, i in zip(native_counts, inherited_counts)]
                            assert min(differences) >= 0
                            item[obs] = {'inherited': distribution(inherited_counts, words),
                                         'native': distribution(native_counts, words),
                                         'native_minus_inherited': distribution(differences, words)}
                        report['capability_comparison'].append(item)
        interfaces.append(report)
    assert counts['base_one_step_comparisons'] == 10720
    assert counts['initial_rule_state_action_combinations'] == 10498560
    assert counts['endpoint_queries'] == 31495680
    assert counts['interface_endpoint_checks'] == 38400
    assert counts['interface_mask_cost_checks'] == 48
    assert all(a.digest() == b.digest() for a, b in hashes.values())
    return {'protocol_commit': PROTOCOL_COMMIT, 'rules': RULES, 'horizons': HORIZONS,
            'contract': {'state': 'known full flat edge field',
                'action': 'one simultaneous flat XOR mask at time zero',
                'budget': 'hard upper bound on flipped stored edge bits',
                'secondary_cost': 'distinct sites owning flipped outgoing edges',
                'capacity_bits': 'log2 of reachable outcome count; deterministic known-state one-shot channel only'},
            'conventions': {'word': 'bit dimension*lexicographic_site_index+axis; last axis fastest',
                'first_witness': 'smallest unsigned stored-edge word',
                'loop_word': 'bit axis; wrapping-loop XOR',
                'counts': 'exact integers; histogram entries [outcome_count, number_of_initial_fields]',
                'interface_witnesses': 'source initial words; apply P for target states',
                'checksum_stream': 'ASCII compact JSON header plus newline; uint32 little-endian payload; headers and payload order in digest_row call sites'},
            'counts': dict(counts), 'discrepancies': [], 'geometry': geometry,
            'checksums': {k: {'primary': a.hexdigest(), 'independent': b.hexdigest()}
                          for k, (a, b) in hashes.items()},
            'outcome_frontiers': records, 'interfaces': interfaces}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
