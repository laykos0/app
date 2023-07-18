from beanie import PydanticObjectId

from src.domain.articles import (
    ArticleCreateDTO,
    ArticleId,
    ArticleUpdateDTO
)
from src.infrastructure.exceptions import (
    ArticleNotFoundException,
    VersionNotFoundException
)
from src.infrastructure.repositories.articles import (
    insert,
    find,
    find_versions,
    find_version,
    find_versions_all,
    find_from_all
)


async def post(author_id: PydanticObjectId, article_create_dto: ArticleCreateDTO):
    article = article_create_dto.to_document()
    article.version.new(author_id)
    return await insert(article)


async def get(article_id: ArticleId, all_articles: bool):
    if all_articles:
        article = await find_from_all(article_id)
    else:
        article = await find(article_id)
    if article:
        return article
    raise ArticleNotFoundException(article_id)


async def get_versions(article_id: ArticleId, all_articles: bool):
    if all_articles:
        versions = await find_versions_all(article_id)
    else:
        versions = await find_versions(article_id)
    if versions:
        return versions
    raise ArticleNotFoundException(article_id)


async def get_version(article_id: ArticleId, version: int):
    if article_version := await find_version(article_id, version):
        return article_version
    raise VersionNotFoundException(article_id, version)


async def put(article_id: ArticleId, user_id: PydanticObjectId, article_update_dto: ArticleUpdateDTO):
    article = await get(article_id, True)
    article_update = article_update_dto.to_document()
    article.patch(user_id, name=article_update.name, description=article_update.description,
                  price=article_update.price)
    return await insert(article)


async def confirm(article_id: ArticleId, user_id: PydanticObjectId, approved: bool = True):
    article = await get(article_id, True)
    article.patch(user_id, approved=approved)
    return await insert(article)


async def remove(article_id: ArticleId, user_id: PydanticObjectId, deleted: bool = True):
    article = await get(article_id, True)
    article.patch(user_id, deleted=deleted)
    return await insert(article)
