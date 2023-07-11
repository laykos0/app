from fastapi import APIRouter

from api.routers import users, articles

router = APIRouter()

router.include_router(users.router,
                      prefix="/users",
                      tags=["users"],
                      )


router.include_router(articles.router,
                      prefix="/articles",
                      tags=["articles"],
                      )
