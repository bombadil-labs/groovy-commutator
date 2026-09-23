#!/usr/bin/env python3
"""Bounded, exact 1D native-G recursion; no encoding or extra state tracks.

Packed truth-table evaluation and separate unpacked certificate replay.
Rule tables list outputs in ascending binary-neighborhood order.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import resource
import signal
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = 'docs/research/protocols/groovy-1d-second-generation-20260923.md'
SCRIPT = 'scripts/groovy_1d_second_generation.py'
INPUT = 'results/groovy_field_20260922/census.json'
RESULT = ROOT / 'results/groovy_1d_second_generation_20260923.json'


@dataclass(frozen=True)
class Rule:
    radius: int
    bits: tuple[int, ...]

    def record(self):
        return {'radius': self.radius, 'outputs_ascending': ''.join(map(str, self.bits))}


def eca(r):
    return Rule(1, tuple((r >> i) & 1 for i in range(8)))


def apply(v, length, rule):
    """Packed finite-cone evaluation, retaining only complete neighborhoods."""
    lut = np.asarray(rule.bits, dtype=np.uint64)
    width = 2*rule.radius + 1
    out = np.zeros_like(v, dtype=np.uint64)
    for shift in range(length-width+1):
        key = (v >> np.uint64(shift)) & np.uint64((1 << width)-1)
        out |= lut[key.astype(np.int64)] << np.uint64(shift)
    return out


def reduce(rule):
    words = np.arange(len(rule.bits), dtype=np.uint64)
    values = np.asarray(rule.bits, dtype=np.uint8)
    for r in range(rule.radius+1):
        key = (words >> np.uint64(rule.radius-r)) & np.uint64((1 << (2*r+1))-1)
        forced = force(key, values, r)
        if forced is not None:
            assert '?' not in forced
            return Rule(r, tuple(map(int, forced)))
    raise AssertionError('a table agrees with itself')


def groovy(rule):
    r = rule.radius
    length = 4*r+1
    v = np.arange(1 << length, dtype=np.uint64)
    ev = apply(v, length, rule)
    ee = apply(ev, length-2*r, rule)
    middle = (v >> np.uint64(r)) & np.uint64((1 << (length-2*r))-1)
    ed = apply(middle ^ ev, length-2*r, rule)
    bits = ((ev >> np.uint64(r)) & 1) ^ ee ^ ed
    return reduce(Rule(2*r, tuple(map(int, bits))))


def compose(outer, inner):
    r = outer.radius+inner.radius
    length = 2*r+1
    v = np.arange(1 << length, dtype=np.uint64)
    bits = apply(apply(v, length, inner), 2*outer.radius+1, outer)
    return reduce(Rule(r, tuple(map(int, bits))))


def force(keys, values, r):
    order = np.argsort(keys, kind='stable')
    k, v = keys[order], values[order]
    if np.any((k[1:] == k[:-1]) & (v[1:] != v[:-1])):
        return None
    table = ['?']*(1 << (2*r+1))
    for i in np.r_[0, np.flatnonzero(k[1:] != k[:-1])+1]:
        table[int(k[i])] = str(int(v[i]))
    return ''.join(table)


def local_factor(observation, evolution, r):
    successor = compose(observation, evolution)
    m = max(observation.radius+r, successor.radius)
    length = 2*m+1
    if length > 21:
        return {'status': 'cone_cap', 'source_bits': length}
    v = np.arange(1 << length, dtype=np.uint64)
    obs = apply(v, length, observation)
    keys = (obs >> np.uint64(m-observation.radius-r)) & np.uint64((1 << (2*r+1))-1)
    values = (apply(v, length, successor) >> np.uint64(m-successor.radius)) & 1
    forced = force(keys, values, r)
    if forced is None:
        return {'status': 'local_conflict', 'radius': r, 'source_bits': length}
    return {'status': 'law', 'radius': r, 'source_bits': length,
            'source_words': 1 << length, 'forced_outputs_ascending': forced}


def total(forced, fill):
    return Rule(forced['radius'], tuple(fill if b == '?' else int(b)
                                       for b in forced['forced_outputs_ascending']))


def ring(words, n, rule):
    out = np.zeros_like(words, dtype=np.uint64)
    lut = np.asarray(rule.bits, dtype=np.uint64)
    for i in range(n):
        key = np.zeros_like(words)
        for d in range(-rule.radius, rule.radius+1):
            bit = (words >> np.uint64(n-1-((i+d) % n))) & 1
            key = (key << np.uint64(1)) | bit
        out = (out << np.uint64(1)) | lut[key.astype(np.int64)]
    return out


def periodic_collision(observation, evolution, n):
    words = np.arange(1 << n, dtype=np.uint64)
    obs = ring(words, n, observation)
    nxt = ring(ring(words, n, evolution), n, observation)
    order = np.argsort(obs, kind='stable')
    same = obs[order][1:] == obs[order][:-1]
    diff = nxt[order][1:] != nxt[order][:-1]
    at = np.flatnonzero(same & diff)
    if len(at) == 0:
        return None
    a, b = map(int, order[int(at[0]):int(at[0])+2])
    fmt = lambda x: format(int(x), f'0{n}b')
    return {'period': n, 'sources': [fmt(a), fmt(b)],
            'observations': [fmt(obs[a]), fmt(obs[b])],
            'successors': [fmt(nxt[a]), fmt(nxt[b])]}


def closure(observation, evolution):
    if len(set(observation.bits)) == 1:
        return {**local_factor(observation, evolution, 0),
                'observation_constant': observation.bits[0], 'periods_screened': 0}
    for n in range(1, 13):
        witness = periodic_collision(observation, evolution, n)
        if witness is not None:
            return {'status': 'no_present_only_law', 'witness': witness,
                    'periods_screened': n, 'all_spatial_radii_excluded': True}
    attempts = []
    for r in range(5):
        cert = local_factor(observation, evolution, r)
        attempts.append(cert)
        if cert['status'] == 'law':
            return {**cert, 'periods_screened': 12, 'smaller_radius_attempts': attempts[:-1]}
        if cert['status'] == 'cone_cap':
            break
    return {'status': 'unresolved_within_budget', 'periods_screened': 12,
            'radius_attempts': attempts}


# Separate unpacked arithmetic for certificate replay. It never calls apply,
# ring, compose or groovy to compute a dynamical output.
def matrix(words, n):
    return ((np.asarray(words, dtype=np.uint64)[:, None] >>
             np.arange(n-1, -1, -1, dtype=np.uint64)) & 1).astype(np.uint8)


def matrix_apply(x, rule):
    width = 2*rule.radius+1
    size = x.shape[1]-width+1
    indices = np.zeros((len(x), size), dtype=np.uint32)
    for j in range(width):
        indices = 2*indices+x[:, j:j+size]
    return np.asarray(rule.bits, dtype=np.uint8)[indices]


def matrix_g(x, rule):
    r = rule.radius
    first = matrix_apply(x, rule)
    twice = matrix_apply(first, rule)
    middle = x[:, r:x.shape[1]-r] if r else x
    change_update = matrix_apply(middle ^ first, rule)
    center_first = first[:, r:first.shape[1]-r] if r else first
    return center_first ^ twice ^ change_update


def scalar_ring(s, rule):
    values = [int(b) for b in s]
    out = []
    for i in range(len(s)):
        index = 0
        for d in range(-rule.radius, rule.radius+1):
            index = 2*index+values[(i+d) % len(s)]
        out.append(str(rule.bits[index]))
    return ''.join(out)


def verify_g_table(base, g):
    n = 4*base.radius+1
    x = matrix(np.arange(1 << n), n)
    assert np.array_equal(matrix_g(x, base)[:, 0], matrix_apply(x, g)[:, 2*base.radius-g.radius])
    return 1 << n


def verify_composed_g(source, child, observation):
    n = 2*(2+2*child.radius)+1
    x = matrix(np.arange(1 << n), n)
    direct = matrix_g(matrix_g(x, source), child)[:, 0]
    expected = matrix_apply(x, observation)[:, n//2-observation.radius]
    assert np.array_equal(direct, expected)
    return 1 << n


def verify_closure(observation, evolution, result):
    if result['status'] == 'no_present_only_law':
        w = result['witness']
        obs = [scalar_ring(s, observation) for s in w['sources']]
        nxt = [scalar_ring(scalar_ring(s, evolution), observation) for s in w['sources']]
        assert obs == w['observations'] and nxt == w['successors']
        assert obs[0] == obs[1] and nxt[0] != nxt[1]
        return {'scalar_periodic_witness': True}
    if result['status'] != 'law':
        return {'verified': False, 'reason': 'unresolved search is not a certificate'}
    # Recompute the full uncompressed support rather than trusting the packed
    # composition's reduced radius or recorded cone length.
    r = result['radius']
    m = max(observation.radius+r, observation.radius+evolution.radius)
    n = 2*m+1
    lut = np.array([int(b) if b != '?' else 2 for b in result['forced_outputs_ascending']], dtype=np.uint8)
    checked = 0
    for lo in range(0, 1 << n, 32768):
        x = matrix(np.arange(lo, min(lo+32768, 1 << n)), n)
        obs = matrix_apply(x, observation)
        local = Rule(r, tuple(map(int, lut)))
        predicted = matrix_apply(obs, local)[:, m-observation.radius-r]
        actual = matrix_apply(matrix_apply(x, evolution), observation)[:, m-evolution.radius-observation.radius]
        assert np.array_equal(predicted, actual)
        checked += len(x)
    return {'unpacked_source_words': checked, 'source_bits': n, 'verified': True}


def evaluate():
    census = json.loads((ROOT/INPUT).read_text())['data']
    selected = [r for r in range(256) if census[str(r)]['G_only']['k1']['verdict'] == 'L']
    assert len(selected) == 36
    first, children = [], []
    for r in selected:
        source = eca(r)
        obs = groovy(source)
        verify_g_table(source, obs)
        radius = census[str(r)]['G_only']['k1']['radius']
        lower = [local_factor(obs, source, k) for k in range(radius)]
        assert all(a['status'] == 'local_conflict' for a in lower)
        cert = local_factor(obs, source, radius)
        assert cert['status'] == 'law'
        verification = verify_closure(obs, source, cert)
        primary = total(cert, 0)
        child_g = groovy(primary)
        first.append({'source_rule': r, 'factor_certificate': cert,
                      'smaller_radius_attempts': lower, 'zero_fill_rule': primary.record(),
                      'native_g': child_g.record(), 'verification': verification})
        if radius == 0:
            assert len(set(child_g.bits)) == 1 and child_g.bits[0] == primary.bits[0]
            continue
        variants = []
        inherited_observations = []
        for fill in (0, 1):
            f = total(cert, fill)
            g = groovy(f)
            inherited = compose(g, obs)
            native_cases = verify_g_table(f, g)
            composed_cases = verify_composed_g(source, f, inherited)
            full = closure(g, f)
            actual = closure(inherited, source)
            full['verification'] = verify_closure(g, f, full)
            actual['verification'] = verify_closure(inherited, source, actual)
            variants.append({'fill': fill, 'derived_rule': f.record(), 'native_g': g.record(),
                             'inherited_observation': inherited.record(),
                             'full_descendant_domain': full, 'inherited_domain': actual,
                             'independent_g_table_words': native_cases,
                             'independent_composed_words': composed_cases})
            inherited_observations.append(inherited)
        children.append({'source_rule': r, 'variants': variants,
                         'inherited_observation_same_under_two_fills':
                         inherited_observations[0] == inherited_observations[1]})
    assert [c['source_rule'] for c in children] == [2, 16, 32]
    return {'present_only_sources': selected, 'first_stage': first, 'nonpointwise_descendants': children,
            'pointwise_count': len(selected)-len(children),
            'scope': 'present-only binary 1D; specified minimal-radius zero/one completions; no memory search'}


def hashes():
    return {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
            for p in (PROTOCOL, SCRIPT, INPUT)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.record == args.check:
        parser.error('choose --record or --check')
    if args.record:
        if RESULT.exists():
            raise FileExistsError('canonical result exists; preserve it')
        for p in (SCRIPT, PROTOCOL):
            assert (ROOT/p).read_bytes() == subprocess.check_output(['git', 'show', 'HEAD:'+p], cwd=ROOT)
    else:
        old = json.loads(RESULT.read_text())
        assert old['sha256'] == hashes(), 'pinned input or implementation changed'
    resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
    signal.alarm(120)
    data = evaluate()
    if args.record:
        record = {'schema': 1, 'sha256': hashes(), 'implementation_commit':
                  subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  'data': data}
        with RESULT.open('x') as f:
            f.write(json.dumps(record, indent=2, sort_keys=True)+'\n')
    else:
        assert old['data'] == data
    print(json.dumps({'pointwise_constant_children': data['pointwise_count'],
                      'descendants': [
                          {'source_rule': c['source_rule'],
                           'same_inherited_observation': c['inherited_observation_same_under_two_fills'],
                           'variants': [
                               {'fill': v['fill'],
                                'derived_rule': v['derived_rule'],
                                'full': v['full_descendant_domain'],
                                'inherited': v['inherited_domain']}
                               for v in c['variants']]}
                          for c in data['nonpointwise_descendants']]}, indent=2))


if __name__ == '__main__':
    main()
