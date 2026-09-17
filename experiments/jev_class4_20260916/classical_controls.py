#!/usr/bin/env python3
from pathlib import Path
import csv,json,math
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

ROOT=Path(__file__).resolve().parent
truth=json.loads((ROOT/'truth_private.json').read_text())
with (ROOT/'primitive_features.csv').open() as f:
    rows=list(csv.DictReader(f))
names=[x for x in rows[0] if x!='alias']
aliases=[r['alias'] for r in rows]
X=np.array([[float(r[n]) for n in names] for r in rows])
y=np.array([1 if truth[a]['primary_positive'] else 0 for a in aliases])
use=np.array([not truth[a]['disputed'] for a in aliases])
Xu,yu=X[use],y[use]; au=[a for a,u in zip(aliases,use) if u]

def auc(pos,neg):
 return (sum(p>n for p in pos for n in neg)+.5*sum(p==n for p in pos for n in neg))/(len(pos)*len(neg))
def rank(scores,i):
 x=scores[i]; return 1+sum(v>x for j,v in enumerate(scores) if j!=i)+.5*sum(v==x for j,v in enumerate(scores) if j!=i)
def metric(scores,aliases2):
 pos=[i for i,a in enumerate(aliases2) if truth[a]['primary_positive']]
 neg=[i for i,a in enumerate(aliases2) if truth[a]['class'] in (1,2,3)]
 c3=[i for i,a in enumerate(aliases2) if truth[a]['class']==3]
 ranks={truth[aliases2[i]]['rule']:rank(scores,i) for i in pos}
 lo=min(scores[i] for i in pos)
 negat=[truth[aliases2[i]]['rule'] for i in neg if scores[i]>=lo]
 return {'ranks':ranks,'negatives_at_or_above':len(negat),'negative_rules':negat,
         'auc_all':auc([scores[i] for i in pos],[scores[i] for i in neg]),
         'auc_c3':auc([scores[i] for i in pos],[scores[i] for i in c3])}

uni=[]
for j,n in enumerate(names):
 for sign in (1,-1):
  m=metric(sign*Xu[:,j],au)
  uni.append({'feature':n,'direction':'high' if sign==1 else 'low',**m})
uni=sorted(uni,key=lambda r:(r['negatives_at_or_above'],-r['auc_all'],max(r['ranks'].values())))

models={
 'logistic_l2':make_pipeline(StandardScaler(),LogisticRegression(C=1.0,solver='liblinear',class_weight='balanced',random_state=20260916)),
 'tree_depth2':DecisionTreeClassifier(max_depth=2,min_samples_leaf=2,class_weight='balanced',random_state=20260916),
 'rf_depth3':RandomForestClassifier(n_estimators=500,max_depth=3,min_samples_leaf=2,max_features='sqrt',class_weight='balanced_subsample',random_state=20260916,n_jobs=-1),
}
modelres={}
for name,m in models.items():
 m.fit(Xu,yu); s=m.predict_proba(Xu)[:,1];modelres[name]=metric(s,au)
 if name=='logistic_l2':
  co=m[-1].coef_[0]
  modelres[name]['top_coefficients']=[{'feature':names[i],'coefficient':float(co[i])} for i in np.argsort(np.abs(co))[::-1][:12]]
 elif name=='tree_depth2':
  modelres[name]['feature_importance']=[{'feature':names[i],'importance':float(m.feature_importances_[i])} for i in np.argsort(m.feature_importances_)[::-1][:8] if m.feature_importances_[i]>0]
 else:
  modelres[name]['feature_importance']=[{'feature':names[i],'importance':float(m.feature_importances_[i])} for i in np.argsort(m.feature_importances_)[::-1][:12]]

out={'univariate_top20':uni[:20],'models_full_fit_descriptive_only':modelres}
(ROOT/'classical_controls.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
