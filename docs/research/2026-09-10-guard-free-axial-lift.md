# A guard-free dimensional tower: compatibility and axis order

Can the same elementary cellular automaton be applied along every spatial axis, with no correction rows or guard roles, while preserving its lower-dimensional evolution? **Yes for exactly 66 of the 256 source rules under literal replication.** The same 66 pass every adjacent dimensional interface. Exactly 24 rules are independent of axis order in every dimension; 14 satisfy both requirements.

These are results for one fixed constructor and encoding. They establish a binary dimensional family on the full ambient lattice, not a uniquely selected extension, self-assembly, or an intrinsic minimum dimension. Rule32 fails this constructor; its earlier guarded correction closure remains a separate valid result.

## Frozen construction and evidence

The [protocol](protocols/guard-free-axial-lift-20260910.md) was committed at `c5c380ecd80e53ff7ac1e8c64edcd267a8d61cd4`. The [standalone verifier](../../scripts/verify_guard_free_axial_lift.py) was committed at `3e694a1f1caca9c0e2c6f54db34de7a8380b159f` before evaluation. No implementation corrections or protocol deviations were needed. The protocol retains its original pre-execution status as a historical record; this note reports its completion.

Let $F_{r,i}$ apply ECA word $r$ along axis $i$, independently on each parallel line. Freeze

$$
G_{r,d}=F_{r,d}\circ\cdots\circ F_{r,1}.
$$

The last axis acts last. This is a binary CA on every configuration of $\mathbb Z^d$, with Moore radius at most one. There are no guards, reserved rows, program species, or missing-cell boundaries. The native description retains $r$, $d$, and the axis order. The source word is part of the law, rather than mutable spatial program data.

The embedding $R_d$ copies a field unchanged along the new axis. It is injective and preserves all source information, but supplies an infinite replication constraint. A local source edit changes an entire target line. An $n^{d+1}$ target box in this image contains only $n^d$ freely chosen source bits, so this embedding supplies zero information per target volume in the large-box limit.

The [canonical JSON](../../results/guard_free_axial_lift_20260910.json) saves every rule's mismatch counts and first witnesses, exact successful lists, all 512 axis-order disagreement bits per rule, and independent checksums. Reproduce it with:

```bash
python scripts/verify_guard_free_axial_lift.py > /tmp/guard-free-axial-lift.json
diff -u results/guard_free_axial_lift_20260910.json /tmp/guard-free-axial-lift.json
```

## Exact census

| Literal replication at every interface | Axis order independent in every dimension | Rules |
| --- | --- | ---: |
| Yes | Yes | 14 |
| Yes | No | 52 |
| No | Yes | 10 |
| No | No | 180 |

The compatible set is **0, 255, and every even rule from 128 through 254**. The first and second interfaces each accept exactly this set, with 190 failures retained at each interface. The second test covers arbitrary two-dimensional source fields, not just fields already copied from one dimension.

The 24 rules independent of axis order are:

```text
0,15,51,60,85,90,102,105,128,136,150,153,
160,165,170,192,195,204,238,240,250,252,254,255
```

They comprise all 16 affine ternary Boolean functions and eight additional AND/OR functions. The 14 passing both requirements have the following forms, with $l,c,r$ the left, center, and right inputs:

| Form | ECA words |
| --- | --- |
| Constant zero or one | 0, 255 |
| Copy one input | 170, 204, 240 |
| $l\oplus c\oplus r$ | 150 |
| AND of two or three inputs | 128, 136, 160, 192 |
| OR of two or three inputs | 238, 250, 252, 254 |

The first two rows include degenerate examples. Passing a commuting identity alone is not evidence of richer spatial behavior. Nevertheless, the full ambient laws of Rule128, Rule150, and Rule254 respectively compute AND, parity, and OR over the whole $3^d$ block. Every site in that block is essential to their local truth function, so these examples really use the added axes. This dependency statement does not establish a minimum dimension under arbitrary encodings.

## Why the compatibility classification continues forever

Define the uniform response $u_r(b)=f_r(b,b,b)$. All old-axis passes preserve constancy along the new axis, and the last pass therefore gives the identity

$$
G_{r,d+1}R_d=R_d\,u_r\,G_{r,d},
$$

where $u_r$ acts pointwise. Thus compatibility asks whether $u_r$ fixes every attainable output bit of $G_{r,d}$.

If $f_r$ is nonconstant, both output bits are attainable at every dimension. To prove this, its local composite is a tree: the outer application of $f_r$ reads three independently assignable lower-dimensional slabs. By induction, each child can produce either bit, so the parent can produce either bit too. This is a statement about the **one-site output range**, not surjectivity of the global configuration map.

Consequently, for every nonconstant $r$ and every $d\geq1$, the interface holds if and only if

$$
f_r(0,0,0)=0,\qquad f_r(1,1,1)=1.
$$

These two prescribed truth bits leave 64 ECA words. Constants0 and255 also pass, since their single attainable output is fixed. No other source fails an early interface and starts passing at a later one under this constructor.

For each successful rule, induction gives the all-time identity

$$
G_{r,d+1}^{\,t}R_d=R_dG_{r,d}^{\,t}
$$

for every configuration and nonnegative integer $t$. Composed embeddings preserve whole trajectories, including their distinctions and any source orbit period. No factor of 20 or dimension-dependent change of macro time is introduced.

## Why the axis test also has an all-dimensional consequence

The two possible orders on a 3-by-3 patch compare $f_r$ applied to the three row results against $f_r$ applied to the three column results. Exhausting all 512 patches is an exact test of $F_{r,1}F_{r,2}=F_{r,2}F_{r,1}$ on the unrestricted plane.

For any two axes in a higher-dimensional lattice, hold the other coordinates fixed. The same two-dimensional equality proves that the corresponding axial operators commute. Adjacent transpositions then reorder every finite sequence of axes, establishing axis-permutation equivariance for all 24 passing rules in every dimension. The other 232 fail already in dimension two; no claim about unrelated constructors follows.

Affine controls also have a direct proof. Write an axial affine map as $F_i(X)=L_iX\oplus e$, where each $L_i$ is the same linear combination of shifts along its own axis. Distinct-axis shifts commute. If $s$ is the XOR of the three coefficients, both compositions have constant term $se\oplus e$, hence $F_iF_j=F_jF_i$.

Axis permutations are not reflections: a copy-left rule passes this test without becoming invariant under reversal of one axis. We make no full rotational or reflection classification here. The enumeration and proof are scoped results, without a novelty claim or a classification of general multidimensional CA.

## Failures retained

Rule32 sends the source triple101 to1, then sends its uniform copy111 to0 on the next axis. Its first interface therefore fails immediately. There is one failing source triple, seven failing second-interface patches, and ten axis-order disagreements. Its first axis-order witness has rows111,000,101: axis0-then-axis1 gives0, while the reverse gives1.

Rule90 illustrates the separation between the tests. Its axial operators commute, but its uniform response sends both bits to0, so replication loses the nonzero source output. Rule232 gives the opposite separation: it preserves replication, but disagrees on 72 axis-order patches. The first has rows101,110,000, giving1 versus0.

These failures concern the frozen law, code, and cadence. The earlier [Rule32 cap](2026-09-10-rule32-physical-cap.md) uses a different state representation and remains valid. No code change or corrective pass was introduced to rescue the present failures.

## Independent audits and costs

The primary evaluator composes integer truth tables. A separate evaluator parses Boolean truth words into tuple-keyed functions and shrinks coordinate arrays along named axes. It checks all 2,048 first-interface triples, all 131,072 second-interface patches using full replicated 3-by-3-by-3 arrays, and all 131,072 axis-order patches. The two streams agree on all 397,312 output bytes; their SHA-256 is `36e5030ac1eb364c0737e4656e547eca6e01b41bfa4a7297b334807989000444`.

Finite controls compare actual periodic lattice passes against a separate recursive local truth-function evaluation:

| Periodic shape | All initial states per rule | Macro updates across all 256 rules | Compared output cells |
| --- | ---: | ---: | ---: |
| Width4 | 16 | 4,096 | 16,384 |
| 2 by 2 | 16 | 4,096 | 16,384 |
| 2 by 2 by 2 | 256 | 65,536 | 524,288 |
| Total | — | 73,728 | 557,056 |

Identity204, constants0/255, and all 16 affine commutation controls pass. Small periodic controls do not replace the unrestricted causal-window proofs.

One compiled CA update is one macro tick. Evaluating it as lattice sweeps takes $d$ sequential parallel passes; a naive single-output tree needs $(3^d-1)/2$ ECA lookups on $3^d$ source sites. The alphabet and Moore-radius bound stay fixed; the processing does not.

## What this changes, and the next test

Removing guard machinery does not prevent exact dimensional compatibility. It does remove the earlier promise to accept every source rule and to carry mutable spatial program fields. Replication, the source word, and usually an axis order remain supplied choices. The 14 rules passing both tests have elementary algebraic forms; the 52 other compatible rules retain ordered axes. Neither population is selected by Class-IV behavior.

The beam is now a directly expressible coordinate constraint. For a two-dimensional field define its transverse difference

$$
T(X)(x,y)=X(x,y)\oplus X(x,y+1).
$$

Then $T(X)=0$ exactly when the field is copied unchanged along the second axis. This suggests asking whether departures from the beam have an autonomous law, or whether their evolution needs the underlying field and further corrections.

The [next frozen protocol](protocols/transverse-difference-closure-20260910.md) tests that question for all 66 compatible sources with fixed local budgets and independent finite controls. It has not been executed. This connects the guard-free construction back to derivatives and closure without adding corrective state in advance. Minimum dimensional ancestry, endogenous law changes, and natural selection of a beam remain open.
