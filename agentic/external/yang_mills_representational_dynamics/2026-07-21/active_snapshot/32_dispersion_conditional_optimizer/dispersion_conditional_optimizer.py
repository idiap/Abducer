"""Finite-time conditional optimization indexed by exact staple dispersion."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import argparse,json,math,sys
from pathlib import Path
from typing import Any
PACKAGE=Path(__file__).resolve().parents[1]
for s in ("28_coherent_partition_optimizer","29_coherence_charge_tradeoff"):
 p=PACKAGE/s
 if str(p) not in sys.path: sys.path.insert(0,str(p))
from coherent_partition_optimizer import optimize_delta,HEAT_TIME,INCIDENT_STAPLES,TARGET_WEIGHTED_CEILING
from coherence_charge_tradeoff import coherent_eta_ceiling

@dataclass(frozen=True)
class DispersionConditionalCertificate:
 dispersion:float; effective_rms_radius:float; incident_staples:int; curvature_radius:float
 selected_delta:float; denominator_energy_upper:float; finite_time_gap:float
 log_probability_upper:float; probability_upper:float; target_probability:float
 target_met:bool; high_dispersion_action_exponent:float
 frechet_minimizer_assumed_attained:bool; high_dispersion_partition_bound_proved:bool
 def to_dict(self)->dict[str,Any]:return asdict(self)

def certificate(dispersion:float,curvature_radius:float,target:float=TARGET_WEIGHTED_CEILING,heat_time:float=HEAT_TIME,incident_staples:int=INCIDENT_STAPLES)->DispersionConditionalCertificate:
 D=float(dispersion);rho=float(curvature_radius);q=float(target);t=float(heat_time);m=int(incident_staples)
 if not math.isfinite(D) or D<0 or not math.isfinite(rho) or rho<=0 or not 0<q<1 or t<=0 or m<2: raise ValueError("invalid dispersion certificate input")
 eta=math.sqrt(D/m)
 opt=optimize_delta(t,rho,eta,m)
 upper=(math.sqrt(D)+math.sqrt(m)*opt.selected_delta)**2
 gap=rho*rho-upper
 return DispersionConditionalCertificate(D,eta,m,rho,opt.selected_delta,upper,gap,opt.log_probability_upper,opt.probability_upper,q,opt.probability_upper<q,D/(2*t),True,False)

def maximum_dispersion_for_target(curvature_radius:float,target:float=TARGET_WEIGHTED_CEILING)->float:
 eta=coherent_eta_ceiling(curvature_radius,target)
 return INCIDENT_STAPLES*eta*eta

def calibration()->dict[str,Any]:
 rho=2*0.011453785959974176
 Dmax=maximum_dispersion_for_target(rho)
 strict=certificate(.99*.99*Dmax,rho)
 return {"claim_level":"C2 dispersion-aware conditional theorem and finite optimization",
 "maximum_dispersion_for_target":Dmax,"maximum_effective_rms_radius":math.sqrt(Dmax/INCIDENT_STAPLES),
 "strict_low_dispersion_certificate":strict.to_dict(),"identity":"(sqrt(D)+sqrt(m)delta)^2=m(sqrt(D/m)+delta)^2",
 "high_dispersion_action_exponent_at_boundary":Dmax/(2*HEAT_TIME),
 "low_dispersion_channel_closed_conditionally":strict.target_met,
 "high_dispersion_normalized_partition_bound_proved":False,"complete_su2_kernel_proved":False}
def main()->None: argparse.ArgumentParser().parse_args();print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__":main()
