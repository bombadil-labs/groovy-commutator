#!/usr/bin/env python3
"""Summarize frozen scores; no scientific generation or model selection."""
import json
from collections import Counter
from pathlib import Path
from rule_ring_selectors import atomic_json,sha256
ROOT=Path(__file__).resolve().parents[1]
UNIT=ROOT/'experiments/factor_balanced_interactions_20260915'

def main():
 r=json.loads((UNIT/'confirmation-result.json').read_text())
 scores=r['tasks'];pairs=sorted({tuple(t['rules']) for t in scores})
 totals={key:dict(Counter(t[key] for t in scores)) for key in ('M2_vs_M0','M2_vs_M1')}
 totals['strict_joint_improvements']=sum(t['strict_joint_improvement'] for t in scores)
 pair_summary=[{'rules':list(pair),'strict_joint_improvements':sum(t['strict_joint_improvement'] for t in scores if tuple(t['rules'])==pair)} for pair in pairs]
 sources=list(r['source_hashes'])+['scripts/summarize_factor_balanced.py','scripts/package_factor_balanced.py','scripts/plot_factor_balanced.py']
 sources += [str(p.relative_to(ROOT)) for p in sorted(UNIT.glob('*')) if p.is_file() and p.suffix in ('.json','.md') and p.name not in ('evidence.json','cases.json','confirmation-progress.json')]
 sources += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'review/factor_balanced').glob('*')) if p.is_file() and p.suffix in ('.py','.json','.md')]
 sources=sorted(set(sources))
 out={'status':'complete','evidence':'exploratory','rules':r['rules'],'fresh_widths':r['widths'],'source_state_cases':r['source_state_cases'],'tasks':scores,'summary':r['summary'],'totals':totals,'pair_summary':pair_summary,'limits':['Only divisibility by 2 and 3 families are balanced.','Six dependent test ring pairs; overlapping rule-pair tasks.','Size and gap confounding remains.','VI is a scalar projection of retained partitions.','No Class-IV discriminator or lifted completion result.'],'source_hashes':{p:sha256(ROOT/p) for p in sources}}
 atomic_json(ROOT/'results/factor_balanced_interactions_20260915.json',out)
 lines=['# Frozen test scores','', '| Observation | M2 beats size | M2 beats main effects | Beats both |','| --- | ---: | ---: | ---: |']
 for row in r['summary']:lines.append(f"| {row['observation']} | {row['M2_vs_M0'].get('improvement',0)}/28 | {row['M2_vs_M1'].get('improvement',0)}/28 | {row['strict_joint_improvements']}/28 |")
 lines+=['','## Every rule pair','','| Rules | Observations where M2 beats both |','| --- | ---: |']
 for row in pair_summary:lines.append(f"| {' / '.join(map(str,row['rules']))} | {row['strict_joint_improvements']}/9 |")
 lines+=['','## Rule 54 / 110','','| Observation | Size MAE | Main effects MAE | Interactions MAE | Beats both |','| --- | ---: | ---: | ---: | --- |']
 for t in scores:
  if t['rules']==[54,110]:lines.append(f"| {t['observation']} | {t['models']['M0']['mae']:.6f} | {t['models']['M1']['mae']:.6f} | {t['models']['M2']['mae']:.6f} | {t['strict_joint_improvement']} |")
 (UNIT/'score-tables.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps(totals))
if __name__=='__main__':main()
