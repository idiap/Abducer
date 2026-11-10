"""Canonical gauge-invariant plaquette witnesses for failed link collars."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import argparse,json,math,sys
from pathlib import Path
from typing import Iterable,Any
import numpy as np
PACKAGE=Path(__file__).resolve().parents[1]
for s in ("08_su2_nonlinear_block_geometry","12_center_contour_charging"):
 p=PACKAGE/s
 if str(p) not in sys.path:sys.path.insert(0,str(p))
from su2_nonlinear_block_geometry import build_block_complex
from center_contour_charging import plaquette_adjacency

@dataclass(frozen=True)
class WitnessCertificate:
 failed_links:int; distinct_witnesses:int; maximum_witness_multiplicity:int
 incidence_capacity:int; distinct_lower_bound:int; minimum_witness_curvature:float
 threshold:float; gauge_invariant:bool; capacity_bound_met:bool
 def to_dict(self)->dict[str,Any]:return asdict(self)

def incidence_sets()->tuple[tuple[int,...],...]:
 b=build_block_complex();support=np.abs(b.d1)>0
 return tuple(tuple(int(x) for x in np.flatnonzero(support[:,l])) for l in range(len(b.edges)))

def plaquette_boundary_links()->tuple[tuple[int,...],...]:
 b=build_block_complex();support=np.abs(b.d1)>0
 return tuple(tuple(int(x) for x in np.flatnonzero(support[p])) for p in range(len(b.plaquettes)))

def canonical_witnesses(curvature_radii:Iterable[float],failed_links:Iterable[int],threshold:float)->tuple[int,...]:
 r=np.asarray(tuple(curvature_radii),dtype=float);eta=float(threshold);inc=incidence_sets()
 if r.shape!=(len(plaquette_boundary_links()),) or not np.all(np.isfinite(r)) or np.any(r<0) or not math.isfinite(eta) or eta<=0:raise ValueError("invalid curvature or threshold")
 out=[]
 for link in tuple(int(x) for x in failed_links):
  if link<0 or link>=len(inc):raise ValueError("invalid link")
  candidates=inc[link];maximum=max(r[p] for p in candidates)
  if maximum<=eta:raise ValueError("failed collar lacks the required curvature witness")
  out.append(min(p for p in candidates if r[p]==maximum))
 return tuple(out)

def witness_certificate(curvature_radii:Iterable[float],failed_links:Iterable[int],threshold:float)->WitnessCertificate:
 links=tuple(int(x) for x in failed_links);w=canonical_witnesses(curvature_radii,links,threshold)
 counts={p:w.count(p) for p in set(w)};capacity=max(len(x) for x in plaquette_boundary_links())
 distinct=len(counts);lower=math.ceil(len(links)/capacity) if links else 0
 return WitnessCertificate(len(links),distinct,max(counts.values(),default=0),capacity,lower,min((tuple(curvature_radii)[p] for p in w),default=math.inf),float(threshold),True,max(counts.values(),default=0)<=capacity and distinct>=lower)

def calibration()->dict[str,Any]:
 b=build_block_complex();bounds=plaquette_boundary_links();p=next(i for i,x in enumerate(bounds) if len(x)==4)
 r=np.zeros(len(b.plaquettes));r[p]=1.0
 cert=witness_certificate(r,bounds[p],.5)
 adj=plaquette_adjacency()
 return {"claim_level":"C2 exact finite incidence and canonical witness theorem","links":len(b.edges),"plaquettes":len(b.plaquettes),"incidence_capacity":max(map(len,bounds)),"bianchi_plaquette_degree":max(map(len,adj)),"capacity_four_sharpness":cert.to_dict(),"physical_history_uniform_selection_proved":False}
def main()->None:argparse.ArgumentParser().parse_args();print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__":main()
