# A two-rail grammar closes recursively on exactly 64 ECA sources

The frozen selector construction retains all 256 ECA programs through two dimensional lifts. Its fixed spatial encoding intertwines the complete dynamics for exactly 64 sources: the even rules from 128 through 254. Every successful source then lifts through every higher dimension by the same proof.

This is an exact **routing-program control**. The inherited program is part of the local routing law, not mutable truth-table cells in the evolving configuration. It therefore establishes a useful weaker construction and leaves the original active spatial-program target open. It does not implement the ternary L/R/C roles.

The [protocol](2026-09-09-selector-two-lift-protocol.md) was committed at [344e674](https://github.com/bombadil-labs/groovy-commutator/commit/344e67434e735b948b3ff4aaa81cb24f25be8c44) before execution. The counts were algebraic predictions, not discoveries used to tune the construction. The grammar, encoding, and audit bounds were unchanged.

## One program constructor

For a binary local CA F in dimension d, define H = L_d(F) by

\[
b=F(X|_k)(x),\qquad
H(X)(x,k)=
\begin{cases}
X(x,k+1),&b=0,\\
X(x,k-1),&b=1.
\end{cases}
\]

Here X|_k is the central d-dimensional slice. The local program grammar starts with eight-bit ECA tables and adds one constructor:

\[
\mathcal G_1=\{\operatorname{ECA}(r):0\le r<256\},\qquad
\mathcal G_{d+1}=\{\operatorname{Rail}(p):p\in\mathcal G_d\}.
\]

At the first lift, the source truth-table terminal 0 becomes an instruction to read the positive new-axis neighbor; terminal 1 becomes an instruction to read the negative neighbor. At the second lift, the *result of that whole first program* controls the next pair of neighbors. The original program is not discarded or replaced by a fitted upper law.

For source f_r and inputs (l,c,r,n,s,u,v), the first two laws are simply

\[
h_r=(1-f_r(l,c,r))n+f_r(l,c,r)s,
\]

\[
k_r=(1-h_r(l,c,r,n,s))u+h_r(l,c,r,n,s)v.
\]

Products and sums here are Boolean selector formulas evaluated in the integers, with binary outputs. The address convention is q=4l+2c+r.

| Resource | Frozen value |
| --- | --- |
| Alphabet | Binary at every dimension |
| Spatial radius | One |
| Time ratio | One target tick per source tick |
| Effective input stencil in dimension d | At most 2d+1 sites |
| Program description | Eight source bits and d-1 identical Rail constructors |
| Extra internal registers, tags, clock phases | None |
| Source-dependent preparation radius | Zero |
| Prepared background | Two infinite opposite homogeneous half-spaces per lift |
| Decoder | Restriction to the central interface |

Unused Moore-neighborhood positions are ignored by definition. The compact grammar is the native representation; no expanded full-Moore truth table is needed.

## Program inheritance is injective

Set the new positive neighbor to 0 and the negative neighbor to 1. The lifted output is then exactly the output of F on its arbitrary central patch. Therefore

\[
L_d(F)=L_d(G)\quad\Longrightarrow\quad F=G.
\]

The same argument applies at every lift. For each ECA address q, choose its three input bits and set every added rail pair to (0,1). The output of every descendant recovers r_q. Flipping only r_q changes that output.

The audit verifies all eight interventions for every source at both levels, and independently counts 256 distinct first-lift and 256 distinct second-lift effective local tables. This proves causal inheritance in the declared routing syntax. It is **not** an intervention on a mutable lattice cell that stores a rule instruction: changing r changes the law.

## Exact overlap criterion

Encode any source field S as an interface between two backgrounds:

\[
E_d(S)(x,k)=
\begin{cases}
0,&k>0,\\
S(x),&k=0,\\
1,&k<0.
\end{cases}
\]

All target sites subsequently evolve under H. No background is clamped.

**Theorem.** For every binary local CA F,

\[
L_d(F)E_d=E_dF
\quad\Longleftrightarrow\quad
F(0^\infty)=0^\infty\ \text{and}\ F(1^\infty)=1^\infty.
\]

**Proof.** Write a=f(0,...,0) and b=f(1,...,1).

At k=0, the two candidate sites are 0 and 1. The output is f(S), so the data plane is correct for every rule.

At k>=2, both candidate sites are 0; at k<=-2, both are 1. These distant backgrounds always remain correct.

At k=1, the central slice is uniformly 0. The selector is a. If a=0, the site reads the outer zero background; if a=1, it reads S(x) at the data plane. Stability for every S therefore requires and is guaranteed by a=0.

At k=-1, the central slice is uniformly 1. The selector is b. If b=1, it reads the outer one background; if b=0, it reads S(x). Stability for every S therefore requires and is guaranteed by b=1.

These cases exhaust the lattice and use one consistent global assignment of every shared site. They prove sufficiency and give necessity witnesses. No independent-copy assumption about overlapping patches is used. ∎

In particular, if a=1, set S(x)=1: the positive adjacent background changes from 0 to 1. If b=0, set S(x)=0: the negative adjacent background changes from 1 to 0. These are one-tick failures of the whole encoding even though the data plane still computes the right first tick.

The four endpoint pairs (a,b) each contain 64 ECA rules. Only (0,1) passes. The passing list is precisely

    128,130,132,134,136,138,140,142,144,146,148,150,152,154,156,
    158,160,162,164,166,168,170,172,174,176,178,180,182,184,186,
    188,190,192,194,196,198,200,202,204,206,208,210,212,214,216,
    218,220,222,224,226,228,230,232,234,236,238,240,242,244,246,
    248,250,252,254.

The committed result also supplies a concrete local failure witness for every one of the other 192 rules. Failure is relative to this encoding; it is not an impossibility result for other encodings.

## Why the second lift introduces no further obstruction

For arbitrary F, both candidate neighbors in a uniform target configuration have the same value. Thus

\[
L_d(F)(0^\infty)=0^\infty,\qquad
L_d(F)(1^\infty)=1^\infty.
\]

The first descendant always belongs to the two-quiescent-state family, even when the original source does not. Applying the theorem again yields

\[
L_{d+1}(L_d(F))E_{d+1}=E_{d+1}L_d(F)
\]

for **every F**, on arbitrary source fields in dimension d+1. This is stronger than checking only fields in the image of E_d.

Let F_1=F and F_(j+1)=L_j(F_j). If F preserves both uniform configurations, induction gives

\[
F_D E_{D-1}\cdots E_1=E_{D-1}\cdots E_1F_1
\]

for every D>=2, and consequently for every time t. The encoding is injective because restriction recovers S, so this is conjugacy onto the invariant encoded subsystem, with a declared interface/background resource.

For an ECA that fails the first interface, its second interface still passes, but the composed original-to-3D encoding fails: E_2 is injective and cannot erase the first-interface discrepancy. Thus the full two-lift chains number 64, while syntactically valid program lineages and successful second interfaces each number 256.

This gives an injective dimensional lift on the family of binary local CAs preserving both uniform states, with no preferred terminal dimension. The conclusion follows from the theorem, not finite-grid extrapolation.

## Operational preservation

A source bit flip changes only the corresponding central site under E_d. Under E_2 E_1 it changes one site at the intersection of the interfaces. For an action a and its physical implementation a-tilde,

\[
E a=\widetilde a E.
\]

Combining this identity with F_target E = E F_source proves preservation of every finite word of source evolution and matched finite bit-flip actions for successful sources. The field audit includes a fixed four-action sequence. The general statement is algebraic, not limited to that sequence.

This says nothing about arbitrary damage to a background rail, self-repair, or changing the program by a finite action on the evolving configuration.

## Reproducible audit

Run from the repository root:

    node scripts/verify_selector_two_lift.mjs > /tmp/selector-two-lift.json
    diff -u results/selector_two_lift_20260909.json /tmp/selector-two-lift.json

The dependency-free audit compares recursive AST evaluation with direct scalar multiplexer formulas, then uses a separate whole-field implementation. All source families and bounds were frozen before execution.

| Audit | Cases or comparisons | Result |
| --- | ---: | --- |
| First local truth tables | 8,192 comparisons | All agree |
| Second local truth tables | 32,768 comparisons | All agree |
| Distinct lifted programs | 256 at each level | Every source retained |
| Instruction intervention witnesses | 4,096 across both levels | All retained |
| First interface, including adjacent backgrounds | 10,240 comparisons | Exactly 64 rules pass |
| Second interface, arbitrary effective source patches | 40,960 comparisons | All 256 descendants pass |
| First evolving interface, four ticks | 2,048 fields; 245,760 site comparisons | All agree |
| Second evolving interface, three ticks | 131,072 fields; 17,694,720 site comparisons | All agree |
| Composed evolving interfaces, four ticks | 2,048 fields; 1,679,360 site comparisons | All agree |
| Composed interfaces with matched actions | 2,048 fields; 1,679,360 site comparisons | All agree |

There are 21,349,890 successful assertions. The script records local failure witnesses as expected census results, rather than asserting that every first interface passes.

The first and composed field tests exhaust all 32 states on a width-five source ring for each successful rule. The arbitrary second-interface test exhausts all 512 states on a 3-by-3 source torus for every first descendant. Added directions are open, initialized with the declared half-spaces and shortened by one cell at each tick. This avoids an artificial seam between opposite backgrounds. The infinite-lattice claim rests on the local proof; finite fields audit the implementation and overlapping evolution.

## What this changes in the research program

The [correction-coordinate result](2026-09-09-correction-future-coordinates.md) showed that joint information closure can survive unbounded growth in named correction maps. This independent control now shows that recursive program syntax and an invariant source subsystem can coexist with a small exact boundary criterion.

Those two achievements are still weaker than active program spatialization. In this construction, the source bits reside in the local law, represented as geometric routing choices. Infinite homogeneous backgrounds are prepared around an interface; the preparation is local in S but unbounded in volume and not equivariant under translations of the new axis. These resources must remain visible.

The next useful fork is therefore sharper than another enlarged-state simulator:

1. Fix a representation in which source instructions are mutable spatial cells under a common interpreter.
2. Define which finite program edits count as valid operations and require their higher-dimensional images to act on those cells, rather than select a different ambient law.
3. Demand that the induced next program has that same representation at the second interface; verify overlap with a single global field.
4. Compare that candidate against the present routing control under its declared preparation and boundary budget.

No Class-IV label was used, no class-discrimination claim is made, and no dimension-three privilege follows. The original active-program conjecture remains open; the precise result here is a recursively closed, operationally exact routing control on a declared source family.
