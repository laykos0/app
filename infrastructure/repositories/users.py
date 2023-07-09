from beanie import PydanticObjectId

from api.domain.users import User


async def post(user: User):
    return await user.insert()


async def get(user_id: PydanticObjectId):
    return await User.get(user_id)


async def get_all():
    return await User.find_all().to_list()


async def put(user_id: PydanticObjectId, new_user: User):
    user = await get(user_id)
    if user:
        user.name = new_user.name
        user.roles = new_user.roles
        await user.save()
        return user
    return None


async def delete(user_id: PydanticObjectId):
    user = await User.get(user_id)
    await user.delete()
