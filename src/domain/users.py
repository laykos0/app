from enum import Enum

from beanie import Document, Indexed
from dataclass_mapper import mapper, mapper_from, init_with_default, provide_with_extra
from pydantic import Field, BaseModel


class Role(str, Enum):
    user = "user"
    admin = "admin"


class UserCreateDTO(BaseModel):
    name: str = Field(..., description="Name of the new user.", example="name")
    role: Role = Field(..., description="Role of the new user.", example="user")
    password: str = Field(..., description="Password of the new user.", example="password")


class UserUpdateDTO(BaseModel):
    name: str = Field(..., description="New name of the user.", example="new_name")
    role: Role = Field(..., description="New role of the user.", example="admin")
    password: str = Field(..., description="New password of the user.", example="new_password")


@mapper_from(UserCreateDTO)
@mapper_from(UserUpdateDTO)
class User(BaseModel):
    name: str = Field(..., description="Name of the user.", example="name")
    role: Role = Field(..., description="Role of the user.", example="user")


@mapper(User, {"name": lambda self: self.name})
@mapper_from(User, {"name": lambda self: self.name, "id": init_with_default(), "revision_id": init_with_default(),
                    "hashed_password": provide_with_extra()})
class UserInDB(Document):
    name: Indexed(str, unique=True)
    role: Role = Field(..., description="Role of the user.", example="user")
    hashed_password: str = Field(..., description="Hashed password of the user.")

    class Settings:
        name = "users"

    def patch(self, name: str, role: Role, hashed_password: str):
        self.name = name
        self.role = role
        self.hashed_password = hashed_password
