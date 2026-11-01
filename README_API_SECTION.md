## API preview

Install and launch the optional API:

```bash
python -m pip install -e ".[api,dev]"
uvicorn openengineering.api:app --reload
```

Swagger UI: `http://127.0.0.1:8000/docs`

See [docs/api.md](docs/api.md) for the endpoint list and usage.
