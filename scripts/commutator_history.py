#!/usr/bin/env python3
"""Frozen conditional prediction test of G along native trajectories.

Run locally; the time history is G(E^t(S)), never E^t(G(S)).
"""
from __future__ import annotations

import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / 'experiments/commutator_history_20260915'
OLD = ROOT / 'experiments/beam_discriminator_loop_20260915'
LAGS = (4, 8, 16)
THRESHOLD = 0.01


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True,
                                    allow_nan=False) + '\n')


def eca_step(x, rule):
    idx = 4*np.roll(x, 1, axis=-1) + 2*x + np.roll(x, -1, axis=-1)
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    return lut[idx]


def open_step(x, radius, correction):
    out = x[..., 2*radius:].copy()
    if correction:
        gate = np.ones_like(out)
        for j in range(2*radius):
            gate &= x[..., j:j+out.shape[-1]]
        out ^= gate
    return out


def commutator(a, radius=1, rule=None, correction=None):
    d = a[:-1] ^ a[1:]
    if rule is not None:
        return d[1:] ^ eca_step(d[:-1], rule)
    return d[1:, radius:-radius] ^ open_step(d[:-1], radius, correction)


def reflect_rule(rule):
    return sum(((rule >> i) & 1) << (((i & 1) << 2) | (i & 2) | ((i & 4) >> 2))
               for i in range(8))


def conjugate_rule(rule):
    return sum((1 ^ ((rule >> (7-i)) & 1)) << i for i in range(8))


def algebra_checks():
    cases = 0
    words = ((np.arange(32)[:, None] >> np.arange(4, -1, -1)) & 1).astype(np.uint8)
    constant = {}
    for rule in range(256):
        b = eca_step(words, rule)
        c = eca_step(b, rule)
        got = (b ^ c ^ eca_step(words ^ b, rule))[:, 2]
        expected = []
        f = lambda l, z, r: (rule >> (4*l+2*z+r)) & 1
        for word in words.tolist():
            nxt = [f(*word[j:j+3]) for j in range(3)]
            delta = [word[j+1] ^ nxt[j] for j in range(3)]
            expected.append(nxt[1] ^ f(*nxt) ^ f(*delta))
        assert np.array_equal(got, expected)
        assert np.array_equal(eca_step(words[:, ::-1], reflect_rule(rule)), b[:, ::-1])
        assert np.array_equal(eca_step(1 ^ words, conjugate_rule(rule)), 1 ^ b)
        if np.all(got == got[0]):
            constant[str(rule)] = int(got[0])
        cases += 32
    assert constant['90'] == constant['150'] == constant['204'] == 0
    wider = 0
    for radius in (1, 2, 3):
        n = 4*radius+1
        words = ((np.arange(1 << n)[:, None] >> np.arange(n-1, -1, -1)) & 1).astype(np.uint8)
        for correction in (False, True):
            b = open_step(words, radius, correction)
            c = open_step(b, radius, correction)
            d = words[:, radius:-radius] ^ b
            got = (b[:, radius:-radius] ^ c ^ open_step(d, radius, correction))[:, 0]
            def scalar(w):
                gate = int(all(w[:-1])) if correction else 0
                return w[-1] ^ gate
            expected = []
            for word in words.tolist():
                nxt = [scalar(word[j:j+2*radius+1]) for j in range(2*radius+1)]
                delta = [word[j+radius] ^ nxt[j] for j in range(2*radius+1)]
                expected.append(nxt[radius] ^ scalar(nxt) ^ scalar(delta))
            assert np.array_equal(got, expected)
            wider += len(words)
    return {'eca_scalar_contexts': cases, 'wider_scalar_contexts': wider,
            'constant_G_rules': constant}


def counts(field, times, radius, velocity2, periodic):
    """Counts of (present neighborhood, three older bits, future bit).

    velocity2 is twice physical velocity. Nested contexts occupy low bits.
    Every slice has the same number of scored spatial positions.
    """
    margin = 0 if periodic else 17*radius
    stop = field.shape[1] - margin
    width = stop - margin
    assert width > 0
    def shifted(frame, dx):
        if periodic:
            return np.roll(frame, -dx, axis=1)
        return frame[:, margin+dx:stop+dx]
    now = field[times]
    context = np.zeros((len(times), width), dtype=np.uint16)
    for dx in range(-radius, radius+1):
        context = (context << 1) | shifted(now, dx)
    present_bits = 2*radius+1
    for j, lag in enumerate(LAGS):
        dx = -(velocity2*lag)//2
        context |= shifted(field[times-lag], dx).astype(np.uint16) << (present_bits+j)
    target = shifted(field[times+4], 2*velocity2)
    keys = 2*context + target
    table = np.bincount(keys.ravel(), minlength=2**(present_bits+4)).reshape(-1, 2)
    assert int(table.sum()) == len(times)*width
    return table.astype(np.uint64)


def nested_counts(full, present_bits, history_bits):
    return full.reshape(-1, 2**(present_bits+history_bits), 2).sum(axis=0)


def losses(fit, test, present_bits):
    out, unseen = [], []
    for h in range(4):
        a = nested_counts(fit, present_bits, h)
        b = nested_counts(test, present_bits, h)
        n = a.sum(axis=1)
        p = (a[:, 1]+0.5)/(n+1.0)
        out.append(float(-(b[:, 1]*np.log2(p)+b[:, 0]*np.log2(1-p)).sum()/b.sum()))
        unseen.append(float(b[n == 0].sum()/b.sum()))
    return out, unseen


def family_analysis(name, spec, fields, baseline, packed, shuffled=False):
    radius = spec['radius']
    train_seed = min(fields)
    transformed = fields
    if shuffled:
        transformed = {seed: g[np.random.default_rng(seed+9000000).permutation(len(g))]
                       for seed, g in fields.items()}
    fit_times = np.arange(16, 480)
    select_times = np.arange(528, 1026)
    eval_times = np.arange(16, 1026)
    velocities = (0, -radius, radius, -2*radius, 2*radius)
    choices = []
    fits = {}
    for v2 in velocities:
        fit = counts(transformed[train_seed], fit_times, radius, v2, spec['periodic'])
        selection = counts(transformed[train_seed], select_times, radius, v2, spec['periodic'])
        loss, unseen = losses(fit, selection, 2*radius+1)
        fits[v2] = fit
        packed[f'{name}_fit_v{v2}'] = fit
        packed[f'{name}_selection_v{v2}'] = selection
        choices.append({'velocity': v2/2, 'velocity2': v2, 'losses': loss,
                        'gain': loss[0]-loss[3], 'unseen_fraction': unseen})
    chosen = max(choices, key=lambda row: row['gain'])
    v2 = chosen['velocity2']
    rows = []
    for seed, g in transformed.items():
        if seed == train_seed:
            continue
        table = counts(g, eval_times, radius, v2, spec['periodic'])
        packed[f'{name}_test_s{seed}'] = table
        loss, unseen = losses(fits[v2], table, 2*radius+1)
        gain = loss[0]-loss[3]
        density = float(g.mean())
        entropy = float(-density*np.log2(density)-(1-density)*np.log2(1-density)) if 0 < density < 1 else 0.
        rows.append({'seed': seed, 'losses': loss, 'gain_bits': gain,
                     'incremental_gains': [loss[j]-loss[j+1] for j in range(3)],
                     'unseen_fraction': unseen, 'G_density': density, 'G_marginal_entropy': entropy,
                     'memory_selected': gain > THRESHOLD,
                     'baseline_selected': baseline[seed]['selected'],
                     'augmented_selected': bool(baseline[seed]['selected'] and gain > THRESHOLD),
                     'q': baseline[seed]['q'], 'alpha': baseline[seed]['alpha'],
                     'targets': int(table.sum())})
    return {'id': name, **spec, 'shuffled': shuffled, 'fit_seed': train_seed,
            'choices': choices, 'chosen_velocity': v2/2, 'tests': rows}


def main():
    start = time.perf_counter()
    UNIT.mkdir(parents=True, exist_ok=True)
    assert not (UNIT/'result.json').exists(), 'Preserve canonical output; use a fresh directory.'
    inputs = ['scripts/commutator_history.py',
              'experiments/commutator_history_20260915/protocol.md',
              'experiments/commutator_history_20260915/protocol-freeze.json',
              'experiments/on_beam_256_4d_20260914/labels.json']
    inputs += [f'experiments/beam_discriminator_loop_20260915/round{n:02d}/result.json' for n in (6, 10)]
    hashes = {p: digest(ROOT/p) for p in inputs}
    raw_inputs = {f'experiments/beam_discriminator_loop_20260915/round{n:02d}/trajectories.npz':
                  digest(OLD/f'round{n:02d}'/'trajectories.npz') for n in (6, 10)}
    save(UNIT/'freeze.json', {'source_hashes': hashes, 'raw_input_hashes': raw_inputs})
    checks = algebra_checks()
    rows6 = json.loads((OLD/'round06/result.json').read_text())['rules']
    rows10 = json.loads((OLD/'round10/result.json').read_text())['rules']
    packed, families = {}, []
    with np.load(OLD/'round06/trajectories.npz') as data:
        for rule in sorted({row['rule'] for row in rows6}):
            baseline = {row['seed']: row for row in rows6 if row['rule'] == rule}
            arrays = {seed: np.unpackbits(data[f's{seed}_r{rule:03d}'], axis=1)[:, :2039]
                      for seed in baseline}
            variants = [(rule, False, False)]
            if rule in (54, 110):
                seen = {rule}
                for flip, reflect in ((False, True), (True, False), (True, True)):
                    child = conjugate_rule(rule) if flip else rule
                    child = reflect_rule(child) if reflect else child
                    if child not in seen:
                        variants.append((child, flip, reflect)); seen.add(child)
            for child, flip, reflect in variants:
                fields = {}
                for seed, a in arrays.items():
                    x = (1 ^ a) if flip else a
                    x = x[:, ::-1] if reflect else x
                    assert np.array_equal(eca_step(x[:-1], child), x[1:])
                    g = commutator(x, rule=child)
                    assert g.shape == (1030, 2039)
                    fields[seed] = g
                    packed[f'eca{child}_G_s{seed}'] = np.packbits(g, axis=1)
                spec = {'kind': 'eca', 'rule': child, 'representative': rule,
                        'flip': flip, 'reflect': reflect, 'radius': 1, 'periodic': True}
                name = f'eca{child}'
                families.append(family_analysis(name, spec, fields, baseline, packed))
                if child == rule and rule in (30, 54, 73, 106, 110, 126):
                    families.append(family_analysis(name+'_shuffle', spec, fields, baseline, packed, True))
            if len(families) % 8 == 0:
                print('families', len(families), 'seconds', round(time.perf_counter()-start, 2), flush=True)
            assert time.perf_counter()-start < 600, 'Declared analysis budget exceeded.'
    with np.load(OLD/'round10/trajectories.npz') as data:
        for radius in (1, 2, 3):
            for correction in (False, True):
                baseline = {row['seed']: row for row in rows10
                            if row['radius'] == radius and row['correction'] == correction}
                fields = {}
                name = f'wide{radius}_g{int(correction)}'
                for seed in baseline:
                    a = np.unpackbits(data[f'r{radius}_g{int(correction)}_s{seed}'], axis=1)[:, :4093+16*radius]
                    assert np.array_equal(open_step(a[:-1], radius, correction), a[1:, radius:-radius])
                    g = commutator(a, radius, correction=correction)
                    assert g.shape == (1030, 4093+14*radius)
                    fields[seed] = g
                    packed[f'{name}_G_s{seed}'] = np.packbits(g, axis=1)
                spec = {'kind': 'wider', 'radius': radius, 'correction': correction, 'periodic': False}
                families.append(family_analysis(name, spec, fields, baseline, packed))
                families.append(family_analysis(name+'_shuffle', spec, fields, baseline, packed, True))
                print(name, 'seconds', round(time.perf_counter()-start, 2), flush=True)
    raw = UNIT/'histories-and-counts.npz'
    with raw.open('wb') as f:
        np.savez_compressed(f, **packed)
    result = {'source_hashes': hashes, 'raw_input_hashes': raw_inputs,
              'raw_output_sha256': digest(raw), 'raw_output_bytes': raw.stat().st_size,
              'threshold_bits': THRESHOLD, 'algebra_checks': checks,
              'environment': {'python': platform.python_version(), 'numpy': np.__version__,
                              'platform': platform.platform()},
              'families': families, 'seconds': time.perf_counter()-start}
    save(UNIT/'result.json', result)
    for family in families:
        if family.get('representative') in (30, 54, 73, 106, 110, 126) or family['kind'] == 'wider':
            print(json.dumps({'id': family['id'], 'v': family['chosen_velocity'],
                              'gains': [round(x['gain_bits'], 6) for x in family['tests']],
                              'selected': [x['augmented_selected'] for x in family['tests']]}), flush=True)
    print('complete', round(result['seconds'], 3), 'seconds', raw.stat().st_size, 'raw bytes', flush=True)


if __name__ == '__main__':
    main()
