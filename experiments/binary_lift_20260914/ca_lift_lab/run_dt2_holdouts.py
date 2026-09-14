"""Bounded exact DT2 census; whole-rule resumable checkpoints, no old admissions."""
import argparse, hashlib, json, subprocess, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RULES = [30,35,43,49,59,86,104,106,113,115,120,135,136,149,151,152,168,169,171,187,188,192,194,224,225,230,233,234,235,238,241,243,248,249,251,252]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=ROOT/'runs/dt2_holdouts_36'); ap.add_argument('--seconds',type=float,default=90);args=ap.parse_args()
    out=args.output; out.mkdir(parents=True,exist_ok=True)
    source=ROOT/'audit_dt2_holdouts.cpp'; binary=Path('/tmp/audit_dt2_holdouts')
    start_compile=time.monotonic(); subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(binary)],check=True); compile_seconds=time.monotonic()-start_compile
    manifest={'rules':RULES,'source_width':11,'source_origin':5,'sample_bit_order':'bit j -> coordinate j-5','source_assignments':2048,'source_derivative':'r XOR 204','integration':'XOR','native_radius':[2,2],'alphabet_bits':1,'families':{'PD_T2_M':{'period':4,'orders':6,'expected_cases':1728},'PD_T2_M_Q':{'period':5,'orders':24,'references':4,'expected_cases':27648}},'fields':['P','D','T2','M','Q'],'reference_codes':{'-1':'none','0':'S[-2]&S[1]','1':'S[-1]&S[2]','2':'S[-2]&(1-S[1])','3':'(1-S[-1])&S[2]'},'expected_cases':29376,'source_sha256':digest(source),'runner_sha256':digest(Path(__file__)),'protocol_sha256':digest(out/'protocol.md'),'native_outputs':'free except native/probe/centered-zero constraints','G_scope':'exact P and D only; auxiliary T2/M/Q outputs not G constrained','parent_recovery':'equals source recovery at this first floor','workers':2,'worker_budget_seconds':args.seconds,'compile_seconds':compile_seconds,'authorization':'Myk: Let’s do it! after supplied bounded DT2 specification, 2026-09-14'}
    mp=out/'manifest.json'
    if mp.exists(): assert json.loads(mp.read_text())['source_sha256']==manifest['source_sha256'],'Cannot resume changed construction'
    else: mp.write_text(json.dumps(manifest,indent=2)+'\n')
    prior=[]
    for p in sorted(out.glob('part-*.jsonl')): prior.extend(json.loads(x) for x in p.read_text().splitlines())
    counts={r:sum(x['rule']==r for x in prior)for r in RULES}; assert all(n in (0,816)for n in counts.values())
    todo=[r for r in RULES if counts[r]==0]; generation=len(list(out.glob('part-*.jsonl'))); started=time.monotonic()
    def work(i):
        subset=todo[i::2]
        if not subset:return 0
        p=out/f'part-{generation+i:02}.jsonl';log=out/f'part-{generation+i:02}.log'
        with log.open('w')as err:
            proc=subprocess.run([str(binary),','.join(map(str,subset)),str(p),str(args.seconds)],stderr=err)
        if proc.returncode not in (0,10):raise RuntimeError(f'Worker {i} failed: {proc.returncode}')
        return proc.returncode
    with ThreadPoolExecutor(max_workers=2)as pool: list(pool.map(work,range(2)))
    elapsed=time.monotonic()-started
    rows=[]
    for p in sorted(out.glob('part-*.jsonl')):rows.extend(json.loads(x)for x in p.read_text().splitlines())
    tags={(r['rule'],r['mask'],r['shift'],r['reference'],tuple(r['order']))for r in rows};assert len(tags)==len(rows)
    def sets(rr):
        return {g:sorted({r['rule']for r in rr if ((r['gates']['native']and r['gates']['source'])if g=='faithful'else (r['gates']['native']and r['gates']['source']and (r['gates']['raw']if g=='original_G'else (r['gates']['centered0']or r['gates']['centered1']))))})for g in ('faithful','original_G','centered_G')}
    summary={'complete':len(rows)==29376,'cases':len(rows),'expected_cases':29376,'completed_rules':sorted({r['rule']for r in rows}),'seconds_census':elapsed,'families':{}}
    for fam,rr in [('PD_T2_M',[r for r in rows if r['reference']==-1]),('PD_T2_M_Q',[r for r in rows if r['reference']!=-1]),('union',rows)]:
        s=sets(rr);s.update({'cases':len(rr),'native_alone':sorted({r['rule']for r in rr if r['gates']['native']}),'source_alone':sorted({r['rule']for r in rr if r['gates']['source']}),'neither_G':sorted(set(RULES)-set(s['original_G'])-set(s['centered_G']))});summary['families'][fam]=s
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
