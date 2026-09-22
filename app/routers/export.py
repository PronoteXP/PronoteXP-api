from fastapi import APIRouter
from app.routers.auth import credentials, token

router = APIRouter(prefix="/v1/export", tags=["legacy export flows"])
router.add_api_route("/credentials", credentials, methods=["POST"])
router.add_api_route("/token", token, methods=["POST"])
