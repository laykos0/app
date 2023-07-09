from beanie import PydanticObjectId
from fastapi import APIRouter, Path, Body

from api.domain.users import User, CreateUserDTO, UpdateUserDTO
from infrastructure.services.users import find_all, insert, find, update, remove

router = APIRouter()


@router.post("",
             summary="Create",
             description=""
             )
async def post(create_user_dto: CreateUserDTO = Body()):
    await insert(create_user_dto)


@router.get("/{user_id}",
            summary="Read",
            description="",
            response_model=User
            )
async def get(user_id: PydanticObjectId = Path()):
    return await find(user_id)


@router.get("",
            summary="Read all",
            description="",
            response_model=list[User]
            )
async def get_all():
    return await find_all()


@router.put(
    "/{user_id}",
    summary="Update",
    description="",
)
async def put(user_id: PydanticObjectId = Path(), update_user_dto: UpdateUserDTO = Body()):
    await update(user_id, update_user_dto)


@router.delete("/{user_id}",
               summary="Delete",
               description=""
               )
async def delete(user_id: PydanticObjectId = Path()):
    await remove(user_id)
