from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Query, Body, Path, Depends

from src.domain.articles import ArticleId, Article, ArticleCreateDTO, ArticleUpdateDTO
from src.infrastructure.services.articles import post, get, get_versions, get_version, put, remove, confirm
from src.infrastructure.services.auth import get_current_user_admin_status, get_current_user_id, \
    get_current_user_permission

router = APIRouter()


@router.post("",
             description="Creates a new article.",
             dependencies=[Depends(get_current_user_admin_status)],
             )
async def create_article(user_id: Annotated[PydanticObjectId, Depends(get_current_user_id)],
                         article_create_dto: ArticleCreateDTO = Body()):
    return await post(user_id, article_create_dto)


@router.get("/{article_id}",
            description="Retrieves newest approved version of the article.",
            response_model=Article
            )
async def get_article(all_articles: Annotated[bool, Depends(get_current_user_permission)],
                      article_id: ArticleId = Path()):
    return await get(article_id, all_articles)


@router.get("/versions/{article_id}",
            description="Retrieves all approved versions of an article.",
            response_model=list[Article]
            )
async def get_article_versions(all_articles: Annotated[bool, Depends(get_current_user_permission)],
                               article_id: ArticleId = Path()):
    return await get_versions(article_id, all_articles)


@router.get("/versions/{article_id}/{version}",
            description="Retrieves one version of an article.",
            )
async def get_article_version(article_id: ArticleId = Path(), version: int = Path(example="1")):
    return await get_version(article_id, version)


@router.put("/{article_id}",
            description="Updates an article and stores its historical version.",
            dependencies=[Depends(get_current_user_admin_status)],
            )
async def update_article(user_id: Annotated[PydanticObjectId, Depends(get_current_user_id)],
                         article_id: ArticleId = Path(),
                         article_update_dto: ArticleUpdateDTO = Body()):
    return await put(article_id, user_id, article_update_dto)


@router.patch("/{article_id}",
              description="Approves an article version.",
              dependencies=[Depends(get_current_user_admin_status)],
              )
async def approve_article(user_id: Annotated[PydanticObjectId, Depends(get_current_user_id)],
                          article_id: ArticleId = Path(),
                          approved: bool = Query(default=True)):
    return await confirm(article_id, user_id, approved)


@router.delete("/{article_id}",
               description="Soft deletes an article version.",
               dependencies=[Depends(get_current_user_admin_status)],
               )
async def delete_article(user_id: Annotated[PydanticObjectId, Depends(get_current_user_id)],
                         article_id: ArticleId = Path(),
                         deleted: bool = Query(default=True)):
    return await remove(article_id, user_id, deleted)
