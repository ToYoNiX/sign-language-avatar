import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "*")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
WEB_DIR = BASE_DIR / "web-simulator"


@app.get("/embed", response_class=HTMLResponse)
def embed():
    html = (TEMPLATES_DIR / "embed.html").read_text(encoding="utf-8")
    html = html.replace("__ALLOWED_ORIGIN__", ALLOWED_ORIGIN)
    return HTMLResponse(content=html)


@app.get("/playground", response_class=HTMLResponse)
def playground():
    return HTMLResponse(content=(TEMPLATES_DIR / "playground.html").read_text(encoding="utf-8"))


# Must be last — catches everything else as static files
app.mount("/", StaticFiles(directory=WEB_DIR, html=True, follow_symlink=True), name="static")
