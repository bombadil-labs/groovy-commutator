#!/usr/bin/env python3
"""Execute the frozen anonymous Jev feature probe.

Credentials are read only from TYPESAFE_API_KEY by the official TypeSafe SDK.
This script never prints or writes the key.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent

def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x): return hashlib.sha256(canon(x)).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=('semantic','opaque','both'),default='semantic')
    ap.add_argument('--attempts',type=int,default=3)
    ap.add_argument('--model',default=None,help='Optional model override; default uses SDK/env (normally jev-latest).')
    ap.add_argument('--output',default='jev_raw_responses.jsonl')
    ap.add_argument('--limit',type=int,default=None,help='Debug only: run first N aliases. Do not use for canonical evaluation.')
    ap.add_argument('--dry-run',action='store_true')
    args=ap.parse_args()

    if args.attempts < 1: raise SystemExit('--attempts must be >=1')
    modes=['semantic','opaque'] if args.mode=='both' else [args.mode]
    allreq={m:json.loads((ROOT/f'{m}_requests.json').read_text()) for m in modes}
    aliases=sorted(next(iter(allreq.values())))
    if args.limit is not None: aliases=aliases[:args.limit]
    for m in modes:
        if sorted(allreq[m]) != sorted(next(iter(allreq.values()))): raise SystemExit('request alias mismatch')

    if args.dry_run:
        for m in modes:
            qhash=sha(next(iter(allreq[m].values()))['questions'])
            sizes=[len(canon(allreq[m][a]['state'])) for a in aliases]
            print(m,'candidates',len(aliases),'attempts',args.attempts,'question_sha256',qhash,
                  'state_bytes_minmax',min(sizes),max(sizes))
        return

    if not os.environ.get('TYPESAFE_API_KEY','').strip():
        raise SystemExit('TYPESAFE_API_KEY is not set. Set it in the environment; do not put the key in argv or files.')
    try:
        from typesafe_sdk import TypeSafeClient
        import importlib.metadata
        sdk_version=importlib.metadata.version('typesafe-sdk')
    except Exception as e:
        raise SystemExit('Install the official SDK first: `uv add typesafe-sdk` or `pip install typesafe-sdk`. Error: '+repr(e))

    out=Path(args.output)
    if not out.is_absolute(): out=ROOT/out
    done=set()
    if out.exists():
        for line in out.read_text().splitlines():
            if not line.strip(): continue
            row=json.loads(line)
            if row.get('status')=='ok': done.add((row['mode'],row['alias'],row['attempt']))

    print('credential present; SDK',sdk_version,'output',out)
    with TypeSafeClient() as client, out.open('a',buffering=1) as f:
        for m in modes:
            for alias in aliases:
                req=allreq[m][alias]
                sh,qh=sha(req['state']),sha(req['questions'])
                for attempt in range(1,args.attempts+1):
                    key=(m,alias,attempt)
                    if key in done:
                        continue
                    stamp=datetime.now(timezone.utc).isoformat()
                    t=time.perf_counter()
                    base={'mode':m,'alias':alias,'attempt':attempt,'timestamp_utc':stamp,
                          'state_sha256':sh,'questions_sha256':qh,'sdk_version':sdk_version}
                    try:
                        res=client.system_one(state=req['state'],questions=req['questions'],model=args.model)
                        row={**base,'status':'ok','elapsed_seconds':time.perf_counter()-t,
                             'model':res.model,
                             'usage':{'input_tokens':res.usage.input_tokens,'output_tokens':res.usage.output_tokens},
                             'nouls':{name:ans.noul for name,ans in res.nouls.items()}}
                    except Exception as e:
                        row={**base,'status':'error','elapsed_seconds':time.perf_counter()-t,
                             'error_type':type(e).__name__,'error':str(e)[:500]}
                    f.write(json.dumps(row,sort_keys=True,separators=(',',':'))+'\n')
                    print(m,alias,attempt,row['status'],round(row['elapsed_seconds'],3),row.get('model',''))

if __name__=='__main__': main()
