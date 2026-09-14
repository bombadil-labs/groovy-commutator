"""Inspect candidate records or export their complete local constraint tables."""
import argparse, json, sqlite3, zlib
from pathlib import Path
import numpy as np

def table(db, candidate_id, mode='unmarked'):
    nkeys, key_bytes, names, blob = db.execute(
        'SELECT nkeys,key_bytes,targets_json,payload_zlib FROM local_tables WHERE candidate_id=? AND mode=?',
        (candidate_id,mode)).fetchone()
    names = json.loads(names); payload = zlib.decompress(blob)
    end = nkeys*key_bytes
    keys = np.frombuffer(payload[:end],dtype=np.uint8).reshape(nkeys,key_bytes)
    stop = end+nkeys*len(names)
    masks = np.frombuffer(payload[end:stop],dtype=np.uint8).reshape(nkeys,len(names))
    frequency = np.frombuffer(payload[stop:],dtype='<u4')
    return keys,masks,frequency,names

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--run',required=True)
    ap.add_argument('--rule',type=int)
    ap.add_argument('--dimension',type=int,default=3)
    ap.add_argument('--candidate',type=int)
    ap.add_argument('--table',choices=['unmarked','tagged'])
    ap.add_argument('--limit',type=int,default=10,help='Table row limit; 0 prints all')
    args=ap.parse_args();db=sqlite3.connect(Path(args.run)/'constraints.sqlite3')
    if args.candidate is None:
        if args.rule is None:ap.error('Supply --rule or --candidate')
        result=[]
        for cid,pid,ok,text in db.execute('SELECT id,parent_id,strict_pass,record_json FROM candidates WHERE rule=? AND dimension=?',(args.rule,args.dimension)):
            r=json.loads(text)
            result.append({'candidate':cid,'parent':pid,'passes':bool(ok),'recipe':r['recipe'],
                           'conflicts':{mode:{name:x['conflicts'] for name,x in r[mode]['tasks'].items()} for mode in ['unmarked','tagged']}})
        print(json.dumps(result,indent=2));return
    row=db.execute('SELECT rule,parent_id,record_json FROM candidates WHERE id=?',(args.candidate,)).fetchone()
    if row is None:ap.error('Candidate not found')
    rule,parent,text=row;r=json.loads(text)
    if not args.table:
        print(json.dumps({'candidate':args.candidate,'rule':rule,'parent':parent,**r},indent=2));return
    keys,masks,frequency,names=table(db,args.candidate,args.table)
    count=len(keys) if args.limit==0 else min(args.limit,len(keys))
    for i in range(count):
        packed=keys[i,4:] if args.table=='tagged' else keys[i]
        bits=np.unpackbits(packed,bitorder='big')[:r['physical_neighborhood_bits']]
        outputs={name:([0] if masks[i,j]==1 else [1] if masks[i,j]==2 else [0,1]) for j,name in enumerate(names)}
        print(json.dumps({'key_hex':keys[i].tobytes().hex(),
                          'patch':bits.reshape((3,)*r['dimension']).tolist(),
                          'phase_key_hex':keys[i,:4].tobytes().hex() if args.table=='tagged' else None,
                          'required_outputs':outputs,'events':int(frequency[i])}))

if __name__=='__main__':main()
