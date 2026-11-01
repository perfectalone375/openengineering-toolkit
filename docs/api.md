# REST API

Run locally after installing the API extra:

```bash
python -m pip install -e ".[api,dev]"
uvicorn openengineering.api:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive Swagger UI.

## Endpoints

- `GET /health`
- `POST /units/convert`
- `POST /mechanics/normal-stress`
- `POST /mechanics/normal-strain`
- `POST /mechanics/factor-of-safety`
- `POST /beam/center-load/moment`
- `POST /beam/center-load/deflection`
- `POST /beam/bending-stress`
- `POST /aerospace/wing-loading`
- `POST /aerospace/aspect-ratio`
- `POST /aerospace/thrust-to-weight`
- `POST /aerospace/mass-to-weight`

Invalid request shapes and constraint violations are returned as HTTP 422 responses.
Calculation functions also validate values independently of the API layer.

All API outputs are preliminary engineering aids. They are not certified design
verification and must be checked against applicable engineering standards.
