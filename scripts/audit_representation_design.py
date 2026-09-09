"""Independent selected-case audit for Research027 fixed-target calculations."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"src"))
from groovy.ca import rule_lut  # noqa:E402
N=12;RULE=106;PARITY=(0,1,1,0);EVEN=(0,1,1,2);ODD=(0,1,2,0);TOL=1e-9
STATES=np.arange(2**N,dtype=np.uint32)
def stepmap(rule):
 lut=rule_lut(rule);b=((STATES[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8);o=lut[4*np.roll(b,1,1)+2*b+np.roll(b,-1,1)];w=1<<np.arange(N,dtype=np.uint64);e=(o.astype(np.uint64)*w).sum(1).astype(np.uint32);return e[e]
def obs(p):
 b=((STATES[:,None]>>np.arange(N,dtype=np.uint32))&1).astype(np.uint8);c=b.reshape(len(STATES),N//2,2);c=c[:,:,0]+2*c[:,:,1];lut=np.asarray(p,dtype=np.uint8);m=lut[c];base=len(set(p));w=np.asarray([base**i for i in range(N//2)],dtype=np.uint64);return (m.astype(np.uint64)*w).sum(1).astype(np.uint32)
def H_rows(a):
 _,c=np.unique(a,axis=0,return_counts=True);p=c/c.sum();return float(-(p*np.log2(p)).sum())
def direct(zobs,tobs,step,horizon):
 s=STATES.copy();ys=[]
 for _ in range(horizon+1):ys.append(tobs[s]);s=step[s]
 word=np.stack(ys,axis=1);z=zobs[:,None];joint=np.concatenate([z,word],axis=1)
 W=H_rows(joint)-H_rows(z)
 final_unique=len(np.unique(joint,axis=0));tail=0 if W<=TOL else None
 for t in range(1,horizon+1):
  cur=np.concatenate([z,np.stack(ys[1:t+1],axis=1)],axis=1)
  if len(np.unique(cur,axis=0))==final_unique:tail=t;break
 if tail is None:raise AssertionError("audit tail unresolved")
 return {"W":W,"tail":tail}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--summary",type=Path,required=True);ap.add_argument("--output",type=Path,required=True);args=ap.parse_args();summary=json.loads(args.summary.read_text());r=summary["rule106_parity"]
 step=stepmap(RULE);t=obs(PARITY);even=direct(obs(EVEN),t,step,13);odd=direct(obs(ODD),t,step,13)
 ok=abs(even["W"]-r["bulk_split_W"])<TOL and abs(odd["W"]-r["tail_split_W"])<TOL and even["tail"]==13 and odd["tail"]==7
 out={"ok":ok,"method":"explicit target-future words through frozen stable horizon","rule":RULE,"even":even,"odd":odd};args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
 if not ok:raise SystemExit(1)
if __name__=="__main__":main()
