"""Small independent block-word CA implementation for GQR/A5 pair experiments.

Source bit 0 is leftmost. A_k local source radius is k+1. Neither
code nor state is shared with the compiled GQR census.
"""
from __future__ import annotations
import numpy as np


def local_truth_tables(rule: int, maxlevel: int = 5):
    lut=np.array([(rule >> i)&1 for i in range(8)],dtype=np.uint8)
    word=np.arange(8,dtype=np.uint32)
    levels=[(((word>>1)&1) ^ lut[((word&1)*4)+(((word>>1)&1)*2)+((word>>2)&1)]).astype(np.uint8)]
    for k in range(maxlevel):
        r=k+1
        w=np.arange(1<<(2*(r+1)+1),dtype=np.uint32)
        hw=np.zeros(len(w),dtype=np.uint32)
        for pos in range(2*r+1):
            l=(w>>pos)&1;m=(w>>(pos+1))&1;rr=(w>>(pos+2))&1
            hw|=(lut[4*l+2*m+rr].astype(np.uint32)<<pos)
        mask=(1<<(2*r+1))-1
        transported=levels[k][hw]
        a=levels[k][w&mask];b=levels[k][(w>>1)&mask];c=levels[k][(w>>2)&mask]
        levels.append((transported ^ lut[4*a+2*b+c]).astype(np.uint8))
    return levels


def labeled_edges(levels, endlevel):
    r=endlevel+1
    bits=2*r
    states=1<<bits
    words=np.arange(1<<(bits+1),dtype=np.uint32)
    src=(words&(states-1)).astype(np.int32)
    dst=(words>>1).astype(np.int32)
    labels=np.zeros(len(words),dtype=np.uint8)
    for k in range(1,endlevel+1):
        fieldradius=k+1
        shift=r-fieldradius
        mask=(1<<(2*fieldradius+1))-1
        labels|=levels[k][(words>>shift)&mask].astype(np.uint8) << (k-1)
    return src,dst,labels,states,r


def ordered_pair_edges(src, dst, labels, source_states):
    starts=[];ends=[]
    for v in np.unique(labels):
        group=np.flatnonzero(labels==v)
        a=np.repeat(group,len(group));b=np.tile(group,len(group))
        starts.append(src[a].astype(np.int64)*source_states+src[b])
        ends.append(dst[a].astype(np.int64)*source_states+dst[b])
    return np.concatenate(starts),np.concatenate(ends)


def biinfinite_core(n, src, dst):
    def live(reverse=False):
        a,b=(dst,src) if reverse else (src,dst)
        keep=np.ones(n,dtype=bool)
        while True:
            edges=keep[a]&keep[b]
            indeg=np.bincount(a[edges],minlength=n)
            new=keep&(indeg>0)
            if np.array_equal(keep,new):return keep
            keep=new
    return live() & live(True)
