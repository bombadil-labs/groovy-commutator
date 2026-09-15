# Round 9: measurable interval tails and their transport bounds

Protocol review: none at freeze; run authorized by Myk2026-09-15. Evaluation precedes independent review.

Question: does the mathematically invariant asymptotic decay of recurrence-free intervals leave an affordable finite signal, and do actual lifted estimates respect the proved bounds? Do not replace the frozen finite classifier or fit another class threshold in this round.

Reuse all352 R6 native trajectories, with their previously selected(p,v), which is a root-level selector and not claimed invariant. For each residual compute the empirical probability P(L) of an all-zero cyclic interval, counting every spatial origin and every one of1024 times, at L=1,2,4,8,16,32,64,128,256. Record counts and finite slopes [log P(L)-log P(2L)]/L; when a required probability is zero, record null/censored, not a pseudocount or an inferred infinite true rate. Pooled mixtures of components can change asymptotic interpretation, so retain each run.

For roots0,18,54,73,110,126,204 and seed6041511, materialize the same recurrence pair through D3 for256 times at width2039. Let B_d indicate any differing macrocolumn bit. At every L above (where L+2R<width), verify P_A(L+2R)<=P_B(L)<=P_A(L) with R=2(d-1), using complete cyclic-origin counts. Record actual finite slopes at every floor, including their changes. This tests the inclusion consequence exactly on the finite sample; it does not prove stationarity or existence of the infinite-line asymptotic rate. Budget3minutes.
