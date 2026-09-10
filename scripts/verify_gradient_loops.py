#!/usr/bin/env python3
"""Frozen native-gradient / twisted-potential audit; canonical JSON stdout.

No third-party dependencies. Coordinates are lexicographic (last axis fastest).
Edge word bit d*site_index+i is the outgoing edge on axis i.
"""
import hashlib
import itertools
import json
from collections import Counter, deque
from functools import lru_cache

PROTOCOL_COMMIT = '9e5de20f127f7a0047f3d6201abe7f83cd131981'
RULES = (0, 142, 150, 170, 178, 204, 212, 232, 240, 255)
SHAPES = ((4,), (2, 2), (2, 2, 2))
TICKS = 4


def shift(point, axis, amount=1):
    return tuple(x + (amount if i == axis else 0) for i, x in enumerate(point))


@lru_cache(None)
def points(shape):
    return tuple(itertools.product(*(range(n) for n in shape)))


def pack(values):
    return sum(int(v) << i for i, v in enumerate(values))


def reference_pack(values):
    return int(''.join('1' if v else '0' for v in values)[::-1], 2)


@lru_cache(None)
def topology(shape):
    pts = points(shape)
    index = {p: i for i, p in enumerate(pts)}
    d = len(shape)
    neighbors = tuple(tuple(index[tuple(x % n for x, n in zip(shift(p, a), shape))]
                            for a in range(d)) for p in pts)
    rows = []
    for s in range(len(pts)):
        for a in range(d):
            for b in range(a+1, d):
                row = 0
                for edge in (d*s+a, d*neighbors[s][a]+b, d*neighbors[s][b]+a, d*s+b):
                    row ^= 1 << edge
                rows.append(row)
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length()-1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    assert d*len(pts)-len(pivots) == len(pts)-1+d
    return neighbors, tuple(rows), len(pivots)


def encode(potential, loops, shape):
    neighbors, _, _ = topology(shape)
    d = len(shape)
    return pack(potential[s] ^ potential[neighbors[s][a]] ^
                (loops[a] if p[a] == shape[a]-1 else 0)
                for s, p in enumerate(points(shape)) for a in range(d))


def inspect(word, shape):
    neighbors, rows, _ = topology(shape)
    d = len(shape)
    for row in rows:
        assert (word & row).bit_count() % 2 == 0, ('curl', shape, word, row)
    loops = []
    for a, n in enumerate(shape):
        values = set()
        for start in range(len(points(shape))):
            s, parity = start, 0
            for _ in range(n):
                parity ^= (word >> (d*s+a)) & 1
                s = neighbors[s][a]
            assert s == start
            values.add(parity)
        assert len(values) == 1
        loops.append(values.pop())
    return tuple(loops)


def recover(word, shape):
    """A fixed non-wrapping path reconstructs each tile potential, anchor zero."""
    d = len(shape)
    index = {p: i for i, p in enumerate(points(shape))}
    values = []
    for target in points(shape):
        p, value = (0,)*d, 0
        for a in range(d):
            for _ in range(target[a]):
                value ^= (word >> (d*index[p]+a)) & 1
                p = shift(p, a)
        values.append(value)
    loops = inspect(word, shape)
    assert encode(values, loops, shape) == word
    return tuple(values), loops


@lru_cache(None)
def local_geometry(d):
    sites = tuple(itertools.product((-1, 0, 1), repeat=d))
    edges = tuple((p, shift(p, a)) for p in sites for a in range(d))
    vertices = {p for edge in edges for p in edge}
    assert len(vertices) == 3**d+d*3**(d-1)
    return sites, edges


@lru_cache(None)
def integrate(d, bits):
    _, edges = local_geometry(d)
    adjacency = {}
    for (p, q), value in zip(edges, bits):
        adjacency.setdefault(p, []).append((q, value))
        adjacency.setdefault(q, []).append((p, value))
    anchor = (-1,)*d
    field, queue = {anchor: 0}, deque([anchor])
    while queue:
        p = queue.popleft()
        for q, value in adjacency[p]:
            candidate = field[p] ^ value
            if q in field:
                assert field[q] == candidate, ('inconsistent native neighborhood', d, bits)
            else:
                field[q] = candidate
                queue.append(q)
    assert len(field) == len(adjacency)
    return field


@lru_cache(None)
def native_local(rule, d, bits):
    source = integrate(d, bits)
    outcomes = []
    for anchor in (0, 1):
        @lru_cache(None)
        def tree(stage, p):
            if stage == 0:
                return source[p] ^ anchor
            triple = [tree(stage-1, shift(p, stage-1, offset)) for offset in (-1, 0, 1)]
            return (rule >> (4*triple[0]+2*triple[1]+triple[2])) & 1
        origin = (0,)*d
        center = tree(d, origin)
        outcomes.append(tuple(center ^ tree(d, shift(origin, a)) for a in range(d)))
    assert outcomes[0] == outcomes[1], ('anchor-dependent', rule, d, bits)
    return outcomes[0]


@lru_cache(None)
def neighborhood_indices(shape):
    d = len(shape)
    sites, _ = local_geometry(d)
    index = {p: i for i, p in enumerate(points(shape))}
    return tuple(tuple(d*index[tuple((x+y) % n for x, y, n in zip(p, offset, shape))]+a
                       for offset in sites for a in range(d)) for p in points(shape))


def native_step(rule, word, shape):
    return pack(value for indices in neighborhood_indices(shape)
                for value in native_local(rule, len(shape), tuple((word >> i) & 1 for i in indices)))


def reference_step(rule, potential, loops, shape):
    """Boolean finite-halo contraction. Infer output twists; never assign prediction."""
    d = len(shape)
    tile = dict(zip(points(shape), map(bool, potential)))
    ranges = [range(-1, n+2) for n in shape]
    field = {}
    for p in itertools.product(*ranges):
        value = tile[tuple(x % n for x, n in zip(p, shape))]
        for x, n, h in zip(p, shape, loops):
            if h and (x//n) % 2:
                value = not value
        field[p] = value
    truth = {tuple(c == '1' for c in format(i, '03b')): c == '1'
             for i, c in enumerate(format(rule, '08b')[::-1])}
    for a, n in enumerate(shape):
        ranges[a] = range(n+1)
        field = {p: truth[tuple(field[shift(p, a, offset)] for offset in (-1, 0, 1))]
                 for p in itertools.product(*ranges)}
    after_loops = []
    for a, n in enumerate(shape):
        parities = {field[p] != field[shift(p, a, n)] for p in field if p[a] == 0}
        assert len(parities) == 1, ('output has inconsistent twist', rule, shape)
        after_loops.append(int(parities.pop()))
    after = tuple(int(field[p]) for p in points(shape))
    gradient = reference_pack(field[p] != field[shift(p, a)] for p in points(shape) for a in range(d))
    return gradient, after, tuple(after_loops)


def embed(word, shape):
    d = len(shape)
    index = {p: i for i, p in enumerate(points(shape))}
    return pack(0 if a == d else (word >> (d*index[p[:-1]]+a)) & 1
                for p in points(shape+(2,)) for a in range(d+1))


def update_hash(pair, prefix, primary, reference):
    for digest, value in zip(pair, (primary, reference)):
        digest.update(json.dumps([*prefix, *value], separators=(',', ':')).encode('ascii')+b'\n')


def audit():
    records, geometry_records = [], []
    hashes = {key: [hashlib.sha256(), hashlib.sha256()] for key in ('base', 'interfaces')}
    counts = Counter()
    for shape in SHAPES:
        pts, d = points(shape), len(shape)
        n = len(pts)
        ensemble, seen = [], set()
        for potential_word in range(0, 1 << n, 2):
            potential = tuple((potential_word >> i) & 1 for i in range(n))
            for hword in range(1 << d):
                loops = tuple((hword >> a) & 1 for a in range(d))
                word = encode(potential, loops, shape)
                assert word not in seen
                seen.add(word)
                assert recover(word, shape) == (potential, loops)
                assert encode(tuple(1-v for v in potential), loops, shape) == word
                ensemble.append((potential_word, hword, potential, loops, word))
        _, rows, rank = topology(shape)
        assert len(seen) == 1 << (d*n-rank)
        geometry_records.append({'shape': shape, 'sites': n, 'stored_edge_bits': d*n,
                                 'plaquette_equations': len(rows), 'plaquette_rank': rank,
                                 'flat_fields': len(seen), 'loop_sectors': 1 << d,
                                 'fields_per_sector': 1 << (n-1),
                                 'local_edge_reads': d*3**d,
                                 'local_potential_vertices': 3**d+d*3**(d-1)})
        counts['ensemble_fields'] += len(ensemble)
        for rule in RULES:
            transitions, certificates = Counter(), []
            for pword, hword, potential, loops, word in ensemble:
                native, ref_potential, ref_loops = word, potential, loops
                timeline = [{'edge_word': word, 'loop_word': hword}]
                counts['base_initial_rule_field_cases'] += 1
                for tick in range(1, TICKS+1):
                    before = native
                    before_loops = inspect(before, shape)
                    native = native_step(rule, before, shape)
                    reference, ref_potential, ref_loops = reference_step(rule, ref_potential, ref_loops, shape)
                    assert native == reference, ('native/reference', shape, rule, pword, hword, tick)
                    after_loops = inspect(native, shape)
                    assert after_loops == ref_loops
                    assert after_loops == ((0,)*d if rule in (0, 255) else loops)
                    assert encode(ref_potential, ref_loops, shape) == native
                    recover(native, shape)
                    transitions[tick, pack(before_loops), pack(after_loops)] += 1
                    update_hash(hashes['base'], [shape, rule, pword, hword, tick, before],
                                (native, pack(after_loops)), (reference, reference_pack(ref_loops)))
                    timeline.append({'edge_word': native, 'loop_word': pack(after_loops)})
                    counts['base_macro_updates'] += 1
                    counts['base_component_comparisons'] += d*n
                if pword == 0:
                    certificates.append({'initial_loop_word': hword, 'initial_potential_word': 0,
                                         'trajectory': timeline})
                if d < 3:
                    target_shape = shape+(2,)
                    source_word, target_word = word, embed(word, shape)
                    target_potential = tuple(potential[pts.index(p[:-1])] for p in points(target_shape))
                    target_loops = loops+(0,)
                    assert inspect(target_word, target_shape) == target_loops
                    assert encode(target_potential, target_loops, target_shape) == target_word
                    counts['interface_initial_rule_field_cases'] += 1
                    for tick in range(1, TICKS+1):
                        source_word = native_step(rule, source_word, shape)
                        target_word = native_step(rule, target_word, target_shape)
                        reference, target_potential, target_loops = reference_step(
                            rule, target_potential, target_loops, target_shape)
                        assert target_word == reference == embed(source_word, shape)
                        native_loops = inspect(target_word, target_shape)
                        assert native_loops == inspect(source_word, shape)+(0,) == target_loops
                        recover(target_word, target_shape)
                        update_hash(hashes['interfaces'], [shape, rule, pword, hword, tick, source_word],
                                    (target_word, pack(native_loops)), (reference, reference_pack(target_loops)))
                        counts['interface_updates'] += 1
                        counts['interface_target_component_comparisons'] += (d+1)*len(points(target_shape))
            records.append({'shape': shape, 'rule': rule,
                            'loop_transitions': [{'tick': t, 'from': a, 'to': b, 'count': count}
                                                 for (t, a, b), count in sorted(transitions.items())],
                            'certificates': certificates})
    assert counts['base_initial_rule_field_cases'] == 10720
    assert counts['base_macro_updates'] == 42880
    assert counts['interface_initial_rule_field_cases'] == 480
    assert counts['interface_updates'] == 1920
    assert all(a.digest() == b.digest() for a, b in hashes.values())
    return {'protocol_commit': PROTOCOL_COMMIT, 'source_rules': RULES, 'ticks': TICKS,
            'conventions': {'coordinates': 'lexicographic; last axis fastest; axis 0 evolves first',
                            'potential': 'bit site_index; origin anchored zero in initial enumeration',
                            'gradient': 'bit dimension*site_index+axis; outgoing positive edge',
                            'loop_word': 'bit axis; positive wrapping-loop XOR',
                            'checksums': 'ASCII compact JSON array per update plus newline; prefix shape,rule,initial potential word,initial loop word,tick; base adds previous edge word,next edge word,next loop word; interfaces add next source edge word,next target edge word,next target loop word'},
            'counts': dict(counts), 'geometry': geometry_records,
            'native_cache': {'integrated_neighborhoods': integrate.cache_info().currsize,
                             'rule_neighborhoods_both_anchors': native_local.cache_info().currsize},
            'discrepancies': [],
            'checksums': {key: {'native': a.hexdigest(), 'independent': b.hexdigest()}
                          for key, (a, b) in hashes.items()}, 'records': records}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
