# PronoteXP-api

## Disclaimer

> <span style="color:red; font-weight:bold;">⚠️ DISCLAIMER / WARNING</span>  
> **This project is an unofficial, third-party client developed strictly for educational purposes and personal interoperability.**
> 
> - It is in no way affiliated with, maintained, sponsored, or endorsed by **INDEX ÉDUCATION** or **DOCAPOSTE Group**.
> - **PRONOTE** is a registered trademark of INDEX ÉDUCATION.
> - Usage of this tool is entirely at your own risk. You are responsible for complying with all applicable regulations and the Terms of Service of the services you access.
> - This API operates statelessly: no personal data, credentials, tokens, or passwords are ever stored or retained.

Stateless FastAPI backend shared by **PronoteXPr** and **ProXP**. It is the only project component that communicates with `pronotepy`, PRONOTE, and ENT providers.

```text
PronoteXPr / ProXP -> PronoteXP-api -> pronotepy -> PRONOTE / ENT
```

## Features

- PRONOTE QR code and PIN authentication.
- Direct credentials or ENT authentication.
- Reusable token authentication.
- Normalized exports for profiles, periods, grades, averages, timetables, homework, absences, delays, punishments, news, and menus.
- Resource selection to reduce response size.
- Compatibility with the legacy `main-old.py` routes.
- No persistent storage of accounts, sessions, or exports.

## Structure

```text
app/main.py                 FastAPI entry point
app/routers/auth.py         /v1 authentication
app/routers/data.py         Data and resource selection
app/routers/export.py       /v1 export routes
app/routers/compat.py       Legacy /api compatibility
app/pronote/auth.py         pronotepy login and URL normalization
app/pronote/extract.py      Data extraction and normalization
app/schemas/                Pydantic request models
tests/                      Contract and compatibility tests
```

## Versioned API

All routes use `POST` unless stated otherwise. Interactive API documentation is available at `/docs`, and the OpenAPI schema is available at `/openapi.json`.

### Health

```text
GET /v1/health
```

Response:

```json
{ "status": "ok", "service": "PronoteXP-api", "version": "1" }
```

### Authentication and export

```text
POST /v1/auth/qr-and-export
POST /v1/auth/credentials
POST /v1/auth/token
POST /v1/auth/get-token
POST /v1/export/credentials
POST /v1/export/token
```

QR code request:

```json
{
  "qr_data": { "login": "...", "jeton": "...", "url": "..." },
  "pin": "1234"
}
```

`qr_data` can also be a JSON string. The response contains the export and, when PRONOTE allows it, a reusable session:

```json
{
  "export_metadata": {
    "app": "PronoteXP",
    "generated_at": "...",
    "logged_in": true
  },
  "user_info": { "name": "...", "class_name": "...", "establishment": "..." },
  "periods": [],
  "timetable": [],
  "homework": [],
  "auth_session": {
    "url": "...",
    "username": "...",
    "token": "...",
    "uuid": "..."
  }
}
```

Credentials request:

```json
{
  "url": "https://example.pronote.net/",
  "username": "first.last",
  "password": "...",
  "ent_name": "monlycee_net"
}
```

`ent_name` is optional. An unknown ENT name is treated as a direct connection.

Token request:

```json
{
  "url": "https://example.pronote.net/",
  "username": "first.last",
  "token": "...",
  "uuid": "..."
}
```

`uuid` is optional. Clients should preserve it when it is returned in `auth_session`.

### Session data

```text
POST /v1/data
POST /v1/profile
POST /v1/timetable
POST /v1/periods
POST /v1/grades
POST /v1/averages
POST /v1/homework
POST /v1/absences
POST /v1/delays
POST /v1/punishments
POST /v1/news
POST /v1/menus
```

Complete request:

```json
{
  "session": {
    "url": "https://example.pronote.net/",
    "username": "first.last",
    "token": "...",
    "uuid": "..."
  },
  "resources": ["profile", "timetable", "grades", "homework"]
}
```

`/v1/data` without `resources` returns the complete export. Specialized routes return only their resource. `grades` and `averages` remain grouped by period.

Supported resources are `profile`, `periods`, `timetable`, `homework`, `absences`, `delays`, `punishments`, `news`, `menus`, `grades`, and `averages`. Unknown resources are ignored and reported in `export_metadata.warnings`.

## Legacy API compatibility

These routes remain available for clients that still use the paths from `main-old.py`:

```text
POST /api/export/qrcode
POST /api/export/credentials
POST /api/export/token
POST /api/auth/get-token
```

These routes preserve the historical response format. The newer `/v1` routes may include `auth_session` in addition to the export data.

## Responses and errors

Dates are returned in ISO 8601 format. Partial extraction errors are stored in `export_metadata.errors`, so an unavailable resource does not discard the whole export.

Main status codes:

| Status | Meaning                                               |
| ------ | ----------------------------------------------------- |
| `200`  | Authentication or export succeeded                    |
| `400`  | Invalid payload, invalid QR code, or connection error |
| `401`  | Invalid or expired credentials, token, or session     |
| `422`  | Request structure could not be validated              |

## Security and configuration

- Never log passwords, QR payloads, tokens, or student data.
- The server does not persist PRONOTE sessions.
- `CORS_ALLOW_ORIGINS` accepts a comma-separated list of origins.
- The default `*` value is convenient for development. In production, set the exact allowed origins, for example `https://organization.github.io`.
- Clients send secrets in HTTPS request bodies; deploy the API behind HTTPS.

## Local development

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py run.py
```

The API is available at `http://127.0.0.1:8000`.

Run the tests with:

```powershell
py -m pip install pytest
py -m pytest -q
```

Run a syntax-only validation with:

```powershell
py -m compileall -q app tests
```

## Render deployment

The [render.yaml](render.yaml) configuration uses:

```text
Build command: pip install -r requirements.txt
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set `CORS_ALLOW_ORIGINS` in Render environment variables to the PronoteXPr domain and, if needed, the ProXP domain.

## Frontends

PronoteXPr remains an independent static frontend repository. It calls `/v1/auth/qr-and-export`, `/v1/export/token`, and `/v1/export/credentials`, then generates JSON, XLSX, and ODS files in the browser.

The backend can also serve a local `frontend/Exporter` directory automatically when it exists, without modifying or depending on the frontend repository.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before making changes. Any HTTP contract change should add or update a test under `tests/`.

## License

MIT - Copyright (c) 2026 Pyronixus.
