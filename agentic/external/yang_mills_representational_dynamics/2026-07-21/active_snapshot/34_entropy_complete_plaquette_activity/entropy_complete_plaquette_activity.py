"""Action-only versus radial-entropy-complete plaquette activities."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import argparse,json,math,sys
from pathlib import Path
from typing import Any
PACKAGE=Path(__file__).resolve().parents[1];p=PACKAGE/"13_dependent_gaussian_polymers"
if str(p) not in sys.path:sys.path.insert(0,str(p))
from dependent_gaussian_polymers import radial_gaussian_rate
T=3e-6;DEGREE=20;ALPHA=.1;F_REQUIRED=6.712921011389365

@dataclass(frozen=True)
class ActivityCertificate:
 radius:float; normalized_radius_squared:float; bare_action_rate:float; radial_entropy_rate:float
 radial_entropy_deficit:float; degree:int; action_branching_ratio:float; entropy_branching_ratio:float
 action_only_convergent:bool; entropy_complete_convergent:bool; entropy_complete_root_free_energy:float|None
 def to_dict(self)->dict[str,Any]:return asdict(self)

def certificate(radius:float,time:float=T,degree:int=DEGREE,alpha:float=ALPHA)->ActivityCertificate:
 r=float(radius);t=float(time);d=int(degree);a=float(alpha)
 if not math.isfinite(r) or r<=0 or t<=0 or d<2 or a<0:raise ValueError("invalid activity input")
 s=r*r/t;bare=.5*s;rad=radial_gaussian_rate(s,3)
 ta=math.exp(a)*d*d*math.exp(-bare);te=math.exp(a)*d*d*math.exp(-rad)
 f=rad-a+math.log(1-te) if te<1 else None
 return ActivityCertificate(r,s,bare,rad,bare-rad,d,ta,te,ta<1,te<1,f)

def radius_for_rate(target_rate:float,time:float=T)->float:
 target=float(target_rate)
 if not math.isfinite(target) or target<=0:raise ValueError("target rate positive")
 lo=math.sqrt(3*time);hi=.05
 for _ in range(120):
  m=(lo+hi)/2
  if radial_gaussian_rate(m*m/time,3)<target:lo=m
  else:hi=m
 return hi

def radius_for_root_free_energy(required:float=F_REQUIRED)->float:
 req=float(required);lo=radius_for_rate(ALPHA+2*math.log(DEGREE));hi=.05
 for _ in range(120):
  m=(lo+hi)/2
  value=certificate(m).entropy_complete_root_free_energy
  if value is None or value<req:lo=m
  else:hi=m
 return hi

def calibration()->dict[str,Any]:
 eta=.007171451491488068;c=certificate(eta);rconv=radius_for_rate(ALPHA+2*math.log(DEGREE));rfree=radius_for_root_free_energy()
 return {"claim_level":"C2 Gaussian radial-entropy theorem plus finite threshold calibration","coherent_eta_activity":c.to_dict(),"entropy_convergence_radius":rconv,"required_free_energy_radius":rfree,"gap_from_coherent_eta_to_required_radius":rfree-eta,"action_only_would_close":c.action_only_convergent,"entropy_complete_closes":c.entropy_complete_root_free_energy is not None and c.entropy_complete_root_free_energy>F_REQUIRED,"nonlinear_su2_partition_activity_proved":False}
def main()->None:argparse.ArgumentParser().parse_args();print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__":main()
