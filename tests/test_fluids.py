import pytest

from openengineering.fluids import (
    dynamic_pressure_pa,
    haaland_friction_factor,
    mach_number,
    reynolds_number,
    stagnation_pressure_ratio,
)


def test_reynolds_number():
    # rho=1.225, v=50, L=2, mu=1.789e-5
    re = reynolds_number(1.225, 50.0, 2.0, 1.789e-5)
    assert re == pytest.approx(6.8474e6, rel=1e-3)


def test_dynamic_pressure():
    q = dynamic_pressure_pa(1.225, 100.0)
    assert q == pytest.approx(6125.0)


def test_mach_number():
    # v=340 m/s at T=288.15 K
    m = mach_number(340.0, 288.15)
    assert m == pytest.approx(0.9992, rel=1e-3)


def test_stagnation_pressure_ratio():
    p_ratio = stagnation_pressure_ratio(0.8)
    assert p_ratio == pytest.approx(1.524, rel=1e-3)


def test_haaland_friction_factor():
    f_lam = haaland_friction_factor(1000.0, 0.001)
    assert f_lam == pytest.approx(0.064)

    f_turb = haaland_friction_factor(1e5, 0.0001)
    assert 0.015 < f_turb < 0.030
