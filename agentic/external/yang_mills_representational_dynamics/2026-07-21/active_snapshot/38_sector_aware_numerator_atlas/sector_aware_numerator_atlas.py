"""Exact multichannel union and free-energy allocation laws."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import argparse,json,math
from typing import Sequence,Any
CHANNELS=("center","continuous_low_dispersion","continuous_high_dispersion","cut_orbit","topology")

@dataclass(frozen=True)
class AllocationCertificate:
 channels:tuple[str,...]; target_ceiling:float; shares:tuple[float,...]; channel_ceilings:tuple[float,...]
 required_free_energies:tuple[float,...]; union_ceiling:float; exact_budget_exhausted:bool
 ownership_labels_retained:bool; physical_channel_bounds_proved:bool
 def to_dict(self)->dict[str,Any]:return asdict(self)

def union_ceiling(channel_ratios:Sequence[float])->float:
 r=tuple(float(x) for x in channel_ratios)
 if not r or any(not math.isfinite(x) or x<0 for x in r):raise ValueError("invalid channel ratios")
 return math.fsum(r)
def allocation_certificate(target:float,shares:Sequence[float],comparison_losses:Sequence[float]|None=None)->AllocationCertificate:
 q=float(target);s=tuple(float(x) for x in shares);ell=tuple(float(x) for x in (comparison_losses if comparison_losses is not None else [0]*len(s)))
 if not 0<q<1 or len(s)!=len(CHANNELS) or len(ell)!=len(s) or any(x<=0 or not math.isfinite(x) for x in s) or any(x<0 or not math.isfinite(x) for x in ell) or abs(sum(s)-1)>1e-12:raise ValueError("invalid allocation")
 ceilings=tuple(q*x for x in s);F=tuple(ell[i]-math.log(ceilings[i]) for i in range(len(s)))
 return AllocationCertificate(CHANNELS,q,s,ceilings,F,sum(ceilings),abs(sum(ceilings)-q)<1e-14,True,False)
def channel_status()->tuple[dict[str,Any],...]:
 statuses=("restricted center contour","conditional low-dispersion closure","restricted Gaussian dispersion polymer","finite orbit atlas only","center-flux carrier constructed at Stage 39")
 return tuple({"channel":c,"status":s,"physical_uniform_bound":False} for c,s in zip(CHANNELS,statuses))
def calibration()->dict[str,Any]:
 q=.002430277501841998;equal=allocation_certificate(q,[.2]*5,[2.7e-5,2.7e-5,0,0,0]);weighted=allocation_certificate(q,[.05,.35,.35,.1,.15])
 return {"claim_level":"C2 exact multichannel partition-budget theorem","equal_allocation":equal.to_dict(),"illustrative_weighted_allocation":weighted.to_dict(),"channel_status":channel_status(),"single_total_free_energy":-math.log(q),"equal_channel_free_energy_without_loss":-math.log(q/5),"physical_union_bound_proved":False}
def main()->None:argparse.ArgumentParser().parse_args();print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__":main()
