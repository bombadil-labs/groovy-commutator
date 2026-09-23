#!/usr/bin/env python3
"""Frozen finite search pilot. Results are exclusive-create; no paid call in tests.

Each timed arm runs in a fresh Python process and a fresh SWI-Prolog WASM
process. The parent includes process startup, serialization and shutdown in
wall time. A timeout kills the complete process group and retains its trace.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import statistics
import subprocess
import sys
import time
import urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TARGET = (0, 1, 0, 0, 0, 0, 1, 0)
ARMS = ('cost_scan', 'witness_guided', 'jev_ranked')
JEV_MODEL = 'jev-1.13.0'
INPUTS = [str(p.relative_to(ROOT)) for p in (
    HERE/'run.py', HERE/'verify.py', HERE/'grammar.pl', HERE/'bridge.mjs',
    HERE/'package.json', HERE/'package-lock.json',
    ROOT/'scripts/audit_block3_representation_design.py',
    ROOT/'docs/research/protocols/relational-search-pilot-20260923.md')]


def load_audit():
    spec = importlib.util.spec_from_file_location(
        'block3_audit', ROOT/'scripts/audit_block3_representation_design.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def weight(p):
    return math.prod(c**c for c in Counter(p).values())


def order(ps):
    return sorted(map(tuple, ps), key=lambda p: (-weight(p), p))


def validate_stream(ps, reference):
    ps = list(map(tuple, ps))
    if len(ps) != len(set(ps)) or set(ps) != set(reference):
        raise ValueError('candidate stream is incomplete, duplicated, or outside grammar')
    return order(ps)


def codes(state):
    return [(int(state) >> (3*i)) & 7 for i in range(4)]


def collides(p, a, b):
    return all(p[x] == p[y] for x, y in zip(a, b, strict=True))


class Domain:
    def __init__(self):
        self.audit = load_audit()
        import numpy as np
        self.np = np
        fine = self.audit.fine_state_map()
        self.step = fine[fine[fine]]
        self.target = self.audit.observation(TARGET)
        self.word, self.hstar = self.audit.explicit_future(self.step, self.target)
        _, first, self.future = np.unique(self.word, axis=0,
                                        return_index=True, return_inverse=True)
        representatives = first[self.future]
        # Stabilization is a certificate only with a deterministic quotient.
        if not (np.array_equal(self.target, self.target[representatives]) and
                np.array_equal(self.future[self.step],
                               self.future[self.step[representatives]])):
            raise AssertionError('target-future partition is not forward-consistent')

    def oracle(self, p):
        z = self.audit.observation(p)
        _, first, inverse = self.np.unique(z, return_index=True, return_inverse=True)
        representatives = first[inverse]
        bad = self.np.flatnonzero(self.future != self.future[representatives])
        if not len(bad):
            return None
        b = int(bad[0])
        a = int(representatives[b])
        t = int(self.np.flatnonzero(self.word[a] != self.word[b])[0])
        return {'states': [a, b], 'codes_a': codes(a), 'codes_b': codes(b),
                'first_target_difference': t}

    def validate_witness(self, p, w):
        a, b = w['states']
        if not (0 <= a < 4096 and 0 <= b < 4096):
            raise ValueError('witness state outside ring')
        if w['codes_a'] != codes(a) or w['codes_b'] != codes(b):
            raise ValueError('forged block codes')
        if not collides(p, codes(a), codes(b)):
            raise ValueError('witness does not collide under rejected encoder')
        bad = self.np.flatnonzero(self.word[a] != self.word[b])
        if not len(bad) or int(bad[0]) != w['first_target_difference']:
            raise ValueError('witness does not certify the stated target disagreement')


class Bridge:
    def __init__(self):
        self.proc = subprocess.Popen(['node', str(HERE/'bridge.mjs')],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        ready = json.loads(self.proc.stdout.readline())
        if not ready.get('ready'):
            raise RuntimeError('Prolog engine did not start')
        self.version = ready['version']

    def call(self, op, **kwargs):
        self.proc.stdin.write(json.dumps({'op': op, **kwargs}) + '\n')
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError('Prolog bridge exited')
        reply = json.loads(line)
        if not reply['ok']:
            raise RuntimeError(reply['error'])
        return reply['result']

    def close(self):
        if self.proc.poll() is None:
            self.call('close')
            self.proc.wait(timeout=5)
        self.proc.stdin.close()
        self.proc.stdout.close()


@contextmanager
def phase(times, name):
    started = time.perf_counter()
    try:
        yield
    finally:
        times[name] = times.get(name, 0.0) + time.perf_counter()-started


def emit(kind, **data):
    print(json.dumps({'event': kind, **data}), flush=True)


def representation_cost(p):
    labels = len(set(p))
    bits = (labels-1).bit_length()
    return {'labels': labels, 'fixed_width_row_bits': 4*bits,
            'encoding_table_bits': 8*bits, 'source_bits_per_block_read': 3,
            'encoding_lookups_per_row': 4, 'retained_source_bits_for_refresh': 12,
            'fine_updates_per_refresh': 3, 'autonomous_update_synthesized': False}


def jev_request(ps, indices, witnesses):
    state = {
        'contract': 'Choose an encoder that separates states with different entire fixed-target futures. '
                    'Four disjoint three-bit blocks form a periodic binary row. '
                    'Codes use little-endian bits. Target is applied separately to every block. '
                    'Compare the target at cadence three. The exact verifier tests all 4096 rows. '
                    'Candidates shown have equal uniform-source observation entropy. '
                    'Witness pairs have equal observations under previous failed candidates '
                    'but different fixed-target futures. These are constraints, not random examples.',
        'target': list(TARGET),
        'candidates': {f'c{i}': {'classes': [[j for j, v in enumerate(ps[i]) if v == label]
                          for label in sorted(set(ps[i]))], **representation_cost(ps[i])}
                       for i in indices},
        'recent_witnesses': [{k: v for k, v in w.items() if k != 'candidate'}
                             for w in witnesses[-4:]]}
    return {'model': JEV_MODEL, 'state': state, 'questions': {'next': {
        'type': 'choice',
        'instructions': 'Select the candidate most likely to pass the exact target-future verifier. '
                        'A zero immediate information gain does not disqualify a distinction. '
                        'Return one supplied choice; this is heuristic search advice, not a proof.',
        'criteria': {f'c{i}': f'Candidate c{i}' for i in indices}}}}


def choose_jev(ps, indices, witnesses, attempts):
    if len(indices) == 1:
        return indices[0], attempts, None
    if attempts >= 6:
        return indices[0], attempts, {'status': 'budget_fallback'}
    request = jev_request(ps, indices, witnesses)
    body = json.dumps(request, separators=(',', ':')).encode()
    record = {'request': request, 'request_bytes': len(body)}
    if len(body) > 8000:
        record['status'] = 'request_size_fallback'
        return indices[0], attempts, record
    attempts += 1
    try:
        http = urllib.request.Request('https://api.typesafe.ai/v1/systemone', data=body,
            headers={'Authorization': 'Bearer '+os.environ['TYPESAFE_API_KEY'],
                     'Content-Type': 'application/json'})
        with urllib.request.urlopen(http, timeout=20) as response:
            raw = response.read().decode()
        record['raw_response'] = raw
        response = json.loads(raw)
        record['model'] = response.get('model')
        record['usage'] = response.get('usage')
        choice = response['answers']['next']['choice']
        selected = {f'c{i}': i for i in indices}[choice]
        record['status'] = 'selected'
        return selected, attempts, record
    except Exception as exc:
        # Exceptions can include response details; do not persist headers/keys.
        record.update(status='api_or_choice_fallback', error_type=type(exc).__name__)
        return indices[0], attempts, record


def worker(arm):
    started = time.perf_counter()
    times, witnesses, queries, jev_records = {}, [], [], []
    bridge = None
    try:
        with phase(times, 'domain_and_future'):
            domain = Domain()
        with phase(times, 'prolog_startup'):
            bridge = Bridge()
        with phase(times, 'grammar_and_order'):
            raw = bridge.call('generate', target=TARGET)
            ps = validate_stream(raw, domain.audit.target_interval())
            if len(ps) != 406:
                raise AssertionError('wrong grammar size')
            bridge.call('install', rows=[[i, weight(p), p] for i, p in enumerate(ps)])
        emit('domain', encoders=ps, hstar=domain.hstar,
             future_classes=int(len(domain.np.unique(domain.future))),
             prolog_version=bridge.version)
        attempts = 0
        winner = None
        for _ in range(406):
            with phase(times, 'selection_and_prefilter'):
                indices = bridge.call('next', guided=arm != 'cost_scan',
                                      limit=8 if arm == 'jev_ranked' else 1)
            if not indices:
                break
            selected = indices[0]
            if arm == 'jev_ranked':
                with phase(times, 'jev_selection'):
                    selected, attempts, record = choose_jev(ps, indices, witnesses, attempts)
                if record:
                    jev_records.append(record)
                    emit('jev', **record)
            with phase(times, 'oracle'):
                w = domain.oracle(ps[selected])
            queries.append(selected)
            with phase(times, 'witness_validation_and_insert'):
                bridge.call('mark', index=selected)
                if w is not None:
                    domain.validate_witness(ps[selected], w)
                    w.update(id=len(witnesses), candidate=selected)
                    witnesses.append(w)
                    if arm != 'cost_scan':
                        bridge.call('witness', id=w['id'], a=w['codes_a'], b=w['codes_b'])
            emit('query', candidate=selected, witness=w)
            if w is None:
                winner = selected
                break
        with phase(times, 'collect_and_shutdown'):
            stats = bridge.call('stats')
            version = bridge.version
            bridge.close()
        if winner is None:
            raise RuntimeError('complete grammar exhausted without a sufficient candidate')
        p = ps[winner]
        ht = 4*(3-math.log2(weight(TARGET))/8)
        added = 4*(3-math.log2(weight(p))/8)-ht
        incomplete = any(x['status'] not in ('selected', 'budget_fallback') for x in jev_records)
        emit('finish', status='incomplete_jev' if incomplete else 'complete', arm=arm,
             winner=winner, encoder=p, exact_cost_weight=weight(p), added_entropy_bits=added,
             full_oracle_calls=len(queries), queries=queries, witnesses=witnesses,
             **stats, pruned_candidates=len(stats['rejections']), phase_seconds=times,
             internal_wall_seconds=time.perf_counter()-started,
             parent_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
             prolog_version=version, representation=representation_cost(p),
             jev_requests=attempts, jev_budget_fallbacks=sum(
                 x['status'] == 'budget_fallback' for x in jev_records))
    except Exception as exc:
        emit('failure', status='implementation_failure', arm=arm,
             error_type=type(exc).__name__, message=str(exc), phase_seconds=times)
        return 1
    finally:
        if bridge is not None and bridge.proc.poll() is None:
            bridge.proc.kill()
            bridge.proc.wait()
            bridge.proc.stdin.close()
            bridge.proc.stdout.close()
    return 0


def execute(arm):
    start = time.perf_counter()
    env = {**os.environ, 'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1'}
    proc = subprocess.Popen([sys.executable, str(HERE/'run.py'), '--worker', arm],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env, start_new_session=True)
    status = 'finished'
    try:
        out, err = proc.communicate(timeout=180 if arm == 'jev_ranked' else 120)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        out, err = proc.communicate()
        status = 'resource_limit'
    elapsed = time.perf_counter()-start
    events = []
    for line in out.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append({'event': 'unparsed_stdout', 'line': line})
    finishes = [e for e in events if e.get('event') == 'finish']
    return {'arm': arm, 'status': status, 'exit_code': proc.returncode,
            'total_wall_seconds': elapsed, 'stderr': err, 'events': events,
            'result': finishes[-1] if finishes else None}


def audit_result(run, domain):
    """Replay the complete certificate, independently of Prolog's constraints."""
    result = run['result']
    if run['exit_code'] != 0 or result is None:
        raise ValueError('no completed search certificate')
    entries = [e for e in run['events'] if e.get('event') == 'domain']
    if len(entries) != 1:
        raise ValueError('missing or duplicated domain record')
    ps = validate_stream(entries[0]['encoders'], domain.audit.target_interval())
    if list(map(tuple, entries[0]['encoders'])) != ps:
        raise ValueError('candidate stream is not in exact cost order')
    winner = result['winner']
    if any(not isinstance(i, int) or not 0 <= i < len(ps) for i in result['queries']):
        raise ValueError('query index outside grammar')
    if tuple(result['encoder']) != ps[winner]:
        raise ValueError('wrong winner encoding')
    witnesses = result['witnesses']
    if [w['id'] for w in witnesses] != list(range(len(witnesses))):
        raise ValueError('witness IDs are not unique and consecutive')
    failed = {}
    for w in witnesses:
        domain.validate_witness(ps[w['candidate']], w)
        if w['candidate'] in failed:
            raise ValueError('duplicate failed oracle query')
        failed[w['candidate']] = w['id']
    if result['queries'] != [w['candidate'] for w in witnesses]+[winner]:
        raise ValueError('query trace and witnesses disagree')
    query_events = [e for e in run['events'] if e.get('event') == 'query']
    if [e['candidate'] for e in query_events] != result['queries'] or \
       [e['witness'] for e in query_events] != witnesses+[None]:
        raise ValueError('raw oracle trace and certificate disagree')
    rejected = {}
    for candidate, witness_id in result['rejections']:
        if not (0 <= candidate < len(ps) and 0 <= witness_id < len(witnesses)):
            raise ValueError('rejection reference outside certificate')
        if candidate in rejected or candidate in result['queries']:
            raise ValueError('duplicate or queried pruned candidate')
        w = witnesses[witness_id]
        if not collides(ps[candidate], w['codes_a'], w['codes_b']):
            raise ValueError('pruning reason does not apply')
        rejected[candidate] = witness_id
    covered = set(failed) | set(rejected)
    for i, p in enumerate(ps):
        cheaper = weight(p) > weight(ps[winner])
        before = i < winner and run['arm'] != 'jev_ranked'
        if (cheaper or before) and i not in covered:
            raise ValueError('cheaper or earlier candidate omitted without certificate')
    if winner in covered or not domain.audit.metrics(ps[winner], domain.word)['closed']:
        raise ValueError('winner fails independent target-future sufficiency check')
    if result['full_oracle_calls'] != len(result['queries']) or \
       result['pruned_candidates'] != len(rejected):
        raise ValueError('invalid cost counters')
    expected_entropy = domain.audit.metrics(ps[winner], domain.word)['H'] - \
                       domain.audit.metrics(TARGET, domain.word)['H']
    if abs(expected_entropy-result['added_entropy_bits']) > 1e-9:
        raise ValueError('invalid entropy accounting')
    return True


def final_audit(runs):
    started = time.perf_counter()
    domain = Domain()
    reference = domain.audit.target_interval()
    nodes = {p: domain.audit.metrics(p, domain.word) for p in reference}
    closed = [p for p in reference if nodes[p]['closed']]
    best_weight = max(map(weight, closed))
    optima = sorted(p for p in closed if weight(p) == best_weight)
    greedy = domain.audit.greedy(nodes)
    ht = nodes[TARGET]['H']
    optimum_cost = nodes[optima[0]]['H']-ht
    greedy_cost = nodes[greedy[-1]]['H']-ht
    checks = {'reference_406': len(reference) == 406,
        'known_optimum': tuple(map(int, '01230243')) in optima,
        'known_optimum_cost': abs(optimum_cost-5.754887502163468) < 1e-9,
        'known_greedy_endpoint': greedy[-1] == tuple(map(int, '01230245')),
        'known_greedy_regret': abs(greedy_cost-optimum_cost-1) < 1e-9}
    for i, run in enumerate(runs):
        try:
            checks[f'certificate_{i}'] = audit_result(run, domain)
        except Exception as exc:
            checks[f'certificate_{i}'] = False
            run['audit_error'] = str(exc)
    keys = ('winner', 'encoder', 'exact_cost_weight', 'full_oracle_calls', 'queries',
            'witnesses', 'candidate_visits', 'witness_comparisons', 'rejections')
    for arm in ARMS[:2]:
        complete = [r['result'] for r in runs if r['arm'] == arm and r['result']]
        checks[f'{arm}_repeats_agree'] = len(complete) == 3 and all(
            all(x[k] == complete[0][k] for k in keys) for x in complete[1:])
    return {'ok': all(checks.values()), 'checks': checks, 'global_optima': optima,
            'optimum_added_entropy_bits': optimum_cost, 'greedy_path': greedy,
            'greedy_added_entropy_bits': greedy_cost,
            'elapsed_seconds': time.perf_counter()-started}


def predictions(runs, jev_status, audit):
    local = {a: [r for r in runs if r['arm'] == a] for a in ARMS[:2]}
    local_checks = [v for k, v in audit['checks'].items() if k != 'certificate_6']
    valid = all(local_checks) and all(r['result'] and r['result']['status'] == 'complete'
                                    for r in runs if r['arm'] in ARMS[:2])
    if not valid:
        return {'predictions': {
            **{f'P{i}': {'status': 'invalid', 'reason': 'local execution or audit failed'}
               for i in range(1, 5)},
            'P5': {'status': 'not_evaluated', 'reason': jev_status}}, 'local_summary': {}}
    def score(value):
        return {'status': 'supported' if value else 'failed'}
    summaries = {a: {'median_total_wall_seconds': statistics.median(
                         r['total_wall_seconds'] for r in rs),
                     'full_oracle_calls': rs[0]['result']['full_oracle_calls']}
                 for a, rs in local.items()}
    ps = {'P1': score(all(len(next(e for e in r['events'] if e['event']=='domain')['encoders'])
                                  == 406 for rs in local.values() for r in rs)),
          'P2': score(all(r['result']['encoder'] == list(map(int, '01230243'))
                         for rs in local.values() for r in rs)),
          'P3': score(summaries['witness_guided']['full_oracle_calls'] <
                      summaries['cost_scan']['full_oracle_calls']),
          'P4': score(summaries['witness_guided']['median_total_wall_seconds'] <
                      summaries['cost_scan']['median_total_wall_seconds']),
          'P5': {'status': 'not_evaluated', 'reason': jev_status}}
    jev = [r for r in runs if r['arm'] == 'jev_ranked']
    if jev and jev[0]['result'] and jev[0]['result']['status'] == 'complete' and audit['ok']:
        same = abs(jev[0]['result']['added_entropy_bits'] - audit['optimum_added_entropy_bits']) < 1e-9
        ps['P2']['jev_same_objective'] = same
        if not same:
            ps['P2']['status'] = 'failed'
        ps['P5'] = {**score(jev[0]['total_wall_seconds'] <
                           summaries['witness_guided']['median_total_wall_seconds']),
                    'scope': 'single exploratory acquisition'}
    return {'predictions': ps, 'local_summary': summaries}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--worker', choices=ARMS)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--implementation-commit')
    ap.add_argument('--setup-seconds', type=float, default=None)
    ap.add_argument('--setup-note', default='not recorded')
    args = ap.parse_args()
    if args.worker:
        return worker(args.worker)
    if not args.output or not args.implementation_commit:
        ap.error('--output and --implementation-commit are required')
    # Reserve the canonical path before any evaluation. Never overwrite results.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as destination:
        result = {'schema': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
            'implementation_commit': args.implementation_commit,
            'protocol_commit': 'b244bb99e47d518c946870dcf265a63998cd9253',
            'source_hashes': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS},
            'environment': {'python': sys.version, 'platform': platform.platform(),
                'node': subprocess.check_output(['node', '--version'], text=True).strip(),
                'swipl_wasm_package': '8.1.3', 'numpy': load_audit().np.__version__,
                'thread_limit': 1, 'os_caches_flushed': False},
            'setup': {'npm_install_seconds': args.setup_seconds, 'note': args.setup_note},
            'contract': {'rule': 24, 'ring': 12, 'cadence': 3, 'target': TARGET,
                'candidate_count': 406, 'goal': 'entire fixed-target future on the finite ring'},
            'runs': []}
        has_key = bool(os.environ.get('TYPESAFE_API_KEY'))
        try:
            schedule = ['cost_scan', 'witness_guided', 'witness_guided',
                        'cost_scan', 'cost_scan', 'witness_guided']
            for arm in schedule:
                run = execute(arm)
                result['runs'].append(run)
                print(arm, run['status'], round(run['total_wall_seconds'], 4), flush=True)
            if has_key:
                result['runs'].append(execute('jev_ranked'))
            result['jev'] = {'status': 'evaluated' if has_key else 'not_evaluated',
                             'reason': None if has_key else 'missing_credential'}
            result['independent_audit'] = final_audit(result['runs'])
            result.update(predictions(result['runs'],
                'incomplete_or_failed_acquisition' if has_key else 'missing_credential',
                result['independent_audit']))
        except Exception as exc:
            result['execution_error'] = {'type': type(exc).__name__, 'message': str(exc)}
            result['predictions'] = {f'P{i}': {'status': 'invalid', 'reason': 'execution_error'}
                                     for i in range(1, 6)}
        json.dump(result, destination, indent=2)
        destination.write('\n')
    return 0 if result.get('independent_audit', {}).get('ok') else 1


if __name__ == '__main__':
    raise SystemExit(main())
