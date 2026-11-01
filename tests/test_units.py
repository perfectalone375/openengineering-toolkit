import math

import pytest

from openengineering.units import convert_force, convert_length, convert_pressure


def test_length_mm_to_m() -> None:
    assert convert_length(250, "mm", "m") == pytest.approx(0.25)


def test_length_inches_to_mm() -> None:
    assert convert_length(1, "in", "mm") == pytest.approx(25.4)


def test_pressure_mpa_to_pa() -> None:
    assert convert_pressure(2.5, "MPa", "Pa") == pytest.approx(2_500_000)


def test_pressure_psi_to_kpa() -> None:
    assert convert_pressure(1, "psi", "kPa") == pytest.approx(6.894757293168)


def test_force_kn_to_newton() -> None:
    assert convert_force(3, "kN", "N") == pytest.approx(3000)


def test_unknown_unit_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported length unit"):
        convert_length(1, "yard", "m")


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_non_finite_values_are_rejected(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        convert_length(value, "m", "mm")
