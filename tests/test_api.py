from fastapi.testclient import TestClient

from openengineering.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_unit_conversion_endpoint():
    response = client.post(
        "/units/convert",
        json={"value": 250, "source": "mm", "target": "m", "quantity": "length"},
    )
    assert response.status_code == 200
    assert response.json()["result"] == 0.25


def test_unknown_unit_returns_validation_error():
    response = client.post(
        "/units/convert",
        json={"value": 1, "source": "yard", "target": "m", "quantity": "length"},
    )
    assert response.status_code == 422


def test_normal_stress_endpoint():
    response = client.post(
        "/mechanics/normal-stress", json={"force_n": 10000, "area_mm2": 200}
    )
    assert response.status_code == 200
    assert response.json()["normal_stress_mpa"] == 50


def test_beam_moment_endpoint():
    response = client.post("/beam/center-load/moment", json={"load_n": 1000, "span_m": 2})
    assert response.status_code == 200
    assert response.json()["maximum_moment_nm"] == 500


def test_invalid_zero_span_is_rejected():
    response = client.post("/beam/center-load/moment", json={"load_n": 1000, "span_m": 0})
    assert response.status_code == 422


def test_wing_loading_endpoint():
    response = client.post(
        "/aerospace/wing-loading", json={"weight_n": 12000, "wing_area_m2": 16}
    )
    assert response.status_code == 200
    assert response.json()["wing_loading_n_m2"] == 750
