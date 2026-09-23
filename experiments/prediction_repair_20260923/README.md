# Prediction and one-action repair

See the [frozen protocol](../../docs/research/protocols/prediction-repair-20260923.md).
The native Python witness filter carries the finite-grammar idea of PR #298
into a control task. It also handles conflicts requiring more than two states.
This is not a language performance comparison. No Jev or paid API is used.

Python 3.12 and NumPy suffice. From the repository root:

```sh
python -m unittest discover -s tests -p test_prediction_repair.py
python experiments/prediction_repair_20260923/run.py \
  --implementation-commit IMPLEMENTATION_SHA \
  --output /tmp/prediction-repair-fresh.json
python experiments/prediction_repair_20260923/verify.py \
  /tmp/prediction-repair-fresh.json --output /tmp/prediction-repair-audit.json
```

Outputs are exclusive-create. Never use a canonical result path for a rerun.
Evaluation and verification each have a 120-second POSIX wall cap. A failed
or censored evaluation keeps every prediction explicitly unscored. The
verifier uses the existing scalar library CA, explicit future words,
set-partition enumeration and ordinary Python set intersections. It does not
call the search oracle. It is a separate implementation by the same author,
not independent scientific review.

Action code zero means noop; code i+1 flips physical cell i. Integer bit i is
cell i. Displayed row strings use increasing cell-index order (little-endian),
so they are not the usual printed binary notation for an integer. Observers
read four ordered three-cell blocks starting at cell zero. The controller
can inspect their entire row and address any one of twelve sites.

Passive prediction concerns only membership in the four-phase stripe family,
not the whole microscopic trajectory or autonomous dynamics of the encoder.
Repair concerns endpoint membership after four source steps, then undisturbed
persistence by invariance of that family. No repeated injury or local embodied
controller is tested. The objective and controller are supplied externally.

The evidence includes all 4,140 encoder verdicts, every minimum encoder index,
guided-search witnesses and rejections, exact selected policies and cost
accounting. The larger-witness prediction samples the first failing repair
fiber for each encoder, reduced in source order by deletion; absence of a
larger witness in that deterministic sample is not a general pairwise theorem.
