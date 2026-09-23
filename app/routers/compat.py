from fastapi import APIRouter, HTTPException

from app.pronote.auth import login_credentials, login_token
from app.pronote.extract import extract_pronote_data
from app.routers.auth import get_token, qr_and_export
from app.schemas.auth import CredentialsPayload, TokenPayload

router = APIRouter(prefix="/api", tags=["legacy compatibility"])


def legacy_credentials(payload: CredentialsPayload):
	try:
		client = login_credentials(payload.url, payload.username, payload.password, payload.ent_name)
	except Exception as exc:
		message = str(exc)
		if "Page html is different" in message:
			raise HTTPException(status_code=400, detail="Cet établissement impose une connexion SSO/ENT. Veuillez utiliser l'onglet QR Code.")
		raise HTTPException(status_code=400, detail=f"Échec de connexion : {message}")
	if not client.logged_in:
		raise HTTPException(status_code=401, detail="Identifiants incorrects.")
	return extract_pronote_data(client)


def legacy_token(payload: TokenPayload):
	try:
		client = login_token(payload.url, payload.username, payload.token, payload.uuid)
	except Exception as exc:
		raise HTTPException(status_code=400, detail=f"Échec jeton : {exc}")
	if not client.logged_in:
		raise HTTPException(status_code=401, detail="Jeton expiré ou identifiants incorrects.")
	return extract_pronote_data(client)


router.add_api_route("/export/qrcode", qr_and_export, methods=["POST"])
router.add_api_route("/export/credentials", legacy_credentials, methods=["POST"])
router.add_api_route("/export/token", legacy_token, methods=["POST"])
router.add_api_route("/auth/get-token", get_token, methods=["POST"])
