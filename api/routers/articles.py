from beanie import PydanticObjectId
from fastapi import APIRouter, Query, Body, Path

from domain.articles import Article, CreateArticleDTO, UpdateArticleDTO, ArticleVersion
from infrastructure.services.articles import insert, find, update, remove, find_available, find_versions, find_version

router = APIRouter()


@router.post("",
             description="Creates a new article.",
             )
async def create_article(user_id: PydanticObjectId = Body(example="64ac6904e80399a368013184"),
                         create_article_dto: CreateArticleDTO = Body()):
    await insert(user_id, create_article_dto)


@router.get("/{article_id}",
            description="Retrieves one article.",
            response_model=Article
            )
async def get_article(article_id: PydanticObjectId = Path()):
    return await find(article_id)


@router.get("/{article_id}/versions",
            description="Retrieves all historical versions of an article.",
            response_model=list[ArticleVersion]
            )
async def get_article_versions(article_id: PydanticObjectId = Path(), approved: bool = Query(default=True)):
    return await find_versions(article_id, approved)


@router.get("/{article_id}/versions/{version}",
            description="Retrieves one historical or newest version of an article.",
            response_model=ArticleVersion
            )
async def get_article_version(article_id: PydanticObjectId = Path(), version: int = Path(example="0")):
    return await find_version(article_id, version)


@router.get("",
            description="Retrieves all available articles.",
            response_model=list[Article]
            )
async def get_available_articles(available: bool = Query(default=True)):
    return await find_available(available)


@router.put("/{article_id}",
            description="Updates an article and stores its historical version.",
            response_model=Article
            )
async def update_article(article_id: PydanticObjectId = Path(),
                         user_id: PydanticObjectId = Body(example="64ac6904e80399a368013184"),
                         update_article_dto: UpdateArticleDTO = Body()):
    return await update(article_id, user_id, update_article_dto)


@router.delete("/{article_id}",
               description="Soft deletes an article."
               )
async def delete_article(article_id: PydanticObjectId = Path(),
                         user_id: PydanticObjectId = Body(example="64ac6904e80399a368013184")):
    await remove(article_id, user_id)
