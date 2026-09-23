#!/usr/bin/env python3
"""Exclusive-create bounded evaluation; source pin and every outcome retained."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import signal
import sys
import time
from pathlib import Path
import numpy as np
import core

SOURCES = [
    'experiments/prediction_repair_20260923/core.py',
    'experiments/prediction_repair_20260923/run.py',
    'experiments/prediction_repair_20260923/verify.py',
    'docs/research/protocols/prediction-repair-20260923.md', 'src/groovy/ca.py']


def timeout(*_):
    raise TimeoutError('120-second evaluation wall cap')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--implementation-commit', required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as f:
        record = {'created_utc': datetime.now(timezone.utc).isoformat(),
            'implementation_commit': args.implementation_commit,
            'protocol_commit': '5927301ffae6e6d9af94398712df3b5fb3124485',
            'source_hashes': {p: hashlib.sha256((core.ROOT/p).read_bytes()).hexdigest() for p in SOURCES},
            'contract': {'rule': 54, 'ring': 12, 'repair_horizon': 4, 'damage_bits_max': 1,
                         'repair_flips_max': 1, 'passive_target': 'membership in rotations of (0011)^3'},
            'environment': {'python': sys.version, 'numpy': np.__version__}}
        start = time.perf_counter()
        signal.signal(signal.SIGALRM, timeout)
        signal.alarm(120)
        try:
            record.update(core.evaluate(), status='complete')
        except Exception as exc:
            record.update(status='resource_limit' if isinstance(exc, TimeoutError) else 'invalid',
                          error={'type': type(exc).__name__, 'message': str(exc)},
                          predictions={f'P{i}': 'not_evaluated' for i in range(1, 6)})
        finally:
            signal.alarm(0)
        record['elapsed_seconds'] = time.perf_counter()-start
        json.dump(record, f, indent=2)
        f.write('\n')
    print(json.dumps({k: record[k] for k in ('status', 'predictions', 'elapsed_seconds')}, indent=2))
    return 0 if record['status'] == 'complete' else 1


if __name__ == '__main__':
    raise SystemExit(main())
