"""Rocket propulsion and thermodynamics closed-form analytical equations."""
from __future__ import annotations

import math

from .validation import require_positive


def tsiolkovsky_delta_v(
    isp_s: float,
    initial_mass_kg: float,
    dry_mass_kg: float,
    gravity_m_s2: float = 9.80665,
) -> float:
    """Ideal Tsiolkovsky rocket equation: Delta v = Isp * g0 * ln(m0 / mf)."""
    isp = require_positive(isp_s, "isp_s")
    m0 = require_positive(initial_mass_kg, "initial_mass_kg")
    mf = require_positive(dry_mass_kg, "dry_mass_kg")
    g0 = require_positive(gravity_m_s2, "gravity_m_s2")
    if mf >= m0:
        raise ValueError("dry_mass_kg must be strictly less than initial_mass_kg")
    return isp * g0 * math.log(m0 / mf)


def characteristic_velocity_star(
    gamma: float,
    molecular_weight_kg_kmol: float,
    chamber_temp_k: float,
    universal_r_j_kmol_k: float = 8314.462618,
) -> float:
    """Characteristic exhaust velocity c* (m/s) as a function of chamber thermodynamics."""
    g = require_positive(gamma, "gamma")
    mw = require_positive(molecular_weight_kg_kmol, "molecular_weight_kg_kmol")
    tc = require_positive(chamber_temp_k, "chamber_temp_k")
    if g <= 1.0:
        raise ValueError("gamma must be strictly greater than 1.0")
    r_specific = universal_r_j_kmol_k / mw
    numerator = math.sqrt(g * r_specific * tc)
    denominator = g * math.sqrt((2.0 / (g + 1.0)) ** ((g + 1.0) / (g - 1.0)))
    return numerator / denominator


def thrust_coefficient_ideal(
    gamma: float,
    chamber_pressure_pa: float,
    exit_pressure_pa: float,
    ambient_pressure_pa: float,
    expansion_ratio: float,
) -> float:
    """Nozzle thrust coefficient C_F including pressure mismatch correction."""
    g = require_positive(gamma, "gamma")
    pc = require_positive(chamber_pressure_pa, "chamber_pressure_pa")
    pe = require_positive(exit_pressure_pa, "exit_pressure_pa")
    pa = require_positive(ambient_pressure_pa, "ambient_pressure_pa")
    eps = require_positive(expansion_ratio, "expansion_ratio")
    if g <= 1.0:
        raise ValueError("gamma must be strictly greater than 1.0")
    term1 = (2.0 * (g**2) / (g - 1.0)) * ((2.0 / (g + 1.0)) ** ((g + 1.0) / (g - 1.0)))
    term2 = 1.0 - (pe / pc) ** ((g - 1.0) / g)
    momentum_cf = math.sqrt(max(0.0, term1 * term2))
    pressure_cf = ((pe - pa) / pc) * eps
    return momentum_cf + pressure_cf


def rocket_thrust_n(
    mass_flow_kg_s: float,
    effective_exhaust_velocity_m_s: float,
    exit_pressure_pa: float,
    ambient_pressure_pa: float,
    exit_area_m2: float,
) -> float:
    """Total rocket thrust: F = mdot * ve + (pe - pa) * Ae."""
    mdot = require_positive(mass_flow_kg_s, "mass_flow_kg_s")
    ve = require_positive(effective_exhaust_velocity_m_s, "effective_exhaust_velocity_m_s")
    pe = require_positive(exit_pressure_pa, "exit_pressure_pa")
    pa = require_positive(ambient_pressure_pa, "ambient_pressure_pa")
    ae = require_positive(exit_area_m2, "exit_area_m2")
    return (mdot * ve) + ((pe - pa) * ae)
