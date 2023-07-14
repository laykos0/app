from fastapi import APIRouter, Depends

from api.routers import users, articles
from core.dependencies import get_token_header

router = APIRouter()

router.include_router(users.router,
                      prefix="/users",
                      tags=["users"],
                      )


router.include_router(articles.router,
                      prefix="/articles",
                      tags=["articles"],
                      dependencies=[Depends(get_token_header)],
                      )
