"""Deductive checks of the outer-totalistic dimensional interpreter.

No trajectory screening or Class-IV classifier. Local law is defined for every
positive lower dimension d. Finite checks support the dimension-general proofs
in docs/research/2026-09-08-dimensional-lift.md.
"""
from pathlib import Path
from itertools import product
import hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def address(n,d):
    digits=[]
    for _ in range(d):digits.append(n%3);n//=3
    assert n==0
    return tuple(reversed(digits))

def local(patch):
    d=patch.ndim-1
    c=int(patch[(1,)*(d+1)])
    n=int(patch[1].sum())-c
    return int(patch[((0 if c==0 else 2),)+address(n,d)])

def pattern(z,d):
    k=3**(d+1)
    return np.array([(z>>i)&1 for i in range(k)],dtype=np.uint8).reshape((3,)*(d+1))

def pack(grid):return sum(int(x)<<i for i,x in enumerate(grid.flat))

def step(grid):
    out=np.zeros_like(grid);offsets=list(product([-1,0,1],repeat=grid.ndim))
    for pos in np.ndindex(grid.shape):
        patch=np.array([grid[tuple((a+b)%n for a,b,n in zip(pos,off,grid.shape))]
                        for off in offsets],dtype=np.uint8).reshape((3,)*grid.ndim)
        out[pos]=local(patch)
    return out

def main():
    checks={};witnesses={}
    # Exhaust every local patch for d=1.
    for z in range(512):
        p=pattern(z,1)
        assert local(1-np.flip(p))==1-local(p)
    checks['d1_local_symmetry']=512
    # All 512 central inputs, zero + 18 basis rule tables; fixed-input output
    # and its transformed output are affine in table bits, so this checks all tables.
    basis_count=0
    for z in range(512):
        center=pattern(z,1)
        for j in range(-1,18):
            p=np.zeros((3,3,3),dtype=np.uint8);p[1]=center
            if j>=0:
                plane=0 if j<9 else 2
                p[plane].flat[j%9]=1
            c=int(center[1,1]);n=int(center.sum())-c
            expected=int(j==9*c+n)
            assert local(p)==expected
            assert local(1-np.flip(p))==1-expected
            basis_count+=1
    checks['d2_affine_basis_inputs']=basis_count
    rng=np.random.default_rng(20260908)
    for d in [3,4]:
        for _ in range(200):
            p=rng.integers(0,2,size=(3,)*(d+1),dtype=np.uint8)
            assert local(1-np.flip(p))==1-local(p)
        checks[f'd{d}_sampled_local_symmetry']=200
    for d in range(1,7):
        m=3**d
        for n in range(m):
            assert address(m-1-n,d)==tuple(2-a for a in address(n,d))
    checks['ternary_address_pairs']=sum(3**d for d in range(1,7))
    # Family-closure obstruction works in each tested dimension; proof works in all d>=1.
    for d in [1,2,3,4]:
        a=np.zeros((3,)*(d+1),dtype=np.uint8);b=a.copy();a.flat[0]=1;b.flat[1]=1
        assert local(a)==1 and local(b)==0
        assert a.sum()==b.sum()==1 and a[(1,)*(d+1)]==b[(1,)*(d+1)]==0
    checks['non_outer_totalistic_witnesses']=4
    # Complete 3x3 periodic 2D system (d=1 interpreter), independent of old selector.
    states=np.arange(512,dtype=np.int64)
    f=np.array([pack(step(pattern(int(z),1))) for z in states],dtype=np.int64)
    j=np.array([pack(np.flip(pattern(int(z),1))) for z in states],dtype=np.int64)
    h=511^j
    assert np.array_equal(f[h],h[f])
    delta=states^f;g=delta[f]^f[delta]
    assert np.array_equal(delta[h],j[delta])
    defect=g[h]^j[g]
    rhs=f[j[delta]]^j[f[delta]]
    assert np.array_equal(defect,rhs)
    checks['global_symmetry']=512;checks['derivative_covariance']=512;checks['commutator_defect_identity']=512
    # Deductive follow-up: retain the base state when transporting a change.
    transport=f[:,None]^f[states[:,None]^states[None,:]]
    assert np.array_equal(transport[h[:,None],j[None,:]],j[transport])
    assert np.array_equal(transport[states,delta],delta[f])
    checks['context_transport_covariance']=512*512
    checks['context_transport_derivative_identity']=512
    failures=np.flatnonzero(defect)
    if len(failures):
        z=int(failures[0]);witnesses['commutator']={key:int(value) for key,value in
            dict(state=z,evolved=f[z],derivative=delta[z],commutator=g[z],
                 transformed_state=h[z],commutator_of_transformed=g[h[z]],
                 reflected_commutator=j[g[z]],defect=defect[z]).items()}
    # A direct rule-table consistency check on overlapping windows. A uniform
    # table at every translated anchor forces every adjacent row/column value
    # to agree. Exhaust a 3x3 periodic face as a finite illustration.
    uniform_faces=[]
    for z in range(512):
        face=pattern(z,1)
        views=[tuple(np.roll(np.roll(face,a,axis=0),b,axis=1).flat) for a in range(3) for b in range(3)]
        if len(set(views))==1:uniform_faces.append(z)
    assert uniform_faces==[0,511]
    checks['uniform_face_patterns']=512
    admitted=[]
    for rule in range(256):
        valid=True
        for left,center,right in product([0,1],repeat=3):
            a=(rule>>(4*left+2*center+right))&1
            b=(rule>>(4*right+2*center+left))&1
            valid=valid and a==b
        if valid:admitted.append(rule)
    assert len(admitted)==64
    assert 54 in admitted and 90 in admitted
    assert all(r not in admitted for r in [30,106,110])
    checks['eca_domain_rules']=256
    output=dict(checks=checks,witnesses=witnesses,outer_totalistic_eca=admitted,
       commutator_covariance_failures=int(len(failures)),global_states=512,
       uniform_faces=uniform_faces,numpy=np.__version__,seed=20260908,
       script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       scope='Algebra first; exhaustive d1 and affine-basis d2 checks, sampled d3/d4 checks; general claims have proofs in note.')
    (ROOT/'results/dimensional_lift_20260908_checks.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
if __name__=='__main__':main()
