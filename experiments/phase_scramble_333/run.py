"""Read-only reproduction of the square-grid intervention in Groovy #333."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

N = 16
HORIZONS = (250, 1000, 2500)
SOURCE = "20e50e08fda5b50181cb8c565a41a1e8d950a436"
PROTOCOL = "21e972167dab26e677ffa23f7dd76d079bc483eb"
MODES = np.exp(-2j * np.pi * np.outer((1, -1, 2, -2, 3, -3, 6, -6), np.arange(N)) / N) / N
A = [1 / (math.factorial(m)**2) for m in range(13)]
B = [1 / (math.factorial(m) * math.factorial(m + 1)) for m in range(13)]
ARMS = ("intact", "within_axis", "means", "untrained", "global")

def r0(k):
    # Taylor polynomials in (k/2)^2. K starts <=.3 and stays <=r/2=2.95
    # because R0<=1, dt*eta*2/r<1; truncation negligible there at f32.
    q = k*k/4
    return k/2 * np.polynomial.polynomial.polyval(q, B) / np.polynomial.polynomial.polyval(q, A)

def step(t, k, w):
    t, k = t.astype(np.float64), k.astype(np.float64)
    u = t + .04*(w + k[0]*np.sin(np.roll(t,-1,-1)-t)
                     + np.roll(k[0],1,-1)*np.sin(np.roll(t,1,-1)-t)
                     + k[1]*np.sin(np.roll(t,-1,-2)-t)
                     + np.roll(k[1],1,-2)*np.sin(np.roll(t,1,-2)-t))
    u = u.astype(np.float32)
    v = u.astype(np.float64)
    d = np.stack((np.roll(v,-1,-1)-v, np.roll(v,-1,-2)-v))
    return u, np.maximum(0, k + .5*(r0(k)*np.cos(d) - 2*k/5.9)*.04).astype(np.float32)

def score(t):
    t = t.astype(np.float64)
    h = np.cos(np.roll(t,-1,-1)-t)
    v = np.cos(np.roll(t,-1,-2)-t)
    spec = abs(h.mean(axis=-2) @ MODES.T)**2
    phase = abs(np.exp(1j*t).mean(axis=-2) @ MODES.T)**2
    return np.stack((spec[...,6:8].sum(-1)-spec[...,2:4].sum(-1),
                     phase[...,4:6].sum(-1)-phase[...,0:2].sum(-1),
                     v.mean(axis=(-2,-1))-h.mean(axis=(-2,-1))),axis=-1)

def fixtures():
    patterns = [np.tile(.6*np.sin(k*2*np.pi*np.arange(N)/N),(N,1)) for k in (1,3)]
    assert score(patterns[0])[0] < 0 < score(patterns[1])[0]
    assert abs(score(np.zeros((N,N)))[0]) < 1e-25
    for t in patterns:
        assert abs(score(t.T)[0]) < 1e-25
        np.testing.assert_allclose(score(t),score(np.roll(t,5,axis=1)+.7),atol=1e-15)
    # Isolated horizontal bond, independent scalar arithmetic fixture;
    # phase update is symmetric and learning uses the rounded new phase.
    t = np.zeros((N,N),np.float32); t[0,1] = .5
    k = np.zeros((2,N,N),np.float32); k[0,0,0] = .25
    w = np.full((N,N),.8,np.float32); u,j = step(t,k,w)
    a=np.float32(.04*(float(w[0,0])+.25*math.sin(.5)))
    b=np.float32(.5+.04*(float(w[0,1])-.25*math.sin(.5)))
    assert u[0,0]==a and u[0,1]==b and np.count_nonzero(j)==1
    assert j[0,0,0]==np.float32(.25+.5*(r0(.25)*math.cos(float(b)-float(a))-2*.25/5.9)*.04)

def rng(i, stream):
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence([333,i,stream])))

def run(ids):
    n = len(ids)
    ts, ks, reset, perms, global_perms = [], [], [], [], []
    for i in ids:
        init = rng(i,0)
        ts.append(init.uniform(0,math.tau,(N,N)))
        ks.append(init.uniform(.1,.3,(2,N,N)))
        reset.append(rng(i,1).uniform(0,math.tau,(N,N)))
        sh = rng(i,2); perms.append([sh.permutation(N*N),sh.permutation(N*N)])
        global_perms.append(rng(i,3).permutation(2*N*N))
    ts, ks, reset = (np.asarray(x,dtype=np.float32) for x in (ts,ks,reset))
    sine = np.sin(math.tau*np.arange(N)/N)
    fx = lambda k: np.tile((.8+.9*sine[(k*np.arange(N))%N]).astype(np.float32),(N,1))
    w = np.broadcast_to(np.stack((fx(1),fx(3),fx(1).T)),(n,3,N,N)).copy()
    assert np.array_equal(np.sort(w[0,0],axis=None),np.sort(w[0,1],axis=None))
    t = np.repeat(ts[:,None],3,axis=1)
    k = np.repeat(ks.transpose(1,0,2,3)[:,:,None],3,axis=2)
    for _ in range(3000):
        t,k = step(t,k,w)
    layout = [(arm,h) for arm in range(4) for h in range(3)] + [(4,0),(4,2)]
    post = []
    for arm,h in layout:
        f=k[:,:,h].copy()
        if arm==1:
            for p in range(n):
                for a in range(2):
                    raw=f[a,p].copy().ravel()
                    f[a,p]=raw[perms[p][a]].reshape(N,N)
                    assert np.array_equal(np.sort(raw),np.sort(f[a,p],axis=None))
        if arm==2:
            f=np.broadcast_to(f.mean(axis=(-2,-1),dtype=np.float64,keepdims=True).astype(np.float32),f.shape)
        if arm==3:
            f=ks.transpose(1,0,2,3)
        if arm==4:
            for p in range(n):
                raw=f[:,p].copy().ravel()
                f[:,p]=raw[global_perms[p]].reshape(2,N,N)
                assert np.array_equal(np.sort(raw),np.sort(f[:,p],axis=None))
        post.append(f)
    k=np.stack(post,axis=2)
    t=np.repeat(reset[:,None],len(layout),axis=1)
    w=np.full_like(t,.8)
    for col in range(len(layout)):
        assert t[:,col].tobytes()==reset.tobytes()
        assert w[:,col].tobytes()==w[:,0].tobytes()
    out={}
    baseline_hash=hashlib.sha256()
    for i in range(1,max(HORIZONS)+1):
        t,k=step(t,k,w)
        assert t[:,9].tobytes()==t[:,10].tobytes()==t[:,11].tobytes(), ("matched reset failure",i)
        baseline_hash.update(t[:,9].tobytes())
        if i in HORIZONS:
            assert np.isfinite(t).all() and np.isfinite(k).all()
            s=score(t)
            out[i]={"spacing":{}, "orientation":{}}
            for a,name in enumerate(ARMS):
                if a < 4:
                    out[i]["spacing"][name]=s[:,[3*a,3*a+1],:2].tolist()
                x,y=(3*a,3*a+2) if a<4 else (12,13)
                out[i]["orientation"][name]=s[:,[x,y],2].tolist()
    return out,baseline_hash.hexdigest()

def summarize(out, ids):
    ans={}
    for t in HORIZONS:
        row=out[t]
        inds=np.random.Generator(np.random.PCG64(3331000+t)).integers(0,len(ids),(10000,len(ids)))
        def stat(d):
            return {"mean":float(d.mean()),"ci95":np.quantile(d[inds].mean(1),[.025,.975]).tolist(),
                    "pair_concordance":float(((d>0)+.5*(d==0)).mean())}
        main={}; orientation={}; delta={}
        for arm,xy in row["spacing"].items():
            z=np.asarray(xy); d=z[:,1,0]-z[:,0,0]; delta[arm]=d
            main[arm]={"history_means_k1_k3":z[:,:,0].mean(0).tolist(),"contrast":stat(d),
                       "secondary_direct_phase_mean_contrast":float((z[:,1,1]-z[:,0,1]).mean())}
        for arm,xy in row["orientation"].items():
            z=np.asarray(xy); orientation[arm]=stat(z[:,0]-z[:,1])
            orientation[arm]["balanced_accuracy"]=float(((z[:,0]>0)+.5*(z[:,0]==0)+(z[:,1]<0)+.5*(z[:,1]==0)).mean()/2)
        ans[t]={"spacing":main, "orientation":orientation,
                "placement":{arm:stat(delta["intact"]-delta[arm]) for arm in ("within_axis","means")}}
    return ans

def main():
    cli=argparse.ArgumentParser()
    mode=cli.add_mutually_exclusive_group(required=True)
    mode.add_argument("--fixtures",action="store_true")
    mode.add_argument("--evaluate",type=Path)
    mode.add_argument("--pair",type=int)
    args=cli.parse_args()
    fixtures()
    if args.fixtures:
        print("Analytic score and update fixtures pass"); return
    ids=[args.pair] if args.pair is not None else list(range(1,33))
    all_scores={t:{"spacing":{},"orientation":{}} for t in HORIZONS}
    baseline=[]
    for start in range(0,len(ids),4):
        chunk=ids[start:start+4]
        out,digest=run(chunk); baseline.append({"ids":chunk,"raw_phase_sha256":digest})
        for t,v in out.items():
            for kind,arm_rows in v.items():
                for arm,rows in arm_rows.items():
                    all_scores[t][kind].setdefault(arm,[]).extend(rows)
    result={"upstream_revision":SOURCE,"protocol_revision":PROTOCOL, "numpy":np.__version__,
            "runner_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "pair_ids":ids,
            "matched_reset_trajectory_digests":baseline,"summary":summarize(all_scores,ids),"scores":all_scores}
    encoded=json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n"
    if args.evaluate:
        with args.evaluate.open("x") as f: f.write(encoded)
    else:
        print(encoded,end="")
if __name__=="__main__":
    main()
