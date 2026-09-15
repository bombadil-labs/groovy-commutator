# Round 5: fresh recurrence and disturbance spread

Protocol review: none at freeze; run authorized by Myk 2026-09-15 under standing loop approval. Evaluation precedes review.

Question: does the R4 recurring-background pattern survive prime widths and fresh seeds, and can expanding disturbance support distinguish 54/110 from the 73 confounder? This is an adaptive discovery round, with no fitted class threshold.

For all 88 representatives, use widths 509 and 1021 and fresh seeds 6041502,6041503,6041504, density 1/2, burn 1024, 520 saved frames. Apply exactly the same 80-candidate recurrence selection and statistics as R4. Also record the residual using the R4-selected pair to distinguish selector variation from state variation. Normalize recurrence density by 2*f*(1-f), with f the trajectory's one-bit density; report zero for constant trajectories.

For each width-1021 run, use the first retained state and 16 evenly spaced single-bit perturbation sites, translated to the center. Evolve baseline and perturbed state under the SAME native rule for 256 steps. Record at t=16,32,64,128,256: surviving trial fraction, mean Hamming support, and mean support diameter (max minus min position plus one; extinct=0). No wrap alias: the radius-one lightcone is inside the width-1021 ring. Report log2(mean diameter at256 / mean diameter at128) if both positive, otherwise zero, plus the full trajectories of aggregate support. This is a finite-horizon diagnostic, not an asymptotic growth proof.

Candidate conceptual condition: persistent departures from a recurring domain AND spatially unconfined influence. Each clause should reject a different adversary, without rewarding a motionless state. Inspect all false positives and sensitivity before choosing a threshold. Five-minute compute budget, all outside Actions.
