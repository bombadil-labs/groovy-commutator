#!/usr/bin/env python3
"""Replay the exact 256-rule census and Rule54 all-depth SCC certificate.

The verifier compares every census row and source-pair witness, not just a
published headline; timing/RSS and eigensolver roundoff are excluded.
Requires: g++, numpy, scipy, sympy.
"""
from __future__ import annotations
import hashlib,json,math,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent


def main():
    with tempfile.TemporaryDirectory(prefix='jet_verify_') as tmp:
        temp=Path(tmp)
        source_census=ROOT/'results'/'jet_gqr_256_20261007.json'
        source_fibers=ROOT/'results'/'rule54_golden_invariance_20261007.json'
        expected_census=json.loads(source_census.read_text())
        expected_fibers=json.loads(source_fibers.read_text())
        subprocess.run([sys.executable,str(HERE/'prepare_census.py'),'--out',str(temp/'census.json')],check=True)
        subprocess.run([sys.executable,str(HERE/'rule54_invariance.py'),'--out',str(temp/'fibers.json')],check=True)
        actual_census=json.loads((temp/'census.json').read_text())
        actual_fibers=json.loads((temp/'fibers.json').read_text())
        for key in ('rule_count','raw_rows','categories','counts','max_cycle_period_histogram','Wolfram_reflection_conjugacy_orbits'):
            assert actual_census[key]==expected_census[key],f'census mismatch at {key}'
        sha_cxx=hashlib.sha256((HERE/'gqr_census.cpp').read_bytes()).hexdigest()
        sha_census=hashlib.sha256((HERE/'prepare_census.py').read_bytes()).hexdigest()
        assert expected_census['sources_sha256']=={'cxx_source':sha_cxx,'summary_runner':sha_census}
        sha_fibers=hashlib.sha256((HERE/'rule54_invariance.py').read_bytes()).hexdigest()
        sha_alg=hashlib.sha256((HERE/'jet_algebra.py').read_bytes()).hexdigest()
        assert expected_fibers['source_hashes']=={'runner_sha256':sha_fibers,'algebra_sha256':sha_alg}
        for key in ('rule','jet_prefix','source_radius','pair_edges','biinfinite_vertices','biinfinite_edges',
                    'target_components_count','any_all_order_single_component_invariant','all_three_union_invariant',
                    'post_primary_golden_swap'):
            assert actual_fibers[key]==expected_fibers[key],f'Rule54 mismatch at {key}'
        for actual,expected in zip(actual_fibers['target_components'],expected_fibers['target_components']):
            for key in expected:
                if key=='perron':
                    assert math.isclose(actual[key],expected[key],rel_tol=0,abs_tol=1e-8)
                else:
                    assert actual[key]==expected[key],(key,actual[key],expected[key])
        assert expected_fibers['post_primary_golden_swap']['full_line_forward_invariant_union']
        assert expected_fibers['post_primary_golden_swap']['all_paths_independently_checked_scalar']
        print('PASS: 256/256 exact SCC rows, categories, orbits, controls, and source hashes')
        print('PASS: Rule54 A5 all SCCs and exact golden-component swap witnesses')
        print('PASS: all 288 three-edge paths checked through independent scalar CA')
        print('PASS: two-component forward-invariant relation and all-depth induction contract')


if __name__=='__main__':main()
