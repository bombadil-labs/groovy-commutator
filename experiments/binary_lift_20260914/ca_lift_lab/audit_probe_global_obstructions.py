"""All-radius obstruction certificates from complete periodic configurations.

Normalize the whole period-three sheet to its least horizontal period. Equal
keys then denote identical infinite configurations relative to the target
cell, even across different source-ring lengths. A conflict rules out every
native radius for this carrier; no conflict proves nothing outside these rings.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
from verify_polarization_proposal import d, encode


def full_keys(grid):
    n, _, width = grid.shape
    period = np.full(n, width)
    for p in range(1, width+1):
        if width % p: continue
        equal = np.all(grid == grid[..., np.arange(width) % p], axis=(1, 2))
        period[equal] = np.minimum(period[equal], p)
    result = np.empty((n, 3), dtype=np.uint32)
    for p in np.unique(period):
        select = period == p
        block = grid[select, :, :p]
        for phase in range(3):
            value = np.ones(np.count_nonzero(select), dtype=np.uint32)
            for dy in (0, 1, -1):
                for x in range(p):
                    value = (value << 1) | block[:, (phase+dy) % 3, x]
            result[select, phase] = value
    return result


def conflict(events, centered, zero_bit=None):
    seen = {}
    if zero_bit is not None:
        # Header 1 then three zero cells: constant-zero full configuration.
        seen[8] = (zero_bit, {'kind': 'chosen_zero_bit', 'required': zero_bit})
    for event in events:
        wanted = event['wanted_centered'] if centered else event['wanted_raw']
        if centered and event['kind'] != 'beam': wanted ^= zero_bit
        key = event['key']
        if key in seen and seen[key][0] != wanted:
            return {'obstructed': True, 'whole_sheet_key': key,
                    'existing': seen[key][1], 'new': {**event, 'required': wanted}}
        seen.setdefault(key, (wanted, {**event, 'required': wanted}))
    return {'obstructed': False}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--run', type=Path, required=True)
    args = ap.parse_args(); start = time.perf_counter()
    rows = [json.loads(x) for x in (args.run/'candidates.jsonl').read_text().splitlines()]
    rows = [r for r in rows if r['horizontal_radius'] == 2]
    out = []
    for record in rows:
        rule = record['rule']; choice = record['recipe'][0]
        first = []; probes = {'temporal': [], 'spatial': []}
        for width in (8, 9):
            s = ((np.arange(1 << width)[:, None] >> np.arange(width-1, -1, -1)) & 1).astype(np.uint8)
            ds = d(s, rule); es = s ^ ds
            a = encode(s, rule, choice); b = encode(es, rule, choice)
            c = encode(es ^ d(es, rule), rule, choice)
            flips = a ^ b; bk = full_keys(a)
            for word in range(1 << width):
                for phase in range(3):
                    wanted = int(flips[word, phase, 0])
                    first.append({'kind': 'beam', 'width': width, 'source': format(word, f'0{width}b'),
                                  'phase': phase, 'key': int(bk[word, phase]),
                                  'wanted_raw': wanted, 'wanted_centered': wanted})
            for probe in probes:
                if probe == 'temporal':
                    u = flips; g = d(es, rule) ^ ds ^ d(ds, rule)
                    known = a[:, :2, 0] ^ c[:, :2, 0]
                else:
                    shifted = np.roll(s, -1, axis=-1)
                    u = a ^ np.roll(a, -1, axis=-1)
                    g = ds ^ d(shifted, rule) ^ d(s ^ shifted, rule)
                    known = (flips ^ np.roll(flips, -1, axis=-1))[:, :2, 0]
                carrier = np.stack([g[:, 0] ^ g[:, choice['shift'] % width], g[:, 0]], axis=1)
                target = known ^ carrier; uk = full_keys(u)
                for word in range(1 << width):
                    for phase in range(2):
                        wanted = int(target[word, phase])
                        probes[probe].append({'kind': probe, 'width': width, 'source': format(word, f'0{width}b'),
                                             'phase': phase, 'key': int(uk[word, phase]),
                                             'wanted_raw': wanted,
                                             'wanted_centered': wanted ^ ((rule & 1) if phase == 1 else 0)})
        result = {'candidate': record['candidate'], 'rule': rule, 'recipe': record['recipe'], 'probes': {}}
        for probe, events in probes.items():
            raw = conflict(first+events, False)
            corrected = [conflict(first+events, True, z) for z in (0, 1)]
            result['probes'][probe] = {'raw': raw, 'centered_branches': corrected,
                                      'centered_obstructed': all(x['obstructed'] for x in corrected)}
            local = record['probes']['temporal' if probe == 'temporal' else 'spatial_+1']
            assert not (local['raw']['passes'] and raw['obstructed'])
            assert not (local['centered_pass'] and result['probes'][probe]['centered_obstructed'])
        out.append(result)
    (args.run/'global_obstructions.jsonl').write_text(''.join(json.dumps(r, separators=(',', ':'))+'\n' for r in out))
    summary = {}
    codes = sorted({r['rule'] for r in out})
    for probe in ('temporal', 'spatial'):
        summary[probe] = {}
        for mode in ('raw', 'centered'):
            def obstructed(r):
                p = r['probes'][probe]
                return p['raw']['obstructed'] if mode == 'raw' else p['centered_obstructed']
            summary[probe][mode] = {'codes_obstructed_every_variant': [rule for rule in codes if all(obstructed(r) for r in out if r['rule'] == rule)],
                                    'variants_obstructed': sum(obstructed(r) for r in out)}
    result = {'periods_tested': [8, 9], 'elapsed_seconds': time.perf_counter()-start, 'summary': summary,
              'no_collision_is_not_a_proof_of_existence': True}
    (args.run/'global_obstruction_summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'seconds': result['elapsed_seconds'], 'summary': {
        p:{m:{k:len(v) if isinstance(v,list) else v for k,v in a.items()} for m,a in b.items()} for p,b in summary.items()}}))


if __name__ == '__main__': main()
