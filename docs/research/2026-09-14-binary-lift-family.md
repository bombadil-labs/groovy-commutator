# A four-reference binary lift family covers all 256 ECAs

Status: retrospective exhaustive first-floor census; independent Gate 2 review pending. Catalog status remains exploratory because the family was selected adaptively and evaluated before independent review.

Authored by: Codex (OpenAI), dimensional-lift local working session, 2026-09-14. Reviewed by: none.

## Question and answer

Can one small representation grammar give every ECA a faithful binary 2D realization without increasing the native radius beyond two? **Yes, within the tested four-field prepared family:** all 256 source rules have at least one recipe with a uniform unlabeled binary local update and local source recovery. Recipe selection depends on the source rule. This is not yet a universal G-preserving or indefinitely reusable lift.

Myk approved the Gate 1 exception. Evaluation preceded independent review; see the [retrospective methods and deviations](protocols/binary-lift-retrospective-record-20260914.md).

## Derivative, integration and projections

For source configuration S and ECA code r, define

\[
d_r(a,b,c)=\operatorname{bit}_{4a+2b+c}(r\mathbin{\mathrm{XOR}}204),\qquad
D_r(S)_i=d_r(S_{i-1},S_i,S_{i+1}),\qquad E_r(S)=S\oplus D_r(S).
\]

For a signed shift s in {-1,+1}, let (τ_s S)_i=S_(i+s). The four prepared fields are

\[
P_s(S)=S\oplus\tau_sS,\qquad D(S)=D_r(S),\qquad M(S)=m(S,D_r(S)),\qquad Q_i=q(S_{i+a},S_{i+b}).
\]

All products below are Boolean AND; addition of fields is XOR.

| Mask name | m(S,D) |
|---|---|
| birth | (1-S)D |
| death | SD |
| stay-one | S(1-D) |
| stay-zero | (1-S)(1-D) |

| Reference | Formula |
|---|---|
| symmetric left | S_(i-2) S_(i+1) |
| symmetric right | S_(i-1) S_(i+2) |
| directed left | S_(i-2) (1-S_(i+1)) |
| directed right | (1-S_(i-1)) S_(i+2) |

Each pair of references is closed under reflection. A recipe θ chooses s, m, Q and a cyclic row order π. Fixing P as the first row leaves six orders. If F=(P,D,M,Q), the encoding is

\[
L_{r,\theta}(S)_{i,j}=F_{\pi(j\bmod4)}(S)_i.
\]

The encoding prepares a period-four configuration. The native law receives only binary neighborhood values, with no row-phase label.

## Compiling a native law and decoder

Let N_2 denote the full 5×5 neighborhood. A native derivative table h must satisfy, at every row phase and every source word,

\[
h\!\left(N_2(L(S),i,j)\right)=L(S)_{i,j}\oplus L(E_rS)_{i,j}.
\]

Equal neighborhood keys must demand the same bit. A separate decoder table R must satisfy R(N_2(L(S),i,j))=S_i. When both tables are consistent, choose arbitrary values at their otherwise unspecified keys and integrate the derivative by XOR. The resulting native CA obeys

\[
E^{\uparrow}_{r,\theta}\circ L_{r,\theta}=L_{r,\theta}\circ E_r.
\]

This exact one-step identity makes the prepared image forward invariant and extends the evolution guarantee to every time step. The recipe generator returns an encoding, compatible native CA and decoder; it does not identify a unique off-image CA completion.

## Complete first-floor coverage

Each reference pair was tested on all 256 × 8 × 2 × 6 = 24,576 recipes, with all 2^11 source assignments in the exact dependency interval [-5,+5]. Identical old cases were reused; missing variants were tested without the obsolete three-row admission filter.

| Reference family | Faithful native + recovery | Also original G | Also centered G |
|---|---:|---:|---:|
| symmetric pair | 254 | 131 | 205 |
| directed pair | 254 | 110 | 193 |
| union of four formulas | **256** | **133** | **220** |

Counts are source-rule unions over recipes. Original and centered columns are separate diagnostics, not counts to add. The symmetric pair misses recovery for Rules 23/232; the directed pair misses faithful realization for Rules 77/178. The union repairs both pairs. Both censuses and their gates are closed under reflection.

The [canonical account](../../results/binary_lift_20260914.json) contains the exact rule sets. The [per-rule table](../../results/binary_lift_20260914/rule_coverage.csv) makes the selected path and gate statuses inspectable.

## What G preservation means here

\[
G_r(S)=D_r(E_rS)\oplus E_r(D_rS),\qquad
G_r^\circ(S)=G_r(S)\oplus E_r(0).
\]

For ECAs, E_r(0) is the uniform bit r mod 2. The prescribed P/D carrier is T_P(g)=g XOR τ_sg and T_D(g)=g. It is **not** the full nonlinear encoding L(g). G has no prescribed M/Q carrier in this experiment. Physical G evaluates the lifted rule on the changes of every encoded field, including ΔQ=Q(S) XOR Q(E_rS); Q is not held fixed during that probe.

The [obstruction note](2026-09-14-binary-lift-g-obstructions.md) gives the exact additional consistency condition and explains why faithful evolution does not imply it.

## Costs, controls and verification

Each physical cell has one bit; native locality is radius two on both axes. Preparation uses a radius-one source derivative and a distance-three reference pair whose offsets have magnitude at most two. There are four prepared fields per source site, repeated transversely. The independent information still comes only from the source line. No independent area information or nontriviality follows from faithfulness alone; the [intertwining control](2026-09-09-dimensional-intertwining.md) and [information-budget account](../knowledge/dimensional-information-budget.md) remain relevant.

Independent implementations within the author session checked 359 fresh symmetric representatives (1,795 gate decisions; 708,608 direct physical-G cells) and 319 directed representatives spanning all rules (1,914 decisions; 790,528 G cells), plus every directed repair recipe for 23/232 in its earlier dedicated check. These selected checks address implementation risks; they are not a second independent full 49,152-recipe census or an independent-agent review.

The [bundle guide](../../experiments/binary_lift_20260914/README.md) provides the preserved primary censuses, code, hashes and replay commands. The next question is whether this grammar can repeat with recovery and physical G; the [3D note](2026-09-14-binary-lift-recursion.md) records that completed test.
