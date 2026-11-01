# Contributing

Thank you for considering a contribution.

## Before opening a pull request

1. Open or review an issue describing the change.
2. Keep calculations small, explicit, and unit-aware.
3. Document assumptions and expected input units in docstrings.
4. Add tests for normal cases, boundaries, and invalid inputs.
5. Run `pytest` and `ruff check .`.
6. Do not present preliminary calculations as certified design verification.

## Engineering correctness

- Prefer SI units internally and name non-SI input units explicitly.
- Avoid embedding unreferenced material properties or safety factors.
- Cite authoritative sources when adding engineering constants or standards-derived methods.
- State limitations and applicability in the relevant module documentation.

## Pull request description

Include the motivation, summary of behavior, test evidence, assumptions, and any limitations.
