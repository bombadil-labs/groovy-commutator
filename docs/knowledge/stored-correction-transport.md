# Stored programs execute the correction transport law

The two-word program (r,60) in the existing five-symbol, radius-nine interpreter computes F_r of the current row xor the datum in the positive transverse row. Both r and the XOR-transport table are physical program bits.

For corrections A_0=I xor F and A_(k+1)=A_k F xor F A_k, this realizes U'_k=F(U_k) xor U_(k+1). Preparing rows0..H gives exact A_k(F^t(S)) when k+t<=H. This is a finite-time guarantee and may be a lossy observation of the source.

A finite zero cap is physically stationary but can supply the wrong next correction. Rule255 with H=2 and an all-zero source has first errors in rows2,1,0 at ticks1,2,3. This is a failure of that cap, not a universal obstruction to finite closure.

The [note](../research/2026-09-10-stored-correction-transport.md) includes the local proof, 8,192 exhaustive physical local checks, full finite fields for all256 rules and all8 width-three source states, and the retained witness. Its separately frozen audit passes 51,202 assertions.

The source rule is homogeneous and held in this extension. Arbitrary program changes, semantic repair, and a physically represented local closure cap are not established.
