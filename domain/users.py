from enum import Enum

from beanie import Document
from pydantic import Field, BaseModel


class Role(str, Enum):
    user = "user"
    admin = "admin"


class User(Document):
    name: str = Field(..., description="Name of the user.", example="name")
    roles: list[Role] = Field(..., description="Roles of the user.", example=["user"])


class CreateUserDTO(BaseModel):
    name: str = Field(..., description="Name of the new user.", example="name")
    roles: list[str] = Field(..., description="Roles of the new user.", example=["user"])

    def to_document(self):
        return User(**self.dict())


class UpdateUserDTO(BaseModel):
    name: str = Field(..., description="New name of the new user.", example="name")
    roles: list[str] = Field(..., description="New role of the new user.", example=["user"])

    def to_document(self):
        return User(**self.dict())
