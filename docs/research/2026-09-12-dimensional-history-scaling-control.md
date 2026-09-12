# Product-form linear slice observations are dimension-blind for the frozen history-depth criterion

**Evidence:** exact theorem control on the frozen finite cells.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol. **Independent review:** the original dimensional-scaling protocol was blocked by Claude Code / Fable 5.1 after the reviewer derived the dimension-blind product theorem before implementation; the theorem-control refreeze received renewed Gate 1 on exact head `74393d18a33c51cfff133c88e09a40a2a3018cf6`. Final Gate 2 is pending on gathering PR #171.  
**Protocol:** `docs/research/protocols/dimensional-history-scaling-20260912.md`, superseded for this unit by `docs/research/protocols/dimensional-history-scaling-gate1-refreeze-20260912.md`.  
**Canonical result:** `results/dimensional_history_scaling_control_20260912.json`.

## Question

A suggestive finite 2D interface-history result had raised the hypothesis that the minimum retained history needed for predictive closure might increase with dimensional level. The first proposed matched test used the accepted ordered-axis Rule90 constructor in dimensions 1, 2 and 3 and observed the complete coordinate-zero slice of the newest axis.

Independent Gate 1 showed before implementation that this design cannot test that hypothesis. For a product-form linear law and this coordinate-slice observer, the history criterion factors through one transverse polynomial and is dimension-blind.

This unit therefore preserves and verifies that negative **design theorem/control** rather than presenting a known-false dimensional bet as an experiment.

## Theorem frozen before execution

Let

`F_d = product_i (sigma_i + sigma_i^-1)`

be ordered-axis Rule90 on the `d`-dimensional `n^d` periodic lattice, and let `O_d` retain the complete coordinate-zero slice of the newest axis. Define `H_h` by stacking `O_d F_d^k` for `k=0..h`. Predictive closure at history depth `h` is the exact all-state condition

`ker(H_h) subseteq ker(O_d F_d^(h+1))`.

Write `g = x + x^-1` in `GF(2)[x]/(x^n-1)` and let `D(n)` be the degree of its minimal polynomial. The Gate-1 derivation gives

`h_min(d,n) = D(n) - 1`

for every tested dimensional level: the transverse factors multiply through the slice module and do not change the first dependence among `1,g,g^2,...`.

For the frozen odd rings:

- `D(5)=3`, so `h_min(d,5)=2` for `d=1,2,3`;
- `D(7)=4`, so `h_min(d,7)=3` for `d=1,2,3`.

These values were known before implementation and are regression targets, not discoveries.

## Independent implementations

The pinned verifier uses two materially different paths.

The primary path constructs the full `n^d` Rule90 operator by literal ordered per-axis propagation of GF(2) basis states, forms the coordinate-slice observation rows, and directly measures the rank and kernel-inclusion criterion through `h=8`.

The reference path never constructs or powers that `d`-dimensional matrix. It stays in the one-dimensional cyclic polynomial quotient, repeatedly applies `g=x+x^-1`, and finds the first linear dependence of the power sequence. Agreement therefore checks the product theorem rather than merely reusing one packed implementation twice.

## Exact result

Every frozen cell matches the theorem.

For `n=5` the rank sequences of `H_h` begin:

- `d=1`: `1,2,3,3,...`;
- `d=2`: `5,9,13,13,...`;
- `d=3`: `25,41,57,57,...`.

All three first close at `h=2`.

For `n=7` they begin:

- `d=1`: `1,2,3,4,4,...`;
- `d=2`: `7,13,19,25,25,...`;
- `d=3`: `49,85,121,157,157,...`.

All three first close at `h=3`.

The matrix path agrees with the independent polynomial value in all six cells, and the closing depth is identical across `d=1,2,3` at each fixed `n`.

## Preserved failed evaluation stage

Implementation-only #181 integrated the verifier, permanent workflow and future integrity registration with no canonical result present. The first evaluation PR #183 ran the unchanged scientific verifier and produced result bytes matching the theorem, but the permanent workflow was red because its implementation-stage `--self-test` still asserted that a canonical result must be absent.

PR #183 was preserved and closed unmerged. Workflow-only correction #184 changed only that plumbing: the absence-guard self-test now runs only while the result is absent. The corrected evaluation #185 regenerated the unchanged scientific result from the corrected integrated stage. The canonical JSON is byte-identical to the preserved first-run JSON, and permanent integrity plus byte-for-byte replay are green.

## Interpretation

The result says something useful about experimental design, not about dimensional history scaling itself:

> **Product-form linear ordered-axis laws observed by a complete coordinate slice are structurally incapable of making this `h_min` measure depend on the number of axes.**

For this design, ring arithmetic controls the closing depth through `D(n)` while dimensional level factors out. A future discriminating test of the broader history-to-geometry hypothesis must therefore break at least one of the ingredients that force the theorem—for example the product factorization or the slice-module observation structure—under a separately frozen protocol.

The accepted touching-strip `h=2` result remains motivation only. It is neither confirmed nor refuted by this control.

## Boundaries

Do not infer from this unit:

- that history depth is generally independent of spatial dimension;
- that `h_min(d)=d` is refuted for every dimensional tower or observer;
- intrinsic or representation-independent dimension;
- self-assembly, endogenous control, resonance or self-recognition;
- spacetime emergence, physics, metaphysics, Class IV, universality, renormalization, or any prime/`8n+1` connection.

The exact claim is limited to the frozen product-form linear Rule90 constructor, coordinate-slice observer, odd rings `n=5,7`, dimensions `d=1,2,3`, and the declared all-state history-closure criterion.

## Reproduction

```bash
python scripts/check_result_integrity.py results/dimensional_history_scaling_control_20260912.json
python scripts/verify_dimensional_history_scaling_control.py
```
