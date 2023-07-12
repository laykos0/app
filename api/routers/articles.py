from beanie import PydanticObjectId
from fastapi import APIRouter, Query, Body, Path

from domain.articles import ArticleId, Article, CreateArticleDTO, UpdateArticleDTO
from infrastructure.services.articles import post, get, get_versions, get_version, put, remove, confirm, \
    get_versions_all, get_from_all

router = APIRouter()


@router.post("/create",
             description="Creates a new article.",
             )
async def create_article(author_id: PydanticObjectId = Query(example="64ac6904e80399a368013184"),
                         create_article_dto: CreateArticleDTO = Body()):
    await post(author_id, create_article_dto)


@router.get("/{article_id}",
            description="Retrieves newest approved version of the article.",
            response_model=Article
            )
async def get_article(article_id: ArticleId = Path()):
    return await get(article_id)


@router.get("/all/{article_id}",
            description="Retrieves newest version of the article.",
            response_model=Article
            )
async def get_article_from_all(article_id: ArticleId = Path()):
    return await get_from_all(article_id)


@router.get("/versions/{article_id}",
            description="Retrieves all approved versions of an article.",
            response_model=list[Article]
            )
async def get_article_versions(article_id: ArticleId = Path()):
    return await get_versions(article_id)


@router.get("/versions/all/{article_id}",
            description="Retrieves all versions of an article.",
            response_model=list[Article]
            )
async def get_article_versions_all(article_id: ArticleId = Path()):
    return await get_versions_all(article_id)


@router.get("/versions/{article_id}/{version}",
            description="Retrieves one version of an article.",
            response_model=Article
            )
async def get_article_version(article_id: ArticleId = Path(), version: int = Path(example="1")):
    return await get_version(article_id, version)


@router.put("/update/{article_id}/{version}",
            description="Updates an article and stores its historical version.",
            )
async def update_article(article_id: ArticleId = Path(),
                         user_id: PydanticObjectId = Body(example="64ac6904e80399a368013184"),
                         update_article_dto: UpdateArticleDTO = Body()):
    return await put(article_id, user_id, update_article_dto)


@router.put("/approve/{article_id}/{version}",
            description="Approves an article version.",
            )
async def approve_article(article_id: ArticleId = Path(),
                          user_id: PydanticObjectId = Body(example="64ac6904e80399a368013184"),
                          approved: bool = Query(default=True)):
    return await confirm(article_id, user_id, approved)


@router.delete("/delete/{article_id}/{version}",
               description="Soft deletes an article version."
               )
async def delete_article(article_id: ArticleId = Path(),
                         user_id: PydanticObjectId = Body(example="64ac6904e80399a368013184"),
                         deleted: bool = Query(default=True)):
    await remove(article_id, user_id, deleted)
