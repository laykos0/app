from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import routers
from src.api.routers.exception_handlers import (
    handle_404_not_found,
    handle_401_unauthorized,
    handle_403_forbidden
)
from src.core.mongo import init_db
from src.core.settings import settings
from src.infrastructure.exceptions import (
    CustomNotFoundException,
    CustomUnauthorizedException,
    CustomForbiddenException
)

app = FastAPI(title=settings.API_TITLE,
              description=settings.API_DESCRIPTION,
              openapi_tags=settings.API_TAGS)

app.include_router(routers.router)

app.add_exception_handler(CustomUnauthorizedException, handle_401_unauthorized)
app.add_exception_handler(CustomForbiddenException, handle_403_forbidden)
app.add_exception_handler(CustomNotFoundException, handle_404_not_found)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def connect():
    await init_db()
