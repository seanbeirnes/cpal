from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from web.api import router as api_router
from dotenv import load_dotenv

load_dotenv()

CURR_DIR = Path(__file__).resolve().parent
STATIC_DIR = Path(CURR_DIR,"static").resolve()

app = FastAPI()

app.include_router(api_router, prefix="/api")

app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
