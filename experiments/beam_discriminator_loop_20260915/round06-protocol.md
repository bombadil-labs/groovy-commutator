# Round 6: frozen finite predictor, fresh larger test

Protocol review: none at freeze; run authorized by Myk 2026-09-15. Evaluation precedes independent review. This validates a predictor chosen post hoc in R5, not an a priori theory.

Fix the R5 predictor: 0 < q < 0.5 and alpha > 0.5. Here q is minimum recurrence mismatch over the same 80 (p,v) pairs, divided by 2*f*(1-f); alpha=log2(mean disturbance diameter at512 / at256), with extinct or zero denominator assigned zero. All 88 representatives, width 2039, Bernoulli(1/2), seeds 6041511–6041514, burn 2048, 1032 frames (1024 usable), 32 equally spaced perturbation sites and horizon512. The single-perturbation lightcone remains inside the ring. Freeze p range and both cutoffs unchanged. Report every per-run decision, per-rule hit count and majority >=3/4 classification. Core positives are54/110, disputed41/106 reported separately, all other archived classes retain their labels. Do not choose another cutoff on this validation set.

Save packed trajectories and full aggregate damage curves. Diagnostic success requires both core families pass at least3/4, no undisputed negative pass3/4, and all per-run exceptions remain visible. Failure changes the research direction, not the labels. Six-minute local budget.
