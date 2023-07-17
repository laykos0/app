from src.domain.articles import Article, ArticleId


async def insert(article: Article):
    article.id = None
    await article.insert()


async def find(article_id: ArticleId):
    return await Article.find(Article.article_id == article_id,
                              Article.version.approved == True,
                              Article.version.deleted == False).sort(-Article.id).first_or_none()


async def find_from_all(article_id: ArticleId):
    return await Article.find(Article.article_id == article_id).sort(-Article.id).first_or_none()


async def find_versions(article_id: ArticleId):
    return await Article.find(Article.article_id == article_id,
                              Article.version.approved == True,
                              Article.version.deleted == False).to_list()


async def find_versions_all(article_id: ArticleId):
    return await Article.find(Article.article_id == article_id).to_list()


async def find_version(article_id: ArticleId, version: int):
    return await Article.find(Article.article_id == article_id,
                              Article.version.number == version).sort(-Article.id).first_or_none()
