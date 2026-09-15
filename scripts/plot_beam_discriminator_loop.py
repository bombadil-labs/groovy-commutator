#!/usr/bin/env python3
"""Static scientific figure from completed frozen rounds; no new scoring."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];U=ROOT/'experiments/beam_discriminator_loop_20260915'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'beam-loop-20260915'})
def read(n):return json.loads((U/f'round{n:02d}/result.json').read_text())
def main():
 rows=read(6)['rules']+read(8)['rules'];labels=json.loads((ROOT/'experiments/on_beam_256_4d_20260914/labels.json').read_text());classes={r:c for c,rs in labels['representatives'].items() for r in rs}
 fig,(ax,bx)=plt.subplots(1,2,figsize=(13.8,6),gridspec_kw={'width_ratios':[1.6,1]},layout='constrained');fig.suptitle('Recurrence and spreading: ECA validation and mechanism stress',fontsize=17,fontweight='bold')
 ax.axvspan(0,.5,ymin=(.5+.15)/1.5,ymax=1,color='#cce8df',alpha=.55);ax.axvline(.5,color='#48857a',ls='--',lw=1);ax.axhline(.5,color='#48857a',ls='--',lw=1);ax.axvline(0,color='#777777',ls=':',lw=2)
 style={'1':('o','#b0b7c2','Class I'),'2':('s','#809ca9','Class II'),'3':('^','#b55748','Class III')};seen=set()
 for r in sorted(set(x['rule'] for x in rows)):
  a=[x for x in rows if x['rule']==r];q=np.array([x['q'] for x in a]);alpha=np.array([x['alpha'] for x in a]);qx=float(np.median(q));ay=float(np.median(alpha))
  if r in (54,110):
   ax.scatter(qx,ay,s=240,marker='*',c='#154b75',edgecolor='#102a40',zorder=5,label='Core Class IV (54/110)' if r==54 else None)
   ax.errorbar(qx,ay,xerr=[[qx-q.min()],[q.max()-qx]],yerr=[[ay-alpha.min()],[alpha.max()-ay]],fmt='none',color='#154b75',alpha=.65,lw=1,zorder=4);ax.annotate(str(r),(qx,ay),xytext=(8,7),textcoords='offset points',fontweight='bold',color='#154b75')
  elif r in (41,106):
   ax.scatter(qx,ay,s=90,marker='D',facecolors='none',edgecolor='#8c63a0',lw=1.6,zorder=4,label='Disputed 41/106' if r==41 else None)
   if r==106:ax.annotate('106',(qx,ay),xytext=(8,6),textcoords='offset points',color='#79548b')
  else:
   m,c,l=style[classes[r]];ax.scatter(qx,ay,s=35,marker=m,c=c,alpha=.8,edgecolor='white',linewidth=.35,label=l if l not in seen else None);seen.add(l)
   if r==73:ax.annotate('73',(qx,ay),xytext=(7,5),textcoords='offset points',color='#355467')
 for i,x in enumerate(a for a in read(10)['rules'] if a['radius']==2 and a['correction']):ax.scatter(x['q'],x['alpha'],s=90,marker='D',c='#d98b24',edgecolor='#784816',zorder=6,label='Radius-2 stress (unassigned class)' if i==0 else None)
 ax.set(xlim=(-.055,1.035),ylim=(-.15,1.35),xlabel='Normalized recurrence mismatch q',ylabel='Disturbance-diameter doubling exponent α',title='12 fresh runs per ECA family; points show medians')
 ax.text(.25,1.27,'Candidate: 0 < q < ½ and α > ½',ha='center',fontsize=10,color='#286453');ax.annotate('q = 0 is excluded',xy=(0,.32),xytext=(.04,.37),arrowprops={'arrowstyle':'-','color':'#666'},fontsize=9,color='#666');ax.grid(alpha=.13);ax.legend(loc='lower right',fontsize=8,framealpha=.95)
 data=read(11)['rules'];colors={1:'#596678',2:'#d98b24',3:'#865f98'}
 for r in (1,2,3):
  subset=[x for x in data if x['radius']==r];ts=np.array([512,1024,2048,4096]);ys=np.array([[x['checkpoints'][str(t)]['diameter'] for t in ts] for x in subset])
  for y in ys:bx.plot(ts,y,color=colors[r],alpha=.3,lw=1)
  bx.plot(ts,ys.mean(axis=0),'o-',color=colors[r],lw=2,label=f'Radius {r}')
 bx.set_xscale('log',base=2);bx.set_yscale('log');bx.set_xticks([512,1024,2048,4096],['512','1,024','2,048','4,096']);bx.set(xlabel='Evolution steps',ylabel='Mean disturbance diameter (cells)',title='Exact trial continuations in open windows');bx.grid(alpha=.15);bx.legend(loc='upper left',fontsize=9)
 bx.text(.5,.18,'Each correction rule preserves iid spatial slices.\nSelection does not establish an ordered background.',transform=bx.transAxes,ha='center',fontsize=9,bbox={'facecolor':'white','alpha':.9,'edgecolor':'none'})
 fig.savefig(ROOT/'results/beam_discriminator_loop_20260915.svg',metadata={'Date':None});fig.savefig(ROOT.parent/'beam-discriminator-loop-20260915.png',dpi=160);plt.close(fig)
if __name__=='__main__':main()
