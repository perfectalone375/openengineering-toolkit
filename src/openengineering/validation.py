"""Shared validation helpers for engineering calculations."""

from __future__ import annotations

import math


def require_finite(value: float, name: str) -> float:
    """Return *value* as a float, rejecting NaN and infinite values."""
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a real number") from exc

    if not math.isfinite(numeric):
        raise ValueError(f"{name} must be finite")
    return numeric


def require_positive(value: float, name: str) -> float:
    """Return a finite value greater than zero."""
    numeric = require_finite(value, name)
    if numeric <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return numeric


def require_non_negative(value: float, name: str) -> float:
    """Return a finite value greater than or equal to zero."""
    numeric = require_finite(value, name)
    if numeric < 0:
        raise ValueError(f"{name} must be non-negative")
    return numeric
