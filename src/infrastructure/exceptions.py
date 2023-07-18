from beanie import PydanticObjectId

from src.domain.articles import ArticleId


class CustomException(Exception):
    def __init__(self, error_type: str, message: str):
        self.error_type = error_type
        self.message = message
        super().__init__(self.message)


class CustomNotFoundException(CustomException):
    pass


class UserNotFoundException(CustomNotFoundException):
    def __init__(self, user_id: PydanticObjectId):
        super().__init__('user-not-found', f'User {user_id} not found.')


class ArticleNotFoundException(CustomNotFoundException):
    def __init__(self, article_id: ArticleId):
        super().__init__('article-not-found', f'Article {article_id} not found.')


class VersionNotFoundException(CustomNotFoundException):
    def __init__(self, article_id: ArticleId, version: int):
        super().__init__('article-version-not-found', f'Article {article_id}, version {version} not found.')


class CustomUnauthorizedException(CustomException):
    pass


class InvalidCredentialsException(CustomUnauthorizedException):
    def __init__(self):
        super().__init__('invalid-credentials', 'Could not validate credentials.')


class CustomForbiddenException(CustomException):
    pass


class InsufficientPermissionException(CustomForbiddenException):
    def __init__(self, user_id: PydanticObjectId, role: str):
        super().__init__('insufficient-permission', f'User {user_id} does not have {role} permission.')
