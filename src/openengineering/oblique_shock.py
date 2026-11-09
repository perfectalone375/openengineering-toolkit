"""
Oblique shock wave mechanics, Theta-Beta-Mach relation, and supersonic wedge flow solvers.
Solves exact 2D compressible shock jumps, detachment angles, and post-shock flow fields.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .validation import require_positive


@dataclass
class ObliqueShockResult:
    """Exact flow field properties downstream of a 2D planar oblique shock wave."""

    mach1: float
    theta_deg: float
    beta_deg: float
    mach_n1: float
    mach_n2: float
    mach2: float
    p2_over_p1: float
    t2_over_t1: float
    rho2_over_rho1: float
    p02_over_p01: float
    is_weak_solution: bool


def theta_from_beta(mach1: float, beta_rad: float, gamma: float = 1.4) -> float:
    """
    Calculate flow deflection angle theta in radians from shock angle beta using the Theta-Beta-M relation:
    tan(theta) = 2 * cot(beta) * (M1^2 * sin^2(beta) - 1) / (M1^2 * (gamma + cos(2*beta)) + 2)
    """
    m1 = mach1
    sin_b = math.sin(beta_rad)
    tan_b = math.tan(beta_rad)

    if tan_b == 0.0:
        return 0.0

    cot_b = 1.0 / tan_b
    numerator = 2.0 * cot_b * (m1**2 * (sin_b**2) - 1.0)
    denominator = m1**2 * (gamma + math.cos(2.0 * beta_rad)) + 2.0

    if denominator <= 0.0 or numerator < 0.0:
        return 0.0

    return math.atan2(numerator, denominator)


def oblique_shock_max_theta_deg(mach1: float, gamma: float = 1.4) -> tuple[float, float]:
    """
    Compute the maximum wedge deflection angle theta_max (in degrees) and corresponding
    shock angle beta_max (in degrees) before shock detachment occurs.
    """
    m1 = require_positive(mach1, "mach1")
    g = require_positive(gamma, "gamma")
    if m1 <= 1.0:
        raise ValueError("Mach 1 must be strictly greater than 1.0 for supersonic oblique shock.")

    # Search for maximum theta using Golden Section search over beta in [mu, pi/2]
    mu_rad = math.asin(1.0 / m1)
    beta_low = mu_rad + 1e-5
    beta_high = (math.pi / 2.0) - 1e-5

    # Golden section optimization
    invphi = (math.sqrt(5.0) - 1.0) / 2.0  # 0.618
    invphi2 = (3.0 - math.sqrt(5.0)) / 2.0

    a, b = beta_low, beta_high
    h = b - a
    c = a + invphi2 * h
    d = a + invphi * h
    yc = theta_from_beta(m1, c, g)
    yd = theta_from_beta(m1, d, g)

    for _ in range(80):
        if yc > yd:
            b = d
            d = c
            yd = yc
            h = invphi * h
            c = a + invphi2 * h
            yc = theta_from_beta(m1, c, g)
        else:
            a = c
            c = d
            yc = yd
            h = invphi * h
            d = a + invphi * h
            yd = theta_from_beta(m1, d, g)

    beta_max_rad = (a + b) / 2.0
    theta_max_rad = theta_from_beta(m1, beta_max_rad, g)

    return (math.degrees(theta_max_rad), math.degrees(beta_max_rad))


def oblique_shock_beta_deg(
    mach1: float, theta_deg: float, gamma: float = 1.4, weak: bool = True
) -> float:
    """
    Compute shock wave angle beta in degrees for a given upstream Mach and deflection angle theta.
    If weak=True, returns the weak shock solution (supersonic/transonic post-shock, standard attached shock).
    If weak=False, returns the strong shock solution (subsonic post-shock).
    """
    m1 = require_positive(mach1, "mach1")
    th = require_positive(theta_deg, "theta_deg")
    g = require_positive(gamma, "gamma")

    if m1 <= 1.0:
        raise ValueError("Mach 1 must be > 1.0 for oblique shock.")

    th_rad = math.radians(th)
    th_max_deg, beta_max_deg = oblique_shock_max_theta_deg(m1, g)

    if th > th_max_deg:
        raise ValueError(
            f"Deflection theta={th:.2f} deg exceeds maximum attachment angle "
            f"theta_max={th_max_deg:.2f} deg for Mach {m1:.2f}. Shock is detached."
        )

    mu_rad = math.asin(1.0 / m1)
    beta_max_rad = math.radians(beta_max_deg)

    # Bracket search interval
    if weak:
        low = mu_rad + 1e-6
        high = beta_max_rad
    else:
        low = beta_max_rad
        high = (math.pi / 2.0) - 1e-6

    # Bisection root-finding for exact numerical stability
    target = th_rad
    for _ in range(80):
        mid = (low + high) / 2.0
        val = theta_from_beta(m1, mid, g)
        if weak:
            # For weak branch, theta is increasing with beta
            if val < target:
                low = mid
            else:
                high = mid
        else:
            # For strong branch, theta is decreasing with beta
            if val > target:
                low = mid
            else:
                high = mid

    beta_sol_rad = (low + high) / 2.0
    return math.degrees(beta_sol_rad)


def solve_oblique_shock(
    mach1: float, theta_deg: float, gamma: float = 1.4, weak: bool = True
) -> ObliqueShockResult:
    """
    Full 2D oblique shock jump state solver.
    Computes all downstream thermodynamic and kinematic ratios across the planar shock.
    """
    m1 = require_positive(mach1, "mach1")
    g = require_positive(gamma, "gamma")
    beta_deg = oblique_shock_beta_deg(m1, theta_deg, gamma=g, weak=weak)

    beta_rad = math.radians(beta_deg)
    th_rad = math.radians(theta_deg)

    # Upstream normal Mach number
    mn1 = m1 * math.sin(beta_rad)
    if mn1 < 1.0:
        mn1 = 1.0

    # Downstream normal Mach number via Rankine-Hugoniot
    mn2_sq = (1.0 + 0.5 * (g - 1.0) * (mn1**2)) / (g * (mn1**2) - 0.5 * (g - 1.0))
    mn2 = math.sqrt(max(1e-12, mn2_sq))

    # Downstream total Mach number
    sin_diff = math.sin(beta_rad - th_rad)
    m2 = mn2 / sin_diff if abs(sin_diff) > 1e-12 else mn2

    # Static pressure ratio P2 / P1
    p2_p1 = 1.0 + (2.0 * g / (g + 1.0)) * (mn1**2 - 1.0)

    # Static density ratio rho2 / rho1
    rho2_rho1 = ((g + 1.0) * (mn1**2)) / (2.0 + (g - 1.0) * (mn1**2))

    # Static temperature ratio T2 / T1 via ideal gas equation of state
    t2_t1 = p2_p1 / rho2_rho1

    # Stagnation pressure ratio P02 / P01
    term1 = ((g + 1.0) * (mn1**2)) / ((g - 1.0) * (mn1**2) + 2.0)
    exp1 = g / (g - 1.0)
    term2 = (g + 1.0) / (2.0 * g * (mn1**2) - (g - 1.0))
    exp2 = 1.0 / (g - 1.0)
    p02_p01 = (term1**exp1) * (term2**exp2) if mn1 > 1.00001 else 1.0

    return ObliqueShockResult(
        mach1=m1,
        theta_deg=round(theta_deg, 3),
        beta_deg=round(beta_deg, 3),
        mach_n1=round(mn1, 4),
        mach_n2=round(mn2, 4),
        mach2=round(m2, 4),
        p2_over_p1=round(p2_p1, 4),
        t2_over_t1=round(t2_t1, 4),
        rho2_over_rho1=round(rho2_rho1, 4),
        p02_over_p01=round(p02_p01, 5),
        is_weak_solution=weak,
    )
