"""Independent scalar verification of the Rules 23/232 global collisions."""
import itertools,json,time
from pathlib import Path

def deriv(s,r):
    n=len(s);return [((r^204)>>(4*s[(i-1)%n]+2*s[i]+s[(i+1)%n]))&1 for i in range(n)]
def xor(a,b):return [x^y for x,y in zip(a,b)]
def shift(s,k):return [s[(i+k)%len(s)] for i in range(len(s))]
def fields(s,r,mask,sign,pair):
    ds=deriv(s,r);p=xor(s,shift(s,sign));a,b=pair
    if mask=='birth':m=[(1-x)&y for x,y in zip(s,ds)]
    elif mask=='death':m=[x&y for x,y in zip(s,ds)]
    elif mask=='stay_one':m=[x&(1-y) for x,y in zip(s,ds)]
    else:m=[(1-x)&(1-y) for x,y in zip(s,ds)]
    q=[s[(i+a)%len(s)]&s[(i+b)%len(s)] for i in range(len(s))]
    return [p,ds,m,q]

def main():
    start=time.monotonic();checks=0;orbits=0
    for r in (23,232):
      for mask in ('birth','death','stay_one','stay_zero'):
       d232=0 if ((mask in ('birth','death'))==(r==232)) else 1
       s=list(map(int,'000111' if d232==0 else '01'));c=[1-x for x in s]
       assert deriv(s,r)==deriv(c,r)
       for sign in (-1,1):
        for pair in ((-2,1),(-1,2)):
         a,b=fields(s,r,mask,sign,pair),fields(c,r,mask,sign,pair)
         assert a==b and not any(a[2]) and not any(a[3])
         ns=xor(s,deriv(s,r));nc=xor(c,deriv(c,r))
         assert fields(ns,r,mask,sign,pair)==fields(nc,r,mask,sign,pair);orbits+=1
         for order in itertools.permutations((1,2,3)):
          # Fixing P first quotients cyclic row rotation as in the census.
          o=(0,)+order;assert [a[i] for i in o]==[b[i] for i in o];checks+=1
    result={'status':'passed','independent_scalar_recipe_checks':checks,'independent_next_orbits':orbits,
            'all_rows_equal_pointwise':True,'seconds':time.monotonic()-start}
    out=Path(__file__).parent/'runs/decoder_obstruction_23_232/verification.json'
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
