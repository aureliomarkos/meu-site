import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger("uvicorn.error")

BASE_DIR = Path(__file__).resolve().parent.parent  # raiz do projeto

from app.config import settings
from app.database import engine, Base
from app.seed import seed_news

from app.routes import clients, client_messages, contact, news, admin, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_news()
    yield


app = FastAPI(
    title="MarkosDev API",
    description="Backend do portfólio MarkosDev — formulário de contato e blog.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────

origins = [origin.strip() for origin in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files ─────────────────────────────────────────────────

app.mount("/page", StaticFiles(directory=str(BASE_DIR / "app" / "page"), html=True), name="page")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/page/")


@app.get("/download/app", include_in_schema=False)
def download_app():
    apk_path = BASE_DIR / "mobile" / "meu-site.apk"
    logger.info(f"[download/app] BASE_DIR={BASE_DIR}")
    logger.info(f"[download/app] resolved={apk_path.resolve()}")
    logger.info(f"[download/app] exists={apk_path.exists()}")
    if not apk_path.exists():
        raise HTTPException(status_code=404, detail=f"APK não encontrado em {apk_path.resolve()}")
    return FileResponse(
        path=apk_path,
        media_type="application/vnd.android.package-archive",
        filename="meu-site.apk",
    )


# ── Routers ──────────────────────────────────────────────────────

app.include_router(clients.router)
app.include_router(client_messages.router)
app.include_router(contact.router)
app.include_router(news.router)
app.include_router(admin.router)
app.include_router(chat.router)


