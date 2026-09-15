# Response quotient and retained source distinctions

Question: does counting genuinely distinct responses of compatible completions, together with source-state information retained across them, improve on static completion counts? Myk authorized this experiment with "let's do it" after the cohabitation discussion and granted blanket Gate 1 approval and one final push. Protocol review: none at local freeze; implementation/evaluation authorized by Myk 2026-09-15. No per-step PR or approval wait. Independent review follows execution. This is a new bounded experiment; it does not alter the preceding failed discriminator results.

## Fixed domain and meanings

Use the preserved uniform six-field cache, dimension 2 only, for every one of the 88 minimum ECA reflection/complement-conjugation representatives, at widths 7 and 8. Each finite invariant beam contains all 2^W source states, in binary numerical order, with shape 6 by W. Its native physical neighborhood has radius 3 vertically and 2 horizontally. Read the archived grid and forced flip-mask entries; do not reconstruct a new lift or modify its on-beam law. Verify source recovery F4 xor F5 and native successor equality with the encoded ECA successor for every state.

A probe flips exactly the cell at column 0 in row j, j=0,...,5. This is one cell of a periodic fundamental domain; its copies repeat on the infinite lattice. Average over all source states S and six known probe rows J. All horizontal translates are represented by the complete source ensemble. A separate unperturbed control must give the same endpoint for all completions at every measured time. Observable Y is the entire child configuration at a specified final time, not its trace or decoded source only. "Past" here means the initial W-bit source state, not an unbounded prehistory. Completion choice varies across counterfactual experiments and is fixed throughout each trajectory; this does not claim multiple futures under one fully specified deterministic CA.

## Exact one-step response count

For each perturbed configuration, let u be the number of distinct physical neighborhood keys that are queried but absent from the forced table. Every such key supplies one independent Boolean flip-mask variable; repeated occurrences share the variable. Every variable appears in at least one output position, so the mapping from its u assignments to next configurations is injective. The number of distinct one-step responses over all unrestricted binary local completions is exactly 2^u. Save u for every (S,J), plus summaries. Unqueried entries contribute zero. This exact count is not a count of future trajectories or of jointly realizable endpoint maps across all probes.

## Fixed longer-horizon completion bank

All completions retain the exact forced flip mask. On every other physical key q use these eight globally fixed policies:

1. flip mask 0 (identity off the forced domain);
2. flip mask 1;
3. flip mask equal to the central bit (output 0);
4. flip mask equal to one xor the central bit (output 1);
5–8. the low bit of SplitMix64(q + seed), with seeds 1701,1702,1703,1704.

SplitMix64 is the standard sequence add 0x9e3779b97f4a7c15, xor-shift 30 and multiply 0xbf58476d1ce4e5b9, xor-shift 27 and multiply 0x94d049bb133111eb, xor-shift 31, all modulo 2^64. Keys use row-major lexicographic offsets (-3..3,-2..2), first bit most significant. The central bit is bit 17. Hash policies use only the physical key and fixed seed, never row phase, source state, time or ECA label. They define fixed laws, not fresh noise on each query.

Measure endpoints after 1,2,4,8 native steps. Primary is W=7,t=4, full eight-policy bank. W=8,t=4 is the declared cross-width check; t=1,2,8 are sensitivities. Do not select a best horizon. For each time and bank, group completion policies that have identical endpoint maps on the ENTIRE (S,J) probe panel. Count each resulting behavioral class once. These are equal only on this finite probe panel and horizon, not globally equal rules.

Let A be uniform over those behavioral classes, independently of uniform S and J. With Y=Y_A(S,J), calculate exactly from the finite endpoint table:

- M = I(S;Y | J) / W, source information retained when the completion class is unknown to the observer;
- F = H(Y | S,J), response diversity in bits across behaviorally distinct completions;
- fixed candidate score T = M * F / log2(B), where B is the original bank size (8 or 4). A one-class quotient has F=0. The denominator never shrinks to make a sparse quotient look better;
- known-completion retention I(S;Y | A,J)/W, as a diagnostic distinguishing loss of source distinctions from uncertainty about which law acted;
- the raw and quotient completion counts and per-completion source-output entropy.

The completion distribution is a declared finite experimental choice, not a uniform sample over every compatible full rule. Report the structured-only four-policy bank and hash-only four-policy bank as prespecified sensitivity checks. Report M and F alone as ablations. No classifier fitting, threshold tuning, cycle-growth factor or new scoring formula follows this run. A high joint score can occur in simple systems; it is a candidate, not a definition of complexity. Scores refer to the minimum representatives in the declared physical orientation; covariance of the hash bank under reflection/complement of the root is not asserted. This orientation qualification was added before implementation or scientific execution.

## Predictions and reporting

P1: unperturbed endpoints collapse to one behavioral class for every source beam and all measured times. This is an exact expected control, not a Class-IV claim.

P2, deliberately strong discrimination bet: at the primary full-bank score, both 54 and 110 exceed every included negative, separately at W=7 and W=8. Primary positives remain 54/110; disputed 41/106 are excluded from the 84-negative comparison and reported separately. 122/126 remain negatives. Report all 88 scores, tied ranks, AUC overall and against Class III, exact separation margins and every negative at or above the lower positive. All sensitivity and ablation results remain visible.

P3: both primary positives outrank identity, both shift directions, and affine/additive controls at primary horizon, with separately reported outcomes. Equivalent rules may be represented by their minimum family representative; controls explicitly include families of 0,1,15,51,60,90,105,150,170,204, plus prior failures 9,73,122,126. Do not redefine these controls after results.

P4: the P2 separation holds for the structured-only and hash-only banks at primary horizon in both widths. Failure indicates this candidate lacks the tested bank robustness; changing bank also changes the declared completion prior and is not proof about every completion family.

## Verification, cost and provenance

Before science, compare packed physical keys with explicit tuple neighborhoods; validate all eight completion evaluations against scalar calculations; enumerate all assignments in small synthetic one-step examples; validate entropy and quotient logic using duplicate policies, an identity channel, a complete-erasure channel, and an XOR channel where knowing A restores S but not knowing A hides it. This guards against conditional-mutual-information double counting.

Scientific evaluation runs outside Actions with a 900-second wall cap and per-rule/width checkpoints. Report progress at least every minute. A partial population is censored and must not be reported as a complete discriminator. Save all endpoint arrays, u counts, source and input hashes, timings, bank definitions and per-rule metrics. Freeze this document and implementation hashes locally before the run; push source, evidence and interpretation together at the end under Myk's authorization. No new trajectory experiment after inspecting this run within this bounded attempt. Independent review may perform small controls and recompute every metric from saved endpoints; it need not rerun the whole science.
