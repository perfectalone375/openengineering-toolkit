import pytest

from openengineering.mechanics import factor_of_safety, normal_strain, normal_stress


def test_normal_stress_returns_mpa() -> None:
    assert normal_stress(force_n=10_000, area_mm2=200) == pytest.approx(50.0)


def test_normal_stress_supports_compression_sign() -> None:
    assert normal_stress(force_n=-10_000, area_mm2=200) == pytest.approx(-50.0)


def test_normal_stress_rejects_zero_area() -> None:
    with pytest.raises(ValueError, match="area_mm2 must be greater than zero"):
        normal_stress(force_n=10, area_mm2=0)


def test_normal_strain() -> None:
    assert normal_strain(change_in_length_mm=0.2, original_length_mm=100) == pytest.approx(0.002)


def test_normal_strain_rejects_negative_original_length() -> None:
    with pytest.raises(ValueError, match="original_length_mm"):
        normal_strain(change_in_length_mm=1, original_length_mm=-10)


def test_factor_of_safety() -> None:
    assert factor_of_safety(250, 100) == pytest.approx(2.5)


def test_factor_of_safety_rejects_zero_applied_stress() -> None:
    with pytest.raises(ValueError, match="applied_stress_mpa"):
        factor_of_safety(250, 0)
