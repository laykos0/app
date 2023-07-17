from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from pydantic.class_validators import validator


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

    @validator('date_modified', pre=True, always=True)
    def validate_datetime(cls, v):
        if isinstance(v, datetime):
            return v
        elif isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError("Invalid format")
        else:
            raise ValueError("Invalid format")
