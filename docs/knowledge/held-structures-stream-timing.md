# Held-structures healing predictions have a time-index error

`transverse_streams()` records the first successor’s two input columns, while
`gadget_heal()` initializes its state at time zero. The correct first input is
at time zero. The frozen control uses that correct ordering; the measurement
path does not. The exact source-level mismatch invalidates P4a/P4c/P4d.

The [completion record](../research/2026-09-21-held-structures-account.md)
links a bounded diagnostic: 3,916 stored driven-prediction mismatches in 38,016
K-arm trials, plus three selected witnesses whose driven predictions become
correct with pre-step inputs. This is an exact diagnosis on those bytes and
witnesses, not a corrected full census, independent replication, or new
aggregate predictive-performance claim. The original evidence is preserved.
