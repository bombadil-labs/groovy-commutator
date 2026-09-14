"""Widen the first-floor native rule and compare temporal/spatial probes.

Horizontal radii 1 and 2; transverse radius 1 sees the whole period-three
domain. The native rule is resynthesized at the declared radius subject to
beam evolution, not held fixed on arbitrary outer contexts of old cubes.
All source words of width 2*rx+5 exhaust probe contexts and required outputs.
"""
import argparse
import hashlib
import json
import sqlite3
import time
from pathlib import Path

import numpy as np
from verify_polarization_proposal import d, encode


def patches(grid, rx):
    center = grid.shape[-1]//2
    result = np.zeros(grid.shape[:2], dtype=np.uint32)
    for dy in (0, 1, -1):
        phases = (np.arange(3)+dy) % 3
        for dx in range(-rx, rx+1):
            result = (result << 1) | grid[:, phases, center+dx]
    return result


def requirements(keys, targets, size):
    req = np.zeros(size, dtype=np.uint8)
    np.bitwise_or.at(req, keys.ravel(), (1 << targets.ravel()).astype(np.uint8))
    return req


def verdict(base, req, zero_bit=None):
    if zero_bit == 1:
        req = ((req & 1) << 1) | ((req & 2) >> 1)
    merged = base | req
    if zero_bit is not None:
        merged[0] |= 1 << zero_bit
    bad = np.flatnonzero(merged == 3)
    return {'passes': not len(bad), 'conflicts': len(bad),
            'first_conflict_key': int(bad[0]) if len(bad) else None,
            'forced_bits': int(np.count_nonzero(merged)),
            'requirements_sha256': hashlib.sha256(merged.tobytes()).hexdigest()}


def evaluate(base, base_by_phase, keys, targets, size, rule):
    raw = requirements(keys, targets, size)
    corrected_targets = targets.copy()
    corrected_targets[:, 1] ^= rule & 1
    centered = requirements(keys, corrected_targets, size)
    unmarked_raw = verdict(base, raw)
    unmarked_centered = [verdict(base, centered, z) for z in (0, 1)]
    tagged = {}
    for name, ys in [('raw', targets), ('centered', corrected_targets)]:
        phase_results = []
        for phase in (0, 1):
            req = requirements(keys[:, phase], ys[:, phase], size)
            phase_results.append([verdict(base_by_phase[phase], req, z)
                                  for z in ((0, 1) if name == 'centered' else (None,))])
        tagged[name] = {'passes': all(any(v['passes'] for v in values) for values in phase_results),
                        'phases': phase_results}
    return {'raw': unmarked_raw, 'centered_branches': unmarked_centered,
            'centered_pass': any(v['passes'] for v in unmarked_centered),
            'tagged': tagged}, raw, centered


def source_radius(rule):
    x = ((np.arange(32)[:, None] >> np.arange(4, -1, -1)) & 1).astype(np.uint8)
    dx = d(x, rule)
    g = (d(x ^ dx, rule) ^ dx ^ d(dx, rule))[:, 2]
    if np.all(g == g[0]): return -1, int(g[0])
    for radius in (0, 1, 2):
        patch = x[:, 2-radius:3+radius]
        keys = patch @ (1 << np.arange(2*radius, -1, -1))
        req = requirements(keys, g, 1 << (2*radius+1))
        if not np.any(req == 3): return radius, None
    raise AssertionError(rule)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args(); args.output.mkdir(parents=True, exist_ok=False)
    root = Path(__file__).resolve().parent
    db = sqlite3.connect(root/'runs/fixed_transverse_to_4/constraints.sqlite3')
    candidates = list(db.execute('SELECT id,rule,record_json FROM candidates WHERE dimension=2 AND strict_pass=1 ORDER BY rule,id'))
    started = time.perf_counter(); records = []
    with (args.output/'candidates.jsonl').open('w') as log:
        for rx in (1, 2):
            width = 2*rx+5; size = 1 << (3*(2*rx+1))
            source = ((np.arange(1 << width)[:, None] >> np.arange(width-1, -1, -1)) & 1).astype(np.uint8)
            mid = width//2
            for cid, rule, raw_record in candidates:
                original = json.loads(raw_record); choice = original['recipe'][0]
                dx = d(source, rule); ex = source ^ dx
                a = encode(source, rule, choice)
                b = encode(ex, rule, choice)
                c = encode(ex ^ d(ex, rule), rule, choice)
                first_flip = a ^ b
                first_keys = patches(a, rx)
                base = requirements(first_keys, first_flip[..., mid], size)
                assert not np.any(base == 3)
                base_by_phase = [requirements(first_keys[:, phase], first_flip[:, phase, mid], size) for phase in range(3)]
                probes = {}
                gs = d(ex, rule) ^ dx ^ d(dx, rule)
                targets = np.stack([gs[:, mid] ^ gs[:, mid+choice['shift']], gs[:, mid]], axis=1)
                temporal_target = a[:, :2, mid] ^ c[:, :2, mid] ^ targets
                probes['temporal'] = (patches(first_flip, rx)[:, :2], temporal_target)
                for sign in (-1, 1):
                    shifted = np.roll(source, -sign, axis=-1)
                    gx = dx ^ d(shifted, rule) ^ d(source ^ shifted, rule)
                    transported = np.stack([gx[:, mid] ^ gx[:, mid+choice['shift']], gx[:, mid]], axis=1)
                    u = a ^ np.roll(a, -sign, axis=-1)
                    wanted = (first_flip ^ np.roll(first_flip, -sign, axis=-1))[:, :2, mid] ^ transported
                    probes[f'spatial_{sign:+d}'] = (patches(u, rx)[:, :2], wanted)
                results = {}; merged_raw = np.zeros(size, dtype=np.uint8); merged_centered = merged_raw.copy()
                reqs = {}
                for name, (keys, desired) in probes.items():
                    results[name], rr, cc = evaluate(base, base_by_phase, keys, desired, size, rule)
                    reqs[name] = (rr, cc)
                    merged_raw |= rr; merged_centered |= cc
                # Reflection of the probe displacement is a translated pair,
                # so symmetry of B makes the two requirements identical.
                assert all(np.array_equal(x, y) for x, y in zip(reqs['spatial_-1'], reqs['spatial_+1']))
                combined_centered = [verdict(base, merged_centered, z) for z in (0, 1)]
                results['joint'] = {'raw': verdict(base, merged_raw),
                                    'centered_branches': combined_centered,
                                    'centered_pass': any(v['passes'] for v in combined_centered)}
                record = {'candidate': cid, 'rule': rule, 'recipe': original['recipe'],
                          'horizontal_radius': rx, 'transverse_radius': 1,
                          'source_width': width, 'source_words': 1 << width,
                          'first_order_observed': int(np.count_nonzero(base)), 'probes': results}
                records.append(record); log.write(json.dumps(record, separators=(',', ':'))+'\n')
            log.flush()
            print(json.dumps({'radius_complete': rx, 'seconds': round(time.perf_counter()-started, 3)}), flush=True)
    summary = {}
    for rx in (1, 2):
        rows = [r for r in records if r['horizontal_radius'] == rx]
        stage = {}
        for probe in ('temporal', 'spatial_+1', 'joint'):
            stage[probe] = {}
            for mode in ('raw', 'centered'):
                def passed(r):
                    obj = r['probes'][probe]
                    return obj['raw']['passes'] if mode == 'raw' else obj['centered_pass']
                good = [r for r in rows if passed(r)]
                stage[probe][mode] = {'rules': sorted({r['rule'] for r in good}), 'candidates': len(good)}
                if probe != 'joint':
                    stage[probe][mode]['tagged_rules'] = sorted({r['rule'] for r in rows if r['probes'][probe]['tagged'][mode]['passes']})
        summary[str(rx)] = stage
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    rad = {str(r): {'minimal_centered_source_radius': source_radius(r)[0], 'constant_value': source_radius(r)[1]} for r in range(256)}
    (args.output/'source_G_radius.json').write_text(json.dumps(rad, indent=2)+'\n')
    manifest = {'elapsed_seconds': time.perf_counter()-started, 'variants': len(candidates),
                'source_codes': len({r[1] for r in candidates}), 'radii': [1, 2],
                'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'probe_constraints_are_separate_except_joint': True,
                'wider_laws_resynthesized_from_beam_only': True,
                'five_vertical_rows_redundant_on_test_domain': True}
    (args.output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (args.output/'source_audit.py').write_text(Path(__file__).read_text())
    print(json.dumps({'seconds': manifest['elapsed_seconds'], 'counts': {
        r: {p: {m: {k:len(v) if isinstance(v,list) else v for k,v in q.items()} for m,q in ps.items()} for p,ps in rs.items()}
        for r,rs in summary.items()}}), flush=True)


if __name__ == '__main__':
    main()
