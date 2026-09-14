"""Exact Rule110 witness analysis for added local reference fields."""
import json
from pathlib import Path
from prove_110_temporal_obstruction import state

def word(k,t,i,r):return tuple(state(k,t,j) for j in range(i-r,i+r+1))
def q(k,t,i,a,b):return state(k,t,i+a)&state(k,t,i+b)
def dq(k,i,a,b):return q(k,0,i,a,b)^q(k,1,i,a,b)

def main():
    representatives=list(range(-5,7))
    for i in representatives:
        assert sorted([word(0,0,i,1),word(0,1,i,1)])==sorted([word(1,0,i,1),word(1,1,i,1)])
    # Local source/evolved-source word pairs have dependency radius two.
    # Period4 for i<=-2, constant for i>=6: these representatives prove
    # equality at every position, for all 256 three-input Boolean q tables.
    pairs={}
    for a,b in [(-2,1),(-1,2),(-2,2)]:
        values={str(i):[dq(k,i,a,b) for k in (0,1)] for i in range(-6,8)}
        differing=[int(i) for i,v in values.items() if v[0]!=v[1]]
        pairs[f'{a},{b}']={'different_reference_derivative_sites':differing,'values':values}
        for k in (0,1):
            for i in range(-6,8):
                x=state(k,0,i+a);y=state(k,0,i+b)
                dx=x^state(k,1,i+a);dy=y^state(k,1,i+b)
                assert dq(k,i,a,b)==((x&dy)^(y&dx)^(dx&dy))
    out={'rule':110,'old_death_mask_collision':'prove_110_temporal_obstruction.py','all_256_radius_one_reference_functions_have_identical_entire_derivatives':True,'proof':'unordered pairs of local source/evolved-source words agree; XOR of q applied to the pair is therefore identical','arbitrarily_many_such_broadcast_reference_channels_still_do_not_resolve_this_witness':True,'finite_representatives':representatives,'pairs':pairs,'product_rule':'D(ab)=a Db XOR b Da XOR Da Db'}
    path=Path(__file__).resolve().parent/'runs/reference_pairs_2/reference_witness.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='pairs'}));print(json.dumps({k:v['different_reference_derivative_sites'] for k,v in pairs.items()}))
if __name__=='__main__':main()
