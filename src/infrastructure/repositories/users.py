from beanie import PydanticObjectId

from src.domain.users import User


async def insert(user: User):
    return await user.insert()


async def find(user_id: PydanticObjectId):
    return await User.get(user_id)


async def find_all():
    return await User.find_all().to_list()


async def update(user: User):
    return await user.save()


async def delete(user: User):
    await user.delete()
