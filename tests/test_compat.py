from types import SimpleNamespace

from app.routers import compat
from app.schemas.auth import CredentialsPayload, TokenPayload


def test_legacy_credentials_returns_export_without_auth_session(monkeypatch):
    client = SimpleNamespace(logged_in=True)
    monkeypatch.setattr(compat, "login_credentials", lambda *args: client)
    monkeypatch.setattr(compat, "extract_pronote_data", lambda value: {"periods": []})

    result = compat.legacy_credentials(
        CredentialsPayload(url="https://example/", username="user", password="secret")
    )

    assert result == {"periods": []}


def test_legacy_token_does_not_require_export_credentials(monkeypatch):
    client = SimpleNamespace(logged_in=True)
    monkeypatch.setattr(compat, "login_token", lambda *args: client)
    monkeypatch.setattr(compat, "extract_pronote_data", lambda value: {"timetable": []})

    result = compat.legacy_token(
        TokenPayload(url="https://example/", username="user", token="token")
    )

    assert result == {"timetable": []}