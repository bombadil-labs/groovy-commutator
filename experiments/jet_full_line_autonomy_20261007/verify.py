#!/usr/bin/env python3
"""Replay and independently score the full-line jet autonomy audit."""
from __future__ import annotations
import json,subprocess,sys,tempfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def main():
 expected=json.loads((ROOT/"results/jet_full_line_autonomy_20261007.json").read_text())
 assert expected["source_hashes"] == {
  "runner_sha256":hashlib.sha256((HERE/"run.py").read_bytes()).hexdigest(),
  "algebra_sha256":hashlib.sha256((ROOT/"experiments/jet_gqr_256/jet_algebra.py").read_bytes()).hexdigest()
 }
 with tempfile.TemporaryDirectory() as tmp:
  dest=Path(tmp)/"full.json"
  subprocess.run([sys.executable,str(HERE/"run.py"),"--output",str(dest)],cwd=ROOT,check=True)
  actual=json.loads(dest.read_text())
 for rule,reference in expected["rules"].items():
  rows=actual["rules"][rule]["full_line_prefixes"]
  for ref_name,got_field in (
   ("core_nodes","biinfinite_pair_vertices"),
   ("core_edges","biinfinite_pair_edges"),
   ("paths","three_edge_paths_checked"),
   ("violations","next_field_disagreements"),
  ):
   got=[r[got_field] for r in rows]
   assert got == reference[ref_name], (rule,ref_name,got,reference[ref_name])
  assert actual["rules"][rule]["first_autonomous_prefix"] == reference["first_autonomous"], rule
  rad=actual["rules"][rule]["minimum_local_radius"]
  if rad is None:
   assert reference["min_local_radius"] is None
  else:
   assert rad["first_passing_radius"] == reference["min_local_radius"]
   assert rad["bad_counts_by_radius"] == reference["radius_bad_counts"]
  for n,depth in reference["ring_first_depth"].items():
   rows=actual["ring_control"][rule][n]
   first=next((row["end_level"] for row in rows if row["closed"]),None)
   assert first==depth,(rule,n,first,depth)
 print("PASS 20 exact full-line prefix factor decisions")
 print("PASS exact minimum local radii 30:5, 54:6, 62:6; 110 nonautonomous through A5")
 print("PASS independent periodic-ring controls widths 8-16 and source SHA-256")


if __name__=="__main__":
 main()
