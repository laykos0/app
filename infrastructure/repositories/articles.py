from datetime import datetime

from beanie import PydanticObjectId

from domain.articles import Article, ArticleVersion


async def post(article: Article):
    await article.insert()


async def post_version(article_version: ArticleVersion):
    await article_version.insert()


async def get(article_id: PydanticObjectId):
    return await Article.get(article_id)


async def get_versions(article_id: PydanticObjectId):
    return await ArticleVersion.find(ArticleVersion.original_article_id == article_id).to_list()


async def get_version(article_id: PydanticObjectId, version: int):
    return await ArticleVersion.find_one(ArticleVersion.original_article_id == article_id,
                                         ArticleVersion.version == version)


async def get_available(available: bool):
    return await Article.find({"deleted": not available}).to_list()


async def put(article_id: PydanticObjectId, user_id: PydanticObjectId, update_article: Article):
    article = await get(article_id)
    article.name = update_article.name
    article.description = update_article.description
    article.price = update_article.price
    article.update_version(user_id)
    await article.save()
    return article


async def delete(article_id: PydanticObjectId, user_id: PydanticObjectId):
    article = await get(article_id)
    article.update_version(user_id)
    article.deleted = True
    await article.save()



