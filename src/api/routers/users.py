from beanie import PydanticObjectId
from fastapi import APIRouter, Path, Body

from src.domain.users import User, CreateUserDTO, UpdateUserDTO
from src.infrastructure.services.users import find_all, insert, find, update, remove

router = APIRouter()


@router.post("",
             description="Creates a new user."
             )
async def create_user(create_user_dto: CreateUserDTO = Body()):
    await insert(create_user_dto)


@router.get("/{user_id}",
            description="Retrieves one user.",
            response_model=User
            )
async def get_user(user_id: PydanticObjectId = Path()):
    return await find(user_id)


@router.get("",
            description="Retrieves all users.",
            response_model=list[User]
            )
async def get_all_users():
    return await find_all()


@router.put(
    "/{user_id}",
    description="Updates an user.",
)
async def update_user(user_id: PydanticObjectId = Path(), update_user_dto: UpdateUserDTO = Body()):
    await update(user_id, update_user_dto)


@router.delete("/{user_id}",
               description="Deletes an user."
               )
async def delete_user(user_id: PydanticObjectId = Path()):
    await remove(user_id)
