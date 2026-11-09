"""
Tests for 2D supersonic oblique shock mechanics and Theta-Beta-M solvers.
"""

import pytest
from fastapi.testclient import TestClient

from openengineering.api import app
from openengineering.mcp_server import handle_call_tool
from openengineering.oblique_shock import (
    oblique_shock_beta_deg,
    oblique_shock_max_theta_deg,
    solve_oblique_shock,
)


def test_oblique_shock_beta_weak_solution():
    # Mach 2.0, theta = 10 degrees, gamma = 1.4
    # NACA 1135 tabular value: beta ~ 39.31 deg, M2 ~ 1.64
    beta = oblique_shock_beta_deg(mach1=2.0, theta_deg=10.0, gamma=1.4, weak=True)
    assert abs(beta - 39.31) < 0.15

    res = solve_oblique_shock(mach1=2.0, theta_deg=10.0, gamma=1.4, weak=True)
    assert res.is_weak_solution is True
    assert res.mach2 > 1.0  # Supersonic downstream
    assert abs(res.p2_over_p1 - 1.707) < 0.05
    assert res.p02_over_p01 < 1.0  # Entropy increase / total pressure loss


def test_oblique_shock_strong_solution():
    # Strong shock solution yields subsonic downstream flow
    beta_strong = oblique_shock_beta_deg(mach1=2.0, theta_deg=10.0, gamma=1.4, weak=False)
    assert abs(beta_strong - 83.7) < 0.5
    assert beta_strong > 40.0

    res = solve_oblique_shock(mach1=2.0, theta_deg=10.0, gamma=1.4, weak=False)
    assert res.is_weak_solution is False
    assert res.mach2 < 1.0  # Subsonic downstream
    assert res.p2_over_p1 > 4.0  # High pressure jump


def test_oblique_shock_max_theta_and_detachment():
    # At Mach 2.0, gamma = 1.4, theta_max ~ 22.97 degrees
    theta_max, beta_max = oblique_shock_max_theta_deg(mach1=2.0, gamma=1.4)
    assert abs(theta_max - 22.97) < 0.2
    assert abs(beta_max - 64.6) < 0.5

    # Exceeding theta_max must trigger a detachment ValueError
    with pytest.raises(ValueError, match="exceeds maximum attachment angle"):
        solve_oblique_shock(mach1=2.0, theta_deg=25.0, gamma=1.4)


def test_oblique_shock_api_endpoint():
    client = TestClient(app)
    response = client.post(
        "/fluids/compressible/oblique-shock",
        json={"mach1": 2.5, "theta_deg": 12.0, "gamma": 1.4, "weak": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mach1"] == 2.5
    assert data["theta_deg"] == 12.0
    assert data["mach2"] > 1.0
    assert data["p2_over_p1"] > 1.5


def test_oblique_shock_mcp_tool():
    args = {"mach1": 3.0, "theta_deg": 15.0, "gamma": 1.4, "weak": True}
    res = handle_call_tool("openeng_oblique_shock", args)
    assert res["mach1"] == 3.0
    assert res["theta_deg"] == 15.0
    assert res["beta_deg"] > 15.0
    assert res["p02_over_p01"] < 1.0
