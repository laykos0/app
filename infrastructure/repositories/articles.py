from beanie import PydanticObjectId
from bson import ObjectId

from domain.articles import Article, ArticleId


async def insert(author_id: PydanticObjectId, article: Article):
    article.version.update_version(author_id)
    await article.insert()


async def find(article_id: ArticleId):
    pipeline = [
        {
            "$match": {
                "article_id": article_id,
                "version.approved": True,
                "version.deleted": False
            }
        },
        {
            "$sort": {
                "_id": -1
            }
        },
        {
            "$limit": 1
        }
    ]
    articles = await Article.aggregate(pipeline).to_list()
    if articles:
        return articles[0]
    else:
        return None


async def find_from_all(article_id: ArticleId):
    article = await Article.find(Article.article_id == article_id).to_list()
    if article:
        return article[-1]
    return None


async def find_versions(article_id: ArticleId):
    pipeline = [
        {
            "$match": {
                "article_id": article_id,
                "version.approved": True,
                "version.deleted": False
            }
        }
    ]
    return await Article.aggregate(pipeline).to_list()


async def find_versions_all(article_id: ArticleId):
    return await Article.find(Article.article_id == article_id).to_list()


async def find_version(article_id: ArticleId, version: int):
    pipeline = [
        {
            "$match": {
                "article_id": article_id,
                "version.number": version
            }
        }
    ]
    version = await Article.aggregate(pipeline).to_list()
    if version:
        return version[0]
    return None


async def update(article_id: ArticleId, author_id: PydanticObjectId, update_article: Article):
    article = await prepare_for_update(article_id)
    article.name = update_article.name
    article.description = update_article.description
    article.price = update_article.price
    article.version.update_version(author_id)
    await article.insert()
    return article


async def delete(article_id: ArticleId, author_id: PydanticObjectId, deleted: bool):
    article = await prepare_for_update(article_id)
    article.version.update_version(author_id, deleted=deleted)
    await article.insert()


async def approve(article_id: ArticleId, author_id: PydanticObjectId, approved: bool):
    article = await prepare_for_update(article_id)
    article.version.update_version(author_id, approved=approved)
    await article.insert()


async def prepare_for_update(article_id: ArticleId):
    article = await find_from_all(article_id)
    article.id = PydanticObjectId(ObjectId())
    article.version.deleted = False
    article.version.approved = False
    return article
