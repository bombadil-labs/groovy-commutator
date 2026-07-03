"""What does Fourier bring? Dispersion relations, and a rhyme spectrum
that finds a rule's ether without being told it exists.

Three probes on space-time fields (steps x n), all built on the same
object -- the 2D power spectrum |FFT2(field)|^2, whose structure encodes
how the field organizes across space AND time at once:

A. DISPERSION BY REGIME. Coherent traveling structure concentrates
   spectral power along lines omega = v*k (a dispersion relation); noise
   spreads power flat; frozen/crystal piles at DC. Metric: spectral
   concentration = fraction of non-DC power in the top 1% of bins.
   Prediction: structured >> noisy, with crystalline trivially high.

B. SOLITON VELOCITY CHECK. Cycle 1 (experiment_remainder_rules.py) found
   pairs whose disagreement field evolves as a pure shift (remainder rule
   170/240). Their diff-field spectra should be razor lines whose slope
   is exactly +/-1 cell/step. Fourier should read the remainder rule's
   velocity straight off the spectrum.

C. THE RHYME SPECTRUM. Self-coupling across time: R[k,s] = mean density
   of S(t) XOR shift_s(S(t-k)) -- the space-time autocorrelation, i.e.
   deja vu as an instrument. A rule with a periodic background (ether)
   has a lattice vector (k*, s*) where R dips toward 0: the background
   cancels and ONLY the defects (gliders) survive the XOR. Run on rule
   110 from soup: the minimum should land on the ether's lattice vector
   with no prior knowledge, and the residual field at that offset is an
   unsupervised glider extractor.

Output: results/fourier_dispersion.csv + printed summaries; the rhyme
minimum's residual field density quantifies "glider mass" left over.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from groovy.ca import apply_rule  # noqa: E402

N = 256
STEPS = 512
BURN = 64


def trajectory(s0, rule, steps):
    s = s0.copy()
    out = np.zeros((steps, len(s0)), dtype=np.uint8)
    for t in range(steps):
        out[t] = s
        s = apply_rule(s, rule)
    return out


def divergence_field(s0, a, b, steps):
    p1, p2 = s0.copy(), s0.copy()
    F = np.zeros((steps, len(s0)), dtype=np.uint8)
    for t in range(steps):
        F[t] = p1 ^ p2
        p1 = apply_rule(apply_rule(p1, a), b)
        p2 = apply_rule(apply_rule(p2, b), a)
    return F


def spectral_concentration(field, top_frac=0.01):
    """Fraction of non-DC spectral power held by the top `top_frac` of
    non-DC bins. 1.0 = all power on a few lines; ~top_frac = white."""
    x = field.astype(np.float64) - field.mean()
    P = np.abs(np.fft.fft2(x)) ** 2
    P[0, 0] = 0.0
    flat = np.sort(P.ravel())[::-1]
    k = max(1, int(len(flat) * top_frac))
    total = flat.sum()
    return float(flat[:k].sum() / total) if total > 0 else 1.0


def dominant_velocity(field):
    """Weighted-peak estimate of the dispersion slope: for each spatial
    frequency k, find the omega of max power; fit omega ~ v*k through the
    strongest columns. Velocity in cells/step, sign = drift direction."""
    x = field.astype(np.float64) - field.mean()
    P = np.abs(np.fft.fft2(x)) ** 2
    steps, n = field.shape
    P[0, :] = 0; P[:, 0] = 0
    ks, ws, wts = [], [], []
    for ki in range(1, n // 2):
        col = P[:, ki]
        wi = int(col.argmax())
        w = wi if wi <= steps // 2 else wi - steps
        ks.append(ki / n)
        ws.append(w / steps)
        wts.append(col[wi])
    ks, ws, wts = map(np.array, (ks, ws, wts))
    keep = wts > np.percentile(wts, 80)
    if keep.sum() < 3:
        return None
    v = float(np.polyfit(ks[keep], ws[keep], 1, w=wts[keep])[0])
    return v


def rhyme_spectrum(field, max_lag=24):
    """R[k, s] = density of field[t] XOR roll(field[t-k], s), averaged over
    t. Returns the full (k, s) surface and its argmin."""
    steps, n = field.shape
    R = np.ones((max_lag + 1, n))
    for k in range(1, max_lag + 1):
        A = field[k:]
        B = field[:-k]
        for s in range(n):
            R[k, s] = float((A ^ np.roll(B, s, axis=1)).mean())
    kk, ss = np.unravel_index(np.argmin(R[1:]), R[1:].shape)
    return R, (int(kk) + 1, int(ss))


def main() -> None:
    rng = np.random.default_rng(0)
    sweep = pd.read_parquet(ROOT / "results" / "sweep_full_classified.parquet")

    # A. dispersion by regime
    rows = []
    for regime in ("structured", "noisy", "crystalline"):
        grp = sweep[sweep.regime == regime].sample(60, random_state=6)
        for r in grp.to_dict("records"):
            s0 = rng.integers(0, 2, N).astype(np.uint8)
            F = divergence_field(s0, int(r["rule_a"]), int(r["rule_b"]), STEPS)[BURN:]
            if F.mean() < 0.02 or (F[1:] ^ F[:-1]).mean() < 0.02:
                continue
            rows.append(dict(regime=regime, rule_a=r["rule_a"], rule_b=r["rule_b"],
                             concentration=round(spectral_concentration(F), 4)))
    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "results" / "fourier_dispersion.csv", index=False)
    print("A. spectral concentration of LIVE diff fields (top-1% bins' power share):")
    print(df.groupby("regime")["concentration"].describe()[["25%", "50%", "75%"]].round(3))

    # B. soliton velocity check on cycle-1 shift-remainder pairs
    print("\nB. dispersion slope of shift-remainder pairs (expect ~ +/-1):")
    rr = pd.read_csv(ROOT / "results" / "remainder_rules.csv")
    for r in rr[rr.remainder_rule.notna()].head(6).to_dict("records"):
        s0 = rng.integers(0, 2, N).astype(np.uint8)
        F = divergence_field(s0, int(r["rule_a"]), int(r["rule_b"]), STEPS)[BURN:]
        v = dominant_velocity(F)
        print(f"  ({int(r['rule_a'])},{int(r['rule_b'])}) remainder={int(r['remainder_rule'])}: "
              f"spectral velocity ~ {v:+.2f} cells/step" if v is not None else "  (flat)")

    # C. rhyme spectrum on rule 110: find the ether lattice vector blind
    print("\nC. rhyme spectrum, rule 110 from soup:")
    s0 = rng.integers(0, 2, N).astype(np.uint8)
    T = trajectory(s0, 110, STEPS)[BURN:]
    R, (k, s) = rhyme_spectrum(T)
    print(f"  raw density: {T.mean():.3f}")
    print(f"  rhyme minimum at lag k={k}, shift s={s}: residual density {R[k, s]:.4f}")
    print(f"  (rule 110 ether lattice vector is (T=7, X=-4)-ish; multiples count)")
    # residual field = glider extraction
    resid = T[k:] ^ np.roll(T[:-k], s, axis=1)
    print(f"  residual (glider) mass fraction: {resid.mean():.4f} of cells")
    # control: rule 30 should have NO deep rhyme minimum
    T30 = trajectory(s0, 30, STEPS)[BURN:]
    R30, (k30, s30) = rhyme_spectrum(T30)
    print(f"  control rule 30: best rhyme (k={k30}, s={s30}) residual density {R30[k30, s30]:.4f} "
          f"(no ether, nothing cancels)")
    # a second structured rule: 54
    T54 = trajectory(s0, 54, STEPS)[BURN:]
    R54, (k54, s54) = rhyme_spectrum(T54)
    print(f"  rule 54: rhyme minimum (k={k54}, s={s54}) residual density {R54[k54, s54]:.4f}")


if __name__ == "__main__":
    main()
