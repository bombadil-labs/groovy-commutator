#!/usr/bin/env python3
"""Jev Run 3: matched operational-codebook ablation (frozen sheet JEV_RUN3_CODEBOOK_ABLATION.md).
Reads codebook_requests.json (built from the Run-1 states, hashes verified), makes three identical
requests per alias, pins model jev-1.13.0 when accepted, records every response before any analysis.
Credential only from TYPESAFE_API_KEY. Resumable."""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parent
def canon(x): return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
def sha(x): return hashlib.sha256(canon(x)).hexdigest()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--attempts', type=int, default=3)
    ap.add_argument('--model', default='jev-1.13.0')
    ap.add_argument('--output', default='jev_codebook_responses.jsonl')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    shared = json.loads((ROOT / 'codebook_shared.json').read_text())
    cands = json.loads((ROOT / 'codebook_candidates.json').read_text())
    meta = json.loads((ROOT / 'codebook_run_meta.json').read_text())
    reqs = {}
    for alias, c in cands.items():
        state = {'candidate': c['candidate'], 'cohort_reference': shared['cohort_reference'],
                 'measurement_contract': shared['measurement_contract'], 'note': shared['note']}
        assert sha(state) == c['transformed_state_sha256'], alias
        reqs[alias] = {'state': state, 'questions': shared['questions'], 'source_state_sha256': c['source_state_sha256']}
    aliases = sorted(reqs)
    if args.dry_run:
        print('aliases', len(aliases), 'attempts', args.attempts, 'questions_sha256', meta['questions_sha256'],
              'state_bytes', min(len(canon(reqs[a]['state'])) for a in aliases), max(len(canon(reqs[a]['state'])) for a in aliases))
        return
    if not os.environ.get('TYPESAFE_API_KEY', '').strip():
        raise SystemExit('TYPESAFE_API_KEY is not set.')
    from typesafe_sdk import TypeSafeClient
    import importlib.metadata
    sdk_version = importlib.metadata.version('typesafe-sdk')
    out = ROOT / args.output
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                if row.get('status') == 'ok': done.add((row['alias'], row['attempt']))
    with TypeSafeClient() as client, out.open('a', buffering=1) as f:
        for alias in aliases:
            req = reqs[alias]
            for attempt in range(1, args.attempts + 1):
                if (alias, attempt) in done: continue
                base = {'mode': 'semantic_codebook', 'alias': alias, 'attempt': attempt,
                        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                        'source_state_sha256': req['source_state_sha256'],
                        'transformed_state_sha256': sha(req['state']),
                        'questions_sha256': sha(req['questions']),
                        'codebook_sha256': meta['codebook_sha256'], 'contract_sha256': meta['contract_sha256'],
                        'sdk_version': sdk_version, 'requested_model': args.model}
                t = time.perf_counter()
                try:
                    kw = {'model': args.model} if args.model else {}
                    res = client.system_one(state=req['state'], questions=req['questions'], **kw)
                    row = {**base, 'status': 'ok', 'elapsed_seconds': time.perf_counter() - t, 'model': res.model,
                           'usage': {'input_tokens': res.usage.input_tokens, 'output_tokens': res.usage.output_tokens},
                           'nouls': {name: ans.noul for name, ans in res.nouls.items()}}
                except Exception as e:
                    row = {**base, 'status': 'error', 'elapsed_seconds': time.perf_counter() - t, 'error': repr(e)[:500]}
                f.write(json.dumps(row, sort_keys=True) + '\n')
                print(alias, attempt, row['status'], row.get('model', ''), flush=True)
if __name__ == '__main__': main()
