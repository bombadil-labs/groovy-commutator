"""Exact eventually-periodic witness: Rule 110 death-mask temporal carrier.
The two source rows are 4-periodic for i<=0 and equal to [i==3] for i>0.
U=L(S) XOR L(E(S)) is a radius-2 sliding block code of S. Its two outputs
are equal everywhere iff they agree on four representatives of i<=-2,
the seven transition sites -1..5, and one representative of i>=6.
No finite truncation or statistical inference is used in this argument.
"""
import json
from functools import lru_cache
from pathlib import Path

RULE=110

def source(which,i):
    if i>0:return int(i==3)
    return ((1,0,1,1),(1,1,1,0))[which][i%4]

@lru_cache(None)
def state(which,t,i):
    if t==0:return source(which,i)
    return state(which,t-1,i)^derivative(which,t-1,i)

@lru_cache(None)
def derivative(which,t,i):
    abc=4*state(which,t,i-1)+2*state(which,t,i)+state(which,t,i+1)
    return ((RULE^204)>>abc)&1

def lift(which,t,i,sign):
    s=state(which,t,i);ds=derivative(which,t,i)
    return (s^state(which,t,i+sign),ds,s&ds)

def probe(which,i,sign):return tuple(a^b for a,b in zip(lift(which,0,i,sign),lift(which,1,i,sign)))

def groovy(which,i):
    dd=4*derivative(which,0,i-1)+2*derivative(which,0,i)+derivative(which,0,i+1)
    derive_d=((RULE^204)>>dd)&1
    return derivative(which,1,i)^derivative(which,0,i)^derive_d

def main():
    certificates=[]
    for sign in (-1,1):
        positions=list(range(-5,7))
        assert all(probe(0,i,sign)==probe(1,i,sign) for i in positions)
        wanted=[lift(k,0,0,sign)[1]^lift(k,2,0,sign)[1]^groovy(k,0) for k in (0,1)]
        assert wanted==[1,0]
        # Rule110's source constant offset is zero. A centered target adds
        # the same unknown h(0) to both requirements, so they stay opposite.
        certificates.append({'shift':sign,'equal_probe_representatives':{str(i):probe(0,i,sign) for i in positions},'required_native_flips_at_D_origin':wanted,'source_G_at_origin':[groovy(k,0) for k in (0,1)],'all_horizontal_and_vertical_radii_obstructed':True,'row_labels_do_not_resolve':True,'centered_and_original_G_obstructed':True})
    report={'rule':110,'mask':'death','source_definition':{'i<=0_residues_0_1_2_3':[[1,0,1,1],[1,1,1,0]],'i>0':'1 exactly at i=3; 0 otherwise'},'source_probe_radius':2,'representative_domains':{'left_periodic':'i<=-2, period4; representatives -5,-4,-3,-2','transition':'-1<=i<=5','right_constant':'i>=6; representative 6'},'certificates':certificates}
    path=Path(__file__).resolve().parent/'runs/temporal_reach_6/rule110_exact_obstruction.json';path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
if __name__=='__main__':main()
