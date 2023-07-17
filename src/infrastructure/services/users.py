from beanie import PydanticObjectId

from src.domain.users import CreateUserDTO, UpdateUserDTO
from src.infrastructure.exceptions import UserNotFoundException
from src.infrastructure.repositories.users import post, get, get_all, put, delete

# TODO: Maybe invert naming


async def insert(create_user_dto: CreateUserDTO):
    user = create_user_dto.to_document()
    await post(user)


async def find(user_id: PydanticObjectId):
    user = await get(user_id)
    if user:
        return user
    raise UserNotFoundException(user_id)


async def find_all():
    return await get_all()


async def update(user_id: PydanticObjectId, update_user_dto: UpdateUserDTO):
    user = update_user_dto.to_document()
    updated_user = await put(user_id, user)
    if updated_user:
        return updated_user
    raise UserNotFoundException(user_id)


async def remove(user_id: PydanticObjectId):
    user = await get(user_id)
    if user:
        await delete(user_id)
    raise UserNotFoundException(user_id)
