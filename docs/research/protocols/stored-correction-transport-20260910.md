# Frozen extension: stored correction transport and its finite-cap boundary

Date: 2026-09-10. Frozen after the finite-routing-boundary audit passed. The prior protocol and result remain unchanged.

## Exact interior law to verify

Keep the unchanged five-symbol radius-nine H_2 in hold mode, with program tuple (r,60) at each logical row site. Word60 implements h(b,n,s)=b xor n under address4b+2n+s. Thus an interior datum should obey

    U'_k(x) = F_r(U_k)(x) xor U_(k+1)(x).

All eight source-rule bits and all eight transport-table bits occupy physical cells. This establishes a physical program realization of the interior law; it does not make a finite stack close. Use one homogeneous fixed ECA r per case and hold all program words. Local program reprogramming and the induced repair of represented corrections are outside this extension.

Define A_0(S)=S xor F_r(S) and A_(k+1)(S)=A_k(F_r(S)) xor F_r(A_k(S)).
Prepare rows0..H with A_k(S), and guard rows -1,H+1 with zero data and the same complete (r,60) program. All other rows are absent. Guards freeze because an outward neighbor is absent. The data rows have both required transverse neighbors.

The predicted finite guarantee is U_k(t)=A_k(F_r^t(S)) whenever k+t<=H. It follows by the triangular transport identity. No guarantee is made outside that triangle. A fixed upper zero cap is not assumed to supply the true next correction.

## Frozen audit

1. Exhaust all256 ECA source words and all32 five-bit 2D data stencils. Compare the unchanged physical interpreter on program(r,60) to an independent integer ECA evaluation xor the positive transverse datum: 8,192 cases.
2. Check all256 rules and all8 width-three source states, with H=2 and four ticks. Generate correction rows using direct recursive operator composition, independently of the physical spatial update. Use periodicity only in the first axis.
3. At every tick compare every nonblank physical symbol with the masked logical step, require fixed support and unchanged programs, and verify all correction cells inside k+t<=2 against the evolved source. Record out-of-triangle mismatches without treating them as failures of the finite guarantee.
4. Retain the explicit rule255, all-zero source witness: the top row first becomes wrong at t=1, the middle at t=2, and the bottom at t=3. At t=3 the bottom is all ones while the true derivative is all zeros. This is a scoped failure of the zero-cap closure choice, not of every finite correction cap.
5. Record case counts, protected-triangle comparisons, complete physical symbol comparisons, number of cases with a bottom discrepancy by tick4, and the rule255 witness. Avoid storing every trajectory. The local proof gives arbitrary source width and all H; the audit is finite and periodic.
6. Commit implementation before execution and reproduce a separate sorted JSON result in CI. Record any implementation correction or protocol deviation.

## What this leaves for the next experiment

Indefinite finite-height closure requires A_(h+1)=g_h(K_h) on the represented image, with K_h=(A_0,...,A_h), and a local physical realization of that cap. Finding a finite-radius truth-table factorization does not itself put its cap program into the current native grammar. The next local closure census should compare K_h, its equivalent forward-observation tuple, and retention of the original source. No census outcome is predicted here.
