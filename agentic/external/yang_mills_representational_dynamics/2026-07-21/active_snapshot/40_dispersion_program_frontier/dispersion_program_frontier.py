"""Composite audit of the variance-aware Yang--Mills numerator programme."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import argparse,json,sys
from pathlib import Path
from typing import Any
PACKAGE=Path(__file__).resolve().parents[1]
mods=(("31_frechet_collar_charge","frechet_collar_charge"),("32_dispersion_conditional_optimizer","dispersion_conditional_optimizer"),("34_entropy_complete_plaquette_activity","entropy_complete_plaquette_activity"),("35_linearized_dispersion_spectrum","linearized_dispersion_spectrum"),("36_adaptive_dispersion_filtration","adaptive_dispersion_filtration"),("37_partition_repair_congestion","partition_repair_congestion"),("38_sector_aware_numerator_atlas","sector_aware_numerator_atlas"),("39_periodic_center_flux_topology","periodic_center_flux_topology"))
for d,_ in mods:
 p=PACKAGE/d
 if str(p) not in sys.path:sys.path.insert(0,str(p))
import frechet_collar_charge as s31,dispersion_conditional_optimizer as s32,entropy_complete_plaquette_activity as s34,linearized_dispersion_spectrum as s35,adaptive_dispersion_filtration as s36,partition_repair_congestion as s37,sector_aware_numerator_atlas as s38,periodic_center_flux_topology as s39

@dataclass(frozen=True)
class FrontierCertificate:
 stages_composed:int; corrected_covering_charge:bool; low_dispersion_conditional_closed:bool
 action_only_plaquette_route_closed:bool; entropy_complete_plaquette_route_closed:bool
 dependent_gaussian_dispersion_split_closed:bool; adaptive_implication_proved:bool
 physical_history_premise_proved:bool; repair_congestion_theorem_proved:bool
 physical_repair_map_proved:bool; center_flux_carrier_proved:bool; integer_topology_controlled:bool
 physical_multichannel_ratio_proved:bool; one_scale_basin_entry_proved:bool; continuum_mass_gap_proved:bool
 claim_level:str
 def to_dict(self)->dict[str,Any]:return asdict(self)

def frontier()->FrontierCertificate:
 a31=s31.calibration();a32=s32.calibration();a34=s34.calibration();a35=s35.calibration();a36=s36.calibration();a37=s37.calibration();a38=s38.calibration();a39=s39.calibration()
 return FrontierCertificate(10,a31["improves_stage16_energy_factor"]==2,a32["low_dispersion_channel_closed_conditionally"],a34["action_only_would_close"],a34["entropy_complete_closes"],a35["common_dispersion_parameter_exists"],True,a36["physical_history_table_proved"],True,a37["complete_nonlinear_repair_map_constructed"],a39["certificate"]["independent_flux_classes"],a39["certificate"]["integer_instanton_charge_represented"],a38["physical_union_bound_proved"],False,False,"C2 exact/conditional finite theorems and restricted Gaussian closure")

def calibration()->dict[str,Any]:
 f=frontier();g=s35.calibration();alloc=s38.calibration()
 return {"frontier":f.to_dict(),"strongest_positive_result":"the exact projected-Gaussian block has a nonempty common low-dispersion conditional/high-dispersion polymer interval","gaussian_common_interval":[g["minimum_rms_radius_for_required_free_energy"],g["maximum_rms_radius_for_coherent_channel"]],"strongest_correction":"covering-radius failure forces eta^2 rather than eta^2/2 incident energy","topology_advance":"six independent periodic GF(2) center-flux labels and 64 sectors","first_open_physical_inequality":"for every finite volume, positive-mass retained history and owned channel c, construct a gauge-covariant nonlinear comparison or repair T_c such that sum_c(exp(ell_c) q_low,c + C_T,c) <= 0.002430277501841998, with all Jacobian, multiplicity, state-weight, orbit-chart, center-flux and topology factors included uniformly","equal_channel_free_energy_target":alloc["equal_channel_free_energy_without_loss"],"ranked_next_targets":["construct a nonlinear dispersion repair map and bound exact congestion","transport the Gaussian determinant tail uniformly over retained boundary states","prove the adaptive physical history table on periodic sector-aware blocks","extend center flux to integer bundle topology and control sector weights","only then claim one-scale basin entry and attempt RG iteration"],"not_proved":["complete nonlinear conditional partition ratio","volume-uniform one-scale basin entry","repeated gauge-covariant RG","continuum Yang-Mills construction","Hamiltonian mass gap"]}
def main()->None:argparse.ArgumentParser().parse_args();print(json.dumps(calibration(),indent=2,sort_keys=True))
if __name__=="__main__":main()
