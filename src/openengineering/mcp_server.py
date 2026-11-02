"""Model Context Protocol (MCP) Server for OpenEngineering Toolkit.

Enables AI agents (Cursor, Claude Desktop, Antigravity) to perform deterministic,
verified computational engineering mechanics calculations.
"""
from __future__ import annotations

import json
import sys
from typing import Any

from .beam import simply_supported_center_load_max_deflection
from .fluids import reynolds_number
from .propulsion import tsiolkovsky_delta_v
from .units import convert_force, convert_length, convert_pressure

TOOLS = [
    {
        "name": "openeng_deltav",
        "description": "Calculate ideal rocket Delta-v (m/s) using Tsiolkovsky equation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "isp_s": {"type": "number", "description": "Specific impulse in seconds"},
                "initial_mass_kg": {"type": "number", "description": "Initial wet mass in kg"},
                "dry_mass_kg": {"type": "number", "description": "Burnout dry mass in kg"},
            },
            "required": ["isp_s", "initial_mass_kg", "dry_mass_kg"],
        },
    },
    {
        "name": "openeng_beam_deflection",
        "description": "Calculate mid-span deflection (m) of a simply-supported beam under central point load.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "load_n": {"type": "number", "description": "Center point load in Newtons"},
                "span_m": {"type": "number", "description": "Clear span in meters"},
                "elastic_modulus_pa": {"type": "number", "description": "Youngs modulus in Pascals (e.g. 200e9)"},
                "second_moment_m4": {"type": "number", "description": "Second moment of area I in m^4"},
            },
            "required": ["load_n", "span_m", "elastic_modulus_pa", "second_moment_m4"],
        },
    },
    {
        "name": "openeng_reynolds",
        "description": "Calculate aerodynamic/hydrodynamic Reynolds number Re = (rho * v * L) / mu.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "density_kg_m3": {"type": "number", "description": "Fluid density in kg/m^3"},
                "velocity_m_s": {"type": "number", "description": "Flow velocity in m/s"},
                "length_m": {"type": "number", "description": "Characteristic chord/diameter in meters"},
                "viscosity_pa_s": {"type": "number", "description": "Dynamic viscosity in Pa*s (default air: 1.789e-5)"},
            },
            "required": ["density_kg_m3", "velocity_m_s", "length_m"],
        },
    },
    {
        "name": "openeng_unit_convert",
        "description": "Convert engineering units between SI, Imperial, and US Customary systems.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["length", "force", "pressure"]},
                "value": {"type": "number"},
                "from_unit": {"type": "string"},
                "to_unit": {"type": "string"},
            },
            "required": ["category", "value", "from_unit", "to_unit"],
        },
    },
]


def handle_call_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name == "openeng_deltav":
        dv = tsiolkovsky_delta_v(args["isp_s"], args["initial_mass_kg"], args["dry_mass_kg"])
        return {"delta_v_m_s": dv, "delta_v_km_s": dv / 1000.0}
    elif name == "openeng_beam_deflection":
        d = simply_supported_center_load_max_deflection(
            args["load_n"], args["span_m"], args["elastic_modulus_pa"], args["second_moment_m4"]
        )
        return {"max_deflection_m": d, "max_deflection_mm": d * 1000.0}
    elif name == "openeng_reynolds":
        mu = args.get("viscosity_pa_s", 1.789e-5)
        re = reynolds_number(args["density_kg_m3"], args["velocity_m_s"], args["length_m"], mu)
        return {"reynolds_number": re, "flow_regime": "turbulent" if re > 5e5 else "laminar"}
    elif name == "openeng_unit_convert":
        cat = args["category"]
        v = args["value"]
        fu = args["from_unit"]
        tu = args["to_unit"]
        if cat == "length":
            res = convert_length(v, fu, tu)
        elif cat == "force":
            res = convert_force(v, fu, tu)
        else:
            res = convert_pressure(v, fu, tu)
        return {"input_value": v, "from_unit": fu, "output_value": res, "to_unit": tu}
    else:
        raise ValueError(f"Unknown tool: {name}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
            elif method == "tools/call":
                params = req.get("params", {})
                name = params.get("name")
                args = params.get("arguments", {})
                result = handle_call_tool(name, args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]},
                }
            elif method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "openengineering-mcp", "version": "0.3.0"},
                        "capabilities": {"tools": {}},
                    },
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method {method} not found"}}
            print(json.dumps(resp), flush=True)
        except Exception as err:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(err)}}
            print(json.dumps(err_resp), flush=True)


if __name__ == "__main__":
    main()
