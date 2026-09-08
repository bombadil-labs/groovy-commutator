"""Research024 exact witness: a Rule-106 defect hidden from block-2 parity."""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src")); sys.path.insert(0,str(ROOT/"scripts"))
from experiment_history_lift_closure import block2_parity_map, compress, state_map  # noqa: E402

RULE,N=106,20


def bits(x:int)->list[int]: return [i for i in range(N) if (x>>i)&1]


def find(step:np.ndarray,obs:np.ndarray)->tuple[int,tuple[int,int]]:
    states=np.arange(len(step),dtype=np.uint32); s=states.copy(); labels=compress(obs); cc=int(labels.max())+1; witness=None
    for h in range(52):
        s=step[s]; target=obs[s]; pair=(labels.astype(np.uint64)<<(N//2))|target.astype(np.uint64); up,inv=np.unique(pair,return_inverse=True)
        if h==50:
            order=np.argsort(labels,kind="stable"); ls=labels[order]; ts=target[order]
            starts=np.r_[0,np.flatnonzero(np.diff(ls))+1]; stops=np.r_[starts[1:],len(order)]
            for a,b in zip(starts,stops):
                vals=np.unique(ts[a:b])
                if len(vals)>1:
                    inds=order[a:b]; i0=inds[np.flatnonzero(ts[a:b]==vals[0])[0]]; i1=inds[np.flatnonzero(ts[a:b]==vals[1])[0]]; witness=(int(i0),int(i1)); break
        if len(up)==cc: return h,witness  # type: ignore[return-value]
        labels=inv.astype(np.uint32); cc=int(labels.max())+1
    raise AssertionError("no closure through h=51")


def main()->None:
    e=state_map(RULE,N); step=e[e]; obs=block2_parity_map(N); hstar,(a,b)=find(step,obs)
    assert hstar==51 and {a,b}=={25,26} and bits(a^b)==[0,1]
    sa,sb=a,b; trace=[]
    for t in range(52):
        ya,yb=int(obs[sa]),int(obs[sb]); dx=int(sa^sb); sites=bits(dx)
        trace.append({"t":t,"observations_equal":ya==yb,"difference_sites":sites,"difference_mass":dx.bit_count()})
        if t<=50:
            assert ya==yb and dx.bit_count()==2
            assert sites==sorted([(-2*t)%N,(-2*t+1)%N])
        if t<51: sa,sb=int(step[sa]),int(step[sb])
    assert not trace[51]["observations_equal"] and trace[51]["difference_mass"]==3
    result={"rule":RULE,"ring_width":N,"cadence":2,"observer":"block2_XOR","hstar":hstar,"witness_microstates":sorted([a,b]),"witness_supports":[bits(x) for x in sorted([a,b])],"initial_difference_sites":[0,1],"same_observation_through_t":50,"first_split_t":51,"mechanism":"difference support is exactly {(-2t) mod 20, (-2t+1) mod 20} through t=50, then changes shape and becomes visible at t=51","trace":trace}
    out=ROOT/"results"/"observer_hidden_defect_rule106_n20_20260908.json"; out.write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps({k:v for k,v in result.items() if k!="trace"},indent=2))


if __name__=="__main__": main()
