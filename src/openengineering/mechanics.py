"""Elementary mechanics calculations with explicit unit conventions."""

from __future__ import annotations

from .validation import require_finite, require_positive


def normal_stress(force_n: float, area_mm2: float) -> float:
    """Calculate average normal stress in MPa from force (N) and area (mm²).

    Since 1 N/mm² equals 1 MPa, the numerical result is force_n / area_mm2.
    This is an average-stress model and does not account for stress
    concentrations, nonuniform loading, buckling, fatigue, or joint effects.
    """
    force = require_finite(force_n, "force_n")
    area = require_positive(area_mm2, "area_mm2")
    return force / area


def normal_strain(change_in_length_mm: float, original_length_mm: float) -> float:
    """Calculate dimensionless engineering normal strain from lengths in mm."""
    change = require_finite(change_in_length_mm, "change_in_length_mm")
    original = require_positive(original_length_mm, "original_length_mm")
    return change / original


def factor_of_safety(allowable_stress_mpa: float, applied_stress_mpa: float) -> float:
    """Return allowable/applied stress; both stresses must be positive MPa values.

    The meaning and suitability of the allowable stress depend on the
    material, failure mode, environment, loading, and governing design rules.
    """
    allowable = require_positive(allowable_stress_mpa, "allowable_stress_mpa")
    applied = require_positive(applied_stress_mpa, "applied_stress_mpa")
    return allowable / applied
