from src.core.exceptions import BaseExceptionError


class MediaNotFoundError(BaseExceptionError):
    detail = "MEDIA_NOT_FOUND_ERROR"
