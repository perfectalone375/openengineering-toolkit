"""Elementary Euler-Bernoulli beam calculations in SI units.

These closed-form equations apply only to idealized, linearly elastic beams
under the stated loading and support conditions. They are not a substitute
for applicable design codes, stability checks, fatigue assessment, or FEA.
"""

from __future__ import annotations

from .validation import require_finite, require_positive


def simply_supported_center_load_max_moment(load_n: float, span_m: float) -> float:
    """Maximum bending-moment magnitude (N·m) for a central point load P."""
    load = require_finite(load_n, "load_n")
    span = require_positive(span_m, "span_m")
    return abs(load) * span / 4.0


def simply_supported_center_load_max_deflection(
    load_n: float, span_m: float, elastic_modulus_pa: float, second_moment_m4: float
) -> float:
    """Maximum mid-span deflection magnitude (m): P L³ / (48 E I)."""
    load = abs(require_finite(load_n, "load_n"))
    span = require_positive(span_m, "span_m")
    modulus = require_positive(elastic_modulus_pa, "elastic_modulus_pa")
    inertia = require_positive(second_moment_m4, "second_moment_m4")
    return load * span**3 / (48.0 * modulus * inertia)


def bending_stress_magnitude(
    moment_nm: float, second_moment_m4: float, outer_fibre_distance_m: float
) -> float:
    """Maximum elastic bending-stress magnitude (Pa): |M| c / I."""
    moment = abs(require_finite(moment_nm, "moment_nm"))
    inertia = require_positive(second_moment_m4, "second_moment_m4")
    distance = require_positive(outer_fibre_distance_m, "outer_fibre_distance_m")
    return moment * distance / inertia
