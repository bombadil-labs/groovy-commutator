"""Fresh n=18 Rule106 confirmation for Research027 bulk-vs-tail repair."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from experiment_history_lift_closure import state_map, compress  # noqa:E402

N = 18
RULE = 106
PARITY = (0, 1, 1, 0)
EVEN = (0, 1, 1, 2)
ODD = (0, 1, 2, 0)
TOL = 1e-10


def entropy(labels):
    _, c = np.unique(labels, return_counts=True); p = c / c.sum()
    return float(-(p * np.log2(p)).sum())


def obs(partition):
    states = np.arange(2**N, dtype=np.uint32)
    bits = ((states[:, None] >> np.arange(N, dtype=np.uint32)) & 1).astype(np.uint8)
    codes = bits.reshape(len(states), N // 2, 2)
    codes = codes[:, :, 0] + 2 * codes[:, :, 1]
    lut = np.asarray(partition, dtype=np.uint8); macro = lut[codes]; base = len(set(partition))
    weights = np.asarray([base**i for i in range(N // 2)], dtype=np.uint64)
    return (macro.astype(np.uint64) * weights).sum(1).astype(np.uint32)


def combine(a,b):
    aa=compress(a);bb=compress(b);k=int(bb.max())+1
    return compress(aa.astype(np.uint64)*np.uint64(k)+bb.astype(np.uint64))


def target_future(step, target_obs):
    states=np.arange(len(step),dtype=np.uint32);s=states.copy();y0=compress(target_obs);k=int(y0.max())+1
    labels=y0.copy();count=int(labels.max())+1;future=[y0.copy()]
    for t in range(1,256):
        s=step[s];y=y0[s];new=compress(labels.astype(np.uint64)*np.uint64(k)+y.astype(np.uint64))
        if int(new.max())+1==count:return labels,t-1,future
        labels=new;count=int(labels.max())+1;future.append(y.copy())
    raise RuntimeError("no target stabilization")


def metrics(zobs,cinf,future):
    z=compress(zobs);joint=combine(z,cinf);w=entropy(joint)-entropy(z);final=int(joint.max())+1
    if w<=TOL:return {"W":0.0,"tail":0}
    current=z.copy()
    for t,y in enumerate(future[1:],start=1):
        current=combine(current,y)
        if int(current.max())+1==final:return {"W":w,"tail":t}
    raise AssertionError("did not reach full future partition")


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output",type=Path,required=True);args=ap.parse_args()
    e=state_map(RULE,N);step=e[e];tobs=obs(PARITY);cinf,hstar,future=target_future(step,tobs)
    base=metrics(tobs,cinf,future);even=metrics(obs(EVEN),cinf,future);odd=metrics(obs(ODD),cinf,future)
    result={"ok":hstar==49 and base["tail"]==49 and even["tail"]==49 and odd["tail"]==19 and even["W"]<=odd["W"]+TOL,
            "ring_width":N,"rule":RULE,"target":"0110","base":{"W":base["W"],"tail":base["tail"]},
            "bulk_even_split":{"partition":"0112",**even},"defect_odd_split":{"partition":"0120",**odd}}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
    if not result["ok"]:raise SystemExit(1)

if __name__=="__main__":main()
