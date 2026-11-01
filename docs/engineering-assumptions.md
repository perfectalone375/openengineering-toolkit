# Engineering assumptions and limitations

## Beam calculations

The beam functions use elementary Euler-Bernoulli theory for slender beams,
linear-elastic material response, small deflections, and idealized supports.
The centre-load formulas assume a simply supported beam with one concentrated
load at mid-span:

- Maximum moment magnitude: `P L / 4`
- Maximum deflection magnitude: `P L³ / (48 E I)`

The bending stress function uses the elastic flexure formula `|M| c / I`.
These functions do not check shear stress, local effects, lateral-torsional
buckling, column instability, fatigue, joints, plasticity, composite
anisotropy, or code-specific load factors.

## Aerospace ratios

- Wing loading is `W / S`, using weight in newtons and reference wing area in m².
- Geometric aspect ratio is `b² / S`, using span in metres and the same
  reference-area convention throughout.
- Thrust-to-weight ratio is `T / W`, with thrust and weight in newtons.
- Mass-to-weight conversion uses standard gravity by default; use local or
  mission-specific gravity when appropriate.

These are preliminary sizing metrics, not aircraft performance predictions
or airworthiness substantiation. Definitions and reference areas must be
consistent with the aircraft configuration and applicable discipline practice.
