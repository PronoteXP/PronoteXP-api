import json
import uuid
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.pronote.auth import login_credentials, login_qr, login_token, session_credentials, clean_pronote_url
from app.pronote.extract import extract_pronote_data
from app.schemas.auth import CredentialsPayload, QRCodePayload, TokenPayload, TokenGenPayload

router = APIRouter(prefix="/v1/auth", tags=["authentication"])


def _parse_qr(qr_data: Any) -> Dict[str, Any]:
    if isinstance(qr_data, str):
        try:
            qr_data = json.loads(qr_data)
        except Exception:
            raise HTTPException(status_code=400, detail="Contenu du QR Code invalide.")
    if not isinstance(qr_data, dict):
        raise HTTPException(status_code=400, detail="Le QR Code doit contenir un objet JSON.")
    missing = [key for key in ("login", "jeton", "url") if not qr_data.get(key)]
    if missing:
        raise HTTPException(status_code=400, detail=f"QR Code PRONOTE incomplet : champ(s) manquant(s) : {', '.join(missing)}.")
    return qr_data


def _profile_session(client, session):
    data = extract_pronote_data(client)
    data["auth_session"] = session
    return data


@router.post("/qr-and-export")
def qr_and_export(payload: QRCodePayload):
    if not payload.pin.isdigit() or len(payload.pin) != 4:
        raise HTTPException(status_code=400, detail="Le code PIN doit contenir exactement 4 chiffres.")
    qr_dict = _parse_qr(payload.qr_data)
    device_uuid = payload.uuid or str(uuid.uuid4())
    try:
        client = login_qr(qr_dict, payload.pin, device_uuid)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"QR Code PRONOTE invalide : champ {exc.args[0]} absent.")
    except Exception as exc:
        message = str(exc).strip() or "Le QR Code n'a pas pu être traité par PRONOTE."
        if "invalid confirmation code" in message.lower():
            message = "Code PIN incorrect pour ce QR Code."
        raise HTTPException(status_code=400, detail=f"Erreur QR Code : {message}")
    if not client.logged_in:
        raise HTTPException(status_code=401, detail="Code PIN invalide ou QR code expiré.")
    return _profile_session(client, session_credentials(client, device_uuid))


@router.post("/credentials")
def credentials(payload: CredentialsPayload):
    try:
        client = login_credentials(payload.url, payload.username, payload.password, payload.ent_name)
    except Exception as exc:
        message = str(exc)
        if "Page html is different" in message:
            raise HTTPException(status_code=400, detail="Cet établissement impose une connexion SSO/ENT. Veuillez utiliser l'onglet QR Code.")
        raise HTTPException(status_code=400, detail=f"Échec de connexion : {message}")
    if not client.logged_in:
        raise HTTPException(status_code=401, detail="Identifiants incorrects.")
    device_uuid = str(uuid.uuid4())
    data = extract_pronote_data(client)
    try:
        data["auth_session"] = session_credentials(client, device_uuid)
    except Exception:
        data["auth_session"] = None
    return data


@router.post("/token")
def token(payload: TokenPayload):
    device_uuid = payload.uuid or str(uuid.uuid4())
    try:
        client = login_token(payload.url, payload.username, payload.token, device_uuid)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Échec jeton : {exc}")
    if not client.logged_in:
        raise HTTPException(status_code=401, detail="Jeton expiré ou identifiants incorrects.")
    return _profile_session(client, session_credentials(client, device_uuid))


@router.post("/get-token")
def get_token(payload: TokenGenPayload):
    try:
        client = login_credentials(payload.url, payload.username, payload.password, payload.ent_name)
        exported = client.export_credentials()
        return {
            "success": True,
            "username": payload.username,
            "url": clean_pronote_url(payload.url),
            "token": exported.get("token") if isinstance(exported, dict) else exported,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Échec de génération du jeton : {exc}")
