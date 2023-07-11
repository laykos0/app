from beanie import PydanticObjectId

from domain.articles import CreateArticleDTO, UpdateArticleDTO
from infrastructure.exceptions import ArticleNotFoundException, VersionNotFoundException
from infrastructure.repositories.articles import post, get, put, delete, post_version, get_available, get_versions, \
    get_version


async def insert(user_id: PydanticObjectId, create_article_dto: CreateArticleDTO):
    await post(create_article_dto.to_document(user_id))


async def find(article_id: PydanticObjectId):
    article = await get(article_id)
    if article:
        return article
    raise ArticleNotFoundException(article_id)


async def find_versions(article_id: PydanticObjectId):
    article = await get(article_id)
    if not article:
        raise ArticleNotFoundException(article_id)
    return await get_versions(article_id)


async def find_version(article_id: PydanticObjectId, version: int):
    article = await get(article_id)
    if not article:
        raise ArticleNotFoundException(article_id)
    if article.version == version:
        return article.to_version()
    article_version = await get_version(article_id, version)
    if not article_version:
        raise VersionNotFoundException(article_id, version)
    return article_version


async def find_available(available: bool):
    return await get_available(available)


async def update(article_id: PydanticObjectId, user_id: PydanticObjectId, update_article_dto: UpdateArticleDTO):
    article = await get(article_id)
    if not article:
        raise ArticleNotFoundException(article_id)
    await post_version(article.to_version())
    await put(article_id, user_id, update_article_dto.to_document(user_id))


async def remove(article_id: PydanticObjectId, user_id: PydanticObjectId):
    article = await get(article_id)
    if not article:
        raise ArticleNotFoundException(article_id)
    await delete(article_id, user_id)
