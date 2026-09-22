from fastapi import APIRouter

from app.routers.auth import credentials, get_token, qr_and_export, token

router = APIRouter(prefix="/api", tags=["legacy compatibility"])
router.add_api_route("/export/qrcode", qr_and_export, methods=["POST"])
router.add_api_route("/export/credentials", credentials, methods=["POST"])
router.add_api_route("/export/token", token, methods=["POST"])
router.add_api_route("/auth/get-token", get_token, methods=["POST"])
