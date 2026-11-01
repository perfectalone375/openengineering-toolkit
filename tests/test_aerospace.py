import pytest

from openengineering.aerospace import (
    aspect_ratio,
    mass_to_weight_newtons,
    thrust_to_weight_ratio,
    wing_loading_n_m2,
)


def test_wing_loading():
    assert wing_loading_n_m2(12000, 16) == pytest.approx(750)


def test_aspect_ratio():
    assert aspect_ratio(10, 16) == pytest.approx(6.25)


def test_thrust_to_weight():
    assert thrust_to_weight_ratio(3000, 6000) == pytest.approx(0.5)


def test_mass_to_weight():
    assert mass_to_weight_newtons(10) == pytest.approx(98.0665)


def test_aerospace_rejects_zero_area():
    with pytest.raises(ValueError, match="wing_area_m2"):
        wing_loading_n_m2(1000, 0)
