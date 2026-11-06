"""OpenEngineering Toolkit - Verified computational mechanics and aerospace sizing library."""
from __future__ import annotations

from .aerospace import (
    aspect_ratio,
    mass_to_weight_newtons,
    thrust_to_weight_ratio,
    wing_loading_n_m2,
)
from .beam import (
    bending_stress_magnitude,
    simply_supported_center_load_max_deflection,
    simply_supported_center_load_max_moment,
)
from .compressible import (
    critical_area_ratio,
    normal_shock_mach,
    normal_shock_pressure_ratio,
    normal_shock_stagnation_pressure_ratio,
    prandtl_meyer_angle_deg,
    stagnation_density_ratio,
    stagnation_temperature_ratio,
)
from .fluids import (
    dynamic_pressure_pa,
    haaland_friction_factor,
    mach_number,
    reynolds_number,
    stagnation_pressure_ratio,
)
from .mechanics import factor_of_safety, normal_strain, normal_stress
from .propulsion import (
    characteristic_velocity_star,
    rocket_thrust_n,
    thrust_coefficient_ideal,
    tsiolkovsky_delta_v,
)
from .units import convert_force, convert_length, convert_pressure

__version__ = "0.3.0"
__all__ = [
    "aspect_ratio",
    "bending_stress_magnitude",
    "characteristic_velocity_star",
    "convert_force",
    "convert_length",
    "convert_pressure",
    "critical_area_ratio",
    "dynamic_pressure_pa",
    "factor_of_safety",
    "haaland_friction_factor",
    "mach_number",
    "mass_to_weight_newtons",
    "normal_shock_mach",
    "normal_shock_pressure_ratio",
    "normal_shock_stagnation_pressure_ratio",
    "normal_strain",
    "normal_stress",
    "prandtl_meyer_angle_deg",
    "reynolds_number",
    "rocket_thrust_n",
    "simply_supported_center_load_max_deflection",
    "simply_supported_center_load_max_moment",
    "stagnation_density_ratio",
    "stagnation_pressure_ratio",
    "stagnation_temperature_ratio",
    "thrust_coefficient_ideal",
    "thrust_to_weight_ratio",
    "tsiolkovsky_delta_v",
    "wing_loading_n_m2",
]
