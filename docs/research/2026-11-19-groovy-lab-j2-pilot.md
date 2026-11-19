# Rules 18 and 126 can forget bits and still update exactly

**Status:** exact, scoped; independent assistant reproduction, not external peer review. The [frozen pilot protocol](protocols/groovy-lab-j2-pilot-20261119.md) tests a conjectured case described by the [October integration](https://github.com/bombadil-labs/groovy-commutator/blob/4883bd96975a45dec29274630f3b134e309ed3d6/docs/research/2026-10-07-jet-full-line-autonomy.md). It is not a new prediction. The result adds explicit local erasure guards and positive lower bounds for the unrestricted source.

On the full binary line, Rules 18 and 126 both induce a radius-three update on the admissible image of the depth-two Groovy jet `J2=(G,Q)`. Radius three is minimal. For fair IID input, the jet forgets at least **1/8 bit per site** for Rule 18 and **1/24 bit per site** for Rule 126, even conditioning on the entire jet. This establishes predictive sufficiency without reconstruction. It does not give exact loss rates, classify all hidden fibers, or establish a correspondence with Class IV.

## A finite certificate for the full line

Let `H` be one synchronous ECA step, `A0=I xor H`, and `A(k+1)=Ak∘H xor H∘Ak`, without centering. `G=A1` has source radius at most two, `Q=A2` at most three, and the next observed pair at the origin has source radius at most four. A current radius-three jet window depends on 13 consecutive source bits. Evaluating all 8,192 source words therefore tests every possible current window and next center on the full line, including contexts that need not occur on small rings. The same local table applies at every site.

| ECA | radius 1: windows/conflicts | radius 2 | radius 3 |
| --- | ---: | ---: | ---: |
| 18 | 33/8 | 135/6 | 448/0 |
| 126 | 25/1 | 82/4 | 258/0 |
| 90 | 1/0 | 1/0 | 1/0 |

A conflict is a current observed window attained by source words with distinct next center pairs. The tuple implementation compares the central `A3`: by the recurrence the next `G` is already determined at radius one and the next `Q` equals `A3 xor H(Q)`. The bit-plane referee separately checks the actual next pair. Radius-two conflicts exclude radius two and smaller; the rule learned at radius three is only asserted on the jet image.

## Which individual bits vanish?

Exhaust all 4,096 contexts for a center flip. Only centers up to distance three can see that flip, so matching the seven-site jet window is necessary and sufficient for equality at *every* site under any common exterior.

- **Rule 18:** exactly 1,024 matches. The single-bit flip is invisible iff the immediate neighbors are both 1.
- **Rule 126:** exactly 512 matches. The four flanking bits at offsets `(-2,-1,+1,+2)` must be `0101` or `1010`.
- **Rule 90:** all 4,096 match because the entire jet vanishes for this additive rule.

The two nonlinear guards make the source trajectories coalesce in one step. For Rule 18, the marked bit is blocked by the two ones, and those neighbors themselves output zero. For Rule 126, every triple affected by the flip contains two unequal fixed bits. Each guard site outputs one because its update also sees a fixed unequal pair. Thus the guards remain true after applying `D=A0` (Rule 18's two bits stay put; Rule 126's four are complemented). Consequently both `H(x)=H(x')` and `H(D(x))=H(D(x'))` hold. The recurrence gives equality of `G`, then of `Q`; in fact the same induction gives equality at every higher jet order *for these pairs*. Enumeration proves guard necessity for single-bit J2 collisions, not for multibit collisions or coalescence generally.

For fair IID source, choose possible flip centers spaced by two (Rule 18) or three (Rule 126). Reveal all other source bits, including those outside a finite target block. The revealed bits fix guard eligibility. Every guarded center can now be flipped, independently of the values at all other candidate centers, while keeping the entire jet fixed. Given the revealed and observed fields, eligible bits are still independent fair bits. The expected eligible fraction is `(1/2)(1/4)=1/8` or `(1/3)(1/8)=1/24`, up to block-end terms. Dividing conditional block entropy by block size proves the lower bounds. Equivalently these lower-bound `1-h(J2)`, since the source boundary needed to evaluate a finite output block contributes only a bounded number of bits.

## What the Rule 90 comparison does and does not explain

The unrestricted Rule 90 jet is identically zero by additivity, unlike the two nonlinear jets. [Rupe and Crutchfield §V.3.1](https://arxiv.org/html/1812.11597#S5.SS3.SSS1) describe the Rule 18 alternating-zero invariant domain on which its evolution agrees with Rule 90. The two Rule 18 words `0000010100011` and `0000011100011` differ only at the center and end in the same `11`, so no extension places either in that domain. Even on that domain, equality of evolution need not transport through `D`, whose output can leave the domain. [Jen's additive reduction](https://doi.org/10.1088/0951-7715/4/2/004) is relevant context, not a theorem about this observable on the unrestricted full line. These checks do not rule out a more elaborate domain-wall description.

## Replay and review

Run `python docs/research/reproducers/groovy_lab_j2_pilot_20261119.py` and `python docs/research/reproducers/groovy_lab_j2_referee_20261119.py`. Both only use the Python standard library. The independent assistant referee derived the result before comparing against the tuple certificate, then verified the guard table in its bit-plane implementation. Evidence: tuple verifier commit `759bf7e49146ac9f8d5140dae4a2b54740771211`; referee verifier commit `9d98dd5edf29693cd3ad1b0c8b79c9425e4c56ad`. The sharp radius and scope are certificate results, not inference from a sample. Proved exact guards and loss floors close this bounded audit; no new science unit is implied.
