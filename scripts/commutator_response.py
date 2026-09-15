#!/usr/bin/env python3
"""Four-arm repeated-pulse interaction, with causally available G histories."""
import json
import time
import numpy as np
from commutator_history import ROOT, UNIT, OLD, digest, save, open_step


def step(x, radius, rule, correction):
    if rule is None:
        return open_step(x, radius, correction)
    lut = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
    return lut[4*x[..., :-2]+2*x[..., 1:-1]+x[..., 2:]]


def short_case(radius, rule=None, correction=True):
    n = 6*radius+1
    x = ((np.arange(1 << n)[:, None] >> np.arange(n-1, -1, -1)) & 1).astype(np.uint8)
    primed = x.copy(); primed[:, 3*radius] ^= 1
    a = step(x, radius, rule, correction)
    b = step(primed, radius, rule, correction)
    a2 = a.copy(); a2[:, 2*radius] ^= 1
    b2 = b.copy(); b2[:, 2*radius] ^= 1
    r0 = step(a2, radius, rule, correction) ^ step(a, radius, rule, correction)
    r1 = step(b2, radius, rule, correction) ^ step(b, radius, rule, correction)
    interaction = r0 ^ r1
    changed = np.any(interaction, axis=1)
    witness = int(np.flatnonzero(changed)[0]) if np.any(changed) else None
    return {'radius': radius, 'rule': rule, 'correction': correction,
            'contexts': len(x), 'interacting_contexts': int(changed.sum()),
            'witness': None if witness is None else {
                'word': x[witness].tolist(), 'response_unprimed': r0[witness].tolist(),
                'response_primed': r1[witness].tolist(), 'interaction': interaction[witness].tolist()}}


def probe(initial, radius, delay, rule=None, correction=True):
    horizon = 32
    remote = radius*(delay+2*horizon)+1
    offsets = np.array([-radius*delay, 0, radius*delay, remote])
    pad = 2*radius*(delay+horizon)+remote
    if rule is not None:
        origins = np.linspace(0, len(initial)-1, 16, dtype=int)
        indices = (origins[:, None]+np.arange(-pad, pad+1)) % len(initial)
    else:
        assert 2*pad+1 <= len(initial)
        origins = np.linspace(pad, len(initial)-pad-1, 16, dtype=int)
        indices = origins[:, None]+np.arange(-pad, pad+1)
    a = initial[indices].copy(); b = a.copy(); b[:, pad] ^= 1
    older_a = older_b = None
    hist_a, hist_b = [], []
    history_times = []
    for tick in range(delay):
        aa = step(a, radius, rule, correction)
        bb = step(b, radius, rule, correction)
        t = tick-1
        if older_a is not None and t >= max(0, delay-17):
            da = older_a[:, radius:-radius] ^ a
            db = older_b[:, radius:-radius] ^ b
            ga = a[:, radius:-radius] ^ aa ^ step(da, radius, rule, correction)
            gb = b[:, radius:-radius] ^ bb ^ step(db, radius, rule, correction)
            center = pad-radius*(t+2)
            at = center+offsets
            assert min(at) >= 0 and max(at) < ga.shape[1]
            hist_a.append(ga[:, at]); hist_b.append(gb[:, at]); history_times.append(t)
        older_a, older_b = a, b
        a, b = aa, bb
    center = pad-radius*delay
    probes = np.tile(center+offsets, 16)
    gone = np.repeat(np.all(a == b, axis=1), 4)
    a = np.repeat(a, 4, axis=0); b = np.repeat(b, 4, axis=0)
    at = probes[:, None]+np.arange(-2*radius, 2*radius+1)
    local_same = np.all(a[np.arange(64)[:, None], at] == b[np.arange(64)[:, None], at], axis=1)
    ha = np.stack(hist_a, axis=-1).reshape(64, -1)
    hb = np.stack(hist_b, axis=-1).reshape(64, -1)
    assert len(history_times) == (15 if delay == 16 else 16)
    history_changed = np.any(ha ^ hb, axis=1)
    a2 = a.copy(); b2 = b.copy()
    a2[np.arange(64), probes] ^= 1; b2[np.arange(64), probes] ^= 1
    assert not np.any((a2 ^ a) ^ (b2 ^ b))
    measurements = []
    for h in range(1, horizon+1):
        a, b, a2, b2 = [step(z, radius, rule, correction) for z in (a, b, a2, b2)]
        if h not in (1, 8, 32):
            continue
        r0, r1 = a2 ^ a, b2 ^ b
        count = (r0 ^ r1).sum(axis=1)
        union = (r0 | r1).sum(axis=1)
        ratio = np.divide(count, union, out=np.zeros(64), where=union > 0)
        metrics = np.stack((count, r0.sum(axis=1), r1.sum(axis=1), union, ratio), axis=1)
        remote_rows = np.arange(3, 64, 4)
        assert np.all(count[remote_rows] == 0)
        assert np.all(count[gone] == 0)
        if h == 1:
            assert np.all(count[local_same] == 0)
        if rule in (0, 90, 150, 204) or (rule is None and not correction):
            assert np.all(count == 0)
        measurements.append(metrics)
    return {'origins': origins, 'offsets': offsets, 'history_times': np.array(history_times),
            'local_same': local_same, 'priming_gone': gone,
            'history_base': ha, 'history_primed': hb, 'history_changed': history_changed,
            'measurements': np.stack(measurements)}, pad


def summarize(case, spec, pad):
    local = np.tile([True, True, True, False], 16)
    rows = []
    for index, h in enumerate((1, 8, 32)):
        m = case['measurements'][index]
        record = {'horizon': h, 'local_trials': int(local.sum()),
                  'changed_local_responses': int(np.sum((m[:, 0] > 0) & local)),
                  'mean_interaction_cells': float(m[local, 0].mean()),
                  'mean_interaction_union_ratio': float(m[local, 4].mean()),
                  'remote_trials': 16, 'remote_changed': int(np.sum(m[~local, 0] > 0)),
                  'strata': []}
        for same in (False, True):
            for history in (False, True):
                mask = local & (case['local_same'] == same) & (case['history_changed'] == history)
                record['strata'].append({'local_same': same, 'G_history_changed': history,
                                         'trials': int(mask.sum()),
                                         'changed': int(np.sum(m[mask, 0] > 0))})
        rows.append(record)
    return {**spec, 'half_padding': pad, 'history_times': case['history_times'].tolist(),
            'priming_gone_trials': int(case['priming_gone'][local].sum()), 'outcomes': rows}


def main():
    start = time.perf_counter()
    assert not (UNIT/'response-result.json').exists()
    inputs = ['scripts/commutator_response.py', 'scripts/commutator_history.py',
              'experiments/commutator_history_20260915/response-protocol.md',
              'experiments/commutator_history_20260915/response-protocol-freeze.json',
              'experiments/commutator_history_20260915/result.json']
    hashes = {name: digest(ROOT/name) for name in inputs}
    raw_inputs = {f'experiments/beam_discriminator_loop_20260915/round{n:02d}/trajectories.npz':
                  digest(OLD/f'round{n:02d}/trajectories.npz') for n in (6, 10)}
    save(UNIT/'response-freeze.json', {'source_hashes': hashes, 'raw_input_hashes': raw_inputs})
    census = [short_case(1, rule) for rule in range(256)]
    wider_census = short_case(2)
    data, cases = {}, []
    with np.load(OLD/'round06/trajectories.npz') as cache:
        for rule in (0, 1, 30, 54, 73, 90, 106, 110, 122, 126, 150, 204):
            for seed in (6041512, 6041513, 6041514):
                initial = np.unpackbits(cache[f's{seed}_r{rule:03d}'][0])[:2039]
                for delay in (16, 64):
                    spec = {'id': f'eca{rule}_s{seed}_d{delay}', 'kind': 'eca', 'rule': rule,
                            'radius': 1, 'seed': seed, 'delay': delay}
                    case, pad = probe(initial, 1, delay, rule=rule)
                    data.update({spec['id']+'_'+key: value for key, value in case.items()})
                    cases.append(summarize(case, spec, pad))
            print('eca', rule, 'seconds', round(time.perf_counter()-start, 2), flush=True)
    with np.load(OLD/'round10/trajectories.npz') as cache:
        seed = 6041542
        for radius in (1, 2, 3):
            for correction in (False, True):
                initial = np.unpackbits(cache[f'r{radius}_g{int(correction)}_s{seed}'][0])[:4093+16*radius]
                for delay in (16, 64):
                    spec = {'id': f'wide{radius}_g{int(correction)}_d{delay}', 'kind': 'wider',
                            'radius': radius, 'correction': correction, 'seed': seed, 'delay': delay}
                    case, pad = probe(initial, radius, delay, correction=correction)
                    data.update({spec['id']+'_'+key: value for key, value in case.items()})
                    cases.append(summarize(case, spec, pad))
    path = UNIT/'response-arrays.npz'
    with path.open('wb') as handle:
        np.savez_compressed(handle, **data)
    result = {'source_hashes': hashes, 'raw_input_hashes': raw_inputs,
              'short_census': census, 'wider_short_census': wider_census, 'cases': cases,
              'raw_sha256': digest(path), 'raw_bytes': path.stat().st_size,
              'seconds': time.perf_counter()-start}
    save(UNIT/'response-result.json', result)
    print('ECA rules admitting short interaction:', sum(c['interacting_contexts'] > 0 for c in census))
    print('Rule 30 witness:', json.dumps(census[30]))
    print('Rule 4:', json.dumps(census[4]))
    for rule in (30, 54, 73, 90, 106, 110, 126):
        z = [c['outcomes'][-1] for c in cases if c.get('rule') == rule]
        print('eca', rule, 'changed', sum(x['changed_local_responses'] for x in z), '/', sum(x['local_trials'] for x in z))
    print('seconds', result['seconds'], flush=True)


if __name__ == '__main__':
    main()
