# PronoteXP-api

The shared, stateless FastAPI backend used by **PronoteXPr** and **ProXP**.

It is the only PronoteXP repository that knows about `pronotepy` and the PRONOTE protocol.

## Architecture

```text
PronoteXPr ─┐
            ├──> PronoteXP-api ──> pronotepy ──> PRONOTE / ENT
ProXP ──────┘
```

## Responsibilities

- Authenticate through PRONOTE QR Code, reusable token, or credentials/ENT.
- Turn a successful QR/credential login into a reusable session token when PRONOTE allows it.
- Fetch PRONOTE data.
- Normalize data into stable JSON structures.
- Serve versioned `/v1` endpoints.
- Keep the service stateless: no student account database and no persistent PRONOTE exports.

## API surface

### Health

```text
GET /v1/health
```

### Authentication

```text
POST /v1/auth/qr-and-export
POST /v1/auth/token
POST /v1/auth/credentials
POST /v1/auth/get-token
```

The QR flow is intended for initial ProXP connection. It returns an `auth_session` object containing the PRONOTE URL, username, reusable token, and device UUID returned/used by the client library.

The token is reusable, not guaranteed to be permanent: validity is controlled by PRONOTE and the school/ENT environment.

### Data

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

`POST /v1/data` accepts:

```json
{
  "session": {
    "url": "https://example/pronote/",
    "username": "prenom.nom",
    "token": "...",
    "uuid": "..."
  },
  "resources": ["profile", "timetable", "grades", "homework"]
}
```

Omit `resources` to fetch the complete export payload.

### Temporary compatibility export routes

```text
POST /v1/export/credentials
POST /v1/export/token
```

These are used by PronoteXPr while preserving the existing export workflow.

## Security notes

- Never log tokens, passwords, QR payloads, or private PRONOTE data.
- Do not persist sessions server-side.
- Set `CORS_ALLOW_ORIGINS` in production to the exact origins that need access.
- Treat `auth_session.token` as a secret.
- The API returns data only for the authenticated PRONOTE session supplied by the caller.

## Local development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The API is available at `http://127.0.0.1:8000` and OpenAPI documentation at `/docs`.

## Render

Use the following build/runtime setup:

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Recommended environment variable:

```text
CORS_ALLOW_ORIGINS=https://<org>.github.io
```

Add additional comma-separated origins when ProXP and PronoteXPr live on different hostnames.

## License

MIT — Copyright (c) 2026 Pyronixus.
