from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class Version(BaseModel):
    author_id: PydanticObjectId | None = Field(None, description="Author of the article.")
    date_modified: datetime = Field(default_factory=lambda: datetime.utcnow(),
                                    description="Date modified of the article.")
    deleted: bool = Field(False, description="Soft delete status.")
    approved: bool = Field(False, description="Approved status.")
    number: int = Field(0, description="Version number of the article.")

    def new(self, author_id: PydanticObjectId, approved: bool = False, deleted: bool = False):
        self.author_id = author_id
        self.date_modified = datetime.utcnow()
        self.number += 1
        self.approved = approved
        self.deleted = deleted
