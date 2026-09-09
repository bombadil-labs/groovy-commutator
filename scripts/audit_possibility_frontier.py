"""Independent audits for Research026 possibility-frontier results."""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from groovy.ca import rule_lut  # noqa:E402

N=12; STATES=np.arange(2**N,dtype=np.uint32); SELECTED=[30,54,90,106,110,184]

def state_map(rule:int)->np.ndarray:
    lut=rule_lut(rule);s=((STATES[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8)
    out=lut[4*np.roll(s,1,1)+2*s+np.roll(s,-1,1)]
    return (out.astype(np.uint64)*(1<<np.arange(N,dtype=np.uint64))).sum(1).astype(np.uint32)

def block_obs(b:int,h:int)->np.ndarray:
    bits=((STATES[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8);blocks=bits.reshape(len(STATES),N//b,b)
    codes=(blocks*(1<<np.arange(b,dtype=np.uint8))).sum(2);lut=np.array([(h>>i)&1 for i in range(2**b)],dtype=np.uint8);macro=lut[codes]
    return (macro.astype(np.uint64)*(1<<np.arange(N//b,dtype=np.uint64))).sum(1).astype(np.uint32)

def entropy(labels):
    _,c=np.unique(labels,return_counts=True);p=c/len(labels);return float(-(p*np.log2(p)).sum())

def parse(identifier,rule):
    e=state_map(rule)
    if identifier=="derivative":return e,STATES^e
    kind,h=identifier.split(":");h=int(h);b=2 if kind=="block2" else 3
    return (e[e] if b==2 else e[e[e]]),block_obs(b,h)

def direct(rule,identifier,hstar):
    step,obs=parse(identifier,rule);s=STATES.copy();words=[obs.copy()]
    for _ in range(hstar):s=step[s];words.append(obs[s])
    _,lab=np.unique(np.stack(words,axis=1),axis=0,return_inverse=True);_,y0=np.unique(obs,return_inverse=True)
    return entropy(lab)-entropy(y0)

def main():
    summary=json.loads((ROOT/"results"/"possibility_frontier_20260908_summary.json").read_text());rows=[]
    for rule in SELECTED:
        for key,val in summary["selected_curves"][str(rule)].items():
            got=direct(rule,val["observer"],int(val["hstar"]));ok=abs(got-float(val["future_repertoire_bits"]))<1e-9
            rows.append({"rule":rule,"selection":key,"observer":val["observer"],"expected_future_bits":val["future_repertoire_bits"],"direct_future_bits":got,"passes":ok})
            if not ok:raise AssertionError(rows[-1])
    checks=0
    for b,maxh,comp in ((2,7,15),(3,127,255)):
        mask=(1<<(N//b))-1
        for h in range(1,maxh+1):
            if not np.array_equal(block_obs(b,comp-h),block_obs(b,h)^mask):raise AssertionError((b,h))
            checks+=1
    result={"ok":all(r["passes"] for r in rows),"selected_direct_future_partition_checks":len(rows),"output_complement_relabel_checks":checks,"selected_checks":rows}
    (ROOT/"results"/"possibility_frontier_20260908_audit.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
if __name__=="__main__":main()
