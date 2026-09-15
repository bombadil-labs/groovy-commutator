# Factor-balanced interaction study

Protocol: docs/research/protocols/factor-balanced-interactions-20260915.md.
Gate 1 approved protocol 00bc0841a820e912d63a089d890745159aba75e7:
https://github.com/bombadil-labs/groovy-commutator/pull/266#issuecomment-5688014363.
Implementation 587d8fc9c83d74349493b8b28d4a5bf7326b36e6; predictions
committed a42df7e5c887bf5f20454340bd42d852416cc4b7 and sealed
8cf20c3ab61b5734bb49168368252af666221595 before fresh evaluation.

Requires Python 3.12 and NumPy (execution records pin the version).
From repository root, in a separate copy with generated outputs removed:

```sh
OPENBLAS_NUM_THREADS=1 python scripts/factor_balanced_interactions.py fit
OPENBLAS_NUM_THREADS=1 python scripts/factor_balanced_interactions.py confirmation
```

Keep historical-relations.json, historical-provenance.json, implementation-freeze.json,
and prediction-seal.json. The regenerated predictions must match the committed seal
before confirmation runs. Completed outputs and partition files are deliberately
not overwritten. Fitting is limited to 120 seconds; confirmation to 900 seconds;
each process has a 3-GiB memory cap. Scientific generation and independent replay
run outside CI. The fast CI tier compiles sources and verifies recorded hashes only.

All raw partitions and comparison evidence are in the accompanying archive; the
repository retains predictions, scored results, provenance, and independent review.
The historical relation input is a byte-identical copy of the previous study's
compact-relations.json, with its original archive provenance recorded separately.

For the independent audit after the seal and fresh output are present:

```sh
OPENBLAS_NUM_THREADS=1 python review/factor_balanced/verify.py fit
OPENBLAS_NUM_THREADS=1 python review/factor_balanced/verify.py cases
OPENBLAS_NUM_THREADS=1 python review/factor_balanced/verify.py score
```

Check the verifier CLI and independent-review.md for exact audit commands.
For publication-only rendering, run scripts/plot_factor_balanced.py (Matplotlib)
and scripts/summarize_factor_balanced.py; neither generates CA data or refits models.
