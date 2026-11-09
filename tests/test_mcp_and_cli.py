from openengineering.mcp_server import TOOLS, handle_call_tool


def test_tools_schema_validity():
    assert len(TOOLS) >= 4
    tool_names = [t["name"] for t in TOOLS]
    assert "openeng_deltav" in tool_names
    assert "openeng_beam_deflection" in tool_names
    assert "openeng_reynolds" in tool_names


def test_handle_deltav_tool():
    res = handle_call_tool(
        "openeng_deltav", {"isp_s": 300, "initial_mass_kg": 1000, "dry_mass_kg": 200}
    )
    assert "delta_v_m_s" in res
    assert res["delta_v_m_s"] > 4000


def test_handle_reynolds_tool():
    res = handle_call_tool(
        "openeng_reynolds", {"density_kg_m3": 1.225, "velocity_m_s": 30, "length_m": 1.0}
    )
    assert res["flow_regime"] == "turbulent" or res["flow_regime"] == "laminar"
