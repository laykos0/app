from src.domain.articles import (
    ArticleCreateDTO,
    ArticleId,
    ArticleUpdateDTO
)
from src.domain.users import (
    UserInDB,
    Role
)
from src.infrastructure.exceptions import (
    ArticleNotFoundException,
    VersionNotFoundException,
    InsufficientPermissionException
)
from src.infrastructure.repositories.articles import (
    insert,
    find,
    find_from_all,
    find_version,
    find_version_all,
    find_versions,
    find_versions_all,
)


async def post(user: UserInDB, article_create_dto: ArticleCreateDTO):
    is_admin(user)
    article = article_create_dto.to_document()
    article.version.new(user.id)
    return await insert(article)


async def get(user: UserInDB, article_id: ArticleId):
    if user.role == Role.admin:
        article = await find_from_all(article_id)
    else:
        article = await find(article_id)
    if article:
        return article
    raise ArticleNotFoundException(article_id)


async def get_versions(user: UserInDB, article_id: ArticleId):
    if user.role == Role.admin:
        versions = await find_versions_all(article_id)
    else:
        versions = await find_versions(article_id)
    if versions:
        return versions
    raise ArticleNotFoundException(article_id)


async def get_version(user: UserInDB, article_id: ArticleId, version_number: int):
    if user.role == Role.admin:
        version = await find_version_all(article_id, version_number)
    else:
        version = await find_version(article_id, version_number)
    if version:
        return version
    raise VersionNotFoundException(article_id, version_number)


async def put(user: UserInDB, article_id: ArticleId, article_update_dto: ArticleUpdateDTO):
    is_admin(user)
    article = await get(user, article_id)
    article_update = article_update_dto.to_document()
    article.patch(user.id, name=article_update.name, description=article_update.description,
                  price=article_update.price)
    return await insert(article)


async def confirm(user: UserInDB, article_id: ArticleId, approved: bool = True):
    is_admin(user)
    article = await get(user, article_id)
    article.patch(user.id, approved=approved)
    return await insert(article)


async def remove(user: UserInDB, article_id: ArticleId, deleted: bool = True):
    is_admin(user)
    article = await get(user, article_id)
    article.patch(user.id, deleted=deleted)
    return await insert(article)


def is_admin(user: UserInDB):
    if user.role != Role.admin:
        raise InsufficientPermissionException(user.id, user.role)
