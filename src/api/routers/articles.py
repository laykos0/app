from typing import Annotated

from fastapi import APIRouter, Query, Body, Path, Depends

from src.domain.articles import (
    ArticleId,
    Article,
    ArticleCreateDTO,
    ArticleUpdateDTO
)
from src.domain.users import UserInDB
from src.infrastructure.services.articles import (
    post,
    get,
    get_versions,
    get_version,
    put,
    remove,
    confirm
)
from src.infrastructure.services.auth import (
    get_current_user, is_admin
)

router = APIRouter()


@router.post("",
             description="Creates a new article.",
             dependencies=[Depends(is_admin)]
             )
async def create_article(user: Annotated[UserInDB, Depends(get_current_user)],
                         article_create_dto: ArticleCreateDTO = Body()):
    return await post(user, article_create_dto)


@router.get("/{article_id}",
            description="Retrieves newest approved version of the article.",
            response_model=Article
            )
async def get_article(user: Annotated[UserInDB, Depends(get_current_user)],
                      article_id: ArticleId = Path()):
    return await get(user, article_id)


@router.get("/versions/{article_id}",
            description="Retrieves all approved versions of an article.",
            response_model=list[Article]
            )
async def get_article_versions(user: Annotated[UserInDB, Depends(get_current_user)],
                               article_id: ArticleId = Path()):
    return await get_versions(user, article_id)


@router.get("/versions/{article_id}/{version}",
            description="Retrieves one version of an article.",
            )
async def get_article_version(user: Annotated[UserInDB, Depends(get_current_user)],
                              article_id: ArticleId = Path(),
                              version: int = Path(example="1")):
    return await get_version(user, article_id, version)


@router.put("/{article_id}",
            description="Updates an article and stores its historical version.",
            dependencies=[Depends(is_admin)]
            )
async def update_article(user: Annotated[UserInDB, Depends(get_current_user)],
                         article_id: ArticleId = Path(),
                         article_update_dto: ArticleUpdateDTO = Body()):
    return await put(user, article_id, article_update_dto)


@router.patch("/{article_id}",
              description="Approves an article version.",
              dependencies=[Depends(is_admin)]
              )
async def approve_article(user: Annotated[UserInDB, Depends(get_current_user)],
                          article_id: ArticleId = Path(),
                          approved: bool = Query(default=True)):
    return await confirm(user, article_id, approved)


@router.delete("/{article_id}",
               description="Soft deletes an article version.",
               dependencies=[Depends(is_admin)]
               )
async def delete_article(user: Annotated[UserInDB, Depends(get_current_user)],
                         article_id: ArticleId = Path(),
                         deleted: bool = Query(default=True)):
    return await remove(user, article_id, deleted)
