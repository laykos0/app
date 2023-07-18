from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Path, Body, Depends

from src.domain.users import (
    User,
    UserCreateDTO,
    UserUpdateDTO
)
from src.infrastructure.services.auth import get_current_user
from src.infrastructure.services.users import (
    post,
    get,
    get_all,
    put,
    remove
)

router = APIRouter()


@router.post("",
             description="Creates a new user."
             )
async def create_user(user_create_dto: UserCreateDTO = Body()):
    await post(user_create_dto)


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/{user_id}",
            description="Retrieves one user.",
            response_model=User
            )
async def get_user(user_id: PydanticObjectId = Path()):
    return await get(user_id)


@router.get("",
            description="Retrieves all users.",
            response_model=list[User]
            )
async def get_all_users():
    return await get_all()


@router.put("/{user_id}",
            description="Updates an user.",
            )
async def update_user(user_id: PydanticObjectId = Path(), user_update_dto: UserUpdateDTO = Body()):
    await put(user_id, user_update_dto)


@router.delete("/{user_id}",
               description="Deletes an user."
               )
async def delete_user(user_id: PydanticObjectId = Path()):
    await remove(user_id)
