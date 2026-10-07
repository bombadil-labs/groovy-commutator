#!/usr/bin/env python3
"""Independent saved-result replay check for the Rule54 periodic J5 fiber census."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json,subprocess,sys,math,hashlib
ROOT=Path(__file__).resolve().parents[2]
RUN=Path(__file__).with_name('periodic_fiber_diagnostic.py')
RESULT=ROOT/'results'/'rule54_periodic_j5_fibers_20261007.json'
def main():
    saved=json.loads(RESULT.read_text())
    assert saved['source_hashes']['runner_sha256']==hashlib.sha256(RUN.read_bytes()).hexdigest()
    with TemporaryDirectory() as work:
        output=Path(work)/'result.json'
        subprocess.run([sys.executable,str(RUN),'--output',str(output)],cwd=ROOT,check=True)
        replay=json.loads(output.read_text())
    assert list(saved['rows'])==list(replay['rows'])
    for n,ref in saved['rows'].items():
        actual=replay['rows'][n]
        for key in ['n','source_states','jet_image_states','fiber_histogram',
                    'colliding_fibers','unordered_equal_jet_pairs','mechanisms',
                    'entire_current_J5_determines_next_J5']:
            assert ref[key]==actual[key],(n,key,ref[key],actual[key])
        assert math.isclose(ref['uniform_source_bits_forgotten'],
                            actual['uniform_source_bits_forgotten'],rel_tol=0,abs_tol=1e-12)
    print('PASS: all six complete Rule54 ring-fiber histograms, orbit categories, entropy, and factor checks')
if __name__=='__main__':main()
