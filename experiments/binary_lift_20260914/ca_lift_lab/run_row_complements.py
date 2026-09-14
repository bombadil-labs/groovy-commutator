"""Bounded all-eight exact row-polarity census; no prior admission filter."""
import hashlib,json,subprocess,time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path(__file__).resolve().parent
RUN=ROOT/'runs/row_complements_8'
RULES=[171,187,233,235,241,243,249,251]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    started=time.monotonic();binary=Path('/tmp/audit_row_complements')
    inputs={p.name:digest(p)for p in [ROOT/'audit_row_complements.cpp',ROOT/'audit_dt2_holdouts.cpp',Path(__file__),RUN/'protocol.md']}
    manifest={'rules':RULES,'cases_expected':202752,'cases_per_rule':25344,'fields':['P','D','T2','M','Q'],'polarity_bit_order':'bit f complements field f; all 16 or 32 vectors','families':{'PD_T2_M':6144,'PD_T2_M_Q':196608},'source_interval':[-5,5],'probe_assignments':2048,'native_interval':[-4,4],'native_assignments':512,'native_radius':[2,2],'alphabet_bits':1,'source_preparation_radius':2,'periods':[4,5],'carrier':'unchanged P_s(G),G on exact P/D only','native_outputs':'free except explicit native/probe/zero constraints','source_hashes':inputs,'budget_seconds_per_worker':95,'workers':2}
    mp=RUN/'manifest.json'
    if mp.exists():assert json.loads(mp.read_text())['source_hashes']==inputs
    else:mp.write_text(json.dumps(manifest,indent=2)+'\n')
    subprocess.run(['g++','-O3','-std=c++17',str(ROOT/'audit_row_complements.cpp'),'-o',str(binary)],check=True)
    compile_seconds=time.monotonic()-started
    old=[]
    for p in sorted(RUN.glob('part-*.jsonl')):old.extend(json.loads(s)for s in p.read_text().splitlines())
    counts={r:sum(x['rule']==r for x in old)for r in RULES};assert all(n in(0,25344)for n in counts.values())
    todo=[r for r in RULES if not counts[r]];generation=len(list(RUN.glob('part-*.jsonl')));start=time.monotonic()
    def worker(i):
        subset=todo[i::2]
        if not subset:return
        with(RUN/f'part-{generation+i:02}.log').open('w')as log:
            p=subprocess.run([str(binary),','.join(map(str,subset)),str(RUN/f'part-{generation+i:02}.jsonl'),'95'],stderr=log)
        assert p.returncode in(0,10),p.returncode
    with ThreadPoolExecutor(max_workers=2)as pool:list(pool.map(worker,range(2)))
    elapsed=time.monotonic()-start
    records=[]
    for p in sorted(RUN.glob('part-*.jsonl')):records.extend(json.loads(s)for s in p.read_text().splitlines())
    def tag(r):return(r['rule'],r['mask'],r['shift'],r['reference'],tuple(r['order']),r['polarity'])
    assert len({tag(r)for r in records})==len(records)
    cached={}
    for p in sorted((ROOT/'runs/dt2_holdouts_36').glob('part-*.jsonl')):
        for s in p.read_text().splitlines():
            r=json.loads(s)
            if r['rule']in RULES:cached[tag(dict(r,polarity=0))]=r
    zero=0
    for r in records:
        if r['polarity']==0:assert r['gates']==cached[tag(r)]['gates'],tag(r);zero+=r['polarity']==0
    def passes(r,g):
        v=r['gates'];faithful=v['native']and v['source']
        if g=='faithful':return faithful
        if g=='original_G':return faithful and v['raw']
        if g=='centered_G':return faithful and(v['centered0']or v['centered1'])
        return v[g]
    summary={'complete':len(records)==202752,'cases':len(records),'seconds_census':elapsed,'seconds_compile':compile_seconds,'zero_polarity_controls':zero,'families':{}}
    for name,rr in [('PD_T2_M',[r for r in records if r['reference']==-1]),('PD_T2_M_Q',[r for r in records if r['reference']!=-1]),('union',records),('auxiliary_only',[r for r in records if r['polarity']&3==0])]:
        item={'cases':len(rr)}
        for g in('native','source','faithful','original_G','centered_G'):
            item[g]=sorted({r['rule']for r in rr if passes(r,g)})
        item['passing_recipes']={g:{str(rule):sum(r['rule']==rule and passes(r,g)for r in rr)for rule in RULES}for g in('faithful','original_G','centered_G')}
        summary['families'][name]=item
    selected={}
    for r in sorted(records,key=lambda r:(r['polarity'].bit_count(),r['polarity'],r['reference']!=-1,tag(r))):
        for g in('faithful','original_G','centered_G'):
            if passes(r,g):selected.setdefault((r['rule'],g),dict(r,selected_for=g))
    (RUN/'selected.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n'for _,r in sorted(selected.items())))
    (RUN/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
