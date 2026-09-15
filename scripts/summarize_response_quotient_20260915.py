#!/usr/bin/env python3
"""Recover the completed run's report from immutable checkpoints, no simulation.

The original run completed every trajectory and checkpoint, then JSON rejected
a NumPy Boolean in P3. Two reporting corrections cast that Boolean and restore
the archive's zero-padded rule locator. Endpoints and metrics are reused.
"""
import json
from pathlib import Path
import response_quotient_20260915 as experiment

ROOT=Path(__file__).resolve().parents[1]
RUN=ROOT/'experiments/response_quotient_20260915/run'
FROZEN='experiments/response_quotient_20260915/frozen_runner.py'


def main():
    execution=json.loads((RUN/'execution.json').read_text())
    assert execution['status']=='complete' and execution['completed']==176
    old=(ROOT/FROZEN).read_text()
    a="predictions[f'P3_w{w}_{p}_beats_{c}']=selected[p]['metrics']['4']['all']['score']>selected[c]['metrics']['4']['all']['score']"
    b="predictions[f'P3_w{w}_{p}_beats_{c}']=bool(selected[p]['metrics']['4']['all']['score']>selected[c]['metrics']['4']['all']['score'])"
    c="input_record=f'w{w}/rule{r}/d2.json'"
    e="input_record=f'w{w}/rule{r:03d}/d2.json'"
    assert a in old and c in old and old.replace(a,b).replace(c,e)==(ROOT/'scripts/response_quotient_20260915.py').read_text()
    assert experiment.sha(ROOT/FROZEN)==execution['source_hashes']['scripts/response_quotient_20260915.py']
    for key,value in execution['source_hashes'].items():
        if key!='scripts/response_quotient_20260915.py':assert experiment.sha(ROOT/key)==value
    rows=[json.loads(f.read_text()) for f in sorted((RUN/'rules').glob('*.json'))]
    assert len(rows)==176
    corrected_locators=0
    for row in rows:
        assert experiment.sha(RUN/row['endpoints']['path'])==row['endpoints']['sha256']
        locator=f"w{row['width']}/rule{row['rule']:03d}/d2.json"
        assert locator in execution['input_record_sha256']
        corrected_locators+=int(row['input_record']!=locator)
        row['input_record']=locator
    for name,digest in execution['input_record_sha256'].items():assert experiment.sha(RUN/'inputs'/name)==digest
    class_by_rule=experiment.labels();reports,predictions=experiment.summarize(rows,class_by_rule)
    sources={p:experiment.sha(ROOT/p) for p in (*experiment.SOURCE_PATHS,FROZEN,'scripts/summarize_response_quotient_20260915.py')}
    result=dict(schema_version=1,status='complete',evidence='exploratory',source_hashes=sources,
                execution=execution,controls=experiment.self_test(),per_rule=rows,reports=reports,predictions=predictions,
                class_by_representative={str(k):v for k,v in class_by_rule.items()},
                independent_positive_representatives=list(experiment.POSITIVES),disputed_representatives=list(experiment.DISPUTED),
                reporting_recovery=dict(reason='NumPy Boolean in P3 was not JSON serializable after all trajectories completed',
                    frozen_scientific_runner=FROZEN,correction='Cast P3 comparison to Python bool and restore zero-padded input locator; exact two-line diff asserted',
                    corrected_input_locators=corrected_locators,
                    regenerated_trajectories=False,reused_metric_checkpoints=176))
    experiment.write_json(ROOT/'results/response_quotient_20260915.json',result)
    print(json.dumps(dict(status='complete',scientific_seconds=execution['elapsed_seconds'],report_recovered=True)))


if __name__=='__main__':main()
