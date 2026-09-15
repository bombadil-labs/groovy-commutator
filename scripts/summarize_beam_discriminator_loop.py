#!/usr/bin/env python3
"""Assemble provenance and descriptive outcomes from the completed adaptive loop."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];UNIT=ROOT/'experiments/beam_discriminator_loop_20260915'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 results={n:json.loads((UNIT/f'round{n:02d}/result.json').read_text()) for n in range(1,12)}
 holdouts=results[6]['rules']+results[8]['rules'];core={54,110};disputed={41,106}
 hits={str(r):sum(x['selected'] for x in holdouts if x['rule']==r) for r in sorted(set(x['rule'] for x in holdouts))}
 sources=sorted(set(list((ROOT/'scripts').glob('beam_loop_*.py'))+[ROOT/'scripts/summarize_beam_discriminator_loop.py',ROOT/'scripts/plot_beam_discriminator_loop.py',ROOT/'scripts/package_beam_loop_raw.py',ROOT/'src/groovy/ca.py',ROOT/'experiments/on_beam_256_4d_20260914/labels.json',ROOT/'review/beam_loop_independent.py',ROOT/'review/beam_loop_independent.json']+list(UNIT.glob('*.md'))+list(UNIT.glob('*.json'))+list(UNIT.glob('round*/*.json'))))
 assert all(p.is_file() for p in sources)
 external={}
 for n,d in results.items():
  for p,h in d['source_hashes'].items():
   if p.endswith('.npz'):external[p]=h
 table={str(n):{'result':str((UNIT/f'round{n:02d}/result.json').relative_to(ROOT)),'seconds':d.get('seconds'),'recovery_seconds':d.get('recovery_seconds')} for n,d in results.items()}
 audit=json.loads((ROOT/'review/beam_loop_independent.json').read_text());assert set(audit['rounds'])=={str(n) for n in range(1,12)}, 'Final independent round audit still incomplete'
 d={'schema_version':1,'scope':'Eleven adaptive rounds; finite ECA prediction, ancestral support invariants and wider-radius mechanism tests; no universal Class IV theorem.',
 'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in sources},'external_array_inputs':external,
 'original_cache_sha256':'766e4db7083fbdb551bc4aee66abc554079c5d118905f6d65aa5e5372c9418d1','raw_archive_manifest':str((UNIT/'raw-archive.json').relative_to(ROOT)),
 'rounds':table,'fresh_tests':{'core_hits':{str(r):hits[str(r)] for r in sorted(core)},'runs_per_rule':12,'undisputed_negative_rules':84,'undisputed_negative_runs':sum(x['rule'] not in core|disputed for x in holdouts),'undisputed_negative_positive_runs':sum(x['selected'] and x['rule'] not in core|disputed for x in holdouts),'disputed_hits':{str(r):hits[str(r)] for r in sorted(disputed)},'all_rule_hits':hits},
 'first_lift_full_input':{'native_failed':results[1]['native_failed'],'decoder_failed':results[1]['decoder_failed']},
 'support_transport_checks':len(results[7]['rows']),'interval_probability_inequalities':len(results[9]['transport'])*9,
 'wider_radius_scope':'No Wolfram labels assigned. Right-permutive iid spatial slices challenge the ordered-background interpretation; q is held fixed for R11.',
 'wider_radius_extended':results[11]['rules'],'review_report':'review/beam_loop_independent.json',
 'review_scope':'Independent report specifies complete versus targeted replays; evaluation preceded review under standing user authorization.'}
 out=ROOT/'results/beam_discriminator_loop_20260915.json';out.write_text(json.dumps(d,sort_keys=True,indent=2)+'\n');print(json.dumps({'source_files':len(sources),'fresh_tests':{k:v for k,v in d['fresh_tests'].items() if k!='all_rule_hits'}}))
if __name__=='__main__':main()
