#!/usr/bin/env python3
"""Compare relations between rules across rings, without pooling contracts.

This module is an analysis instrument, not a CA simulator or a classifier.
For each matched rectangle (a,n), (b,n), (a,m), (b,m), it retains the
rule relation at each ring and their comparison. All extension points are
ordinary registered functions; JSON query files contain no executable code.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import importlib.util
from itertools import combinations
import json
import math
from pathlib import Path
import tempfile


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def positive_int(value, label='ring'):
    if type(value) is not int or value < 1:
        raise ValueError(f'{label} must be a positive integer')
    return value


@lru_cache(maxsize=4096)
def factorization(n):
    """Exact trial division for experimental ring lengths, including 1."""
    positive_int(n)
    out, p = [], 2
    while p * p <= n:
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        if exponent:
            out.append((p, exponent))
        p = 3 if p == 2 else p + 2
    if n > 1:
        out.append((n, 1))
    return tuple(out)


def arithmetic(n, m):
    a, b = dict(factorization(n)), dict(factorization(m))
    union = set(a) | set(b)
    return {
        'size_gap': m - n, 'gcd': math.gcd(n, m), 'lcm': math.lcm(n, m),
        'n_divides_m': int(m % n == 0), 'm_divides_n': int(n % m == 0),
        'coprime': int(math.gcd(n, m) == 1),
        'same_prime_support': int(set(a) == set(b)),
        'prime_support_jaccard': len(set(a) & set(b)) / len(union) if union else 1.,
        'exponent_l1': sum(abs(a.get(p, 0) - b.get(p, 0)) for p in union),
        'n_distinct_primes': len(a), 'm_distinct_primes': len(b),
        'n_total_prime_factors': sum(a.values()), 'm_total_prime_factors': sum(b.values()),
        'n_prime': int(len(a) == 1 and sum(a.values()) == 1),
        'm_prime': int(len(b) == 1 and sum(b.values()) == 1),
    }


def divisibility(n, m, divisor):
    positive_int(divisor, 'divisor')
    a, b = int(n % divisor == 0), int(m % divisor == 0)
    return {'n': a, 'm': b, 'both': a * b, 'same': int(a == b)}


def valuation(n, m, prime):
    positive_int(prime, 'prime')
    if factorization(prime) != ((prime, 1),):
        raise ValueError('valuation requires a prime')
    a, b = dict(factorization(n)).get(prime, 0), dict(factorization(m)).get(prime, 0)
    return {'n': a, 'm': b, 'gap': b - a, 'absolute_gap': abs(b - a)}


def eca_number(rule):
    try:
        n = int(rule)
    except (ValueError, TypeError) as error:
        raise ValueError('eca features require decimal ECA identifiers') from error
    if str(n) != rule or not 0 <= n <= 255:
        raise ValueError('eca features require canonical identifiers "0" through "255"')
    return n


@lru_cache(maxsize=256)
def eca_orbit(rule):
    mirror = sum(((rule >> i) & 1) << (((i & 1) << 2) | (i & 2) | (i >> 2))
                 for i in range(8))
    complement = lambda r: sum((1 ^ ((r >> (7 - i)) & 1)) << i for i in range(8))
    return frozenset((rule, mirror, complement(rule), complement(mirror)))


def eca_features(a, b):
    a, b = eca_number(a), eca_number(b)
    return {'truth_table_hamming': (a ^ b).bit_count(),
            'same_symmetry_orbit': int(b in eca_orbit(a))}


def number(value):
    if value is not None and (type(value) not in (int, float, bool) or not math.isfinite(value)):
        raise ValueError('expected a finite number or null')
    return value


def difference(a, b):
    number(a); number(b)
    return None if a is None or b is None else b - a


def change(a, b):
    number(a); number(b)
    delta = None if a is None or b is None else b - a
    return {'at_n': a, 'at_m': b, 'change': delta,
            'absolute_change': None if delta is None else abs(delta)}


class Registry:
    """Named, versioned extension functions. Duplicate registration is an error."""

    KINDS = ('ring', 'rule', 'relation', 'comparison')

    def __init__(self):
        self.functions = {}

    def add(self, kind, name, function, *, version='1'):
        if kind not in self.KINDS or not isinstance(name, str) or not name or not callable(function):
            raise ValueError('invalid registry entry')
        if (kind, name) in self.functions:
            raise ValueError(f'duplicate registration: {kind}/{name}')
        self.functions[kind, name] = (str(version), function)

    def resolve(self, kind, specs):
        out, ids = [], set()
        for spec in specs:
            if set(spec) - {'name', 'id', 'params', 'version'}:
                raise ValueError(f'unknown selector fields: {spec}')
            name, params = spec['name'], spec.get('params', {})
            version, function = self.functions[kind, name]
            identifier = spec.get('id', name)
            if not isinstance(identifier, str) or not identifier or identifier in ids:
                raise ValueError(f'duplicate or invalid selector id: {identifier}')
            if not isinstance(params, dict):
                raise ValueError('selector params must be an object')
            if str(spec.get('version', version)) != version:
                raise ValueError(f'version mismatch: {kind}/{name}')
            canonical(params)
            ids.add(identifier)
            out.append(({'id': identifier, 'name': name, 'version': version, 'params': params}, function))
        return out


def default_registry():
    registry = Registry()
    for kind, name, function in [('ring', 'arithmetic', arithmetic),
                                 ('ring', 'divisibility', divisibility),
                                 ('ring', 'valuation', valuation),
                                 ('rule', 'eca', eca_features),
                                 ('relation', 'difference', difference),
                                 ('comparison', 'change', change)]:
        registry.add(kind, name, function)
    return registry


@dataclass(frozen=True)
class Case:
    rule: str
    ring: int
    observation: str
    payload: object
    context: dict
    source: str

    def __post_init__(self):
        positive_int(self.ring)
        for field in ('rule', 'observation', 'source'):
            if not isinstance(getattr(self, field), str) or not getattr(self, field):
                raise ValueError(f'{field} must be a nonempty string')
        if not isinstance(self.context, dict) or not self.context:
            raise ValueError('a nonempty experimental context is required')
        canonical(self.context)
        canonical(self.payload)


def numeric_map(value):
    if not isinstance(value, dict) or any(not isinstance(k, str) for k in value):
        raise ValueError('features and comparisons must return a named numeric mapping')
    for item in value.values():
        number(item)
    return value


def features(functions, a, b):
    result = {}
    for spec, function in functions:
        values = numeric_map(function(a, b, **spec['params']))
        named = {f"{spec['id']}.{key}": val for key, val in values.items()}
        if result.keys() & named.keys():
            raise ValueError('feature names collide; choose different selector ids')
        result.update(named)
    return result


def rule_order(rule):
    return (0, int(rule), rule) if rule.isdecimal() else (1, rule, rule)


def compare(cases, query=None, registry=None):
    """Return complete evidence rows and coverage, with no statistical inference.

    The input iterable is indexed once. Work grows with complete four-case
    rectangles times relation/comparison counts. max_comparisons is checked
    before evaluating any relation, and is not a limit on the registry size.
    """
    query = {} if query is None else query
    allowed = {'rules', 'rings', 'observations', 'contexts', 'ring', 'rule',
               'relation', 'comparison', 'max_comparisons'}
    if set(query) - allowed:
        raise ValueError(f'unknown query keys: {set(query) - allowed}')
    for name in allowed - {'max_comparisons'}:
        if name in query and not isinstance(query[name], list):
            raise ValueError(f'query {name} must be a list')
    registry = default_registry() if registry is None else registry
    defaults = {'ring': [{'name': 'arithmetic'}], 'rule': [{'name': 'eca'}],
                'relation': [{'name': 'difference'}], 'comparison': [{'name': 'change'}]}
    resolved = {kind: registry.resolve(kind, query.get(kind, defaults[kind]))
                for kind in Registry.KINDS}
    if not resolved['relation'] or not resolved['comparison']:
        raise ValueError('at least one relation and comparison are required')
    limit = positive_int(query.get('max_comparisons', 100000), 'max_comparisons')
    selected_rules = None if 'rules' not in query else set(query['rules'])
    if selected_rules is not None and any(not isinstance(r, str) or not r for r in selected_rules):
        raise ValueError('query rules must be string identifiers')
    selected_rings = None if 'rings' not in query else set(query['rings'])
    if selected_rings is not None:
        for ring in selected_rings:
            positive_int(ring)
    selected_contexts = None if 'contexts' not in query else {canonical(c) for c in query['contexts']}
    groups, seen, read, kept = defaultdict(dict), set(), 0, 0
    for case in cases:
        read += 1
        ctx = canonical(case.context)
        key = (ctx, case.observation, case.ring, case.rule)
        if key in seen:
            raise ValueError(f'duplicate case key: {key}')
        seen.add(key)
        if ((selected_rules is not None and case.rule not in selected_rules)
            or (selected_rings is not None and case.ring not in selected_rings)
            or ('observations' in query and case.observation not in query['observations'])
            or (selected_contexts is not None and ctx not in selected_contexts)):
            continue
        groups[ctx, case.observation][case.ring, case.rule] = case
        kept += 1
    plans, coverage, required = [], [], 0
    multiplier = len(resolved['relation']) * len(resolved['comparison'])
    for (ctx, observation), cells in sorted(groups.items()):
        rules = sorted(selected_rules if selected_rules is not None else {r for _, r in cells}, key=rule_order)
        rings = sorted(selected_rings if selected_rings is not None else {n for n, _ in cells})
        complete = 0
        for n, m in combinations(rings, 2):
            common = [r for r in rules if (n, r) in cells and (m, r) in cells]
            count = math.comb(len(common), 2)
            complete += count
            if count:
                plans.append((ctx, observation, cells, n, m, common))
        possible = math.comb(len(rules), 2) * math.comb(len(rings), 2)
        required += complete * multiplier
        coverage.append({'context': json.loads(ctx), 'observation': observation,
                         'cases': len(cells), 'rules': rules, 'rings': rings,
                         'complete_rectangles': complete, 'missing_rectangles': possible - complete})
    if required > limit:
        raise ValueError(f'comparison budget exceeded: {required} > {limit}; select a smaller panel or raise the explicit budget')
    rows = []
    ring_cache, rule_cache = {}, {}
    for ctx, observation, cells, n, m, rules in plans:
        if (n, m) not in ring_cache:
            ring_cache[n, m] = features(resolved['ring'], n, m)
        for a, b in combinations(rules, 2):
            if (a, b) not in rule_cache:
                rule_cache[a, b] = features(resolved['rule'], a, b)
            corners = [cells[n, a], cells[n, b], cells[m, a], cells[m, b]]
            for rel, relation in resolved['relation']:
                rn = relation(corners[0].payload, corners[1].payload, **rel['params'])
                rm = relation(corners[2].payload, corners[3].payload, **rel['params'])
                canonical([rn, rm])
                for comp, comparison in resolved['comparison']:
                    scores = numeric_map(comparison(rn, rm, **comp['params']))
                    rows.append({'context': json.loads(ctx), 'observation': observation,
                                 'rules': [a, b], 'rings': [n, m],
                                 'factorizations': [factorization(n), factorization(m)],
                                 'relation': rel, 'comparison': comp,
                                 'relation_values': [rn, rm], 'scores': scores,
                                 'ring_features': ring_cache[n, m], 'rule_features': rule_cache[a, b],
                                 'sources': [c.source for c in corners]})
    return {'schema': 'rule-ring-selectors/v1', 'status': 'complete',
            'interpretation': 'descriptive exploration; dependent pairs; no significance or classifier claim',
            'query': query, 'resolved_selectors': {k: [s for s, _ in v] for k, v in resolved.items()},
            'input_cases': read, 'selected_cases': kept, 'comparison_count': required,
            'coverage': coverage, 'rows': rows}


def pearson(pairs):
    if len(pairs) < 3:
        return None, 'fewer_than_three_rows'
    xs, ys = zip(*pairs)
    # Scale before centering to keep ordinary finite inputs from overflowing.
    sx, sy = max(abs(x) for x in xs), max(abs(y) for y in ys)
    if sx == 0 or sy == 0:
        return None, 'constant_input'
    xs, ys = [x / sx for x in xs], [y / sy for y in ys]
    mx, my = math.fsum(xs) / len(xs), math.fsum(ys) / len(ys)
    dx, dy = [x - mx for x in xs], [y - my for y in ys]
    xx, yy = math.fsum(x*x for x in dx), math.fsum(y*y for y in dy)
    if xx == 0 or yy == 0:
        return None, 'constant_input'
    value = math.fsum(x*y for x, y in zip(dx, dy)) / math.sqrt(xx * yy)
    return max(-1., min(1., value)), None


def correlations(report):
    """Full descriptive scan; never rank/select winners or compute IID p-values."""
    groups = defaultdict(list)
    for row in report['rows']:
        key = canonical([row['context'], row['observation'], row['relation'], row['comparison']])
        groups[key].append(row)
    out = []
    for key, rows in sorted(groups.items()):
        context, observation, relation, comparison = json.loads(key)
        feature_names = sorted({(kind, name) for r in rows for kind in ('ring_features', 'rule_features')
                                for name in r[kind]})
        score_names = sorted({name for r in rows for name in r['scores']})
        for kind, feature in feature_names:
            for score in score_names:
                usable = [r for r in rows if r[kind].get(feature) is not None and r['scores'].get(score) is not None]
                value, reason = pearson([(r[kind][feature], r['scores'][score]) for r in usable])
                out.append({'context': context, 'observation': observation, 'relation': relation,
                            'comparison': comparison, 'feature': f'{kind}.{feature}', 'score': score,
                            'pearson': value, 'undefined_reason': reason, 'usable_rows': len(usable),
                            'omitted_rows': len(rows) - len(usable),
                            'distinct_rule_pairs': len({tuple(r['rules']) for r in usable}),
                            'distinct_ring_pairs': len({tuple(r['rings']) for r in usable})})
    return {'interpretation': 'descriptive only; pairs share endpoints; all attempted correlations retained',
            'attempted_correlations': len(out), 'entries': out}


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, sort_keys=True, separators=(',', ':'), allow_nan=False)
            stream.write('\n')
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', required=True, type=Path, help='JSONL Case objects')
    parser.add_argument('--query', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--plugin', action='append', default=[], type=Path,
                        help='trusted Python file exporting register(registry)')
    parser.add_argument('--correlations', action='store_true')
    args = parser.parse_args()
    inputs = [args.cases, args.query, *args.plugin, Path(__file__)]
    if args.output.resolve() in {p.resolve() for p in inputs}:
        parser.error('output must not overwrite an input')
    before = {str(p.resolve()): sha256(p) for p in inputs}
    registry = default_registry()
    for i, path in enumerate(args.plugin):
        spec = importlib.util.spec_from_file_location(f'rule_ring_plugin_{i}', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.register(registry)
    with args.cases.open() as stream:
        report = compare((Case(**json.loads(line)) for line in stream if line.strip()),
                         json.loads(args.query.read_text()), registry)
    if args.correlations:
        report['correlations'] = correlations(report)
    if before != {str(p.resolve()): sha256(p) for p in inputs}:
        raise RuntimeError('an input changed while the query was running')
    report['input_sha256'] = before
    atomic_json(args.output, report)


if __name__ == '__main__':
    main()
