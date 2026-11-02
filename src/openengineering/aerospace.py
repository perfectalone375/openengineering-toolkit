"""Basic aircraft sizing ratios; inputs use SI units."""
from __future__ import annotations

from .validation import require_positive


def wing_loading_n_m2(weight_n: float, wing_area_m2: float) -> float:
    """Calculate aircraft wing loading W/S in N/m²."""
    weight = require_positive(weight_n, "weight_n")
    area = require_positive(wing_area_m2, "wing_area_m2")
    return weight / area


def aspect_ratio(span_m: float, wing_area_m2: float) -> float:
    """Calculate geometric wing aspect ratio b²/S for a straight reference wing."""
    span = require_positive(span_m, "span_m")
    area = require_positive(wing_area_m2, "wing_area_m2")
    return span**2 / area


def thrust_to_weight_ratio(thrust_n: float, weight_n: float) -> float:
    """Calculate dimensionless thrust-to-weight ratio T/W."""
    thrust = require_positive(thrust_n, "thrust_n")
    weight = require_positive(weight_n, "weight_n")
    return thrust / weight


def mass_to_weight_newtons(mass_kg: float, gravity_m_s2: float = 9.80665) -> float:
    """Convert mass (kg) to weight (N) using the supplied gravitational acceleration."""
    mass = require_positive(mass_kg, "mass_kg")
    gravity = require_positive(gravity_m_s2, "gravity_m_s2")
    return mass * gravity
