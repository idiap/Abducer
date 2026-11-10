"""Exact finite repair-map congestion bounds for weighted partition numerators."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import argparse,json,math
from typing import Sequence,Any
import numpy as np

@dataclass(frozen=True)
class RepairCertificate:
 good_states:int; bad_states:int; maximum_fiber_multiplicity:int; exact_weighted_bad_numerator:float
 good_partition:float; exact_congestion:float; exact_ratio_to_good:float; congestion_bound_verified:bool
 positive_weights:bool; full_normalizer_used:bool; physical_repair_map_verified:bool
 def to_dict(self)->dict[str,Any]:return asdict(self)

def repair_certificate(good_weights:Sequence[float],bad_weights:Sequence[float],next_state_weights:Sequence[float],repair_targets:Sequence[int],current_weight:float=1.0)->RepairCertificate:
 g=np.asarray(good_weights,float);b=np.asarray(bad_weights,float);v=np.asarray(next_state_weights,float);targets=np.asarray(repair_targets,int);V=float(current_weight)
 if g.ndim!=1 or len(g)==0 or b.ndim!=1 or len(b)==0 or v.shape!=b.shape or targets.shape!=b.shape or not np.all(np.isfinite(g)) or not np.all(np.isfinite(b)) or not np.all(np.isfinite(v)) or np.any(g<=0) or np.any(b<0) or np.any(v<=0) or V<=0 or np.any(targets<0) or np.any(targets>=len(g)):raise ValueError("invalid repair data")
 numerators=np.zeros(len(g));counts=np.zeros(len(g),int)
 for i,j in enumerate(targets):numerators[j]+=b[i]*v[i];counts[j]+=1
 congestion=float(np.max(numerators/(g*V)));B=float(np.sum(b*v));ZG=float(np.sum(g));ratio=B/(ZG*V)
 return RepairCertificate(len(g),len(b),int(np.max(counts)),B,ZG,congestion,ratio,ratio<=congestion+1e-14,True,False,False)

def multiplicity_energy_bound(multiplicity:int,energy_drop:float,jacobian_loss:float=0.0)->dict[str,float|bool]:
 M=int(multiplicity);D=float(energy_drop);J=float(jacobian_loss)
 if M<1 or not math.isfinite(D) or D<0 or not math.isfinite(J) or J<0:raise ValueError("invalid multiplicity-energy input")
 bound=M*math.exp(J-D)
 return {"multiplicity":M,"energy_drop":D,"log_jacobian_loss":J,"congestion_upper":bound,"free_energy_lower":D-J-math.log(M),"strictly_subunit":bound<1}
def entropy_counterexample(charge:float=10)->dict[str,Any]:
 M=math.ceil(math.exp(charge));bound=multiplicity_energy_bound(M,charge)
 return {"charge":charge,"multiplicity":M,"congestion_upper":bound["congestion_upper"],"action_only_sufficient":False}
def calibration()->dict[str,Any]:
 c=repair_certificate([1,2],[1e-4,2e-4],[2,1],[0,1],1)
 cor=multiplicity_energy_bound(2,8)
 return {"claim_level":"C2 exact finite repair-congestion theorem","finite_exact_example":c.to_dict(),"multiplicity_energy_example":cor,"entropy_counterexample":entropy_counterexample(),"required_physical_free_energy":6.712921011389365,"complete_nonlinear_repair_map_constructed":False}
def main()->None:argparse.ArgumentParser().parse_args();print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__":main()
