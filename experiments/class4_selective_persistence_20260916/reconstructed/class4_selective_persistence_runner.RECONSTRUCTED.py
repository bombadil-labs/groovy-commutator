#!/usr/bin/env python3
"""
Reconstructed 2026-09-16 selective-persistence × spreading runner.

PROVENANCE WARNING
------------------
This is NOT the lost historical runner. It reimplements the scientific
measurements from:
  * the surviving 2026-09-16 report; and
  * the exact R/M definitions in scripts/class4_independent_20260915.py.

Historical fresh seed lists are unrecovered. The exact radius-2
rare-correction challenge is unrecovered and is therefore not simulated.
Use --verify-recovered to verify the surviving numerical evidence without
inventing those missing inputs.

Dependencies: Python 3.10+ and numpy.
"""
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path
import numpy as np

W = 7
H = 8
BURN = 2048
STEPS = 512
S_THRESHOLD = 0.20
ALPHA_THRESHOLD = 0.50
ORIGINS = 16

CONDITIONS = {
    "P":  dict(width=2053, density=0.5, burn=2048, steps=512),
    "V1": dict(width=2063, density=0.3, burn=2048, steps=512),
    "V2": dict(width=2081, density=0.7, burn=2048, steps=512),
    "S1": dict(width=2069, density=0.1, burn=2048, steps=512),
    "S2": dict(width=2099, density=0.9, burn=2048, steps=512),
}

def eca_step(x, rule):
    left = np.roll(x, 1, axis=-1)
    center = x
    right = np.roll(x, -1, axis=-1)
    idx = 4*left + 2*center + right
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    return lut[idx]

def local_table(rule, w=W):
    # Exact reconstruction of the retained Class-IV program's same-window R.
    cores = np.arange(1 << w, dtype=np.int64)
    bits = ((cores[:, None] >> np.arange(w)) & 1).astype(np.uint8)
    q = bits[:,0] + 2*bits[:,1] + 4*bits[:,-2] + 8*bits[:,-1]
    qcounts = np.bincount(q, minlength=16)
    losses = np.zeros((4, 1 << w))
    residuals = np.zeros_like(losses)
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)
    for e in range(4):
        ext = np.column_stack((
            np.full(1 << w, e & 1, dtype=np.uint8),
            bits,
            np.full(1 << w, e >> 1, dtype=np.uint8),
        ))
        out = lut[4*ext[:,:-2] + 2*ext[:,1:-1] + ext[:,2:]]
        y = (out.astype(np.int64) * (1 << np.arange(w))).sum(axis=1)
        counts = np.bincount(y, minlength=1 << w)
        losses[e] = np.log2(counts[y])
        means = np.bincount(q, weights=losses[e], minlength=16) / qcounts
        residuals[e] = means[q] - losses[e]
    sigma = float(residuals.std())
    words = np.arange(1 << (w+2), dtype=np.int64)
    b = (words >> 1) & ((1 << w)-1)
    e = (words & 1) + 2*(words >> (w+1))
    return residuals[e,b], sigma

def trajectory(rule, cfg, seeds):
    n, density = cfg["width"], cfg["density"]
    states = np.stack([
        (np.random.Generator(np.random.PCG64(seed)).random(n) < density).astype(np.uint8)
        for seed in seeds
    ])
    total = cfg["burn"] + cfg["steps"] + 1
    out = np.empty((total, len(seeds), n), dtype=np.uint8)
    out[0] = states
    for t in range(1, total):
        states = eca_step(states, rule)
        out[t] = states
    return out

def spatial_counts(series, cfg, w=W):
    frames = series[cfg["burn"]:cfg["burn"]+cfg["steps"]]
    words = np.zeros(frames.shape, dtype=np.uint16)
    half = w//2
    for j, off in enumerate(range(-half-1, half+2)):
        words |= np.roll(frames, -off, axis=2).astype(np.uint16) << j
    return np.stack([
        np.bincount(words[:,s].ravel(), minlength=1 << (w+2))
        for s in range(words.shape[1])
    ])

def retention(series, cfg, rule, w=W):
    counts = spatial_counts(series, cfg, w)
    residual, sigma = local_table(rule, w)
    totals = counts.sum(axis=1)
    numer = counts @ residual / totals
    if sigma < 1e-12:
        return 0.0
    return float((numer/sigma).mean())

def history_counts(series, cfg, h=H):
    burn, steps = cfg["burn"], cfg["steps"]
    words = np.zeros(series[burn:burn+steps].shape, dtype=np.uint16)
    for lag in range(h+1):
        words |= series[burn-lag:burn+steps-lag].astype(np.uint16) << lag
    joint = (words << 1) | series[burn+1:burn+steps+1]
    return np.stack([
        np.bincount(joint[:,s].ravel(), minlength=1 << (h+2)).reshape(1 << (h+1), 2)
        for s in range(joint.shape[1])
    ])

def current_counts(counts):
    return np.stack((counts[::2].sum(axis=0), counts[1::2].sum(axis=0)))

def predictive_gain(series, cfg, h=H):
    counts = history_counts(series, cfg, h)
    if counts.shape[0] != 6:
        raise ValueError("historical protocol requires six seeds")
    gains = []
    for train_slice, test_slice in ((slice(0,3), slice(3,6)), (slice(3,6), slice(0,3))):
        train = counts[train_slice].sum(axis=0)
        test = counts[test_slice].sum(axis=0)
        train_c, test_c = current_counts(train), current_counts(test)
        p_h = (train + 0.5) / (train.sum(axis=1, keepdims=True) + 1.0)
        p_c = (train_c + 0.5) / (train_c.sum(axis=1, keepdims=True) + 1.0)
        ce_h = float(-np.sum(test*np.log2(p_h)) / test.sum())
        ce_c = float(-np.sum(test_c*np.log2(p_c)) / test.sum())
        gains.append(ce_c-ce_h)
    return float(np.mean(gains))

def cyclic_support_diameter(diff):
    idx = np.flatnonzero(diff)
    if len(idx) == 0:
        return 0
    if len(idx) == 1:
        return 1
    n = len(diff)
    gaps = np.diff(np.r_[idx, idx[0] + n])
    return int(n - gaps.max() + 1)

def spreading(rule, burned, origins=ORIGINS):
    n = burned.shape[1]
    origin_idx = np.floor(np.arange(origins) * n / origins).astype(int)
    d256, d512 = [], []
    for seed_row in burned:
        base = np.repeat(seed_row[None,:], origins, axis=0)
        pert = base.copy()
        pert[np.arange(origins), origin_idx] ^= 1
        for t in range(1, 513):
            base = eca_step(base, rule)
            pert = eca_step(pert, rule)
            if t in (256,512):
                vals = [cyclic_support_diameter(base[j] ^ pert[j]) for j in range(origins)]
                (d256 if t == 256 else d512).extend(vals)
    m256 = float(np.mean(d256))
    m512 = float(np.mean(d512))
    alpha = 0.0 if m256 <= 0 or m512 <= 0 else math.log2(m512/m256)
    return m256, m512, alpha

def simulate_rule(rule, cfg, seeds):
    series = trajectory(rule, cfg, seeds)
    R = retention(series, cfg, rule)
    M = predictive_gain(series, cfg)
    S = max(0.0, R)*max(0.0, M)
    burned = series[cfg["burn"]]
    d256, d512, alpha = spreading(rule, burned)
    return dict(
        rule=rule, R=R, M=M, S=S, alpha=alpha,
        mean_d256=d256, mean_d512=d512,
        passes_S=S > S_THRESHOLD,
        passes_alpha=alpha > ALPHA_THRESHOLD,
        selected=(S > S_THRESHOLD and alpha > ALPHA_THRESHOLD),
    )

def load_seeds(path):
    obj = json.loads(Path(path).read_text())
    for key in CONDITIONS:
        vals = obj[key]
        if len(vals) != 6:
            raise ValueError(f"{key} needs exactly 6 seeds")
    return obj

def read_recovered(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def verify_recovered(path):
    rows = read_recovered(path)
    assert len(rows) == 450
    conditions = {}
    pos = neg = disputed = 0
    ctrl = {"radius2-correction":0, "radius2-pure-shift":0}
    pos_S, pos_a = [], []
    fast_neg_S, highS_neg_a = [], []
    for row in rows:
        conditions[row["condition"]] = conditions.get(row["condition"], 0) + 1
        R,M,S = map(float, (row["R"],row["M"],row["S"]))
        a,d256,d512 = map(float, (row["alpha"],row["mean_d256"],row["mean_d512"]))
        expected_S = max(0,R)*max(0,M)
        assert abs(expected_S-S) < 2e-12
        expected_a = 0.0 if d256 <= 0 or d512 <= 0 else math.log2(d512/d256)
        assert abs(expected_a-a) < 2e-12
        ps = row["passes_S"] == "True"
        pa = row["passes_alpha"] == "True"
        sel = row["selected"] == "True"
        assert ps == (S > 0.20)
        assert pa == (a > 0.50)
        assert sel == (ps and pa)
        name = row["name"]
        rule = None if row["rule"] == "" else int(float(row["rule"]))
        cls = None if row["class"] == "" else int(float(row["class"]))
        disp = row["disputed"] == "True"
        if rule in (54,110):
            pos += int(sel); pos_S.append(S); pos_a.append(a)
        elif rule is not None and not disp and cls in (1,2,3):
            neg += int(sel)
            if a > .5: fast_neg_S.append(S)
            if S > .2: highS_neg_a.append(a)
        elif disp:
            disputed += int(sel)
        elif name in ctrl:
            ctrl[name] += int(sel)
    assert conditions == {"P":90,"V1":90,"V2":90,"S1":90,"S2":90}
    assert pos == 10 and neg == 0 and disputed == 0
    assert ctrl == {"radius2-correction":0,"radius2-pure-shift":0}
    assert abs(min(pos_S)-0.2049895616147079) < 1e-12
    assert abs(min(pos_a)-0.6831268634682903) < 1e-12
    assert max(fast_neg_S) == 0.0
    assert abs(max(highS_neg_a)-0.498938756887789) < 1e-12
    print("Recovered evidence verifies: 450 rows, frozen formulas/thresholds, all headline counts and margins.")

def self_test():
    rng=np.random.default_rng(1)
    x=rng.integers(0,2,size=(4,31),dtype=np.uint8)
    for r in (0,30,54,90,110,122,126,204):
        y=eca_step(x,r)
        assert y.shape == x.shape
    # Rule 90 single-bit cone spans exactly 2t+1 before wrap.
    n=2053
    base=np.zeros((1,n),dtype=np.uint8)
    pert=base.copy(); pert[0,n//2]=1
    for t in range(1,257):
        base=eca_step(base,90); pert=eca_step(pert,90)
    assert cyclic_support_diameter(base[0]^pert[0]) == 513
    print("self-test OK")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--verify-recovered", type=Path)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--simulate-rule", type=int)
    ap.add_argument("--condition", choices=CONDITIONS)
    ap.add_argument("--seed-manifest", type=Path,
                    help="JSON object with exactly six integer seeds for each P/V1/V2/S1/S2.")
    args=ap.parse_args()
    if args.self_test:
        self_test()
    if args.verify_recovered:
        verify_recovered(args.verify_recovered)
    if args.simulate_rule is not None:
        if not args.condition or not args.seed_manifest:
            ap.error("--simulate-rule requires --condition and --seed-manifest")
        seeds=load_seeds(args.seed_manifest)[args.condition]
        print(json.dumps(simulate_rule(args.simulate_rule, CONDITIONS[args.condition], seeds), indent=2))
if __name__ == "__main__":
    main()
