import pytest

from openengineering.beam import (
    bending_stress_magnitude,
    simply_supported_center_load_max_deflection,
    simply_supported_center_load_max_moment,
)


def test_center_load_max_moment():
    assert simply_supported_center_load_max_moment(1000, 2) == pytest.approx(500)


def test_center_load_max_deflection():
    # P=1000 N, L=2 m, E=200 GPa, I=1e-6 m^4
    assert simply_supported_center_load_max_deflection(1000, 2, 200e9, 1e-6) == pytest.approx(0.0004166666667)


def test_bending_stress():
    assert bending_stress_magnitude(500, 1e-6, 0.01) == pytest.approx(5e6)


def test_beam_rejects_zero_span():
    with pytest.raises(ValueError, match="span_m"):
        simply_supported_center_load_max_moment(100, 0)
