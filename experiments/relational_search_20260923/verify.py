#!/usr/bin/env python3
"""Audit saved certificates; no Prolog process, timed search or Jev requests."""
import argparse
import hashlib
import json
from pathlib import Path

import run

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('result', type=Path)
args = parser.parse_args()
data = json.loads(args.result.read_text())
expected = set(run.INPUTS)
if set(data['source_hashes']) != expected:
    raise SystemExit('incomplete source manifest')
for path in expected:
    if hashlib.sha256((run.ROOT/path).read_bytes()).hexdigest() != data['source_hashes'][path]:
        raise SystemExit('source hash mismatch: '+path)
audit = run.final_audit(data['runs'])
summary = run.predictions(data['runs'],
    'missing_credential' if data['jev']['status']=='not_evaluated' else 'incomplete_or_failed_acquisition', audit)
assert summary['predictions'] == data['predictions'], 'prediction accounting changed'
assert summary['local_summary'] == data['local_summary'], 'timing summary changed'
print(json.dumps(audit, indent=2))
raise SystemExit(0 if audit['ok'] else 1)
