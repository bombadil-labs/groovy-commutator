# Nonlinear Rules 4 and 200 have zero commutator

## Counterexamples

Rule 4 has Boolean expression \(c(1+l)(1+r)\); Rule 200 has \(lc\oplus cr\oplus lcr\). Here \(l,c,r\) are the neighborhood bits, not the affine bias vector. Products make both rules nonlinear.

For each rule, the self-commutator vanishes on all 32 five-cell neighborhoods. Five cells contain its full local causal window, so this is exhaustive rather than a sampled orbit result.

## Reproduce

The [algebra verification script](../../scripts/verify_history_algebra.py) records the result in [the exact-check output](../../results/history_algebra_checks.json). The general classification is specific to elementary CA; the counterexamples suffice to disprove the broader converse.
