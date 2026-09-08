"""Fresh Research025 check of Rule-106 hidden-defect visibility scaling."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DISCOVERY=list(range(12,101,2))
FRESH=list(range(102,201,2))


def v2(k:int)->int:
    c=0
    while k%2==0:
        c+=1;k//=2
    return c


def offset_for_group(m:int)->int:
    a=1
    for j in range(1,m+1):
        a += 8*(4**v2(j+1))-2
    return a


def predicted_tau(n:int)->int:
    if n<12 or n%2: raise ValueError(n)
    m=(n-12)//6
    return n+offset_for_group(m)


def step106(x:int,n:int)->int:
    mask=(1<<n)-1
    left=((x<<1)&mask)|(x>>(n-1))
    right=(x>>1)|((x&1)<<(n-1))
    return right ^ (left & x)


def macro(x:int,n:int)->int:
    return step106(step106(x,n),n)


def parity_equal(a:int,b:int,n:int)->bool:
    d=a^b
    even_mask=sum(1<<i for i in range(0,n,2))
    return (((d^(d>>1)) & even_mask)==0)


def observed_tau(n:int,pred:int)->int|None:
    a,b=25,26
    for t in range(pred+1):
        if not parity_equal(a,b,n):
            return t
        if t<pred:
            a,b=macro(a,n),macro(b,n)
    return None


def main()->None:
    rows=[]; failures=[]
    for n in FRESH:
        pred=predicted_tau(n)
        got=observed_tau(n,pred)
        row={"n":n,"group":(n-12)//6,"predicted_tau":pred,"observed_tau":got,"passes":got==pred}
        rows.append(row)
        if not row["passes"]: failures.append(row)
    result={
        "ok":not failures,
        "discovery_even_widths":[12,100],
        "fresh_even_widths":[102,200],
        "fresh_cases":len(rows),
        "formula":"tau(n)=n+a_m for m=floor((n-12)/6), a_0=1, a_m=a_(m-1)+8*4^nu2(m+1)-2",
        "failures":failures,
        "rows":rows,
    }
    out=ROOT/'results'/'rule106_visibility_scaling_fresh_20260908.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
    if failures: raise SystemExit(1)

if __name__=='__main__':main()
