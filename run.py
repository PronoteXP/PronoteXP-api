import os
import sys
from pathlib import Path
import uvicorn

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))


    reload = os.getenv("ENV", "production") == "development"

    uvicorn.run("app.main:app", host=host, port=port, reload=reload)