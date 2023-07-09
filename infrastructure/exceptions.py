from beanie import PydanticObjectId


class CustomException(Exception):
    def __init__(self, error_type: str, message: str):
        self.error_type = error_type
        self.message = message
        super().__init__(self.message)


class CustomNotFoundException(CustomException):
    def __init__(self, error_type: str, message: str):
        super().__init__(error_type, message)


class UserNotFoundException(CustomNotFoundException):
    def __init__(self, user_id: PydanticObjectId):
        super().__init__('user-not-found', f'User {user_id} not found.')
