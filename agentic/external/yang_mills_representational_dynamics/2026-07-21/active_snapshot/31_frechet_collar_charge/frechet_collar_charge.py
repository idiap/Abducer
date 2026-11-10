"""Exact Fréchet-dispersion and covering-radius charges for staple collars."""

from __future__ import annotations
from dataclasses import asdict, dataclass
import argparse, json, math
from typing import Iterable, Any

HEAT_TIME=3.0e-6

@dataclass(frozen=True)
class CoveringChargeCertificate:
    coherence_radius: float
    heat_time: float
    old_energy_charge: float
    corrected_energy_charge: float
    old_gibbs_exponent: float
    corrected_gibbs_exponent: float
    exponent_amplification: float
    link_value_uniform: bool
    gauge_invariant: bool
    normalized_probability_proved: bool
    def to_dict(self)->dict[str,Any]: return asdict(self)

@dataclass(frozen=True)
class CommutingFrechetCertificate:
    staple_count:int
    frechet_center:float
    link_energy_minimizer:float
    frechet_dispersion:float
    minimum_link_energy:float
    covering_radius:float
    identity_error:float
    def to_dict(self)->dict[str,Any]: return asdict(self)

def _positive(name:str,x:float)->float:
    x=float(x)
    if not math.isfinite(x) or x<=0: raise ValueError(f"{name} must be finite and positive")
    return x

def commuting_frechet_certificate(staple_angles:Iterable[float])->CommutingFrechetCertificate:
    q=tuple(float(x) for x in staple_angles)
    if len(q)<2 or any(not math.isfinite(x) for x in q): raise ValueError("at least two finite angles required")
    if max(q)-min(q)>=math.pi: raise ValueError("angles must stay in one convex chart")
    center=math.fsum(q)/len(q)
    dispersion=math.fsum((x-center)**2 for x in q)
    u=-center
    energy=math.fsum((u+x)**2 for x in q)
    radius=0.5*(max(q)-min(q))
    return CommutingFrechetCertificate(len(q),center,u,dispersion,energy,radius,abs(energy-dispersion))

def covering_charge_certificate(coherence_radius:float,heat_time:float=HEAT_TIME)->CoveringChargeCertificate:
    eta=_positive("coherence_radius",coherence_radius); t=_positive("heat_time",heat_time)
    old=eta*eta/2.0; corrected=eta*eta
    return CoveringChargeCertificate(eta,t,old,corrected,old/(2*t),corrected/(2*t),2.0,True,True,False)

def frechet_energy_lower_bound(dispersion_lower:float)->float:
    d=float(dispersion_lower)
    if not math.isfinite(d) or d<0: raise ValueError("dispersion lower bound must be nonnegative")
    return d

def calibration()->dict[str,Any]:
    eta=0.007171451491488068
    return {
      "claim_level":"C2 exact metric-group collar identities plus finite calibration",
      "covering_charge":covering_charge_certificate(eta).to_dict(),
      "commuting_example":commuting_frechet_certificate((-eta,-eta/2,0,0,eta/2,eta)).to_dict(),
      "theorem":"E_U=sum_i d(I,US_i)^2=Phi(U^{-1}); if no eta-ball contains the staples then E_U>eta^2 for every U",
      "improves_stage16_energy_factor":2.0,
      "haar_radial_entropy_included":False,
      "complete_partition_ratio_proved":False
    }

def main()->None:
    argparse.ArgumentParser().parse_args(); print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__": main()
