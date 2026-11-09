# GQR census and Rule-54 invariant golden fibers (2026-10-07)

**Scientific scope:** 256 elementary CAs at jet prefix (G,Q,R), followed by
a separately frozen Rule-54 G..A5 full-line source-pair invariance test.
The experiment is deterministic: no random seeds and no class labels are
used in selection. The initial design was frozen before the census. A
second, narrower golden-component swap question was frozen **after** the
primary Rule-54 outcomes and is therefore exploratory in its selection.

## Requirements

- Python 3.10+;
- C++17 compiler (g++);
- NumPy, SciPy, SymPy.

Install the optional research dependencies in a virtual environment:

    python -m pip install numpy scipy sympy

## Reproduce

From the repository root:

    python experiments/jet_gqr_256/prepare_census.py
    python experiments/jet_gqr_256/rule54_invariance.py
    python experiments/jet_gqr_256/verify.py

The first command compiles a fresh temporary C++17 executable and processes
all 256 rules. The second reconstructs the 3,561,416-edge Rule-54 A5 equal-jet
source-pair graph, identifies the three pure off-diagonal branching recurrent
SCCs, enumerates **all** their consecutive three-edge paths, and tests each
evolved patch with a separate scalar implementation.

The verification script replays both and compares every saved census row and
every saved Rule-54 local witness (excluding nondeterministic timings and
floating-point differences below 1e-8). It also checks source SHA-256 hashes.

Output files:

- results/jet_gqr_256_20261007.json
- results/rule54_golden_invariance_20261007.json

## Source bit convention

A word's bit 0 is its **leftmost** spatial source bit. For a 13-bit input
window, the local Rule-54 jet is centered on bit 6. The three-step pair path
uses a pair of initial 12-bit de Bruijn contexts and appends three source
bits, covering 15 cells. Rule-54 evolution produces a 13-bit central window.

The pair relation compares complete current **spatial** jet fields, not
only temporal trajectories from isolated finite initial conditions.

## Proof boundary

The two golden components C_plus and C_minus are positively entropic source
*pair* subshifts, and their exact local evolution swaps them by inclusion.
Induction using the commutator recurrence then shows **all future jet levels
A_k, k>=1, agree within these pairs**. This is not a positive typical
conditional-entropy theorem, not a statement about the source coordinate S,
and not a Class-IV discriminator.

The full rule histogram confirms that branching at GQR is common. The
exceptional invariant subsystem, not the bare presence of branching, is the
structural Rule-54 result.

See docs/research/2026-10-07-jet-gqr-census-fibonacci.md for details.
