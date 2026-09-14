#!/usr/bin/env python3
"""Fast preserved-data accounting; scientific verification is explicit and off CI."""
from __future__ import annotations
import argparse,base64,csv,hashlib,io,json,shutil,subprocess,sys,tarfile,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'results/binary_lift_20260914_extension'
RESULT='results/binary_lift_20260914_extension.json'
MANIFEST=DATA/'bundle_manifest.json'
BASELINE=ROOT/'results/binary_lift_20260914.json'
PROTOCOLS=['docs/research/protocols/'+n for n in ['dt2-holdouts-20260914.md','row-complements-20260914.md','binary-lift-extension-record-20260914.md']]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sources():
    m=read(MANIFEST)
    paths=[str(Path(__file__).relative_to(ROOT)),str(MANIFEST.relative_to(ROOT)),str(BASELINE.relative_to(ROOT)),*PROTOCOLS,'experiments/binary_lift_20260914/dt2-bridge-reconciliation.md',*m['code_files'],*[p['path']for p in m['archive_parts']]]
    return {f'input_{i:03d}':p for i,p in enumerate(sorted(paths))}
def integrity():
    import check_result_integrity as engine
    engine.REGISTRY[RESULT]=sources();problems=engine.check(RESULT)
    if problems:raise RuntimeError('\n'.join(problems))
def extract(dst):
    dst=dst.resolve();dst.mkdir(parents=True,exist_ok=True)
    if any(dst.iterdir()):raise ValueError('Extraction destination must be empty')
    m=read(MANIFEST);parts=[]
    for p in m['archive_parts']:
        path=ROOT/p['path'];assert sha(path)==p['sha256'];parts.append(path.read_bytes())
    archive=base64.b64decode(b''.join(parts),validate=True)
    assert hashlib.sha256(archive).hexdigest()==m['archive_sha256']
    expected={x['path']:x for x in m['members']}
    with tarfile.open(fileobj=io.BytesIO(archive),mode='r:xz')as tar:
        members=tar.getmembers();assert len(members)==len(expected)and {x.name for x in members}==set(expected)
        for item in members:
            name=Path(item.name);assert item.isfile()and not name.is_absolute()and '..'not in name.parts
            data=tar.extractfile(item).read();spec=expected[item.name]
            assert len(data)==spec['bytes']and hashlib.sha256(data).hexdigest()==spec['sha256']
            p=dst/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    lab=dst/'ca_lift_lab'
    for name in m['code_files']:shutil.copyfile(ROOT/name,lab/Path(name).name)
    return lab
def rows(lab,name):
    return [json.loads(line)for p in sorted((lab/'runs'/name).glob('part-*.jsonl'))for line in p.read_text().splitlines()]
def tag(r):return(r['rule'],r['mask'],r['shift'],r['reference'],tuple(r['order']),r.get('polarity',0))
def gate(r,g):
    v=r['gates'];f=v['native']and v['source']
    return f if g=='faithful'else f and(v['raw']if g=='original_G'else v['centered0']or v['centered1'])
def account(lab):
    gates=('faithful','original_G','centered_G');sets={};totals={}
    dt=rows(lab,'dt2_holdouts_36');co=rows(lab,'row_complements_8')
    assert len(dt)==29376 and len(co)==202752
    for name,rr in [('DT2',dt),('complement',co)]:
        assert len({tag(r)for r in rr})==len(rr)
        sets[name]={g:sorted({r['rule']for r in rr if gate(r,g)})for g in gates}
        totals[name]={family:{'cases':len(sub),**{g:len({r['rule']for r in sub if gate(r,g)})for g in gates}}for family,sub in [('four_fields',[r for r in rr if r['reference']==-1]),('five_fields',[r for r in rr if r['reference']!=-1])]}
    old={tag(r):r for r in dt};controls=[r for r in co if r['polarity']==0]
    assert len(controls)==6528 and all(r['gates']==old[tag(r)]['gates']for r in controls)
    baseline=read(BASELINE)['first_floor']['combined'];mapping=dict(zip(gates,['first_order_pass','joint_raw','joint_centered']))
    union={g:sorted(set(baseline[mapping[g]])|set(sets['DT2'][g])|set(sets['complement'][g]))for g in gates}
    assert [len(union[g])for g in gates]==[256,156,256]
    common=[json.loads(s)for s in(lab/'runs/row_complements_8/common_recipe.jsonl').read_text().splitlines()]
    indexed={tag(r):r for r in co}
    assert len(common)==8 and all(r==indexed[tag(r)]and gate(r,'centered_G')and r['overlap_keys']==0 for r in common)
    for r in common:assert(r['mask'],r['shift'],r['reference'],r['order'],r['polarity'])==('birth',1,3,[0,1,2,3,4],4)
    verification={name:read(lab/'runs'/name/'verification.json')for name in ('dt2_holdouts_36','row_complements_8')}
    export=read(lab/'runs/row_complements_8/common_recipe_verification.json')
    assert all(v['status']=='passed'for v in verification.values())and export['status']=='passed'
    for e in export['table_sizes'].values():assert sha(lab/'runs/row_complements_8'/e['file'])==e['sha256']
    return {'baseline_summary':read(BASELINE)['summary'],'new_rule_sets':sets,'family_counts':totals,'cumulative_first_floor':union,'zero_polarity_controls':len(controls),'common_complement_recipe':{'rules':[r['rule']for r in common],'mask':'birth','shift':1,'reference':3,'order':['P','D','T2','M','Q'],'polarity':4,'complemented_field':'T2','native_probe_overlap':0,'centered_native_zero_choices':[0,1]},'verification':verification,'concrete_exports':export,'summary':{'faithful_first_floor':256,'original_G_first_floor':156,'centered_G_first_floor':256,'DT2_cases':len(dt),'complement_cases':len(co),'new_recursive_run':False,'prior_best_known_3d_G':206,'prior_4d_faithful':113,'prior_4d_G':105}}
def canonical(lab):
    s=sources()
    return {'schema_version':1,'date':'2026-09-14','review_status':'Evaluation before independent review under Myk\'s explicit authorization; Gate2 pending','scope':'Prepared first floors, P/D carrier only; cumulative recipe union, no new recursive guarantee','source_paths':s,'source_hashes':{k:sha(ROOT/p)for k,p in s.items()},**account(lab)}
def coverage(record):
    stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n')
    writer.writerow(['rule','faithful_first_floor','original_G_first_floor','centered_G_first_floor','new_DT2_original_G','new_DT2_centered_G','new_complement_centered_G'])
    f=record['cumulative_first_floor'];n=record['new_rule_sets']
    for r in range(256):writer.writerow([r,*[int(r in f[g])for g in('faithful','original_G','centered_G')],int(r in n['DT2']['original_G']),int(r in n['DT2']['centered_G']),int(r in n['complement']['centered_G'])])
    return stream.getvalue()
def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    for flag in('integrity','check','write-record','replay'):g.add_argument('--'+flag,action='store_true')
    g.add_argument('--extract',type=Path);args=p.parse_args()
    if not args.write_record:integrity()
    if args.integrity:print('Binary lift extension: registered source and evidence hashes match');return
    if args.extract:print(extract(args.extract));return
    with tempfile.TemporaryDirectory(prefix='binary-lift-extension-')as tmp:
        lab=extract(Path(tmp));record=canonical(lab);text=coverage(record)
        if args.write_record:(ROOT/RESULT).write_text(json.dumps(record,indent=2)+'\n');(DATA/'rule_coverage.csv').write_text(text)
        else:assert record==read(ROOT/RESULT)and text==(DATA/'rule_coverage.csv').read_text()
        print(json.dumps(record['summary']))
        if args.replay:
            for name in('verify_dt2_holdouts.py','verify_row_complements.py','export_complement_carriers.py'):subprocess.run([sys.executable,str(lab/name)],cwd=lab,check=True)
            print('Independent implementation checks replayed off CI; primary censuses were not rerun')
if __name__=='__main__':main()
