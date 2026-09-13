# Protocol: predictive assembly support in the finite dimensional interface family — 2026-09-12

**Status:** frozen before implementation/evaluation. Nothing in this protocol has been run.  
**Program:** *Dimensional Closure and the Commutator Lift*.  
**Authored by:** Codex / OpenAI GPT-5.6 Sol.  
**Protocol review:** pending independent Gate 1 on the exact integrated gathering head. No implementation or evaluation is authorized before Gate 1.

## 1. Question

The dimensional program has begun to expose a joint space/time resource problem: some observed futures become deterministic only after enough history and enough spatial extent are retained. The user connected this to Lee Cronin's Assembly Theory intuition: instead of asking only whether a state is predictable, ask what minimal structured support is required to make that state or transition constructible/identifiable.

This unit does **not** claim to compute Cronin's molecular assembly index. It freezes an assembly-style quantity native to the accepted finite interface-history data:

> What is the minimum subset of retained spacetime coordinates needed to preserve deterministic prediction of the next retained field?

Call that quantity the **predictive assembly support** (PAS). It is a representation-relative causal-support index, not a universal assembly index.

## 2. Frozen predecessor domain

Import the accepted #157 complete-history result and exact source-domain machinery by hash. Do not regenerate scientific choices from memory.

Primary cells are exactly the nine predecessor cells that were globally deterministic at `D2,h=2`:

- ring 6 masks `{11,13,15}`;
- ring 7 masks `{3,5,7,11,13,15}`.

The retained history stack is the predecessor's three-time complete ring field, oldest to newest, with mandatory `A,B` and mask-selected interface bits in the accepted coordinate order.

No new width, history depth, mask, physical law, or source family is introduced in this unit.

## 3. Atomic support coordinates

For one fixed passing `(n,mask)` cell, let the complete retained history key have atomic coordinates

`c = (lag, site, retained_channel)`

with:

- `lag in {2,1,0}` ordered oldest to newest;
- `site in {0,...,n-1}`;
- retained channels in accepted predecessor order.

The target is the **complete next retained field** at the next coarse time.

A support set `S` is any subset of these atomic coordinates. Two records agree on `S` when every retained bit indexed by `S` agrees.

## 4. Predictive assembly support

A support `S` is **prediction-sufficient** iff

> whenever two exhaustive predecessor records agree on `S`, their complete next retained fields are equal.

Define

`PAS(n,mask) = min |S|`

over all prediction-sufficient supports.

This is equivalent to an exact hitting-set problem. For every pair of records with different targets, form the set of atomic coordinates on which their history keys differ. A valid `S` must hit every such difference set.

The implementation must solve the minimum hitting set exactly, not greedily.

## 5. Translation-aware quotient diagnostic

A raw minimum support may pick arbitrary site labels on a periodic ring. Therefore report two quantities separately:

1. `PAS_raw`: minimum atomic support with no symmetry restriction;
2. `PAS_orbit`: minimum number of translation orbits of atomic coordinates whose **entire orbits** are retained.

For a fixed `(lag,channel)`, the translation orbit contains that coordinate at every ring site. Thus `PAS_orbit` counts retained lag/channel fields, while `PAS_raw` measures literal bit support.

Do not collapse these into one score. `PAS_orbit` is a symmetry-respecting descriptive control, not automatically a better index.

## 6. Reuse-aware assembly-style diagnostic

To make the Assembly Theory analogy explicit without claiming equivalence, freeze one optional secondary quantity that rewards repeated support motifs.

For any exact minimum raw support `S`, encode each site's selected `(lag,channel)` subset as a local support symbol. Define `grammar_cost(S)` as the minimum number of binary concatenation nodes in a straight-line grammar that constructs the cyclic sequence of site-support symbols from atomic symbols, allowing previously constructed substrings to be reused.

The protocol does **not** call this Cronin assembly index. Report the minimum grammar cost among all canonical minimum-cardinality supports only if an exact solver can certify it. If exact certification is not practical before implementation review, Gate 1 may strike this secondary diagnostic without changing PAS itself.

## 7. Frozen predictions

### P1 — exact predecessor reconstruction

The imported complete-history grouping exactly reproduces all nine accepted global passes and their target hashes. Any discrepancy blocks interpretation.

### P2 — support is nontrivial

For every primary cell,

`0 < PAS_raw < N_full`,

where `N_full` is the total number of atomic coordinates in the complete three-time history key.

The lower inequality says the target is not constant; the upper inequality predicts that some retained coordinates are redundant for prediction.

### P3 — two-lag necessity leaves a support trace

Every exact minimum support for full `P15` on both rings uses at least one coordinate from the oldest retained lag `t-2`.

This is stronger than the predecessor's statement that the **complete** one-lag field conflicts: a minimum support might conceivably omit some current/one-lag bits while still requiring no oldest-lag bit. P3 says it cannot.

### P4 — cross-ring support-density stability

For full `P15`, freeze the descriptive prediction that

`PAS_raw / N_full`

differs by at most `0.15` between rings 6 and 7.

This is an intentionally weak finite-size stability bet, not a scaling law.

### P5 — orbit support uses multiple times

For full `P15` on both rings, every exact minimum `PAS_orbit` solution uses coordinates from at least two distinct lag values.

A failure would mean the apparent temporal need of the full-field predecessor can be replaced by a translation-symmetric selection from a single time slice once channels are chosen appropriately.

## 8. What PAS means and does not mean

Allowed meaning:

- exact minimum amount of the **declared retained spacetime record** needed to keep the next retained field single-valued on the accepted finite reachable family;
- a way to compare history, channel, and spatial-support costs inside one frozen representation;
- an assembly-style causal-support diagnostic.

Not allowed:

- Cronin molecular assembly index;
- thermodynamic or chemical assembly;
- Kolmogorov complexity;
- intrinsic dimension;
- causal emergence or consciousness;
- proof that the selected coordinates are physically assembled by the CA;
- a claim that lower PAS means greater naturalness.

## 9. Canonical minima and no witness shopping

If multiple minimum supports exist, order atomic coordinates by `(lag_oldest_first, site, channel)` and represent a support by its sorted tuple. The canonical minimum is the lexicographically smallest exact minimum support.

Report:

- minimum cardinality;
- canonical support;
- count of exact minimum supports if tractable;
- lag/channel/site occupancy profile;
- target-class count;
- exact certificate that every conflicting-target pair is hit.

For orbit supports, order `(lag,channel)` lexicographically and apply the same canonical rule.

## 10. Independent implementation requirements

After Gate 1, implementation-only/no-result must pin:

1. exact import/hash verification of #157 records;
2. two independent constructions of conflict difference sets;
3. an exact branch-and-bound minimum hitting-set solver;
4. an independent exhaustive-size verifier that confirms no support of size `<PAS` works and that the reported support does;
5. translation-orbit solver/checker;
6. canonical ordering and certificates;
7. permanent two-tier result integrity/replay with a green no-result stage.

No scientific PAS value may be inspected before the implementation-only stage is green and integrated.

## 11. Relation to dimensional scaling

PAS complements, but does not replace, history depth `h` or locality radius `R`.

A future dimensional tower could compare a support vector such as

`Sigma_d = (history depth, spatial extent, retained channels, PAS_raw, PAS_orbit)`

across rungs. This protocol establishes only the finite 2D predecessor baseline needed before any such dimensional comparison.

## 12. Gate-1 questions

The independent reviewer should attack especially:

1. Is PAS a meaningful causal-support quantity or merely a renamed feature-selection problem?
2. Is the hitting-set equivalence exact for whole-field deterministic prediction?
3. Does restricting to the nine passing #157 cells introduce unacceptable selection bias, or is it the correct domain because PAS is undefined/infinite on conflicting cells?
4. Should globally conflicting predecessor cells receive `PAS=∞` as controls, or remain outside the scored family?
5. Are P3 and P5 genuinely stronger than the accepted two-lag result?
6. Is the 0.15 density bet defensible or arbitrary enough that it should be removed?
7. Is `PAS_orbit` useful or does taking full translation orbits obscure the resource question?
8. Should the reuse-aware grammar diagnostic be removed to avoid conflating this with Assembly Theory?
9. Are exact minimum certificates computationally practical on the declared finite cells?
10. Are the non-claims strong enough to prevent reporting PAS as Cronin assembly index?

Binding changes to predecessor domain, support atoms, target, optimization objective, predictions or interpretation require renewed exact-head Gate 1 before evaluation.