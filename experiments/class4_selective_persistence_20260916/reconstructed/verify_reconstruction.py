#!/usr/bin/env python3
import csv, json, math, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
csv_path = root/"evidence"/"class4_selective_persistence_all_conditions_20260916.RECOVERED.csv"
json_path = root/"reconstructed"/"class4_selective_persistence_20260916.CANONICAL_RECONSTRUCTED.json"

with csv_path.open(newline="") as f:
    rows=list(csv.DictReader(f))
assert len(rows)==450
obj=json.loads(json_path.read_text())
assert len(obj["rows"])==450

conditions={}
pos_sel=neg_sel=disp_sel=0
ctrl={"radius2-correction":0,"radius2-pure-shift":0}
posS=[]; posA=[]; fastNegS=[]; highSNegA=[]

for r in rows:
    conditions[r["condition"]]=conditions.get(r["condition"],0)+1
    R,M,S=map(float,(r["R"],r["M"],r["S"]))
    a,d256,d512=map(float,(r["alpha"],r["mean_d256"],r["mean_d512"]))
    assert abs(S-max(0,R)*max(0,M)) < 2e-12
    ea=0.0 if d256<=0 or d512<=0 else math.log2(d512/d256)
    assert abs(a-ea) < 2e-12
    ps=r["passes_S"]=="True"; pa=r["passes_alpha"]=="True"; sel=r["selected"]=="True"
    assert ps==(S>.20); assert pa==(a>.50); assert sel==(ps and pa)
    rule=None if not r["rule"] else int(float(r["rule"]))
    cls=None if not r["class"] else int(float(r["class"]))
    disp=r["disputed"]=="True"
    if rule in (54,110):
        pos_sel += int(sel); posS.append(S); posA.append(a)
    elif rule is not None and (not disp) and cls in (1,2,3):
        neg_sel += int(sel)
        if a>.5: fastNegS.append(S)
        if S>.2: highSNegA.append(a)
    elif disp:
        disp_sel += int(sel)
    elif r["name"] in ctrl:
        ctrl[r["name"]] += int(sel)

assert conditions=={"P":90,"V1":90,"V2":90,"S1":90,"S2":90}
assert (pos_sel,neg_sel,disp_sel)==(10,0,0)
assert ctrl=={"radius2-correction":0,"radius2-pure-shift":0}
assert abs(min(posS)-0.2049895616147079)<1e-12
assert abs(min(posA)-0.6831268634682903)<1e-12
assert max(fastNegS)==0.0
assert abs(max(highSNegA)-0.498938756887789)<1e-12

h=obj["headline"]
assert h["core_positive_selected"]==10
assert h["undisputed_negative_selected"]==0
assert h["disputed_selected"]==0
print("OK: recovered rows, reconstructed JSON, formulas, thresholds, counts, and margins agree.")
