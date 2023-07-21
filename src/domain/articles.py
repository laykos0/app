from datetime import datetime

from beanie import Document, PydanticObjectId
from dataclass_mapper import mapper_from, init_with_default
from pydantic import Field

from src.domain.version import Version
from src.infrastructure.dto import (
    ArticleCreateDTO,
    ArticleUpdateDTO
)

ArticleId = str


@mapper_from(ArticleCreateDTO,
             {"id": init_with_default(),
              "revision_id": init_with_default(),
              "article_id": init_with_default(),
              "version": init_with_default()
              })
@mapper_from(ArticleUpdateDTO,
             {"id": init_with_default(),
              "revision_id": init_with_default(),
              "article_id": init_with_default(),
              "version": init_with_default()
              })
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
