from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from app.core.config import settings
from app.db.session import init_db
from app.api.routes import auth, news, offers, activities, join_us, keep_in_touch

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include API routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(news.router, prefix=settings.API_PREFIX)
app.include_router(offers.router, prefix=settings.API_PREFIX)
app.include_router(activities.router, prefix=settings.API_PREFIX)
app.include_router(join_us.router, prefix=settings.API_PREFIX)
app.include_router(keep_in_touch.router, prefix=settings.API_PREFIX)


@app.on_event("startup")
async def on_startup() -> None:
    init_db()


@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
