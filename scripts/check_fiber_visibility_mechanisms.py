"""Research025 mechanism checks: linear shielding vs context-dependent visibility."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
N=20
MASK=(1<<N)-1
EVEN_MASK=sum(1<<i for i in range(0,N,2))
CTX_POS=(-4,-3,-2,-1,2,3,4,5)


def rot_left1(x:int,n:int)->int:
    mask=(1<<n)-1
    return ((x<<1)&mask)|(x>>(n-1))


def rot_right1(x:int,n:int)->int:
    return (x>>1)|((x&1)<<(n-1))


def step90(x:int,n:int)->int:
    return rot_left1(x,n)^rot_right1(x,n)


def step106(x:int,n:int)->int:
    return rot_right1(x,n) ^ (rot_left1(x,n)&x)


def macro(step,x:int,n:int)->int:
    return step(step(x,n),n)


def parity_equal(a:int,b:int,n:int)->bool:
    d=a^b; even=sum(1<<i for i in range(0,n,2))
    return ((d^(d>>1))&even)==0


def support(x:int,n:int=N)->list[int]:
    return [i for i in range(n) if (x>>i)&1]


def joint_trace(step,a:int,b:int,n:int,limit:int=100)->dict:
    seen={}; trace=[]
    for t in range(limit+1):
        if not parity_equal(a,b,n):
            return {"kind":"visible","time":t,"trace":trace,"a":a,"b":b}
        if a==b:
            return {"kind":"coalesced","time":t,"trace":trace}
        if (a,b) in seen:
            return {"kind":"repeat","time":t,"repeat_from":seen[(a,b)],
                    "period":t-seen[(a,b)],"trace":trace}
        seen[(a,b)]=t
        trace.append({"t":t,"difference_sites":support(a^b,n),"difference_mass":int((a^b).bit_count())})
        a,b=macro(step,a,n),macro(step,b,n)
    raise AssertionError("joint trace did not terminate")


def local_step106(bits:list[int])->list[int]:
    return [bits[i+2] ^ (bits[i]*bits[i+1]) for i in range(len(bits)-2)]


def evolve2_local(bits:list[int])->list[int]:
    return local_step106(local_step106(bits))


def visibility_formula(c:dict[int,int])->bool:
    return bool(
        (c[-2] and c[-3])
        or (c[-1] and not c[2])
        or (c[2] and c[3] and c[4])
        or (c[2] and not c[3] and not c[4])
    )


def rigid_formula(c:dict[int,int])->bool:
    return bool((not c[-1]) and (not c[2]) and ((not c[-2]) or (not c[-3])))


def local_context_census()->dict:
    hidden=visible=rigid=0; failures=[]
    for mask in range(256):
        c={p:(mask>>j)&1 for j,p in enumerate(CTX_POS)}
        a={p:c.get(p,0) for p in range(-4,6)}
        a[0],a[1]=1,0
        b=dict(a);b[0]^=1;b[1]^=1
        wa=[a[p] for p in range(-4,6)]; wb=[b[p] for p in range(-4,6)]
        da=[x^y for x,y in zip(evolve2_local(wa),evolve2_local(wb))]
        par=(da[0]^da[1],da[2]^da[3],da[4]^da[5])
        direct_visible=bool(any(par))
        direct_rigid=tuple(i-2 for i,x in enumerate(da) if x)==(-2,-1)
        if direct_visible: visible+=1
        else:hidden+=1
        if direct_rigid:rigid+=1
        if direct_visible!=visibility_formula(c) or direct_rigid!=rigid_formula(c):
            failures.append({"mask":mask,"context":c,"difference":da,"parity_difference":par})
    assert not failures and hidden==96 and visible==160 and rigid==48
    return {"contexts":256,"hidden_next_step":hidden,"visible_next_step":visible,
            "rigid_left_shift":rigid,
            "visible_predicate":"(c[-2]&c[-3]) OR (c[-1]&~c[+2]) OR (c[+2]&c[+3]&c[+4]) OR (c[+2]&~c[+3]&~c[+4])",
            "rigid_predicate":"~c[-1] & ~c[+2] & (~c[-2] OR ~c[-3])"}


def shared_context(a:int,b:int,t:int)->list[int]:
    p=(-2*t)%N; out=[]
    for off in CTX_POS:
        q=(p+off)%N
        va=(a>>q)&1;vb=(b>>q)&1
        assert va==vb
        if va: out.append(off)
    return out


def main()->None:
    r90=joint_trace(step90,0,3,N)
    assert r90["kind"]=="repeat" and r90["repeat_from"]==1 and r90["period"]==6
    assert all(x["difference_mass"]>0 for x in r90["trace"])

    shield=joint_trace(step106,1,2,N)
    assert shield["kind"]=="repeat" and shield["repeat_from"]==0 and shield["period"]==10
    for row in shield["trace"]:
        t=row["t"]
        assert row["difference_sites"]==sorted([(-2*t)%N,(-2*t+1)%N])

    a,b=25,26; latent=[]
    context_runs=[]; last=None
    for t in range(52):
        eq=parity_equal(a,b,N); dsites=support(a^b,N)
        ctx=shared_context(a,b,t) if t<=50 else None
        latent.append({"t":t,"observations_equal":eq,"difference_sites":dsites,"shared_context":ctx})
        if t<=50:
            assert eq and dsites==sorted([(-2*t)%N,(-2*t+1)%N])
            if ctx!=last:
                if last is not None: context_runs[-1]["end"]=t-1
                context_runs.append({"start":t,"end":None,"context":ctx});last=ctx
        if t<51:a,b=macro(step106,a,N),macro(step106,b,N)
    context_runs[-1]["end"]=50
    assert not latent[51]["observations_equal"] and len(latent[51]["difference_sites"])==3
    assert context_runs==[
        {"start":0,"end":31,"context":[3,4]},
        {"start":32,"end":48,"context":[-4,3,4]},
        {"start":49,"end":49,"context":[-4,-2,3,4]},
        {"start":50,"end":50,"context":[-4,-1,3,4]},
    ]
    census=local_context_census()
    final_c={p:int(p in context_runs[-1]["context"]) for p in CTX_POS}
    assert visibility_formula(final_c)

    result={
        "rule90_linear_control":{"pair":[0,3],"repeat_from":1,"period":6,
            "interpretation":"nonzero observer-null difference persists forever under exact factor closure"},
        "rule106_same_defect_two_fates":{
            "shielded_pair":[1,2],"shielded_period":10,
            "latent_pair":[25,26],"latent_first_visibility":51,
            "common_initial_difference_sites":[0,1],
            "latent_context_runs":context_runs,
        },
        "rule106_local_visibility_gate":census,
        "rule106_difference_identity":"delta'_i = delta_(i+1) XOR S_(i-1)delta_i XOR S_i delta_(i-1) XOR delta_(i-1)delta_i",
    }
    (ROOT/'results'/'fiber_visibility_mechanisms_20260908.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
