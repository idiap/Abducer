"""Exact finite-block spectra and Chernoff tails for staple dispersion."""
from __future__ import annotations
from dataclasses import asdict,dataclass
from functools import lru_cache
import argparse,json,math,sys
from pathlib import Path
from typing import Any
import numpy as np
PACKAGE=Path(__file__).resolve().parents[1]
for s in ("08_su2_nonlinear_block_geometry","13_dependent_gaussian_polymers"):
 p=PACKAGE/s
 if str(p) not in sys.path:sys.path.insert(0,str(p))
from su2_nonlinear_block_geometry import build_block_complex
from dependent_gaussian_polymers import curvature_projection
T=3e-6;DEGREE=18;ALPHA=.1;F_REQUIRED=6.712921011389365

@dataclass(frozen=True)
class SpectrumCertificate:
 six_staple_links:int; nonzero_eigenvalues:tuple[float,...]; trace:float; maximum_eigenvalue:float
 covariance_contraction_used:bool; color_multiplicity:int
 def to_dict(self)->dict[str,Any]:return asdict(self)
@dataclass(frozen=True)
class DispersionTailCertificate:
 effective_rms_radius:float; dispersion_threshold:float; rate_lower:float; probability_upper:float
 branching_ratio:float; rooted_free_energy_lower:float; entropy_convergent:bool; required_free_energy_met:bool
 dependence_retained:bool; nonlinear_su2_transfer_proved:bool
 def to_dict(self)->dict[str,Any]:return asdict(self)

@lru_cache(maxsize=1)
def six_link_spectra()->tuple[tuple[float,...],...]:
 b=build_block_complex();P=curvature_projection();support=np.abs(b.d1)>0;out=[]
 for l in range(len(b.edges)):
  idx=np.flatnonzero(support[:,l]);m=len(idx)
  if m!=6:continue
  C=np.eye(m)-np.ones((m,m))/m;vals=np.linalg.eigvalsh(C@P[np.ix_(idx,idx)]@C)
  # Canonicalize the published finite spectrum.  Different LAPACK reduction
  # paths can otherwise vary the last one or two bits between runs.
  out.append(tuple(round(float(x),14) for x in vals if x>1e-10))
 return tuple(out)

def spectrum_certificate()->SpectrumCertificate:
 spectra=six_link_spectra();ref=spectra[0]
 if max(max(abs(a-b) for a,b in zip(v,ref)) for v in spectra)>1e-10:raise ArithmeticError("interior spectra differ")
 return SpectrumCertificate(len(spectra),ref,sum(ref),max(ref),True,3)

def chernoff_rate(eigenvalues:tuple[float,...],threshold:float,time:float=T)->float:
 D=float(threshold);t=float(time);v=tuple(float(x) for x in eigenvalues)
 if D<0 or t<=0 or not v or min(v)<=0:raise ValueError("invalid Chernoff input")
 mean=3*t*sum(v)
 if D<=mean:return 0.0
 lo=0.;hi=(1-1e-12)/(2*t*max(v))
 for _ in range(120):
  lam=(lo+hi)/2;der=D-3*t*sum(x/(1-2*lam*t*x) for x in v)
  if der>0:lo=lam
  else:hi=lam
 lam=(lo+hi)/2
 return lam*D+1.5*sum(math.log(1-2*lam*t*x) for x in v)

def tail_certificate(effective_rms_radius:float)->DispersionTailCertificate:
 eta=float(effective_rms_radius)
 if not math.isfinite(eta) or eta<=0:raise ValueError("effective radius positive")
 D=6*eta*eta;rate=min(chernoff_rate(v,D) for v in six_link_spectra());q=math.exp(-rate)
 theta=math.exp(ALPHA)*DEGREE*DEGREE*q
 f=rate-ALPHA+math.log(1-theta) if theta<1 else -math.inf
 return DispersionTailCertificate(eta,D,rate,q,theta,f,theta<1,f>F_REQUIRED,True,False)

def radius_for_free_energy(required:float=F_REQUIRED)->float:
 req=float(required);lo=1e-6;hi=.02
 for _ in range(120):
  m=(lo+hi)/2
  if tail_certificate(m).rooted_free_energy_lower<req:lo=m
  else:hi=m
 return hi

def calibration()->dict[str,Any]:
 lower=radius_for_free_energy();upper=.007171451491488068;at_upper=tail_certificate(upper)
 return {"claim_level":"C2 exact dependent-Gaussian dispersion spectrum and polymer theorem","spectrum":spectrum_certificate().to_dict(),"minimum_rms_radius_for_required_free_energy":lower,"maximum_rms_radius_for_coherent_channel":upper,"feasible_interval_width":upper-lower,"common_dispersion_parameter_exists":lower<upper,"upper_endpoint_tail":at_upper.to_dict(),"selected_midpoint_tail":tail_certificate((lower+upper)/2).to_dict(),"complete_nonlinear_su2_transfer_proved":False}
def main()->None:argparse.ArgumentParser().parse_args();print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__":main()
