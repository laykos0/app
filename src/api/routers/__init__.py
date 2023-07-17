from fastapi import APIRouter

from src.api.routers import articles, users

router = APIRouter()

router.include_router(users.router,
                      prefix="/users",
                      tags=["users"],
                      )


router.include_router(articles.router,
                      prefix="/articles",
                      tags=["articles"],
                      )
