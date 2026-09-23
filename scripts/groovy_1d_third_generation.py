#!/usr/bin/env python3
"""One additional inherited 1D G generation, for the saved Rule-2/16 chains.

The second-generation implementation and result are immutable dependencies.
This runner streams complete cones; it never introduces another state track.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal
import subprocess

import numpy as np

import groovy_1d_second_generation as prior

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = 'docs/research/protocols/groovy-1d-third-generation-20260923.md'
SCRIPT = 'scripts/groovy_1d_third_generation.py'
PREVIOUS = 'results/groovy_1d_second_generation_20260923.json'
RESULT = ROOT/'results/groovy_1d_third_generation_20260923.json'
CHUNK = 32768


def from_record(record):
    return prior.Rule(record['radius'], tuple(map(int, record['outputs_ascending'])))


def digest(rule):
    return hashlib.sha256(bytes(rule.bits)).hexdigest()


def describe(rule):
    return {'radius': rule.radius, 'table_size': len(rule.bits),
            'one_entries': sum(rule.bits), 'output_bytes_sha256': digest(rule)}


def stream_factor(observation, source, radius):
    """Exhaustive local identity at a requested radius, in bounded chunks."""
    m = observation.radius+max(radius, source.radius)
    n = 2*m+1
    if n > 23:
        return {'status': 'cone_cap', 'radius': radius, 'source_bits': n}
    size = 1 << (2*radius+1)
    lows = np.full(size, 2, dtype=np.int8)
    highs = np.full(size, -1, dtype=np.int8)
    for lo in range(0, 1 << n, CHUNK):
        v = np.arange(lo, min(lo+CHUNK, 1 << n), dtype=np.uint64)
        obs = prior.apply(v, n, observation)
        keys = ((obs >> np.uint64(m-observation.radius-radius)) &
                np.uint64(size-1)).astype(np.int64)
        after = prior.apply(v, n, source)
        nxt = prior.apply(after, n-2*source.radius, observation)
        values = ((nxt >> np.uint64(m-source.radius-observation.radius)) & 1).astype(np.int8)
        np.minimum.at(lows, keys, values)
        np.maximum.at(highs, keys, values)
        conflicts = np.flatnonzero((highs >= 0) & (lows != highs))
        if len(conflicts):
            return {'status': 'local_conflict', 'radius': radius, 'source_bits': n,
                    'source_words_checked': min(lo+CHUNK, 1 << n),
                    'conflicting_neighborhood': int(conflicts[0])}
    forced = ''.join('?' if high < 0 else str(int(high)) for high in highs)
    return {'status': 'law', 'radius': radius, 'source_bits': n,
            'source_words': 1 << n, 'forced_outputs_ascending': forced}


def closure(observation, source):
    if len(set(observation.bits)) == 1:
        return {**stream_factor(observation, source, 0),
                'observation_constant': observation.bits[0], 'periods_screened': 0}
    for n in range(1, 13):
        witness = prior.periodic_collision(observation, source, n)
        if witness is not None:
            return {'status': 'no_present_only_law', 'witness': witness,
                    'periods_screened': n, 'all_spatial_radii_excluded': True}
    attempts = []
    for r in range(5):
        cert = stream_factor(observation, source, r)
        attempts.append(cert)
        if cert['status'] == 'law':
            return {**cert, 'periods_screened': 12, 'smaller_radius_attempts': attempts[:-1]}
        if cert['status'] == 'cone_cap':
            break
    return {'status': 'unresolved_within_budget', 'periods_screened': 12,
            'radius_attempts': attempts}


def scalar_xor(a, b):
    assert len(a) == len(b)
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))


def scalar_g(s, rule):
    first = prior.scalar_ring(s, rule)
    twice = prior.scalar_ring(first, rule)
    changed = prior.scalar_ring(scalar_xor(s, first), rule)
    return scalar_xor(scalar_xor(first, twice), changed)


def scalar_third(s, source, f, h):
    return scalar_g(scalar_g(scalar_g(s, source), f), h)


def verify_observation(source, f, h, observation):
    """Direct unpacked triple G on its unreduced original-source support."""
    n = 4*(source.radius+f.radius+h.radius)+1
    assert n <= 21
    checked = 0
    for lo in range(0, 1 << n, CHUNK):
        x = prior.matrix(np.arange(lo, min(lo+CHUNK, 1 << n)), n)
        direct = prior.matrix_g(prior.matrix_g(prior.matrix_g(x, source), f), h)[:, 0]
        table = prior.matrix_apply(x, observation)[:, n//2-observation.radius]
        assert np.array_equal(direct, table)
        checked += len(x)
    return {'direct_unpacked_triple_g': True, 'source_bits': n, 'source_words': checked}


def verify_result(source, f, h, observation, result):
    if result['status'] == 'no_present_only_law':
        w = result['witness']
        actual = [scalar_third(s, source, f, h) for s in w['sources']]
        after = [scalar_third(prior.scalar_ring(s, source), source, f, h) for s in w['sources']]
        assert actual == w['observations'] and after == w['successors']
        assert actual[0] == actual[1] and after[0] != after[1]
        return {'direct_scalar_triple_g_periodic_witness': True}
    return prior.verify_closure(observation, source, result)


def check_prior_hashes():
    record = json.loads((ROOT/PREVIOUS).read_text())
    assert record['sha256'] == prior.hashes(), 'second-generation inputs changed'
    return record


def evaluate():
    previous = check_prior_hashes()['data']
    cases = []
    for child in previous['nonpointwise_descendants']:
        r = child['source_rule']
        if r not in (2, 16):
            continue
        source = prior.eca(r)
        for variant in child['variants']:
            f = from_record(variant['derived_rule'])
            second = from_record(variant['inherited_observation'])
            cert = variant['inherited_domain']
            assert cert['status'] == 'law'
            for h_fill in (0, 1):
                h = prior.total(cert, h_fill)
                gh = prior.groovy(h)
                observation = prior.compose(gh, second)
                composition_verification = verify_observation(source, f, h, observation)
                answer = closure(observation, source)
                answer['verification'] = verify_result(source, f, h, observation, answer)
                case = {'source_rule': r, 'first_fill': variant['fill'],
                        'second_fill': h_fill, 'first_update': f.record(),
                        'second_update': h.record(), 'native_g_of_second_update': gh.record(),
                        'third_observation': describe(observation),
                        'same_as_second_observation': observation == second,
                        'composition_verification': composition_verification,
                        'inherited_domain': answer}
                cases.append(case)
                print(json.dumps({'source': r, 'fills': [variant['fill'], h_fill],
                                  'observation': describe(observation),
                                  'same_as_second': case['same_as_second_observation'],
                                  'closure': answer['status'], 'radius': answer.get('radius'),
                                  'period': answer.get('witness', {}).get('period')}), flush=True)
    assert len(cases) == 8
    return {'cases': cases, 'scope': 'third inherited generation only; sources 2/16; fixed zero/one completions',
            'fourth_generation_evaluated': False}


def hashes():
    paths = (PROTOCOL, SCRIPT, PREVIOUS, prior.PROTOCOL, prior.SCRIPT, prior.INPUT)
    return {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--record', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.record:
        if RESULT.exists():
            raise FileExistsError('preserve the canonical result')
        for p in (SCRIPT, PROTOCOL):
            assert (ROOT/p).read_bytes() == subprocess.check_output(['git', 'show', 'HEAD:'+p], cwd=ROOT)
    else:
        old = json.loads(RESULT.read_text())
        assert old['sha256'] == hashes(), 'pinned file changed'
    resource.setrlimit(resource.RLIMIT_AS, (2*1024**3, 2*1024**3))
    signal.alarm(120)
    data = evaluate()
    if args.record:
        record = {'schema': 1, 'sha256': hashes(), 'data': data,
                  'implementation_commit': subprocess.check_output(
                      ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()}
        with RESULT.open('x') as out:
            out.write(json.dumps(record, indent=2, sort_keys=True)+'\n')
    else:
        assert old['data'] == data
    print('Third-generation certificates verified.', flush=True)


if __name__ == '__main__':
    main()
