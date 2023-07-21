from pydantic import BaseModel, Field

from src.domain.role import Role


class UserCreateDTO(BaseModel):
    name: str = Field(..., description="Name of the new user.", example="name")
    role: Role = Field(..., description="Role of the new user.", example="user")
    password: str = Field(..., description="Password of the new user.", example="password")


class UserUpdateDTO(BaseModel):
    name: str = Field(..., description="New name of the user.", example="new_name")
    role: Role = Field(..., description="New role of the user.", example="admin")
    password: str = Field(..., description="New password of the user.", example="new_password")


class ArticleCreateDTO(BaseModel):
    name: str = Field(..., description="Name of the new article.", example="Book")
    description: str | None = Field(..., description="Description of the new article.")
    price: int = Field(..., description="Price of the new article.", example="1")


class ArticleUpdateDTO(BaseModel):
    name: str = Field(..., description="New name of the article.", example="Book")
    description: str | None = Field(..., description="New description of the article.")
    price: int = Field(..., description="New price of the article.", example="1")
