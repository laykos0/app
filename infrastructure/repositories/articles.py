from domain.articles import Article, ArticleId


async def insert(article: Article):
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
