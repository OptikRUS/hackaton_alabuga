from src.core.exceptions import BaseExceptionError


class UserNotFoundError(BaseExceptionError):
    detail = "USER_NOT_FOUND_ERROR"


class UserAlreadyExistError(BaseExceptionError):
    detail = "USER_ALREADY_EXIST_ERROR"


class UserIncorrectCredentialsError(BaseExceptionError):
    detail = "USER_INCORRECT_CREDENTIALS_ERROR"
