# Every binary CA lifts: the affine-oriented jet lift theorem

Does every binary cellular automaton with finite memory admit an exact, locally
recoverable representation one dimension higher, and does that representation
lift again through every finite depth? Yes. The proof is GPT-5.6 Sol's
2026-09-16 proof state, imported verbatim into this repository as
[`docs/research/proofs/affine-oriented-lift-proof-state-20260917.md`](proofs/affine-oriented-lift-proof-state-20260917.md).
This note is Fable's acceptance record: what the theorem says, what an
independent reimplementation verifies on finite domains, what is accepted on
the argument alone, and what the theorem does not say. With it, the
dimensional-lift Program's existence question is closed.

Evidence: exact, with the scope of each claim stated below. Proof authored by
GPT-5.6 Sol (Myk's GPT session, 2026-09-14 to 2026-09-16). Verification and
integration by Claude/Fable 5.1, 2026-09-17. **Review status:** GPT lost
GitHub write access and no other collaborating agent was available; Myk
suspended the cross-model review gates on 2026-09-17 and authorized Fable to
integrate, self-review and merge. Author and verifier are different agents, so
the verification below is independent of authorship; the merge is not
independently gated, and retrospective review by another agent follows the
correction path.

## The theorem

Let `H` be a binary CA on `Z^d` with finite memory `M` (take `0 ∈ M`) and
choose a primitive direction `e`. Translation is `τ_v X(p) = X(p+v)`. The
affine-oriented six-field grammar encodes a parent state `X` along a new
period-six axis as

```
F0 = X ⊕ τ_{v+} X
F1 = 1 ⊕ X ⊕ τ_{v−} X
F2 = X ⊕ H(X)
F3 = X ⊕ H²(X)
F4 = 0
F5 = X
```

The *marked beam* is the image of every source state; its *phase saturation*
is the union of the six cyclic row rotations.

**Entry.** With `v+ = e`, `v− = −e`, there is a binary CA one dimension
higher whose local rule evolves the encoding exactly on the marked beam and
all its phase translates, and locally recovers `X` and the phase. A sufficient
inherited memory is `W = M + {−e, 0, e}`, with radius 3 on the new axis.

**Recursion.** Let `a_n` be the newest lifted axis. With `v+ = a_n + e`,
`v− = a_n − e`, the same grammar phase-synchronizes without using the parent
truth table, and a sufficient child memory is `{−3,…,3} × M_n`. So for every
finite depth `N` there are descendant CAs and beams with
`H_{n+1} ∘ L_n = L_n ∘ H_n` for `0 ≤ n < N`. For ECA roots the compact radii
are (3,2), (3,3,2), (3,3,3,2), …; entry widens the inherited memory once and
no later floor widens it again.

**Not claimed:** uniqueness or minimality of the operator; nonbinary alphabets;
an infinite-dimensional limit; any unique or preferred off-beam completion;
any property of ambient states off the beam; preservation of the descendant
rule's native single-track commutator.

The proof's logical structure is a rule-independent entry lemma (the six-row
syntax alone admits false phases for rotations 2, 3, 4; locality, finite
memory and translation equivariance of one deterministic rule exclude them)
plus a rule-free recursive lemma (in the affine gauge every wrong rotation has
a two-bit linear separator). The all-256 ECA census and the Life checks are
verifications, not premises.

## What Fable verified

`scripts/verify_affine_lift.py` implements the construction from the theorem
statement alone (no code from the GPT session was available) and writes
`results/affine_lift_20260917.json`. It runs in about ten minutes and is not
run in Actions; the fast integrity tier checks its hashes. Every section
passes.

| Section | Domain | What is checked | Count |
| --- | --- | --- | ---: |
| A | all 256 ECAs, every 9-bit source dependency word, every field row | the entry decoder finds exactly one admissible rotation and it is the true one; recovered `X` and native output are functions of the 7×5 window; output equals the lifted successor | 3,072 windows per rule |
| B1 | eight radius-two 1D rules (six random tables, two shifts), all 2^15 dependency words | same checks with `W = [−3, 3]` | 196,608 windows per rule |
| B2 | Conway's Life, `e` along one axis, `W` a 5×3 stencil | same checks; exhaustive on the 3×3 torus and 400 random 7×7 tori | 3,072 + 117,600 windows |
| C | the proof's syntactic witnesses | with the `F2`/`F3` dynamical checks off, the constant codewords admit a rotation of order two and the alternating codeword a rotation of order three; with them on, the false reading is admissible under none of the 256 rules | 3 witnesses × 256 rules |
| D | all 256 ECA roots at ring width 7, sixteen at width 8 | the D2 beam is lifted again with diagonal rails; the D3 window `{−3..3}² × {−2..2}` determines phase, parent cell and native output with no collision over all source words | 32,256 windows per rule |
| E | 7-ring, all 256 rules | `G°(X) = B_H(X, D_H X)`; all-pairs polarization vanishes exactly for the 16 affine rules and the graph restriction for those plus 4 and 200; the affine-jet residual is `(0,0,K_1,K_2,0,0)` with `K_1 = G`; the horizon cocycle for `t ≤ 3`; the signed-translation grading `G_{T(v,ε)} ≡ ε` | 128 states × 256 rules |

Section A is the theorem's ECA case on its complete local domain (the same 512
words the proof's own census used). Sections B1 and B2 are the part of the
domain that is new relative to the repository: parents that are not
elementary. Section D checks the recursion at the first floor where the
diagonal rails and the "no further widening" claim bite, in the affine gauge;
the repository's earlier census through 4D on rings 7 and 8 used the
historical recovery gauge and is a verified special case of the same statement.

Two details found while implementing, both consistent with the proof: the
proof's rotation `s` appears in the decoder as candidate `p = −s mod 6`, so
each constant witness admits one direction of rotation and its complement
codeword the other; and the syntactic witness `(X,Y,Z) = (0,0,1)` is not a
trajectory of any rule (it would need `H(0) = 0` and `H(0) = 1`), which is
exactly why the dynamical check is rule-free.

## What is accepted on the argument

The general entry lemma for arbitrary `H` (proof section 27) and the affine
recursive separators (section 5) are proofs, not enumerations; Fable read
them and finds them sound, and the finite sections above confirm every
instance they touch. Two of the proof's computations were not reproduced here
and are recorded as GPT's: the 512-random-radius-two control (Fable ran eight
rules exhaustively instead) and the section-37 first-floor completion
invariants (affine hull dimension 30, degree distributions, the 88-value
orbit fingerprint). Those numbers should be treated as reported, not verified,
until someone reruns them.

## What the theorem changes in the Program

- The dimensional lift's **existence and recursion are settled** for the whole
  binary finite-memory class. The Program's remaining question is what the
  lift makes visible, not whether it exists.
- The beam is a **rule beam**: the encoded image of every state of the source
  rule, on which the descendant is conjugate to the source
  (`H^↑|_B ≅ H`, and on the phase-saturated beam `≅ H × id_P`). A trajectory
  is a path through the beam, not the beam.
- The **completion freedom of native G** (the 2026-09-15 audit) has an exact
  explanation. Under any intertwining lift `F ∘ L = L ∘ H`, the finite
  differences obey `∂F_{L(X)}(∂L_X U) = ∂L_{H(X)}(∂H_X U)`: beam evolution
  fixes the transport of a displacement as a tangent vector. Native
  `G_F(LX) = ∂F_{LX}(D_F LX) ⊕ F(D_F LX)` adds the point evolution of the same
  displacement, whose input need not lie on the beam. Points and differences
  are different types; only the first is beam-determined.
- **Centered Groovy is polarization on the trajectory graph.** With
  `B_H(X,U) = H(X⊕U) ⊕ H(X) ⊕ H(U) ⊕ H(0)`, `G°_H(X) = B_H(X, D_H X)`. All-pairs
  polarization vanishes iff `H` is affine; the graph restriction also vanishes
  for rules 4 and 200 (`B_H(1,2) ≠ 0` for both on the 7-ring). This is the
  geometric account of established result 1's corrected converse.
- **Ancestral G transports without a completion.** The product lift `L×L`
  intertwines `H×H`, so `L(X)` and `L(D_H X)` are two states on the same
  descendant beam and `K_t(X) = D_H(H^t X) ⊕ H^t(D_H X)`, with `K_1 = G`, is
  locally recoverable at every depth. The affine jet exposes `K_1` and `K_2`
  as its two temporal residual rows, and the horizon commutators obey
  `K_{t+1} = G(H^t X) ⊕ ∂H_{H^t D_H X}(K_t)`, which unrolls to
  `⊕_j M^j c` exactly in the affine case. This is not the repository's
  "commutator history" `G(H^t X)`; the two are related by that cocycle.

## What it does not say, and prior art

The lift is **not unique**. A period-three necklace code (`001` for 0, `011`
for 1, phase read from the cyclic orbit) lifts any binary finite-memory CA
with memory `M × {−1,0,1}`, phase-free and recursively, and is simpler by the
broad criteria. Coset-induced CA (Capobianco; Ceccherini-Silberstein and
Coornaert) already give the trivial layered version of "every CA lifts one
dimension up, recursively", and self-synchronizing block presentations are
established (Cervelle, Formenti and Guillon; Guillon and Richard); Toffoli's
1977 reversible embedding and Smith's 1971 binary self-addressing macrocells
are the older relatives. The candidate contribution is the specific
presentation: binary, one affine orientation bit, no address tape, the added
axis carrying `X`, `HX`, `H²X` and two oriented spatial differences so that
Groovy, polarization and tangent structure become spatial coordinates, closed
under its own grammar. The strongest canonicity statement available is that
the orientation bit is unique among one-row markers in the frozen six-row
grammar, up to chirality. Call it *the affine-oriented jet lift*, never *the
lift*.

Nothing here is a statement about ambient states. A first-floor completion
forces only a partial table on the 35-bit neighborhood; every completion
agreeing on it carries the beam and can do anything else elsewhere, so the
ambient Wolfram class of a lifted rule is not determined by its root. A 1D
Class-IV root gives a Class-IV-like invariant subsystem by conjugacy and
nothing more.

## Open questions that stay in this Program

The typed Groovy bundle: whether the two-beam carrier compresses to one marked
beam plus a locally defined vector sector while staying completion-independent
(two beams suffice; one native cellwise `G` does not; the object in between is
undetermined). Classification of lifts under an explicit representation
contract, so that a canonicity claim could be made or refuted. Nonbinary
alphabets, which need a different grading. The Class-IV question leaves this
Program for the refinement Program opened the same day.

## Reproduction

```bash
python scripts/verify_affine_lift.py            # ~10 min, writes results/affine_lift_20260917.json
python scripts/check_result_integrity.py results/affine_lift_20260917.json
```

The verifier is pure NumPy and needs only the repository's `pyproject.toml`
dependency.
