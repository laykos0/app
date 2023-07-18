from fastapi import APIRouter

from src.core.settings import settings

router = APIRouter()


@router.get("/")
async def root():
    return {
        "app_name": settings.APP_NAME,
    }
