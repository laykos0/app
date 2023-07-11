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


class ArticleNotFoundException(CustomNotFoundException):
    def __init__(self, article_id: PydanticObjectId):
        super().__init__('article-not-found', f'Article {article_id} not found.')


class VersionNotFoundException(CustomNotFoundException):
    def __init__(self, article_id: PydanticObjectId, version: int):
        super().__init__('article-version-not-found', f'Article {article_id}, version {version} not found.')
