"""Adaptive retained-state filtration for dispersion witnesses."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import argparse,json,math
from typing import Mapping,Sequence,Any

@dataclass(frozen=True)
class RetainedStateSchema:
 dispersion_class:bool=True; frechet_center_chart:bool=True; center_flux:bool=True
 boundary_holonomy:bool=True; orbit_chart:bool=True; topology_sector:bool=True
 def to_dict(self)->dict[str,bool]:return asdict(self)
@dataclass(frozen=True)
class AdaptiveCertificate:
 exposure_steps:int; histories_required:int; histories_supplied:int; maximum_conditional_probability:float
 target_ceiling:float; history_uniform:bool; bernoulli_domination_certified:bool
 branching_ratio:float; rooted_sum_upper:float; strict_cluster_subcritical:bool
 positive_mass_histories_only:bool; complete_nonlinear_measure_verified:bool
 def to_dict(self)->dict[str,Any]:return asdict(self)

def adaptive_certificate(table:Mapping[tuple[int,...],float],steps:int,target:float,degree:int=18,alpha:float=.1)->AdaptiveCertificate:
 n=int(steps);q=float(target);d=int(degree);a=float(alpha)
 if n<1 or not 0<q<1 or d<1 or a<0:raise ValueError("invalid adaptive input")
 required={h for k in range(n) for h in __import__('itertools').product((0,1),repeat=k)}
 supplied=set(table);vals=[]
 for h,p in table.items():
  x=float(p)
  if h not in required or not math.isfinite(x) or not 0<=x<=1:raise ValueError("invalid history table")
  vals.append(x)
 complete=supplied==required;maximum=max(vals,default=0);uniform=complete and maximum<=q
 theta=math.exp(a)*d*d*q;root=math.exp(a)*q/(1-theta) if theta<1 else math.inf
 return AdaptiveCertificate(n,len(required),len(supplied),maximum,q,uniform,uniform,theta,root,theta<1,True,False)

def split_ceiling(low_dispersion:float,high_dispersion:float,target:float)->dict[str,float|bool]:
 lo=float(low_dispersion);hi=float(high_dispersion);q=float(target)
 if min(lo,hi)<0 or not 0<q<1:raise ValueError("invalid split")
 return {"low_dispersion_ceiling":lo,"high_dispersion_ceiling":hi,"combined_ceiling":lo+hi,"target":q,"target_met":lo+hi<=q}

def moment_only_counterexample()->dict[str,Any]:
 return {"P00":0.,"P01":.5,"P10":.5,"P11":0.,"marginal_bad_probability":.5,"conditional_second_bad_given_first_good":1.,"dominated_by_bernoulli_half":False}
def erased_state_counterexample()->dict[str,Any]:
 return {"retained_states":2,"same_erased_label":True,"conditional_probabilities":[0.,1.],"erased_scalar_ceiling":1.,"state_erasure_preserves_rare_entry":False}
def calibration()->dict[str,Any]:
 q=.002430277501841998;table={():.0012,(0,):.0012,(1,):.0012}
 cert=adaptive_certificate(table,2,q)
 return {"claim_level":"C2 exact adaptive coupling interface plus illustrative restricted calibration","retained_schema":RetainedStateSchema().to_dict(),"illustrative_history_certificate":cert.to_dict(),"illustrative_dispersion_split":split_ceiling(.0012,5.510583579299742e-10,q),"moment_counterexample":moment_only_counterexample(),"erased_state_counterexample":erased_state_counterexample(),"physical_history_table_proved":False}
def main()->None:argparse.ArgumentParser().parse_args();print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__":main()
