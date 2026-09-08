"""Exact finite-cone responses to periodic and isolated six-cell defects."""
from pathlib import Path
import base64
import hashlib
import json
import sys
import time
import zlib
import numpy as np
from experiment_column_compatibility import step2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from groovy.ca import apply_rule
STEM = ROOT / 'results/encoded_defects_20260908'
MODES = ['periodic', 'isolated']
TIMES = [0, 2, 4]


def digest(a):
    return hashlib.sha256(np.packbits(a.ravel(), bitorder='little').tobytes()).hexdigest()


def encode(bits, ys, xs):
    s = bits[:, (xs // 2) + 4]
    out = np.zeros((len(bits), len(ys), len(xs)), dtype=np.uint8)
    for row, y in enumerate(ys):
        if y % 3 == 0:
            out[:, row] = np.where(xs % 2 == 0, s, 1)
        elif y % 3 == 1:
            out[:, row] = xs % 2
        else:
            out[:, row] = np.where(xs % 2 == 0, 0, 1 ^ s)
    return out


def classify(field, delta, mode):
    blocks = field.reshape(512, 5, 3, 5, 2).transpose(0, 1, 3, 2, 4)
    code = (blocks * (1 << np.arange(6).reshape(3, 2))).sum(axis=(-1, -2))
    local = ((code == 42) | (code == 11)).all(axis=(1, 2))
    same = ~delta.any(axis=(1, 2))
    # In isolated mode, untouched remote vertical copies fix global content.
    globally_valid = local if mode == 'periodic' else same
    status = np.where(same, 0, np.where(globally_valid, 1, 2)).astype(np.uint8)
    return status, local


def main():
    start = time.time()
    inputs = ((np.arange(512)[:, None] >> np.arange(9)) & 1).astype(np.uint8)
    ys, xs = np.arange(-10, 13), np.arange(-8, 10)
    initial = encode(inputs, ys, xs)
    natural = {}
    field = initial.copy()
    for t in range(5):
        if t in TIMES:
            margin = 4 - t
            natural[t] = field[:, margin:margin+15, margin:margin+10].copy()
        if t < 4:
            field = step2(field, shrink=True)
    responses = np.empty((2, 64, 3, 512, 15, 10), dtype=np.uint8)
    statuses = np.empty((2, 64, 3, 512), dtype=np.uint8)
    records = []
    for mode_i, mode in enumerate(MODES):
        for mask in range(64):
            field = initial.copy()
            for bit in range(6):
                if (mask >> bit) & 1:
                    y, x = divmod(bit, 2)
                    rows = np.flatnonzero(ys % 3 == y) if mode == 'periodic' else np.flatnonzero(ys == y)
                    field[:, rows, int(np.flatnonzero(xs == x)[0])] ^= 1
            for t in range(5):
                if t in TIMES:
                    ti = TIMES.index(t); margin = 4-t
                    cropped = field[:, margin:margin+15, margin:margin+10]
                    delta = cropped ^ natural[t]
                    responses[mode_i, mask, ti] = delta
                    status, local = classify(cropped, delta, mode)
                    statuses[mode_i, mask, ti] = status
                    packed = np.packbits(delta.reshape(512, -1), axis=1, bitorder='little')
                    records.append(dict(mode=mode, mask=mask, fine_ticks=t,
                        same=int((status == 0).sum()), valid_changed=int((status == 1).sum()),
                        outside=int((status == 2).sum()), local_valid=int(local.sum()),
                        local_valid_changed=int((local & (status != 0)).sum()),
                        distinct_responses=len(np.unique(packed, axis=0)), changed_cells=int(delta.sum()),
                        response_sha256=digest(delta)))
                if t < 4:
                    field = step2(field, shrink=True)
        print(f'{mode}: all 64 masks and 512 backgrounds complete', flush=True)
    pairs = []; witnesses = []
    for mode_i, mode in enumerate(MODES):
        for a in range(6):
            for b in range(a+1, 6):
                mask = (1 << a) | (1 << b)
                for ti, t in enumerate(TIMES):
                    interaction = responses[mode_i, mask, ti] ^ responses[mode_i, 1 << a, ti] ^ responses[mode_i, 1 << b, ti]
                    active = interaction.any(axis=(1, 2))
                    pairs.append(dict(mode=mode, a=a, b=b, fine_ticks=t,
                        nonlinear_backgrounds=int(active.sum()), changed_cells=int(interaction.sum()),
                        interaction_sha256=digest(interaction)))
                    if active.any() and t == 4:
                        bg = int(np.flatnonzero(active)[0])
                        witnesses.append(dict(mode=mode, a=a, b=b, background=bg,
                            input_bits=inputs[bg].tolist(), fine_ticks=t,
                            interaction_cells=(np.argwhere(interaction[bg]) + [-6, -4]).tolist()))
    # Matched logical flip: package Rule 90 gives its background-independent response.
    logical_delta = np.zeros((1, 9), dtype=np.uint8); logical_delta[0, 4] = 1
    for ti, t in enumerate(TIMES):
        if ti:
            logical_delta[0] = apply_rule(logical_delta[0], 90)
        expected = np.zeros((15, 10), dtype=np.uint8)
        for iy, y in enumerate(range(-6, 9)):
            for ix, x in enumerate(range(-4, 6)):
                if (y % 3, x % 2) in [(0, 0), (2, 1)]:
                    expected[iy, ix] = logical_delta[0, x // 2 + 4]
        assert np.all(responses[0, 33, ti] == expected)
        assert np.all(statuses[0, 33, ti] == 1)
    assert np.all(statuses[:, 0] == 0)
    sources = ['scripts/experiment_encoded_defects.py','scripts/experiment_column_compatibility.py',
               'src/groovy/ca.py','docs/research/protocols/encoded-defects-20260908.md']
    payload = dict(schema_version=1, modes=MODES, times=TIMES, backgrounds=512,
        output_rows=[-6,8], output_columns=[-4,5], records=records, pairs=pairs)
    Path(str(STEM)+'_responses.json').write_text(json.dumps(payload, indent=2)+'\n')
    raw = statuses.tobytes()
    Path(str(STEM)+'_classifications.json').write_text(json.dumps(dict(
        shape=list(statuses.shape), axes=['mode','mask','sample_time','background'],
        modes=MODES, times=TIMES, dtype='uint8', order='C',
        meanings={'0':'same','1':'valid_changed','2':'outside'},
        raw_sha256=hashlib.sha256(raw).hexdigest(), compression='zlib+base64',
        data=base64.b64encode(zlib.compress(raw, 9)).decode()), indent=2)+'\n')
    Path(str(STEM)+'_witnesses.json').write_text(json.dumps(witnesses, indent=2)+'\n')
    Path(str(STEM)+'_metadata.json').write_text(json.dumps(dict(
        mask_background_cases=2*64*512, sampled_responses=2*64*3*512,
        pair_background_checks=2*15*3*512, seconds=round(time.time()-start,3),
        sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}), indent=2)+'\n')
    for mode in MODES:
        print(mode, [r for r in records if r['mode']==mode and r['fine_ticks']==4 and r['mask'] in [1,2,4,8,16,32,33]])


if __name__ == '__main__':
    main()
