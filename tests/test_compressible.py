"""Tests for compressible gas dynamics and normal shock relations."""

from __future__ import annotations

import math

import pytest

from openengineering.compressible import (
    critical_area_ratio,
    normal_shock_mach,
    normal_shock_pressure_ratio,
    normal_shock_stagnation_pressure_ratio,
    prandtl_meyer_angle_deg,
    stagnation_density_ratio,
    stagnation_temperature_ratio,
)


def test_isentropic_temperature_ratio():
    assert stagnation_temperature_ratio(1.0, 1.4) == pytest.approx(1.2, rel=1e-5)
    assert stagnation_temperature_ratio(2.0, 1.4) == pytest.approx(1.8, rel=1e-5)


def test_isentropic_density_ratio():
    assert stagnation_density_ratio(1.0, 1.4) == pytest.approx(1.2**2.5, rel=1e-5)


def test_critical_area_ratio():
    # At M=1, A/A* must be exactly 1.0
    assert critical_area_ratio(1.0, 1.4) == pytest.approx(1.0, rel=1e-5)
    # At M=2, A/A* is approximately 1.6875
    assert critical_area_ratio(2.0, 1.4) == pytest.approx(1.6875, rel=1e-3)


def test_normal_shock_relations():
    # At M1 = 2.0
    m2 = normal_shock_mach(2.0, 1.4)
    assert m2 == pytest.approx(math.sqrt(1.0 / 3.0), rel=1e-4)

    p2_p1 = normal_shock_pressure_ratio(2.0, 1.4)
    assert p2_p1 == pytest.approx(4.50, rel=1e-4)

    p02_p01 = normal_shock_stagnation_pressure_ratio(2.0, 1.4)
    assert p02_p01 == pytest.approx(0.7209, rel=1e-3)


def test_normal_shock_sonic_limit():
    assert normal_shock_mach(1.0, 1.4) == pytest.approx(1.0, rel=1e-5)
    assert normal_shock_pressure_ratio(1.0, 1.4) == pytest.approx(1.0, rel=1e-5)
    assert normal_shock_stagnation_pressure_ratio(1.0, 1.4) == pytest.approx(1.0, rel=1e-5)


def test_prandtl_meyer_expansion():
    assert prandtl_meyer_angle_deg(1.0, 1.4) == pytest.approx(0.0, abs=1e-4)
    # M = 2.0 in air has nu approx 26.38 deg
    assert prandtl_meyer_angle_deg(2.0, 1.4) == pytest.approx(26.3798, rel=1e-3)


def test_validation_errors():
    with pytest.raises(ValueError, match="mach1 must be >= 1.0"):
        normal_shock_mach(0.8, 1.4)

    with pytest.raises(ValueError, match="gamma must be strictly greater than 1.0"):
        stagnation_temperature_ratio(1.5, 0.9)
