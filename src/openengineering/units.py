"""Explicit conversions for commonly used engineering units."""

from __future__ import annotations

from .validation import require_finite

_LENGTH_TO_METRE = {
    "m": 1.0,
    "cm": 0.01,
    "mm": 0.001,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
}

_PRESSURE_TO_PASCAL = {
    "Pa": 1.0,
    "kPa": 1_000.0,
    "MPa": 1_000_000.0,
    "GPa": 1_000_000_000.0,
    "bar": 100_000.0,
    "psi": 6_894.757293168,
}

_FORCE_TO_NEWTON = {
    "N": 1.0,
    "kN": 1_000.0,
    "lbf": 4.4482216152605,
}


def _convert(
    value: float, source: str, target: str, factors: dict[str, float], quantity: str
) -> float:
    numeric = require_finite(value, "value")
    if source not in factors:
        raise ValueError(f"Unsupported {quantity} unit: {source!r}")
    if target not in factors:
        raise ValueError(f"Unsupported {quantity} unit: {target!r}")
    return numeric * factors[source] / factors[target]


def convert_length(value: float, source: str, target: str) -> float:
    """Convert length between m, cm, mm, km, in, and ft."""
    return _convert(value, source, target, _LENGTH_TO_METRE, "length")


def convert_pressure(value: float, source: str, target: str) -> float:
    """Convert pressure between Pa, kPa, MPa, GPa, bar, and psi."""
    return _convert(value, source, target, _PRESSURE_TO_PASCAL, "pressure")


def convert_force(value: float, source: str, target: str) -> float:
    """Convert force between N, kN, and lbf."""
    return _convert(value, source, target, _FORCE_TO_NEWTON, "force")
