# Contributing to PronoteXP-api

Keep this repository independent from the web interfaces.

Rules:

- PRONOTE-specific code goes under `app/pronote/`.
- HTTP contracts go under `app/schemas/` and `app/routers/`.
- Do not persist user sessions or exports by default.
- Never log credentials, QR data, tokens, or student data.
- Add a test when changing an API contract.
- Keep `/v1` backwards-compatible when possible; add a new version only for breaking changes.
