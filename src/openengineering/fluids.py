"""Fluid mechanics equations: Reynolds number, dynamic pressure, and pipe friction."""
from __future__ import annotations

import math

from .validation import require_positive


def reynolds_number(
    density_kg_m3: float,
    velocity_m_s: float,
    characteristic_length_m: float,
    dynamic_viscosity_pa_s: float,
) -> float:
    """Reynolds number Re = (rho * v * L) / mu."""
    rho = require_positive(density_kg_m3, "density_kg_m3")
    v = require_positive(velocity_m_s, "velocity_m_s")
    l_char = require_positive(characteristic_length_m, "characteristic_length_m")
    mu = require_positive(dynamic_viscosity_pa_s, "dynamic_viscosity_pa_s")
    return (rho * v * l_char) / mu


def dynamic_pressure_pa(density_kg_m3: float, velocity_m_s: float) -> float:
    """Dynamic pressure q = 0.5 * rho * v^2 in Pascals."""
    rho = require_positive(density_kg_m3, "density_kg_m3")
    v = require_positive(velocity_m_s, "velocity_m_s")
    return 0.5 * rho * (v**2)


def mach_number(
    velocity_m_s: float,
    temperature_k: float,
    gamma: float = 1.4,
    gas_constant_j_kg_k: float = 287.05,
) -> float:
    """Mach number M = v / sqrt(gamma * R * T)."""
    v = require_positive(velocity_m_s, "velocity_m_s")
    t = require_positive(temperature_k, "temperature_k")
    g = require_positive(gamma, "gamma")
    r = require_positive(gas_constant_j_kg_k, "gas_constant_j_kg_k")
    speed_of_sound = math.sqrt(g * r * t)
    return v / speed_of_sound


def stagnation_pressure_ratio(mach: float, gamma: float = 1.4) -> float:
    """Isentropic total-to-static pressure ratio P_0 / P."""
    m = require_positive(mach, "mach")
    g = require_positive(gamma, "gamma")
    return (1.0 + 0.5 * (g - 1.0) * (m**2)) ** (g / (g - 1.0))


def haaland_friction_factor(reynolds: float, relative_roughness: float) -> float:
    """Turbulent pipe Darcy friction factor using the Haaland explicit equation."""
    re = require_positive(reynolds, "reynolds")
    eps_d = require_positive(relative_roughness, "relative_roughness")
    if re < 2300:
        return 64.0 / re
    term = (eps_d / 3.7) ** 1.11 + 6.9 / re
    inv_sqrt_f = -1.8 * math.log10(term)
    return 1.0 / (inv_sqrt_f**2)
