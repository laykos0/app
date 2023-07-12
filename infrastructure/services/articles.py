from beanie import PydanticObjectId

from domain.articles import CreateArticleDTO, ArticleId, UpdateArticleDTO
from infrastructure.exceptions import ArticleNotFoundException, VersionNotFoundException
from infrastructure.repositories.articles import insert, find, find_versions, update, delete, find_version, approve, \
    find_versions_all, find_from_all


async def post(author_id: PydanticObjectId, create_article_dto: CreateArticleDTO):
    await insert(author_id, create_article_dto.to_document())


async def get(article_id: ArticleId):
    article = await find(article_id)
    if article:
        return article
    raise ArticleNotFoundException(article_id)


async def get_from_all(article_id: ArticleId):
    article = await find_from_all(article_id)
    if article:
        return article
    raise ArticleNotFoundException(article_id)


async def get_versions(article_id: ArticleId):
    versions = await find_versions(article_id)
    if versions:
        return versions
    raise ArticleNotFoundException(article_id)


async def get_versions_all(article_id: ArticleId):
    versions = await find_versions_all(article_id)
    if versions:
        return versions
    raise ArticleNotFoundException(article_id)


async def get_version(article_id: ArticleId, version: int):
    article_version = await find_version(article_id, version)
    if article_version:
        return article_version
    raise VersionNotFoundException(article_id, version)


async def put(article_id: ArticleId, user_id: PydanticObjectId, update_article_dto: UpdateArticleDTO):
    await get_from_all(article_id)
    await update(article_id, user_id, update_article_dto.to_document())


async def confirm(article_id: ArticleId, user_id: PydanticObjectId, approved: bool = True):
    await get_from_all(article_id)
    await approve(article_id, user_id, approved)


async def remove(article_id: ArticleId, user_id: PydanticObjectId, deleted: bool = True):
    await get_from_all(article_id)
    await delete(article_id, user_id, deleted)
