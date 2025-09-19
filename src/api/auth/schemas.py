from typing import Self

import jwt as pyjwt
from pydantic import Field

from src.api.boundary import BoundaryModel
from src.config.settings import settings
from src.core.exceptions import InvalidJWTTokenError
from src.core.users.enums import UserRoleEnum


class JwtUser(BoundaryModel):
    login: str = Field(default="", alias="login", examples=["user123"])
    role: UserRoleEnum = Field(
        default=UserRoleEnum.CANDIDATE,
        alias="role",
        examples=[UserRoleEnum.CANDIDATE],
    )

    @classmethod
    def decode(
        cls,
        payload: str = "",
        public_key: str = settings.AUTH.PUBLIC_KEY.get_secret_value(),
    ) -> Self:
        token = payload.split("Bearer ", maxsplit=1)[-1] if payload else ""
        try:
            message = pyjwt.decode(
                jwt=token,
                key=public_key,
                options={"verify_signature": False},
                algorithms=[settings.AUTH.ALGORITHM],
            )
            return cls.model_validate(message)
        except Exception as ex:
            raise InvalidJWTTokenError from ex
