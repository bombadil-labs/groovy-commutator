# Adjacent strips interact but usually leave their code

For directly adjacent aligned strips, the composition residual

$$
C_0=F^2V_0(a,b)\oplus V_0(\phi_{90}(a),\phi_{90}(b))
$$

is nonzero on 47 of 64 local input patterns. It is confined to the two
touching physical rows and contains only mixed monomials involving both
logical inputs, with maximum Boolean degree five. Two physical cells in
each strip depend on the other strip's input.

All 17 locally valid outputs equal the independent Rule-90 outputs. Since
the other 47 leave the code, no total coupled logical update exists in
this representation at cadence two. This does not exclude another encoding,
additional interface state, or another cadence.

A known input can also cancel its intermediate interaction: both logical
rows identically one interact at the first fine tick but become the zero
logical pair at tick two with zero composition residual. This is a specific
input result, not general closure. See the
[full truth tables and formulas](../research/2026-09-08-coupled-strips.md).
