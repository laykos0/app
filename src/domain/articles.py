from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import Field, BaseModel

from src.domain.version import Version

ArticleId = str


class Article(Document):
    article_id: ArticleId = Field(default_factory=lambda: datetime.utcnow().isoformat(),
                                  description="Id of the article.")
    name: str = Field(..., description="Name of the article.", example="Book")
    description: str | None = Field(..., description="Description of the article.")
    price: int = Field(..., description="Price of the article.", example="1")
    version: Version = Field(Version(), description="Version of the article.")

    class Settings:
        name = "articles"

    def patch(self, user_id: PydanticObjectId, name: str = None, description: str = None,
              price: int = None, approved: bool = False, deleted: bool = False):
        if name:
            self.name = name
        if description:
            self.description = description
        if price:
            self.price = price
        self.version.new(user_id, approved, deleted)


class ArticleCreateDTO(BaseModel):
    name: str = Field(..., description="Name of the new article.", example="Book")
    description: str | None = Field(..., description="Description of the new article.")
    price: int = Field(..., description="Price of the new article.", example="1")

    def to_document(self):
        return Article(**self.dict())


class ArticleUpdateDTO(BaseModel):
    name: str = Field(..., description="New name of the article.", example="Book")
    description: str | None = Field(..., description="New description of the article.")
    price: int = Field(..., description="New price of the article.", example="1")

    def to_document(self):
        return Article(**self.dict())
