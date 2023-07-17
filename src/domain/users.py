from enum import Enum

from beanie import Document
from pydantic import Field, BaseModel


class Role(str, Enum):
    user = "user"
    admin = "admin"


class User(Document):
    name: str = Field(..., description="Name of the user.", example="name")
    role: Role = Field(..., description="Role of the user.", example="user")

    class Settings:
        name = "users"

    def patch(self, name: str, role: Role):
        self.name = name
        self.role = role


class UserInDB(User):
    hashed_password: str

    def to_user(self):
        return User(**self.dict())


class UserCreateDTO(BaseModel):
    name: str = Field(..., description="Name of the new user.", example="name")
    role: Role = Field(..., description="Role of the new user.", example="user")

    def to_document(self):
        return User(**self.dict())


class UserUpdateDTO(BaseModel):
    name: str = Field(..., description="New name of the new user.", example="new_name")
    role: Role = Field(..., description="New role of the new user.", example="admin")

    def to_document(self):
        return User(**self.dict())
