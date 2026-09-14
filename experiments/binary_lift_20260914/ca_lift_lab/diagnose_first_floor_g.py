"""Diagnose cached first-floor G failures; do not repeat an admission census.

The new test isolates equal-probe constraints within each P/D field, then
between fields. All saved and newly extracted witnesses are reconstructed
with scalar, nonperiodic dependency windows independent of the numpy encoder.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from audit_binary_reference import keys
from verify_polarization_proposal import d, encode

ROOT = Path(__file__).resolve().parent
N = 2048
FIELDS = ('P', 'D', 'M', 'Q')


def spec(rec):
    if 'reference_spec' in rec:
        return tuple(rec['reference_spec'])
    if rec['reference'].startswith('directed:'):
        _, a, b, relation = rec['reference'].split(':')
        return int(a), int(b), 0 if relation == 'left-and-not-right' else 1
    _, a, b = rec['reference'].split(':')
    return int(a), int(b), -1


def clash(k, v):
    ix = np.argsort(k, kind='stable')
    kk, vv = k[ix], v[ix]
    bad = np.flatnonzero((kk[1:] == kk[:-1]) & (vv[1:] != vv[:-1]))
    if not len(bad):
        return None
    j = int(bad[0])
    return {'key': int(kk[j]), 'indices': [int(ix[j]), int(ix[j+1])],
            'bits': [int(vv[j]), int(vv[j+1])]}


@lru_cache(maxsize=32)
def basis(rule, mask, sign, a, b, reverse):
    s = ((np.arange(N)[:, None] >> np.arange(10, -1, -1)) & 1).astype(np.uint8)
    ds = d(s, rule)
    es = s ^ ds
    ees = es ^ d(es, rule)
    choice = {'mask': mask, 'shift': sign}
    aa, bb, cc = (encode(t, rule, choice) for t in (s, es, ees))
    def q(t):
        x, y = np.roll(t, -a, axis=-1), np.roll(t, -b, axis=-1)
        return x & y if reverse == -1 else (x & (1-y) if reverse == 0 else (1-x) & y)
    aa = np.concatenate([aa, q(s)[:, None, :]], axis=1)
    bb = np.concatenate([bb, q(es)[:, None, :]], axis=1)
    g = d(es, rule) ^ ds ^ d(ds, rule)
    carrier = np.stack([g[:, 5] ^ g[:, 5+sign], g[:, 5]], axis=1)
    desired = aa[:, :2, 5] ^ cc[:, :2, 5] ^ carrier
    return aa, aa ^ bb, desired


class ScalarWindow:
    def __init__(self, rule, mask, sign, a, b, reverse, word):
        self.r, self.mask, self.sign = rule, mask, sign
        self.a, self.b, self.reverse, self.word = a, b, reverse, word
        self.states, self.fields = {}, {}

    def state(self, t, x):
        if (t, x) not in self.states:
            if t == 0:
                assert -5 <= x <= 5, (t, x)
                value = (self.word >> (5-x)) & 1
            else:
                idx = 4*self.state(t-1, x-1)+2*self.state(t-1, x)+self.state(t-1, x+1)
                # Integrate the primitive derivative by XOR.
                value = self.state(t-1, x) ^ (((self.r ^ 204) >> idx) & 1)
            self.states[t, x] = value
        return self.states[t, x]

    def delta(self, t, x):
        return self.state(t, x) ^ self.state(t+1, x)

    def field(self, t, c, x):
        if (t, c, x) not in self.fields:
            s = self.state(t, x)
            if c == 0:
                v = s ^ self.state(t, x+self.sign)
            elif c == 1:
                v = self.delta(t, x)
            elif c == 2:
                dd = self.delta(t, x)
                v = {'birth': (1-s)&dd, 'death': s&dd,
                     'stay_one': s&(1-dd), 'stay_zero': (1-s)&(1-dd)}[self.mask]
            else:
                left, right = self.state(t, x+self.a), self.state(t, x+self.b)
                v = left & right if self.reverse == -1 else (left & (1-right) if self.reverse == 0 else (1-left) & right)
            self.fields[t, c, x] = v
        return self.fields[t, c, x]

    def g(self, x):
        idx = 4*self.delta(0, x-1)+2*self.delta(0, x)+self.delta(0, x+1)
        d_on_delta = ((self.r ^ 204) >> idx) & 1
        return self.delta(1, x) ^ self.delta(0, x) ^ d_on_delta


@lru_cache(maxsize=2048)
def scalar(*args):
    return ScalarWindow(*args)


def event(rec, index, mode):
    z = None if mode == 'raw' else int(mode[-1])
    if index == 6*N:
        assert z is not None
        return {'kind': 'zero', 'key': 0, 'bit': z, 'field': None}
    order = rec['order']
    if index < 4*N:
        kind, word, phase = 'native', index//4, index%4
        c = order[phase]
    else:
        kind, word, c = 'probe', (index-4*N)//2, (index-4*N)%2
        phase = order.index(c)
    ch = rec['recipe'][0]
    w = scalar(rec['rule'], ch['mask'], ch['shift'], *spec(rec), word)
    key = 0
    for dy in (0, 1, 2, -1, -2):
        f = order[(phase+dy) % 4]
        for x in range(-2, 3):
            v = w.field(0, f, x)
            if kind == 'probe':
                v ^= w.field(1, f, x)
            key = (key << 1) | v
    if kind == 'native':
        bit = w.field(0, c, 0) ^ w.field(1, c, 0)
    else:
        carrier = w.g(0) ^ w.g(ch['shift']) if c == 0 else w.g(0)
        bit = w.field(0, c, 0) ^ w.field(2, c, 0) ^ carrier
        if z is not None:
            bit ^= z ^ ((rec['rule'] & 1) if c == 1 else 0)
    return {'kind': kind, 'key': key, 'bit': bit, 'field': FIELDS[c],
            'phase': phase, 'source_word': word, 'source_bits': format(word, '011b'),
            'source_center': w.state(0, 0)}


def verify(rec, cf, mode):
    ev = [event(rec, i, mode) for i in cf['event_indices']]
    assert [e['key'] for e in ev] == [cf['key']]*2, (rec, cf, ev)
    assert [e['bit'] for e in ev] == cf['bits'], (rec, cf, ev)
    assert ev[0]['bit'] != ev[1]['bit']
    return ev


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    holdouts = set(json.loads((ROOT/'runs/universal_3d/summary.json').read_text())['missing_first_floor_G'])
    counters = Counter()
    by_rule = defaultdict(Counter)
    records = []
    inputs = {}
    for family in ('binary_fresh_all256', 'directed_full256'):
        p = ROOT/'runs'/family/'candidates.jsonl'
        inputs[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
        for line in p.open():
            r = json.loads(line)
            if r['rule'] not in holdouts:
                continue
            counters['domain'] += 1
            by_rule[r['rule']]['domain'] += 1
            for gate in ('native', 'source'):
                counters[gate+'_passes'] += r[gate]['passes']
            if r['first_order_pass']:
                r['family'] = family
                records.append(r)
    records.sort(key=lambda r: (r['rule'], r['recipe'][0]['mask'], r['recipe'][0]['shift'], r['reference'], r['order']))
    categories = defaultdict(set)
    with (args.output/'diagnoses.jsonl').open('w') as log:
        for rec in records:
            assert rec['source_width'] == 11 and rec['rx'] == rec['ry'] == 2
            out = {k: rec[k] for k in ('rule', 'recipe', 'reference', 'order', 'family')}
            saved = {}
            for mode, branch in [('raw', rec['raw']), ('z0', rec['centered_branches'][0]), ('z1', rec['centered_branches'][1])]:
                assert not branch['passes']
                cf = branch['conflict']
                ev = verify(rec, cf, mode)
                typ = '/'.join(e['kind'] for e in ev)
                saved[mode] = {'conflict': cf, 'events': ev, 'type': typ,
                               'same_field': ev[0]['field'] == ev[1]['field']}
                counters['saved_'+mode+'_'+typ] += 1
                counters['verified_saved_pairs'] += 1
            ch = rec['recipe'][0]
            aa, delta, desired = basis(rec['rule'], ch['mask'], ch['shift'], *spec(rec))
            order = rec['order']
            pk = keys(delta[:, order, :], 2, 2)[:, [order.index(0), order.index(1)]]
            same = {}
            for c in (0, 1):
                cf = clash(pk[:, c], desired[:, c])
                if cf:
                    cf['event_indices'] = [4*N+2*i+c for i in cf.pop('indices')]
                    ev = verify(rec, cf, 'raw')
                    same[FIELDS[c]] = {'conflict': cf, 'events': ev}
                    counters['verified_new_pairs'] += 1
            out['same_field_probe_conflicts'] = same
            if same:
                category = 'same_field_probe_ambiguity'
            else:
                corrected = desired.copy()
                corrected[:, 1] ^= rec['rule'] & 1
                cf = clash(pk.ravel(), corrected.ravel())
                if cf:
                    cf['event_indices'] = [4*N+i for i in cf.pop('indices')]
                    out['cross_field_probe_conflict'] = {'conflict': cf, 'events': verify(rec, cf, 'z0')}
                    counters['verified_new_pairs'] += 1
                    category = 'cross_field_probe_ambiguity'
                else:
                    category = 'native_probe_or_zero_incompatibility'
            counters[category] += 1
            by_rule[rec['rule']][category] += 1
            categories[category].add(rec['rule'])
            out['category'] = category
            out['saved_witnesses'] = saved
            if same:
                for field, wit in same.items():
                    e, f = wit['events']
                    counters['same_field_'+field] += 1
                    counters['same_field_center_'+str(e['source_center'] == f['source_center'])] += 1
                    counters['same_field_complement_'+str(e['source_word'] ^ f['source_word'] == N-1)] += 1
            log.write(json.dumps(out, separators=(',', ':'))+'\n')
    counters['faithful'] = len(records)
    summary = {'rules': sorted(holdouts), 'counts': dict(counters),
               'rule_categories': {k: sorted(v) for k, v in categories.items()},
               'by_rule': {str(r): dict(c) for r, c in sorted(by_rule.items())},
               'seconds': time.perf_counter()-start,
               'scope': 'All faithful recipes for all36holdouts. Every stored raw/z0/z1 witness independently reconstructed; new complete within-field probe consistency diagnostics at width11. Category precedence: same-field, cross-field, then native/zero overlap.',
               'input_sha256': inputs,
               'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    (args.output/'source_diagnosis.py').write_text(Path(__file__).read_text())
    print(json.dumps({k: summary[k] for k in ('counts', 'rule_categories', 'seconds')}), flush=True)


def tagged_supplement(output):
    """Resolve whether the remaining obstruction survives a phase oracle.

    This is a relaxation for diagnosis only: four row-specific native rules
    are not a uniform unlabeled binary CA and are not counted as successes.
    """
    from audit_temporal_reach import check
    start = time.perf_counter()
    rows = [r for r in map(json.loads, (output/'diagnoses.jsonl').read_text().splitlines())
            if not r['same_field_probe_conflicts']]
    counts, per_rule = Counter(), defaultdict(Counter)
    with (output/'phase_oracle.jsonl').open('w') as log:
        for rec in rows:
            ch, order = rec['recipe'][0], rec['order']
            aa, delta, desired = basis(rec['rule'], ch['mask'], ch['shift'], *spec(rec))
            bk, pk = keys(aa[:, order, :], 2, 2), keys(delta[:, order, :], 2, 2)
            result = {k: rec[k] for k in ('rule', 'recipe', 'reference', 'order', 'category')}
            fields = {}
            for c in (0, 1):
                phase = order.index(c)
                phases = {}
                for mode, z in [('raw', None), ('z0', 0), ('z1', 1)]:
                    target = desired[:, c].copy()
                    if z is not None and c == 1:
                        target ^= rec['rule'] & 1
                    branch = check(bk[:, phase], delta[:, c, 5], pk[:, phase], target, z)
                    if not branch['passes']:
                        cf = branch['conflict']
                        cf['event_indices'] = [4*i+phase if i < N else (4*N+2*(i-N)+c if i < 2*N else 6*N)
                                               for i in cf['event_indices']]
                        branch['events'] = verify(rec, cf, mode)
                        counts['verified_failed_branches'] += 1
                    phases[mode] = branch
                    counts['branches'] += 1
                fields[FIELDS[c]] = phases
            result['fields'] = fields
            result['phase_aware_original_passes'] = all(v['raw']['passes'] for v in fields.values())
            result['phase_aware_centered_passes'] = all(v['z0']['passes'] or v['z1']['passes'] for v in fields.values())
            for name in ('phase_aware_original_passes', 'phase_aware_centered_passes'):
                counts[name] += result[name]
                per_rule[rec['rule']][name] += result[name]
            counts['cases'] += 1
            per_rule[rec['rule']]['cases'] += 1
            log.write(json.dumps(result, separators=(',', ':'))+'\n')
    summary = {'counts': dict(counts), 'by_rule': {str(k): dict(v) for k, v in sorted(per_rule.items())},
               'seconds': time.perf_counter()-start,
               'scope': 'Only608recipes without a same-field probe contradiction; other2432already fail even with phase labels. Each phase may choose its own zero output. Diagnostic relaxation, not a new admitted construction.'}
    (output/'phase_oracle_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    (output/'source_diagnosis.py').write_text(Path(__file__).read_text())
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3 and sys.argv[1] == '--tagged-run':
        tagged_supplement(Path(sys.argv[2]))
    else:
        main()
