"""How much coupling does emergence need? The alpha sweep.

The pre-hoc emergence result (CLAUDE.md result 7) is binary: fully coupled
layers of boring parts produce structure. This makes coupling a KNOB:
gate the fourth input through a mask of density alpha, so each cell of
layer A reads its true fourth input (layer B) with "probability" alpha and
reads 0 otherwise -- at alpha=0 the layers are independent elementary
rules (boring by construction), at alpha=1 the full coupled system.

Two gating modes, because they test different physics:
  quenched  -- one fixed random mask per run (some cells permanently
               coupled, a spatial alloy of wet and dry sites)
  annealed  -- fresh random mask every step (every cell intermittently
               coupled, homogeneous on average)

Measured across alpha, per emergent example pair, 24 seeds per point:
  comp     zlib compressibility of layer A's trajectory (structure band
           is the middle; boring parts sit near 0)
  spec     spectral concentration (top-1% share, experiment_fourier.py's
           instrument) -- high = coherent traveling modes
  var      across-seed variance of comp -- a susceptibility-like signal;
           a peak at intermediate alpha is the signature of a transition

Output: results/critical_coupling.csv + printed curves.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from groovy.metrics import compressibility  # noqa: E402
from groovy import prehoc  # noqa: E402

N = 100
STEPS = 100
SEEDS = 24
ALPHAS = [round(a, 2) for a in np.arange(0.0, 1.0001, 0.05)]
EXAMPLES = [(77, 55, 44, 23), (237, 93, 71, 221)]


def spectral_concentration(field, top_frac=0.01):
    x = np.asarray(field, dtype=np.float64)
    x = x - x.mean()
    P = np.abs(np.fft.fft2(x)) ** 2
    P[0, 0] = 0.0
    flat = np.sort(P.ravel())[::-1]
    k = max(1, int(len(flat) * top_frac))
    tot = flat.sum()
    return float(flat[:k].sum() / tot) if tot > 0 else 1.0


def coupled_run(a0, a1, b0, b1, alpha, mode, rng):
    ta = prehoc.rule4_from_pair(a0, a1)
    tb = prehoc.rule4_from_pair(b0, b1)
    A = rng.integers(0, 2, N).astype(np.uint8)
    B = rng.integers(0, 2, N).astype(np.uint8)
    mask_a = (rng.random(N) < alpha).astype(np.uint8)
    mask_b = (rng.random(N) < alpha).astype(np.uint8)
    out = np.zeros((STEPS, N), dtype=np.uint8)
    for t in range(STEPS):
        out[t] = A
        if mode == "annealed":
            mask_a = (rng.random(N) < alpha).astype(np.uint8)
            mask_b = (rng.random(N) < alpha).astype(np.uint8)
        xa = B & mask_a
        xb = A & mask_b
        A, B = prehoc.apply_rule4(A, xa, ta), prehoc.apply_rule4(B, xb, tb)
    return out


def main() -> None:
    rows = []
    for (a0, a1, b0, b1) in EXAMPLES:
        for mode in ("quenched", "annealed"):
            for alpha in ALPHAS:
                comps, specs = [], []
                for seed in range(SEEDS):
                    rng = np.random.default_rng(10_000 * seed + int(alpha * 100))
                    F = coupled_run(a0, a1, b0, b1, alpha, mode, rng)
                    comps.append(compressibility(F))
                    specs.append(spectral_concentration(F))
                rows.append(dict(example=f"{a0},{a1}|{b0},{b1}", mode=mode, alpha=alpha,
                                 comp_median=round(float(np.median(comps)), 4),
                                 comp_var=round(float(np.var(comps)), 5),
                                 spec_median=round(float(np.median(specs)), 4)))
        print(f"example {a0},{a1}|{b0},{b1} done", flush=True)

    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "results" / "critical_coupling.csv", index=False)
    for (ex, mode), grp in df.groupby(["example", "mode"]):
        print(f"\n{ex}  [{mode}]   alpha: comp (var) | spec")
        for r in grp.itertuples():
            bar = "#" * int(r.comp_median * 40)
            print(f"  {r.alpha:4.2f}: {r.comp_median:6.3f} ({r.comp_var:7.5f}) | {r.spec_median:5.3f} {bar}")


if __name__ == "__main__":
    main()
