"""Compressible fluid dynamics, isentropic flow relations, and normal shock mechanics."""
from __future__ import annotations

import math

from .validation import require_positive


def stagnation_temperature_ratio(mach: float, gamma: float = 1.4) -> float:
    """Isentropic total-to-static temperature ratio T_0 / T = 1 + 0.5 * (gamma - 1) * M^2."""
    m = require_positive(mach, "mach")
    g = require_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError("gamma must be strictly greater than 1.0")
    return 1.0 + 0.5 * (g - 1.0) * (m**2)


def stagnation_density_ratio(mach: float, gamma: float = 1.4) -> float:
    """Isentropic total-to-static density ratio rho_0 / rho = (T_0 / T)^(1 / (gamma - 1))."""
    m = require_positive(mach, "mach")
    g = require_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError("gamma must be strictly greater than 1.0")
    t_ratio = 1.0 + 0.5 * (g - 1.0) * (m**2)
    return t_ratio ** (1.0 / (g - 1.0))


def critical_area_ratio(mach: float, gamma: float = 1.4) -> float:
    """Isentropic nozzle area ratio A / A* (local area relative to sonic throat area)."""
    m = require_positive(mach, "mach")
    g = require_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError("gamma must be strictly greater than 1.0")
    exponent = (g + 1.0) / (2.0 * (g - 1.0))
    base = (2.0 / (g + 1.0)) * (1.0 + 0.5 * (g - 1.0) * (m**2))
    return (1.0 / m) * (base**exponent)


def normal_shock_mach(mach1: float, gamma: float = 1.4) -> float:
    """Calculate downstream Mach number M_2 after a 1D normal shock wave (M_1 >= 1.0)."""
    m1 = require_positive(mach1, "mach1")
    g = require_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError("gamma must be strictly greater than 1.0")
    if m1 < 1.0:
        raise ValueError("mach1 must be >= 1.0 for a physically valid normal shock")
    numerator = 1.0 + 0.5 * (g - 1.0) * (m1**2)
    denominator = g * (m1**2) - 0.5 * (g - 1.0)
    return math.sqrt(numerator / denominator)


def normal_shock_pressure_ratio(mach1: float, gamma: float = 1.4) -> float:
    """Static pressure jump ratio P_2 / P_1 across a normal shock."""
    m1 = require_positive(mach1, "mach1")
    g = require_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError("gamma must be strictly greater than 1.0")
    if m1 < 1.0:
        raise ValueError("mach1 must be >= 1.0 for a normal shock")
    return 1.0 + (2.0 * g / (g + 1.0)) * (m1**2 - 1.0)


def normal_shock_stagnation_pressure_ratio(mach1: float, gamma: float = 1.4) -> float:
    """Total (stagnation) pressure ratio P_02 / P_01 across a normal shock (total pressure loss)."""
    m1 = require_positive(mach1, "mach1")
    g = require_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError("gamma must be strictly greater than 1.0")
    if m1 < 1.0:
        raise ValueError("mach1 must be >= 1.0 for a normal shock")
    if math.isclose(m1, 1.0, abs_tol=1e-7):
        return 1.0
    term1 = ((g + 1.0) * (m1**2)) / ((g - 1.0) * (m1**2) + 2.0)
    exp1 = g / (g - 1.0)
    term2 = (g + 1.0) / (2.0 * g * (m1**2) - (g - 1.0))
    exp2 = 1.0 / (g - 1.0)
    return (term1**exp1) * (term2**exp2)


def prandtl_meyer_angle_deg(mach: float, gamma: float = 1.4) -> float:
    """Prandtl-Meyer expansion angle nu(M) in degrees for supersonic flow (M >= 1.0)."""
    m = require_positive(mach, "mach")
    g = require_positive(gamma, "gamma")
    if g <= 1.0:
        raise ValueError("gamma must be strictly greater than 1.0")
    if m < 1.0:
        raise ValueError("mach must be >= 1.0 for Prandtl-Meyer expansion")
    if math.isclose(m, 1.0, abs_tol=1e-7):
        return 0.0
    factor = math.sqrt((g + 1.0) / (g - 1.0))
    arg1 = math.sqrt(((g - 1.0) / (g + 1.0)) * (m**2 - 1.0))
    arg2 = math.sqrt(m**2 - 1.0)
    nu_rad = factor * math.atan(arg1) - math.atan(arg2)
    return math.degrees(nu_rad)
