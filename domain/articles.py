from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import Field, BaseModel

ArticleId = str


class Version(BaseModel):
    author_id: PydanticObjectId | None = Field(None, description="Author of the article.")
    date_modified: datetime = Field(default_factory=lambda: datetime.utcnow(),
                                    description="Date modified of the article.")
    deleted: bool = Field(False, description="Soft delete status.")
    approved: bool = Field(False, description="Approved status.")
    number: int = Field(0, description="Version number of the article.")

    def update_version(self, author_id: PydanticObjectId, approved: bool = None, deleted: bool = None):
        self.author_id = author_id
        self.date_modified = datetime.utcnow()
        self.number += 1
        if approved is not None:
            self.approved = approved
        if deleted is not None:
            self.deleted = deleted


class Article(Document):
    article_id: ArticleId = Field(default_factory=lambda: datetime.utcnow().isoformat(),
                                  description="Id of the article.")
    name: str = Field(..., description="Name of the article.", example="Book")
    description: str | None = Field(..., description="Description of the article.")
    price: int = Field(..., description="Price of the article.", example="1")
    version: Version = Field(Version(), description="Version of the article.")

    class Settings:
        name = "articles"


class CreateArticleDTO(BaseModel):
    name: str = Field(..., description="Name of the new article.", example="Book")
    description: str | None = Field(..., description="Description of the new article.")
    price: int = Field(..., description="Price of the new article.", example="1")

    def to_document(self):
        return Article(**self.dict())


class UpdateArticleDTO(BaseModel):
    name: str = Field(..., description="New name of the article.", example="Book")
    description: str | None = Field(..., description="New description of the article.")
    price: int = Field(..., description="New price of the article.", example="1")

    def to_document(self):
        return Article(**self.dict())
