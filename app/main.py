import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import auth, data, export, compat

app = FastAPI(
    title="PronoteXP API",
    version="1.0.0",
    description="Stateless PRONOTE data API for PronoteXPr and ProXP.",
)

origins = [item.strip() for item in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",") if item.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(data.router)
app.include_router(export.router)
app.include_router(compat.router)

@app.get("/")
def root():
    return {"service": "PronoteXP-api", "version": "1.0.0", "docs": "/docs"}


frontend_dir = Path(__file__).resolve().parent.parent / "frontend" / "Exporter"
if frontend_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
