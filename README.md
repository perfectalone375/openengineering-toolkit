# OpenEngineering Toolkit

A Python-first collection of transparent, tested engineering utilities for early-stage design calculations, unit conversions, and engineering sanity checks.

> **Status:** early development. This project is an educational and preliminary-design aid, not certified engineering software. Independently verify calculations, assumptions, material data, and applicable standards before using results in real designs.

## Goals

- Make common engineering calculations reproducible and easy to inspect.
- Validate inputs and expose assumptions instead of silently accepting invalid values.
- Provide small, composable Python functions with automated tests.
- Grow toward a documented API and engineering reference datasets.

## Initial modules

- **Units:** explicit conversions for length, pressure, and force.
- **Mechanics:** introductory calculations for normal stress, engineering strain, and factor of safety.
- **Validation:** clear checks for finite, positive, and physically meaningful inputs.

## Quick start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install -e "[dev]"
pytest
```

## Example

```python
from openengineering.units import convert_length
from openengineering.mechanics import normal_stress

print(convert_length(250, "mm", "m"))  # 0.25
print(normal_stress(force_n=10_000, area_mm2=200))  # 50.0 MPa
```

## Engineering conventions

- SI units are preferred internally.
- Function names and docstrings state expected input units.
- Invalid, non-finite, or physically meaningless inputs raise `ValueError`.
- Preliminary results are not design approval or certification.

## Development

```bash
python -m pip install -e "[dev]"
pytest
ruff check .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution and review expectations.

## Roadmap

1. Core unit conversions and elementary mechanics.
2. Boundary-value and property-based tests.
3. Material data with provenance, versioning, and limitations.
4. FastAPI service layer after the calculation library is stable.
5. Examples, engineering notes, and contributor-friendly issues.

## License

MIT. See [LICENSE](LICENSE).
