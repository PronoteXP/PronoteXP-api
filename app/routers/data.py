from fastapi import APIRouter, HTTPException
from app.pronote.auth import login_token
from app.pronote.extract import extract_pronote_data
from app.schemas.auth import DataPayload
from app.schemas.resources import select_resources

router = APIRouter(prefix="/v1", tags=["data"])


def _client(session: dict):
    url = session.get("url")
    username = session.get("username")
    token = session.get("token")
    device_uuid = session.get("uuid")
    if not url or not username or not token:
        raise HTTPException(status_code=400, detail="Session PRONOTE incomplète : url, username et token sont requis.")
    try:
        client = login_token(url, username, token, device_uuid)
    except Exception as exc:
        raise HTTPException(status_code=401, detail=f"Session PRONOTE invalide ou expirée : {exc}")
    if not client.logged_in:
        raise HTTPException(status_code=401, detail="Session PRONOTE invalide ou expirée.")
    return client


@router.get("/health")
def health():
    return {"status": "ok", "service": "PronoteXP-api", "version": "1"}


@router.post("/data")
def data(payload: DataPayload):
    client = _client(payload.session)
    return select_resources(extract_pronote_data(client), payload.resources)


RESOURCE_PATHS = {
    "profile": "profile",
    "timetable": "timetable",
    "homework": "homework",
    "absences": "absences",
    "delays": "delays",
    "punishments": "punishments",
    "news": "news",
    "menus": "menus",
    "periods": "periods",
    "grades": "grades",
    "averages": "averages",
}


for _resource, _path in RESOURCE_PATHS.items():
    def make_handler(resource_name):
        def handler(payload: DataPayload):
            client = _client(payload.session)
            return select_resources(extract_pronote_data(client), [resource_name])
        return handler
    router.add_api_route(f"/{_path}", make_handler(_resource), methods=["POST"], name=f"get_{_resource}")
