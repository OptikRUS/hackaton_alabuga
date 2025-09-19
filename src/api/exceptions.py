from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import Request, status
from fastapi.responses import JSONResponse, Response

from src.core.exceptions import BaseExceptionError, InvalidJWTTokenError
from src.core.missions.exceptions import MissionBranchAlreadyExistError, MissionBranchNotFoundError
from src.core.users.exceptions import (
    UserAlreadyExistError,
    UserIncorrectCredentialsError,
    UserNotFoundError,
)


async def internal_server_error_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "INTERNAL SERVER ERROR"},
    )


def handler(status_code: int) -> Callable[..., Coroutine[Any, Any, JSONResponse]]:
    async def error(_: Request, exc: BaseExceptionError) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={"detail": exc.detail},
        )

    return error


exception_handlers: (
    dict[
        int | type[Exception],
        Callable[[Request, Any], Coroutine[Any, Any, Response]],
    ]
    | None
) = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_exception_handler,
    BaseExceptionError: internal_server_error_exception_handler,
    InvalidJWTTokenError: handler(status_code=status.HTTP_401_UNAUTHORIZED),
    UserNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
    UserAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    UserIncorrectCredentialsError: handler(status_code=status.HTTP_401_UNAUTHORIZED),
    MissionBranchAlreadyExistError: handler(status_code=status.HTTP_409_CONFLICT),
    MissionBranchNotFoundError: handler(status_code=status.HTTP_404_NOT_FOUND),
}
