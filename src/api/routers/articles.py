from beanie import PydanticObjectId
from fastapi import APIRouter, Query, Body, Path

from src.domain.articles import ArticleId, Article, ArticleCreateDTO, ArticleUpdateDTO
from src.infrastructure.services.articles import post, get, get_versions, get_version, put, remove, confirm

router = APIRouter()


@router.post("",
             description="Creates a new article.",
             )
async def create_article(author_id: PydanticObjectId = Query(example="64ac6904e80399a368013184"),
                         article_create_dto: ArticleCreateDTO = Body()):
    await post(author_id, article_create_dto)


@router.get("/{article_id}",
            description="Retrieves newest approved version of the article.",
            response_model=Article
            )
async def get_article(article_id: ArticleId = Path(), all_articles: bool = Query(default=False)):
    return await get(article_id, all_articles)


@router.get("/versions/{article_id}",
            description="Retrieves all approved versions of an article.",
            response_model=list[Article]
            )
async def get_article_versions(article_id: ArticleId = Path(), all_articles: bool = Query(default=False)):
    return await get_versions(article_id, all_articles)


@router.get("/versions/{article_id}/{version}",
            description="Retrieves one version of an article.",
            )
async def get_article_version(article_id: ArticleId = Path(), version: int = Path(example="1")):
    return await get_version(article_id, version)


@router.put("/{article_id}",
            description="Updates an article and stores its historical version.",
            )
async def update_article(article_id: ArticleId = Path(),
                         user_id: PydanticObjectId = Body(example="64ac6904e80399a368013184"),
                         article_update_dto: ArticleUpdateDTO = Body()):
    return await put(article_id, user_id, article_update_dto)


@router.patch("/{article_id}",
              description="Approves an article version.",
              )
async def approve_article(article_id: ArticleId = Path(),
                          user_id: PydanticObjectId = Body(example="64ac6904e80399a368013184"),
                          approved: bool = Query(default=True)):
    return await confirm(article_id, user_id, approved)


@router.delete("/{article_id}",
               description="Soft deletes an article version."
               )
async def delete_article(article_id: ArticleId = Path(),
                         user_id: PydanticObjectId = Body(example="64ac6904e80399a368013184"),
                         deleted: bool = Query(default=True)):
    await remove(article_id, user_id, deleted)
