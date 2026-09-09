"""Fresh n=18 validation for Research026 possibility-frontier ordering."""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"src"))
from groovy.ca import rule_lut  # noqa:E402
N=18;STATES=np.arange(2**N,dtype=np.uint32)
CASES={30:(("block2",3),("block3",1)),54:(("block2",3),("block3",1)),90:(("block2",7),("block3",30)),106:(("block2",6),("block3",127)),110:(("block2",3),("block3",64)),184:(("block2",3),("block2",4))}
def state_map(rule):
 s=((STATES[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8);lut=rule_lut(rule);out=lut[4*np.roll(s,1,1)+2*s+np.roll(s,-1,1)]
 return (out.astype(np.uint64)*(1<<np.arange(N,dtype=np.uint64))).sum(1).astype(np.uint32)
def observation(b,h):
 bits=((STATES[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8);blocks=bits.reshape(len(STATES),N//b,b);codes=(blocks*(1<<np.arange(b,dtype=np.uint8))).sum(2)
 lut=np.array([(h>>i)&1 for i in range(1<<b)],dtype=np.uint8);macro=lut[codes];return (macro.astype(np.uint64)*(1<<np.arange(N//b,dtype=np.uint64))).sum(1).astype(np.uint32)
def entropy(labels):
 c=np.bincount(labels.astype(np.int64)).astype(float);c=c[c>0];p=c/c.sum();return float(-(p*np.log2(p)).sum())
def profile(step,obs,bits):
 _,labels=np.unique(obs,return_inverse=True);labels=labels.astype(np.int32);classes=int(labels.max())+1;h0=entropy(labels);s=STATES.copy()
 for t in range(1,258):
  s=step[s];target=obs[s];code=(labels.astype(np.uint64)<<bits)|target.astype(np.uint64);unique,inverse=np.unique(code,return_inverse=True)
  if len(unique)==classes:
   hp=entropy(labels);L=N-h0;V=hp-h0;return {"forgotten_bits":L,"future_repertoire_bits":V,"shielded_bits":N-hp,"possibility_efficiency":V/L,"hstar":t-1,"closed":abs(V)<1e-12}
  labels=inverse.astype(np.int32);classes=len(unique)
 raise RuntimeError("partition did not stabilize")
def main():
 rows=[]
 for rule,(minimum,maximum) in CASES.items():
  e=state_map(rule);step2=e[e];step3=e[e[e]]
  for selection,(kind,h) in (("minimum",minimum),("maximum",maximum)):
   b=2 if kind=="block2" else 3;rows.append({"rule":rule,"selection":selection,"observer":f"{kind}:{h}",**profile(step2 if b==2 else step3,observation(b,h),N//b)})
 checks=[]
 for rule in CASES:
  x=[r for r in rows if r["rule"]==rule];mn=next(r for r in x if r["selection"]=="minimum");mx=next(r for r in x if r["selection"]=="maximum")
  checks.append({"rule":rule,"minimum_observer":mn["observer"],"maximum_observer":mx["observer"],"minimum_future":mn["future_repertoire_bits"],"maximum_future":mx["future_repertoire_bits"],"future_order_pass":mx["future_repertoire_bits"]>mn["future_repertoire_bits"]+1e-10,"forgetting_order_pass":mn["forgotten_bits"]<mx["forgotten_bits"]-1e-10,"both_nonclosed":not mn["closed"] and not mx["closed"]})
 result={"ok":all(x["future_order_pass"] and x["forgetting_order_pass"] and x["both_nonclosed"] for x in checks),"ring_width":N,"rows":rows,"checks":checks}
 (ROOT/"results"/"possibility_frontier_n18_fresh_20260908.json").write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
 if not result["ok"]:raise SystemExit(1)
if __name__=="__main__":main()
