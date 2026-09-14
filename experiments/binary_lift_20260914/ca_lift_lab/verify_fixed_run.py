"""Check a fixed-mask newest-axis tower and its compiled final-level rules."""
import argparse, hashlib, json, sqlite3, time
from pathlib import Path
from verify_transition_run import verify_periodic

def key(rule,dimension,recipe):
    return (rule,dimension,json.dumps(recipe,sort_keys=True,separators=(',',':')))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--run',required=True)
    ap.add_argument('--prior-run')
    args=ap.parse_args();root=Path(args.run)
    manifest=json.loads((root/'manifest.json').read_text())
    assert manifest['status']=='complete'
    db=sqlite3.connect(root/'constraints.sqlite3')
    result={'prior_candidates_matched':0,'prior_tables_matched':0,
            'recipe_invariants_checked':0,'periodic_candidates':0,
            'periodic_cells':0,'periodic_task_checks':0}
    old={}
    if args.prior_run:
        previous=sqlite3.connect(Path(args.prior_run)/'constraints.sqlite3')
        for rule,dimension,text in previous.execute('SELECT rule,dimension,record_json FROM candidates WHERE dimension<=3'):
            record=json.loads(text)
            old[key(rule,dimension,record['recipe'])]=record
        previous.close()
    for cid,rule,dimension,parent_id,ok,text in db.execute('SELECT id,rule,dimension,parent_id,strict_pass,record_json FROM candidates'):
        record=json.loads(text);path=record['recipe']
        assert len(path)==dimension-1
        for j,choice in enumerate(path):
            assert choice['mask']==path[0]['mask'] and choice['shift']==path[0]['shift']
            assert choice['offsets']==([] if j==0 else [1]+[0]*(j-1))
            assert choice['geometry']==('straight' if j==0 else 'transverse_plus')
        if parent_id is not None:
            p_rule,p_dimension,p_ok,p_text=db.execute('SELECT rule,dimension,strict_pass,record_json FROM candidates WHERE id=?',(parent_id,)).fetchone()
            assert p_rule==rule and p_dimension==dimension-1 and p_ok
            assert json.loads(p_text)['recipe']==path[:-1]
        result['recipe_invariants_checked']+=1
        if dimension<=3 and old:
            previous=old[key(rule,dimension,path)]
            for mode in ('unmarked','tagged'):
                assert record[mode]['table_sha256']==previous[mode]['table_sha256']
                assert record[mode]['tasks']==previous[mode]['tasks']
                result['prior_tables_matched']+=1
            result['prior_candidates_matched']+=1
    for dimension in range(3,manifest['max_dimension']+1):
        children=db.execute('SELECT parent_id,COUNT(*) FROM candidates WHERE dimension=? GROUP BY parent_id',(dimension,)).fetchall()
        assert all(count==1 for _,count in children)
    selected=[];start=time.perf_counter();last=start
    for rule in manifest['rules']:
        row=db.execute('SELECT id,record_json FROM candidates WHERE rule=? AND dimension=? AND strict_pass=1 ORDER BY id LIMIT 1',
                       (rule,manifest['max_dimension'])).fetchone()
        if row is None:continue
        cid,text=row;record=json.loads(text)
        cells,tasks=verify_periodic(db,cid,rule,record)
        result['periodic_candidates']+=1
        result['periodic_cells']+=cells;result['periodic_task_checks']+=cells*tasks
        selected.append({'rule':rule,'candidate_id':cid,'recipe':record['recipe']})
        if time.perf_counter()-last>=5:
            print(json.dumps({'rules_checked':result['periodic_candidates'],'seconds':round(time.perf_counter()-start,2)}),flush=True)
            last=time.perf_counter()
    for name,digest_name in [('source_harness.py','harness_sha256'),('source_lift.py','lift_sha256')]:
        assert hashlib.sha256((root/name).read_bytes()).hexdigest()==manifest[digest_name]
    result['run_source_hashes_match']=True
    result['periodic_check_seconds']=time.perf_counter()-start
    (root/'checks.json').write_text(json.dumps(result,indent=2)+'\n')
    (root/'verified_candidates.json').write_text(json.dumps(selected,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
