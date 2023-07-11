from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import Field, BaseModel


class Article(Document):
    name: str = Field(..., description="Name of the article.", example="Book")
    description: str | None = Field(..., description="Description of the article.")
    price: int = Field(..., description="Price of the article.", example="1")
    author_id: PydanticObjectId = Field(..., description="Author of the article.")
    date_modified: datetime = Field(default_factory=lambda: datetime.utcnow(),
                                    description="Date modified of the article.")
    deleted: bool = Field(False, description="Soft delete status.")
    approved: bool = Field(False, description="Approved status.")
    version: int = Field(0, description="Version of the article.")

    class Settings:
        name = "articles"

    def to_version(self):
        return ArticleVersion(original_article_id=self.id, **self.dict(exclude={"id"}))

    def update_version(self, user_id: PydanticObjectId, date_modified: datetime):
        self.author_id = user_id
        self.date_modified = date_modified
        self.version = self.version + 1


class ArticleVersion(Article):
    original_article_id: PydanticObjectId = Field(description="ID of the original article.")

    class Settings:
        name = "article_versions"


class CreateArticleDTO(BaseModel):
    name: str = Field(..., description="Name of the new article.", example="Book")
    description: str | None = Field(..., description="Description of the new article.")
    price: int = Field(..., description="Price of the new article.", example="1")

    def to_document(self, user_id: PydanticObjectId):
        return Article(author_id=user_id, **self.dict())


class UpdateArticleDTO(BaseModel):
    name: str = Field(..., description="New name of the article.", example="Book")
    description: str | None = Field(..., description="New description of the article.")
    price: int = Field(..., description="New price of the article.", example="1")

    def to_document(self, user_id: PydanticObjectId):
        return Article(author_id=user_id, **self.dict())
