from beanie import PydanticObjectId

from api.domain.users import CreateUserDTO, UpdateUserDTO
from infrastructure.exceptions import UserNotFoundException
from infrastructure.repositories.users import post, get, get_all, put, delete


async def insert(create_user_dto: CreateUserDTO):
    user = create_user_dto.to_document()
    await post(user)


async def find(user_id: PydanticObjectId):
    user = await get(user_id)
    if not user:
        raise UserNotFoundException(user_id)
    return user


async def find_all():
    return await get_all()


async def update(user_id: PydanticObjectId, update_user_dto: UpdateUserDTO):
    user = update_user_dto.to_document()
    updated_user = await put(user_id, user)
    if not updated_user:
        raise UserNotFoundException(user_id)
    return updated_user


async def remove(user_id: PydanticObjectId):
    user = await get(user_id)
    if not user:
        raise UserNotFoundException(user_id)
    await delete(user_id)
