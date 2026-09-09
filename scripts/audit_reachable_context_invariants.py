"""Independent scalar audit for frozen Research033 reachable-context cases."""
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
A=8
CASES=[(1,'01001100',(0,2),48,5,153,3,True,'edge-only'),(5,'01001100',(0,2),64,5,230,4,False,'unresolved'),(122,'00100000',(1,4),64,3,3528,6,False,'sentinel'),(122,'00100000',(1,5),64,3,3523,6,False,'sentinel'),(122,'00100000',(3,6),64,3,3520,6,False,'sentinel'),(122,'00100000',(3,7),64,3,3520,6,False,'sentinel'),(122,'00100000',(4,5),64,3,3523,6,False,'sentinel'),(122,'00100000',(6,7),64,3,3520,6,False,'sentinel'),(161,'00000100',(0,1),64,3,3520,6,False,'sentinel'),(161,'00000100',(0,4),64,3,3520,6,False,'sentinel'),(161,'00000100',(1,4),64,3,3520,6,False,'sentinel'),(161,'00000100',(2,3),64,3,3523,6,False,'sentinel'),(161,'00000100',(2,6),64,3,3523,6,False,'sentinel'),(161,'00000100',(3,6),64,3,3528,6,False,'sentinel')]
def lut(r):return tuple((r>>i)&1 for i in range(8))
def bits3(x):return ((x>>0)&1,(x>>1)&1,(x>>2)&1)
def macro_table(rule):
 t=lut(rule);out={}
 for l,c,r in itertools.product(range(8),repeat=3):
  row=list(bits3(l)+bits3(c)+bits3(r))
  for _ in range(3):row=[t[4*row[i]+2*row[i+1]+row[i+2]] for i in range(len(row)-2)]
  out[(l,c,r)]=row[0]|(row[1]<<1)|(row[2]<<2)
 return out
def paired_table(rule):
 g=macro_table(rule);out={}
 for x,y,z in itertools.product(range(64),repeat=3):
  xa,xb=divmod(x,8);ya,yb=divmod(y,8);za,zb=divmod(z,8);out[(x,y,z)]=8*g[(xa,ya,za)]+g[(xb,yb,zb)]
 return out
def symbol_close(ph,seed):
 s={8*a+a for a in range(8)}|{8*seed[0]+seed[1]};rounds=0
 while True:
  old=set(s)
  for x,y,z in itertools.product(tuple(old),repeat=3):s.add(ph[(x,y,z)])
  rounds+=1
  if s==old:return s,rounds
def edge_close(ph,seed):
 d=[8*a+a for a in range(8)];s=8*seed[0]+seed[1];e={(x,y) for x in d for y in d}|{(x,s) for x in d}|{(s,x) for x in d};rounds=0
 while True:
  old=set(e);pred={i:set() for i in range(64)};succ={i:set() for i in range(64)}
  for x,y in old:succ[x].add(y);pred[y].add(x)
  add=set()
  for p1,p2 in old:
   left={ph[(p0,p1,p2)] for p0 in pred[p1]};right={ph[(p1,p2,p3)] for p3 in succ[p2]};add.update(itertools.product(left,right))
  e|=add;rounds+=1
  if e==old:return e,rounds
def visible(sym,target):
 a,b=divmod(sym,8);return target[a]!=target[b]
def check_edge(ph,e):
 pred={i:set() for i in range(64)};succ={i:set() for i in range(64)}
 for x,y in e:succ[x].add(y);pred[y].add(x)
 for p1,p2 in e:
  left={ph[(p0,p1,p2)] for p0 in pred[p1]};right={ph[(p1,p2,p3)] for p3 in succ[p2]}
  for edge in itertools.product(left,right):
   if edge not in e:return False,{'middle':[p1,p2],'missing':list(edge)}
 return True,None
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();cache={};rows=[]
 for rule,target,seed,wsc,wsr,wec,wer,wsafe,kind in CASES:
  if rule not in cache:cache[rule]=paired_table(rule)
  ph=cache[rule];s,sr=symbol_close(ph,seed);e,er=edge_close(ph,seed);closed,why=check_edge(ph,e);verts={x for edge in e for x in edge};ssafe=not any(visible(x,target) for x in s);esafe=not any(visible(x,target) for x in verts);passes=len(s)==wsc and sr==wsr and len(e)==wec and er==wer and esafe==wsafe and closed
  rows.append({'rule':rule,'target':target,'pair':f'{seed[0]}-{seed[1]}','kind':kind,'symbol_count':len(s),'symbol_rounds':sr,'symbol_safe':ssafe,'edge_count':len(e),'edge_rounds':er,'edge_safe':esafe,'edge_fixed_point_verified':closed,'closure_failure':why,'expected':{'symbol_count':wsc,'symbol_rounds':wsr,'edge_count':wec,'edge_rounds':wer,'edge_safe':wsafe},'passes':passes})
 out={'ok':all(r['passes'] for r in rows),'method':'independent scalar shrinking-cone macro rule + Python set language closure','cases':rows};a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
 if not out['ok']:raise SystemExit(1)
if __name__=='__main__':main()
