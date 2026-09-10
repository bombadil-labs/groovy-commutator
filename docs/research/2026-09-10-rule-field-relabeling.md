# Relabel the state, the tables, and the transport

This is the [issue65](https://github.com/bombadil-labs/groovy-commutator/issues/65#issuecomment-5622838631) archival deliverable. The identities below are algebraic; the numerical checks retain their original exploratory provenance. The proposed rule-field lift remains unspecified.

## Frozen rule fields

Choose a fixed binary site mask c on a periodic ring. For each site i define an involution on its eight-bit table:

$$
\phi_i(r)(l,m,u)=r(l\oplus c_{i-1},m\oplus c_i,u\oplus c_{i+1})\oplus c_i.
$$

Use the standard table index 4l+2m+u. Set S'=S XOR c and R'_i=phi_i(R_i), and decode by XOR with c. Substituting the transformed neighborhood cancels each input mask, leaving

$$
F_{R'}(S\oplus c)=F_R(S)\oplus c.
$$

Applying the transformation twice restores the original state and tables. For frozen R and c the same identity holds at every time by induction. This is an exact relabeling of the represented family of models, with state, tables and decoder transformed together.

## Evolving tables: the schedule is part of the law

The repository's leftward live-gated transport reads **only old arrays**. In one synchronous step:

- S(t+1) is evaluated under R(t).
- R(t+1)_i is R(t)_{i-1} if S(t)_i=1, and R(t)_i otherwise.

For transformed data the gate reads S'(t)_i XOR c_i. When j=i-1 is copied into i, write

$$
\phi_i\bigl(\phi_j^{-1}(R'_j(t))\bigr)
$$

into the destination; otherwise retain R'_i(t). State evolution still uses old R'.

To prove the pair update commutes with relabeling, the state component is the identity above. The decoded gate equals the original gate. At a copying site, phi_j inverse recovers R_j(t), and phi_i expresses that table in the destination convention, giving exactly phi_i(R_i(t+1)). At a retaining site the equality is immediate. Induction gives equality of the decoded joint trajectory. Changing the gate to the new state or copying already updated rule entries would define a different schedule.

Plain copying of R'_j generally omits the destination conversion, and a literal S'_i=1 gate also differs. It need not fail on every input: c=0 is an immediate equality control.

## Preserved exploratory checks

The [original script](../../exploratory/issue65-relabeling/rule_field_relabeling.py) and [stdout](../../exploratory/issue65-relabeling/output.txt) are verbatim from [Claude's supplied comment](https://github.com/bombadil-labs/groovy-commutator/issues/65#issuecomment-5614879501). Run from the repository root:

```sh
python exploratory/issue65-relabeling/rule_field_relabeling.py
```

With NumPy's default RNG seeded at 1 and n=12, the first 200 draws check the frozen-field identity. The following 200 check transformed transport; both checks pass. Unchanged transport disagrees in all 200 cases of that particular second sample. That frequency is a sample result; the general identity rests on substitution.

The exhaustive n=4 union of relabeling orbits of all 256 uniform rule fields contains 1,974 distinct fields out of 256^4. Uniform Rule110 with c=(1,0,0,0) becomes (100,230,110,157). This count describes the specified group action on tables, with no further geometric structure supplied.

Codex reproduced the full stdout against repository commit f69b156ccc5fb7ff75ab4c2db95924dc87cc5d90, [as recorded in the issue](https://github.com/bombadil-labs/groovy-commutator/issues/65#issuecomment-5621679686). The archival replay uses the unchanged ca.py blob38ef0e7cf8c53063e389c4b63c0a1191c16de045 and nonuniform.py blob152d5818dc09f78df7971f2fe5575a281725cbf0 from main25dc5652c15f4dfbaef982dd75d54768a326aa64 and matches byte-for-byte. The dedicated CI replay checks complete stdout. Reproduction uses the same implementation; this is not a newly frozen numerical experiment or independent algorithmic audit.

The archived script's output retains its historical phrase “pure-gauge.” The agreed account uses “union of uniform-field relabeling orbits.” Gauge, flatness, connection and curvature interpretations were withdrawn in the issue discussion.

## Interpretation and remaining work

Table popcount is preserved by input permutation and is replaced by eight minus itself when the output symbol is complemented. A literal live/dead gate and quiescence statistic therefore depend on the chosen symbol convention. This observation does not explain the observed selection mechanism.

The example makes the [representation contract](../knowledge/representation-contract.md) concrete: preserving decoded evolution requires transforming the interpreter, including the gate and table transport. It does not construct a dimensional rule-field lift. Such a proposal still needs an alphabet, storage layout, decoder, ordered updates, admissible family and recovery criterion before any new protocol. A transverse field being constant is not by itself a proved if-and-only-if characterization for an unspecified constructor.
