import os
import sys

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from web.api import router as api_router

CURR_DIR = Path(__file__).resolve().parent
STATIC_DIR = Path(CURR_DIR,"static").resolve()

HOST: str | None = os.getenv("HOST")
if HOST == "" or HOST is None:
    sys.exit(1)

app = FastAPI()

origins: list[str] = [
    HOST
]

print(f"[INFO] Allowed origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
