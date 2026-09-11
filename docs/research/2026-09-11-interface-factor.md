# The frozen six-bit touching-strip interface does not close within longitudinal radius two

**Research note, 2026-09-11.** Bounded interface-factor unit of [Dimensional Closure and the Commutator Lift](2026-09-09-dimensional-closure-program.md). Authored by: Codex / OpenAI GPT-5.6 Sol. Protocol: [`interface-factor-20260911.md`](protocols/interface-factor-20260911.md). Myk authorized execution under the recorded temporary retrospective-review exception while Claude/Fable is unavailable; retrospective cross-model review remains owed. Protocol integration `84f5b5de` preceded implementation integration `f75a4aa2`, which still contained no canonical result. The first frozen evaluation then produced [`results/interface_factor_20260911.json`](../../results/interface_factor_20260911.json) at `aa69196`; source-integrity registration and one-shot cleanup followed, and evaluation integrated at `dd6004d` after all 20 final-head checks were green, including byte-for-byte replay.

## Question

Earlier touching-strip work established two facts that pull in opposite directions. Adjacent finite Rule90 strips interact locally rather than evolving independently, and retaining the obvious six physical band bits repairs the first update but does not stay closed indefinitely. At the same time, raw vertical escape by itself does not prove that no **finite symbolic interface state** can summarize the interaction.

This unit therefore asked a narrower question:

> On the exhaustive declared family of reachable adjacent-strip trajectories, do the two vertex bits plus four natural interface-correction bits define a bounded-radius autonomous local factor?

The test was frozen before implementation and evaluation. It is deliberately a test of one natural finite-state representation family, not a search over arbitrary encodings.

## Frozen representation and domain

The four rows of the touching pair are re-coordinated into six binary symbols at each logical longitudinal site:

`(A, B, E0, E1, E2, E3)`.

`A` and `B` are the two strip vertex bits. `E0..E3` are interface-correction coordinates chosen so that all four are zero on every initially encoded adjacent-strip pair. The map is invertible on the six retained band cells, so this is a recoding rather than a loss of information at one site.

The frozen census exhausts every source pair on horizontal rings `n=6` and `n=7`: `4096 + 16384` source pairs. The physical 2D selector law advances by two fine ticks per coarse update. Primary scoring pools transitions `t=0..3`; a predeclared stress horizon pools `t=0..6`.

Every one of the 16 subsets of `E0..E3` is tested while always retaining `A` and `B`. For each retained state, candidate longitudinal radii are exactly `R=0,1,2`. A candidate passes only when every identical retained local neighborhood in the pooled declared domain has the same next retained center symbol.

Frozen constructive bet J3 was that the full six-bit state, P15, would pass for some `R<=2` on the primary horizon.

## Result: J3 fails

J3 is false within the frozen budget. The full six-bit state has **no passing radius among `R=0,1,2`** on the primary horizon and no passing radius on the stress horizon.

The complete frozen mask census is stronger in the same bounded sense: **none of the 16 interface masks passes at any tested radius** on either horizon. There is therefore no inclusion-minimal passing interface subset and no P15 essential-dependency audit to perform; that audit was predeclared only for a passing full factor.

This is not a statistical failure. For every rejected mask/radius pair, the result records a deterministic canonical pair of pooled records with the same retained local neighborhood and different retained next-center symbols.

## Physical controls pass

The negative factor result is not explained by a broken coordinate map or mismatched simulator.

- J1: the six-bit coordinate map and inverse agree on every recorded symbol, and all four interface coordinates are zero at `t=0` as intended.
- J2: for every declared source, no physical cell outside the four touching rows departs from the alternating background after the first coarse update. Exterior departure does occur by the second update; the first witnesses occur at source index 66 for `n=6` and 130 for `n=7`.
- J8: an independent scalar coordinate implementation of the physical selector law agrees with the vectorized implementation on all replayed controls and canonical full-state conflicts. The exhaustive scalar J2 first-update control also passes on both rings.

The permanent workflow verifies the stored protocol/verifier hashes and regenerates the canonical JSON byte for byte.

## What the full-state conflicts show

At `R=0`, P15 already fails at `t=0`: the local center symbol alone omits ordinary longitudinal-neighbor information. That failure does not require a hidden vertical cause.

At `R=1`, the canonical primary conflict compares `(n=6, source=000001/000001, t=0, site=0)` with `(n=7, source=0010101/1111110, t=3, site=3)`. Their full retained three-symbol neighborhoods agree, but their next center symbols differ (`19` versus `23`). Independent physical replay finds differing cells outside rows `0..3` inside the next-step two-fine-tick causal patch.

At `R=2`, the primary conflict is sharper. The records

- `(n=6, source=010101/010101, t=1, site=0)`, and
- `(n=6, source=010101/111111, t=2, site=0)`

have the same full **five-symbol** local neighborhood but next center symbols `0` and `24`. Independent physical replay again finds differences outside rows `0..3` inside the next-step causal patch. The stress-horizon `R=2` conflict has the same hidden-cause property.

Thus increasing longitudinal context through radius two does not make this fixed four-row/six-bit state autonomous on the declared reachable family. By `R=1` and `R=2`, physically relevant information can lie outside the retained band even when the entire tested symbolic neighborhood matches.

## Relationship to the earlier interface-state result

Research019 showed that the obvious six-cell enlargement repairs only the first update on arbitrary local symbols, fails on reachable trajectories, and that one finite pulse encounter escapes every fixed-height physical band. The present result asks a different, more factor-theoretic question: perhaps the same six retained cells, re-coordinated symbolically and given longitudinal context, still suffice as a local autonomous state on the reachable adjacent-strip family.

Within the frozen radius-two budget, they do not.

The two results therefore reinforce each other without collapsing into the same claim. Raw vertical escape says a fixed physical band is not itself invariant for all relevant trajectories. The new census says the natural six-bit symbolic recoding of that band also fails to factor the declared dynamics locally through radius two, with explicit pooled conflicts and independent physical hidden-cause replays.

## What this does not establish

This is a bounded negative result, not a no-go theorem for interacting-strip state descriptions.

It does **not** rule out:

- larger longitudinal radii;
- finite or unbounded history-bearing state;
- a state variable that tracks a moving support or propagating front;
- different symbolic coordinates not reducible to the frozen interface subsets;
- nonlocal factors;
- special restricted source families;
- arbitrary-width interacting grids; or
- a recursive 2D-to-3D dimensional lift.

The protocol explicitly forbids introducing any of those as a post-hoc rescue inside this unit. They remain possible future questions only if separately motivated and frozen.

## Program interpretation

The useful conclusion is representation-specific:

> For the exhaustive declared `n=6,7` adjacent-strip reachable family and the frozen six-bit `(A,B,E0,E1,E2,E3)` interface representation, no retained interface subset admits an autonomous local factor at longitudinal radius at most two through the primary horizon; the full representation also fails on the longer stress horizon. At radii one and two, canonical full-state conflicts replay to causally relevant physical differences outside the retained four-row band.

This closes one natural finite-interface-state attempt negatively. It does not convert the interacting strips into evidence for intrinsic spatial dimension by itself; instead it identifies a concrete place where a seemingly sufficient local symbolic boundary state still erases distinctions needed by the next update.
