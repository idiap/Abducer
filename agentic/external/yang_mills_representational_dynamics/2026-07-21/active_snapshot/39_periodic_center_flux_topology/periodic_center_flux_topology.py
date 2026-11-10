"""Periodic 2^4 cubical GF(2) cohomology and explicit center-flux carriers."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import argparse,itertools,json
from typing import Any
import numpy as np
L=2;DIM=4

def shift(x:tuple[int,...],mu:int)->tuple[int,...]:
 y=list(x);y[mu]=(y[mu]+1)%L;return tuple(y)
def gf2_rank(matrix:np.ndarray)->int:
 a=np.asarray(matrix,dtype=np.uint8).copy()%2;r=0
 for c in range(a.shape[1]):
  piv=np.flatnonzero(a[r:,c])
  if len(piv)==0:continue
  p=r+int(piv[0]);a[[r,p]]=a[[p,r]]
  for i in range(a.shape[0]):
   if i!=r and a[i,c]:a[i]^=a[r]
  r+=1
  if r==a.shape[0]:break
 return r

@dataclass(frozen=True)
class TopologyCertificate:
 vertices:int;edges:int;plaquettes:int;three_cells:int;four_cells:int
 ranks:tuple[int,int,int,int];betti_numbers:tuple[int,int,int,int,int]
 consecutive_compositions_zero:bool; flux_representatives:int; augmented_exact_rank:int
 independent_flux_classes:bool; center_flux_sectors:int; integer_instanton_charge_represented:bool
 def to_dict(self)->dict[str,Any]:return asdict(self)

def periodic_complex():
 V=tuple(itertools.product(range(L),repeat=DIM));E=tuple((x,m) for x in V for m in range(DIM));P=tuple((x,a,b) for x in V for a,b in itertools.combinations(range(DIM),2));C=tuple((x,a,b,c) for x in V for a,b,c in itertools.combinations(range(DIM),3));Q=V
 vi={x:i for i,x in enumerate(V)};ei={e:i for i,e in enumerate(E)};pi={p:i for i,p in enumerate(P)};ci={c:i for i,c in enumerate(C)}
 d0=np.zeros((len(E),len(V)),np.uint8)
 for i,(x,m) in enumerate(E):d0[i,vi[x]]=1;d0[i,vi[shift(x,m)]]^=1
 d1=np.zeros((len(P),len(E)),np.uint8)
 for i,(x,a,b) in enumerate(P):
  for e in ((x,a),(shift(x,a),b),(shift(x,b),a),(x,b)):d1[i,ei[e]]^=1
 d2=np.zeros((len(C),len(P)),np.uint8)
 for i,(x,a,b,c) in enumerate(C):
  dirs=(a,b,c)
  for n in dirs:
   pair=tuple(d for d in dirs if d!=n)
   d2[i,pi[(x,*pair)]]^=1;d2[i,pi[(shift(x,n),*pair)]]^=1
 d3=np.zeros((len(Q),len(C)),np.uint8)
 for i,x in enumerate(Q):
  for n in range(DIM):
   triple=tuple(d for d in range(DIM) if d!=n)
   d3[i,ci[(x,*triple)]]^=1;d3[i,ci[(shift(x,n),*triple)]]^=1
 return V,E,P,C,Q,d0,d1,d2,d3

def flux_representatives()->np.ndarray:
 V,E,P,C,Q,d0,d1,d2,d3=periodic_complex();pi={p:i for i,p in enumerate(P)};cols=[]
 for a,b in itertools.combinations(range(DIM),2):
  y=np.zeros(len(P),np.uint8)
  for x in V:
   if x[a]==L-1 and x[b]==L-1:y[pi[(x,a,b)]]=1
  cols.append(y)
 return np.column_stack(cols)

def certificate()->TopologyCertificate:
 V,E,P,C,Q,d0,d1,d2,d3=periodic_complex();r=(gf2_rank(d0),gf2_rank(d1),gf2_rank(d2),gf2_rank(d3))
 b=(len(V)-r[0],len(E)-r[1]-r[0],len(P)-r[2]-r[1],len(C)-r[3]-r[2],len(Q)-r[3])
 reps=flux_representatives();zero=not (d1@d0%2).any() and not (d2@d1%2).any() and not (d3@d2%2).any();aug=gf2_rank(np.column_stack((d1,reps)))
 return TopologyCertificate(len(V),len(E),len(P),len(C),len(Q),r,b,zero,reps.shape[1],aug,not (d2@reps%2).any() and aug==r[1]+6,2**6,False)
def calibration()->dict[str,Any]:return {"claim_level":"C2 exact periodic GF(2) cohomology and center-flux carrier","certificate":certificate().to_dict(),"flux_labels":[f"z_{a}{b}" for a,b in itertools.combinations(range(4),2)],"scope":"center two-flux sectors only; integer second-Chern/instanton charge is not represented"}
def main()->None:argparse.ArgumentParser().parse_args();print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__":main()
