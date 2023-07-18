from fastapi import APIRouter

from src.api.routers import (
    articles,
    users,
    auth,
    root
)

router = APIRouter()

router.include_router(users.router,
                      prefix="/users",
                      tags=["users"],
                      )

router.include_router(articles.router,
                      prefix="/articles",
                      tags=["articles"],
                      )
router.include_router(auth.router,
                      prefix="",
                      tags=["auth"],
                      )

router.include_router(root.router,
                      prefix=""
                      )
