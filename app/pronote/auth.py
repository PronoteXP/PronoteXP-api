import uuid as uuid_lib
from typing import Any, Dict, Optional

import pronotepy
from pronotepy import ent


def clean_pronote_url(url: str) -> str:
    clean_url = (url or "").strip().split("/eleve.html")[0]
    if not clean_url.endswith("/"):
        clean_url += "/"
    return clean_url


def resolve_ent(ent_name: Optional[str]):
    if not ent_name:
        return None
    return getattr(ent, ent_name, None)


def login_qr(qr_data: Dict[str, Any], pin: str, device_uuid: Optional[str] = None) -> pronotepy.Client:
    device_uuid = device_uuid or str(uuid_lib.uuid4())
    return pronotepy.Client.qrcode_login(qr_data, pin, device_uuid)


def login_token(url: str, username: str, token: str, device_uuid: Optional[str] = None) -> pronotepy.Client:
    clean_url = clean_pronote_url(url)
    device_uuid = device_uuid or str(uuid_lib.uuid4())
    return pronotepy.Client.token_login(
        pronote_url=clean_url,
        username=username,
        password=token,
        uuid=device_uuid,
    )


def login_credentials(url: str, username: str, password: str, ent_name: Optional[str] = "monlycee_net") -> pronotepy.Client:
    clean_url = clean_pronote_url(url)
    return pronotepy.Client(
        clean_url,
        username=username,
        password=password,
        ent=resolve_ent(ent_name),
    )


def session_credentials(client: pronotepy.Client, device_uuid: str) -> Dict[str, Any]:
    exported = client.export_credentials()
    return {
        "url": getattr(client, "pronote_url", None),
        "username": getattr(client, "username", None),
        "token": exported.get("token") if isinstance(exported, dict) else None,
        "uuid": device_uuid,
    }
