"""Command-line interface for openengineering-toolkit."""
from __future__ import annotations

import argparse
import sys

from .aerospace import wing_loading_n_m2
from .beam import simply_supported_center_load_max_deflection
from .fluids import dynamic_pressure_pa, reynolds_number
from .propulsion import tsiolkovsky_delta_v
from .units import convert_force, convert_length, convert_pressure


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        prog="openeng",
        description="OpenEngineering CLI: Computational engineering mechanics & aerospace solver",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # deltav
    dv = subparsers.add_parser("deltav", help="Compute Tsiolkovsky delta-v (m/s)")
    dv.add_argument("--isp", type=float, required=True, help="Specific impulse (s)")
    dv.add_argument("--m0", type=float, required=True, help="Initial wet mass (kg)")
    dv.add_argument("--mf", type=float, required=True, help="Final dry mass (kg)")

    # beam
    bm = subparsers.add_parser("beam-deflection", help="Compute mid-span deflection (m)")
    bm.add_argument("--load", type=float, required=True, help="Central load (N)")
    bm.add_argument("--span", type=float, required=True, help="Beam span (m)")
    bm.add_argument("--modulus", type=float, default=200e9, help="Elastic modulus E (Pa)")
    bm.add_argument("--inertia", type=float, default=1e-6, help="Second moment of area I (m^4)")

    # reynolds
    re = subparsers.add_parser("reynolds", help="Compute Reynolds number")
    re.add_argument("--density", type=float, required=True, help="Density (kg/m^3)")
    re.add_argument("--velocity", type=float, required=True, help="Velocity (m/s)")
    re.add_argument("--length", type=float, required=True, help="Length (m)")
    re.add_argument("--viscosity", type=float, default=1.789e-5, help="Dynamic viscosity (Pa s)")

    # q
    q_p = subparsers.add_parser("q", help="Compute dynamic pressure (Pa)")
    q_p.add_argument("--density", type=float, required=True, help="Density (kg/m^3)")
    q_p.add_argument("--velocity", type=float, required=True, help="Velocity (m/s)")

    # wing
    wg = subparsers.add_parser("wing-loading", help="Compute wing loading W/S (N/m^2)")
    wg.add_argument("--weight", type=float, required=True, help="Aircraft weight (N)")
    wg.add_argument("--area", type=float, required=True, help="Wing reference area (m^2)")

    # unit
    un = subparsers.add_parser("convert", help="Convert engineering units")
    un.add_argument("--type", choices=["length", "force", "pressure"], required=True)
    un.add_argument("--value", type=float, required=True)
    un.add_argument("--from-unit", dest="from_unit", required=True)
    un.add_argument("--to-unit", dest="to_unit", required=True)

    args = parser.parse_args()

    if args.command == "deltav":
        res = tsiolkovsky_delta_v(args.isp, args.m0, args.mf)
        print(f"Ideal Delta-V: {res:.2f} m/s ({res/1000.0:.3f} km/s)")
    elif args.command == "beam-deflection":
        res = simply_supported_center_load_max_deflection(args.load, args.span, args.modulus, args.inertia)
        print(f"Max Mid-span Deflection: {res*1000.0:.4f} mm ({res:.6e} m)")
    elif args.command == "reynolds":
        res = reynolds_number(args.density, args.velocity, args.length, args.viscosity)
        print(f"Reynolds Number: {res:.3e} ({res:.1f})")
    elif args.command == "q":
        res = dynamic_pressure_pa(args.density, args.velocity)
        print(f"Dynamic Pressure q: {res:.2f} Pa ({res/1000.0:.3f} kPa)")
    elif args.command == "wing-loading":
        res = wing_loading_n_m2(args.weight, args.area)
        print(f"Wing Loading W/S: {res:.2f} N/m^2")
    elif args.command == "convert":
        if args.type == "length":
            res = convert_length(args.value, args.from_unit, args.to_unit)
        elif args.type == "force":
            res = convert_force(args.value, args.from_unit, args.to_unit)
        else:
            res = convert_pressure(args.value, args.from_unit, args.to_unit)
        print(f"{args.value} {args.from_unit} = {res:.6g} {args.to_unit}")


if __name__ == "__main__":
    main()
