import pytest

from openengineering.propulsion import (
    characteristic_velocity_star,
    rocket_thrust_n,
    thrust_coefficient_ideal,
    tsiolkovsky_delta_v,
)


def test_tsiolkovsky_delta_v():
    # Isp=300s, m0=1000kg, mf=200kg => delta_v = 300 * 9.80665 * ln(5)
    dv = tsiolkovsky_delta_v(300, 1000, 200)
    assert dv == pytest.approx(4734.9, rel=1e-3)


def test_tsiolkovsky_rejects_invalid_mass():
    with pytest.raises(ValueError, match="dry_mass_kg must be strictly less than initial_mass_kg"):
        tsiolkovsky_delta_v(300, 500, 500)


def test_characteristic_velocity():
    # gamma=1.2, mw=24 kg/kmol, chamber_temp=3000 K
    c_star = characteristic_velocity_star(1.2, 24.0, 3000.0)
    assert c_star > 1400.0
    assert c_star < 2000.0


def test_thrust_coefficient():
    cf = thrust_coefficient_ideal(1.2, 5e6, 1e5, 1e5, 10.0)
    assert cf > 1.2
    assert cf < 1.8


def test_rocket_thrust():
    f = rocket_thrust_n(10.0, 3000.0, 1e5, 1e5, 0.05)
    assert f == pytest.approx(30000.0)
