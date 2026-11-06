"""FastAPI interface for preliminary OpenEngineering calculations."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from .aerospace import (
    aspect_ratio,
    mass_to_weight_newtons,
    thrust_to_weight_ratio,
    wing_loading_n_m2,
)
from .beam import (
    bending_stress_magnitude,
    simply_supported_center_load_max_deflection,
    simply_supported_center_load_max_moment,
)
from .compressible import (
    critical_area_ratio,
    normal_shock_mach,
    normal_shock_pressure_ratio,
    normal_shock_stagnation_pressure_ratio,
    prandtl_meyer_angle_deg,
    stagnation_density_ratio,
    stagnation_temperature_ratio,
)
from .fluids import stagnation_pressure_ratio
from .mechanics import factor_of_safety, normal_strain, normal_stress
from .units import convert_force, convert_length, convert_pressure

app = FastAPI(
    title="OpenEngineering Toolkit API",
    version="0.2.0",
    description=(
        "Preliminary engineering calculations with explicit SI-unit conventions. "
        "Outputs are educational aids, not certified design verification."
    ),
)


class UnitConversionRequest(BaseModel):
    value: float
    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    quantity: str = Field(description="One of: length, pressure, force")

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: str) -> str:
        if value not in {"length", "pressure", "force"}:
            raise ValueError("quantity must be length, pressure, or force")
        return value


class NormalStressRequest(BaseModel):
    force_n: float
    area_mm2: float = Field(gt=0)


class NormalStrainRequest(BaseModel):
    change_in_length_mm: float
    original_length_mm: float = Field(gt=0)


class FactorOfSafetyRequest(BaseModel):
    allowable_stress_mpa: float = Field(gt=0)
    applied_stress_mpa: float = Field(gt=0)


class BeamMomentRequest(BaseModel):
    load_n: float
    span_m: float = Field(gt=0)


class BeamDeflectionRequest(BeamMomentRequest):
    elastic_modulus_pa: float = Field(gt=0)
    second_moment_m4: float = Field(gt=0)


class BendingStressRequest(BaseModel):
    moment_nm: float
    second_moment_m4: float = Field(gt=0)
    outer_fibre_distance_m: float = Field(gt=0)


class WingLoadingRequest(BaseModel):
    weight_n: float = Field(gt=0)
    wing_area_m2: float = Field(gt=0)


class AspectRatioRequest(BaseModel):
    span_m: float = Field(gt=0)
    wing_area_m2: float = Field(gt=0)


class ThrustWeightRequest(BaseModel):
    thrust_n: float = Field(gt=0)
    weight_n: float = Field(gt=0)


class MassWeightRequest(BaseModel):
    mass_kg: float = Field(gt=0)
    gravity_m_s2: float = Field(default=9.80665, gt=0)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.2.0"}


@app.post("/units/convert", tags=["units"])
def units_convert(request: UnitConversionRequest) -> dict[str, float | str]:
    converters = {
        "length": convert_length,
        "pressure": convert_pressure,
        "force": convert_force,
    }
    try:
        result = converters[request.quantity](request.value, request.source, request.target)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "quantity": request.quantity,
        "value": request.value,
        "source": request.source,
        "target": request.target,
        "result": result,
    }


@app.post("/mechanics/normal-stress", tags=["mechanics"])
def mechanics_normal_stress(request: NormalStressRequest) -> dict[str, float | str]:
    try:
        result = normal_stress(request.force_n, request.area_mm2)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"normal_stress_mpa": result, "unit": "MPa"}


@app.post("/mechanics/normal-strain", tags=["mechanics"])
def mechanics_normal_strain(request: NormalStrainRequest) -> dict[str, float]:
    try:
        result = normal_strain(request.change_in_length_mm, request.original_length_mm)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"normal_strain": result}


@app.post("/mechanics/factor-of-safety", tags=["mechanics"])
def mechanics_factor_of_safety(request: FactorOfSafetyRequest) -> dict[str, float]:
    try:
        result = factor_of_safety(request.allowable_stress_mpa, request.applied_stress_mpa)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"factor_of_safety": result}


@app.post("/beam/center-load/moment", tags=["beam"])
def beam_center_moment(request: BeamMomentRequest) -> dict[str, float | str]:
    try:
        result = simply_supported_center_load_max_moment(request.load_n, request.span_m)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"maximum_moment_nm": result, "unit": "N·m"}


@app.post("/beam/center-load/deflection", tags=["beam"])
def beam_center_deflection(request: BeamDeflectionRequest) -> dict[str, float | str]:
    try:
        result = simply_supported_center_load_max_deflection(
            request.load_n, request.span_m, request.elastic_modulus_pa, request.second_moment_m4
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"maximum_deflection_m": result, "unit": "m"}


@app.post("/beam/bending-stress", tags=["beam"])
def beam_bending_stress(request: BendingStressRequest) -> dict[str, float | str]:
    try:
        result = bending_stress_magnitude(
            request.moment_nm, request.second_moment_m4, request.outer_fibre_distance_m
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"bending_stress_pa": result, "unit": "Pa"}


@app.post("/aerospace/wing-loading", tags=["aerospace"])
def aerospace_wing_loading(request: WingLoadingRequest) -> dict[str, float | str]:
    return {
        "wing_loading_n_m2": wing_loading_n_m2(request.weight_n, request.wing_area_m2),
        "unit": "N/m²",
    }


@app.post("/aerospace/aspect-ratio", tags=["aerospace"])
def aerospace_aspect_ratio(request: AspectRatioRequest) -> dict[str, float]:
    return {"aspect_ratio": aspect_ratio(request.span_m, request.wing_area_m2)}


@app.post("/aerospace/thrust-to-weight", tags=["aerospace"])
def aerospace_thrust_weight(request: ThrustWeightRequest) -> dict[str, float]:
    return {"thrust_to_weight_ratio": thrust_to_weight_ratio(request.thrust_n, request.weight_n)}


@app.post("/aerospace/mass-to-weight", tags=["aerospace"])
def aerospace_mass_weight(request: MassWeightRequest) -> dict[str, float | str]:
    return {
        "weight_n": mass_to_weight_newtons(request.mass_kg, request.gravity_m_s2),
        "unit": "N",
    }


class IsentropicFlowRequest(BaseModel):
    mach: float = Field(gt=0)
    gamma: float = Field(default=1.4, gt=1.0)


class NormalShockRequest(BaseModel):
    mach1: float = Field(ge=1.0)
    gamma: float = Field(default=1.4, gt=1.0)


class PrandtlMeyerRequest(BaseModel):
    mach: float = Field(ge=1.0)
    gamma: float = Field(default=1.4, gt=1.0)


@app.post("/fluids/compressible/isentropic", tags=["fluids", "compressible"])
def fluids_isentropic_flow(request: IsentropicFlowRequest) -> dict[str, float]:
    try:
        return {
            "mach": request.mach,
            "gamma": request.gamma,
            "t0_over_t": stagnation_temperature_ratio(request.mach, request.gamma),
            "p0_over_p": stagnation_pressure_ratio(request.mach, request.gamma),
            "rho0_over_rho": stagnation_density_ratio(request.mach, request.gamma),
            "a_over_astar": critical_area_ratio(request.mach, request.gamma),
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/fluids/compressible/normal-shock", tags=["fluids", "compressible"])
def fluids_normal_shock(request: NormalShockRequest) -> dict[str, float]:
    try:
        return {
            "mach1": request.mach1,
            "mach2": normal_shock_mach(request.mach1, request.gamma),
            "p2_over_p1": normal_shock_pressure_ratio(request.mach1, request.gamma),
            "p02_over_p01": normal_shock_stagnation_pressure_ratio(request.mach1, request.gamma),
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/fluids/compressible/prandtl-meyer", tags=["fluids", "compressible"])
def fluids_prandtl_meyer(request: PrandtlMeyerRequest) -> dict[str, float]:
    try:
        return {
            "mach": request.mach,
            "nu_deg": prandtl_meyer_angle_deg(request.mach, request.gamma),
        }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

