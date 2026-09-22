from app.schemas.auth import TokenPayload, QRCodePayload


def test_token_payload_accepts_optional_uuid():
    payload = TokenPayload(url="https://example/", username="user", token="token")
    assert payload.uuid is None


def test_qr_payload_accepts_dict():
    payload = QRCodePayload(qr_data={"login": "x", "jeton": "y", "url": "z"}, pin="1234")
    assert payload.pin == "1234"
