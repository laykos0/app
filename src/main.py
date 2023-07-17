from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import routers
from src.api.routers.exception_handlers import handle_404_not_found
from src.core.mongo import init_db
from src.core.settings import settings
from src.infrastructure.exceptions import CustomNotFoundException

app = FastAPI(title=settings.api_title,
              description=settings.api_description,
              openapi_tags=settings.api_tags)
app.include_router(routers.router)


@app.on_event('startup')
async def connect():
    await init_db()


@app.get("/")
async def root():
    return {
        "app_name": settings.app_name,
    }


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(CustomNotFoundException, handle_404_not_found)
