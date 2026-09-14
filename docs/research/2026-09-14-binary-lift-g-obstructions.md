# A faithful encoding can lose G information in its field of changes

**Later same-day extension:** the [DT2](2026-09-14-binary-lift-dt2.md) and [row-complement](2026-09-14-binary-lift-complements.md) notes close first-floor centered G across the cumulative family. The original datasets and scoped counts below are retained; recursive closure remains open.

Status: retrospective finite-domain diagnosis and explicit obstruction certificates; independent Gate 2 review pending.

Authored by: Codex (OpenAI), dimensional-lift local working session, 2026-09-14. Reviewed by: none.

## Question and answer

Why do 36 ECAs have no first-floor G carrier in the [four-reference family](2026-09-14-binary-lift-family.md), despite faithful native dynamics and recovery? The main obstruction is that **equal derivative neighborhoods can require different G outputs**, even within the same known row role. Native recovery alone does not guarantee that the field of changes retains what the physical commutator needs.

Myk approved the Gate 1 exception; evaluation preceded independent review. See the [methods and deviations record](protocols/binary-lift-retrospective-record-20260914.md).

## An earlier global loss, and its repair

For Rules 23/232, every one of the 192 symmetric-Q recipes identifies a periodic source and its complement on a period-two or period-six orbit. Their complete P/D/M/Q encodings coincide, as do their next encoded configurations. All 768 phase-aware recovery checks fail. This is genuine source-information loss: no decoder radius or row label can recover what the unchanged complete encoding erased.

Directed mismatch Q breaks that obstruction and restores faithful first-floor coverage. This successful repair motivates inspecting the exact distinction lost by G probes. It does not imply that the G obstruction is the same global color-bit loss.

## Complete G diagnosis

The 36 first-floor holdouts contribute 6,912 saved recipes. Of these, 4,848 pass native evolution, 3,472 pass source recovery and **3,040 pass both**. Every original-G and both centered-G branch failure for these faithful recipes was reconstructed from its source dependency windows.

| First obstruction isolated | Faithful recipes |
|---|---:|
| Same-field derivative-probe ambiguity | **2,432** |
| Cross-field centered-probe ambiguity, with each field separately consistent | **248** |
| Internally consistent centered probes incompatible with native or zero-output constraints | **360** |

Categories use this precedence; a recipe may have additional obstructions. All 2,432 first-category recipes have a D-field contradiction, and 16 also have a P-field contradiction. For 28 rules, every faithful recipe already has a same-D-field contradiction. Rule 151 has a mixture of obstruction types.

The complete rule lists and counts are in the [canonical account](../../results/binary_lift_20260914.json). The [evidence bundle](../../experiments/binary_lift_20260914/README.md) preserves each original and newly isolated witness.

## One exact Rule 30 witness

Choose P_i=S_i XOR S_(i-1), M=S(1-D), Q_i=S_(i-2)S_(i+1), and row order P,D,M,Q.

| Source bits at coordinates -5 through +5 | D-probe neighborhood key | Required derivative output |
|---|---:|---:|
| `10101000001` | 2105544 | 1 |
| `10101101000` | 2105544 | 0 |

The key contains the exact 5×5 binary patch, packed at transverse offsets 0,1,2,-1,-2 and longitudinal offsets -2 through +2. Both probes are centered on the D row. The finite words are dependency windows, not assumptions that the source repeats with period 11. A deterministic rule cannot return both bits for this input. The centered zero choice flips both demands equally and cannot remove the contradiction.

## What a row-identity oracle changes

For diagnosis only, allow separate native rules and separate all-zero outputs for each row phase. The 2,432 same-field witnesses already survive that relaxation, so only the remaining 608 recipes need new tests.

The relaxation rescues 108 recipes for seven source rules: 171, 187, 235, 241, 243, 249 and 251. Rule 151 still has none. Therefore **29 of the 36 holdouts fail every faithful recipe even when row identity is supplied**. The seven rescues diagnose a role-distinction problem; they are not admitted uniform unlabeled binary lifts and do not raise coverage.

Here “faithful recipe” means one that already passed the original uniform native and recovery gates. The 3,872 initially unfaithful recipes were not retested under this relaxation. Consequently this does not rule out a different labeled architecture, or a recipe that becomes eligible only after labels are introduced.

## The consistency condition needed for recursion

Write Y_j=L(E_r^jS), ΔY=Y_0 XOR Y_1 and let h be the lifted local derivative table. Native evolution requires

\[
h\!\left(N_2(Y_0,c)\right)=(Y_0\oplus Y_1)_c.
\]

For mode ε=0 use original G; for ε=1 use centered G. Write g^0=G_r(S), g^1=G_r(S) XOR E_r(0), and z=h(0). The prescribed carriers are T_P(g)=g XOR τ_sg and T_D(g)=g. At a P/D cell c, physical commutator preservation requires

\[
h\!\left(N_2(\Delta Y,c)\right)
=(Y_0\oplus Y_2)_c\oplus T_c(g^\varepsilon)\oplus\varepsilon z.
\]

Equal probe inputs must therefore have equal demands, and those demands must agree with the native table wherever the input sets overlap. Centered mode also imposes h(0)=z. This finite consistency criterion characterizes extension of the constrained local table; otherwise unspecified outputs remain free.

A dimension-induction argument needs a representation invariant that preserves both **sufficiency of derivative neighborhoods** and **compatibility with native evolution**, together with recovery. Faithful native evolution alone does not supply that invariant.

## Dead ends and the next experiment

Row permutations, unused native outputs and the centered zero choice cannot repair certified same-field opposite demands. Simply complementing an existing Q cannot help those witnesses either:

\[
\Delta(1\oplus Q)=\Delta Q.
\]

This is a radius-two obstruction for the stated recipes. It is not an all-radius no-go or an impossibility result for other encodings. The earlier Rules 23/232 complete-image collision is the separately justified all-decoder-radius statement.

Next, test untried two-input Boolean Q functions at the existing offsets against the saved contradictory pairs. Reject an individual recipe immediately if its new temporal derivative leaves an opposite-demand pair unchanged. Surviving witness tests are necessary, not sufficient; native evolution, recovery and both G modes must still be checked. New Q choices must include all mask/sign/order variants rather than inheriting old first-order rejections. No such new-Q experiment is included in this PR.

## Verification

Scalar, cropped-window formulas reconstructed all 9,120 saved contradictory pairs, 2,696 newly isolated pairs and 3,000 failing branches of the 3,648-branch row-identity diagnostic. The primary diagnosis took 7.15 seconds and the targeted supplement 2.01 seconds. Complete collision logs are checked byte for byte by the local replay command. These are independent implementations within the author session, not an independent-agent Gate 2 review.

No coverage count changed: all 256 source rules still have faithful binary paths through 3D, and best-known 3D G coverage remains 206. Alphabet, native radius, period-four preparation and the restriction to nested P/D carriers remain as stated in the [recursion note](2026-09-14-binary-lift-recursion.md).
