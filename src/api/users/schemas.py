from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.users.enums import UserRoleEnum
from src.core.users.schemas import CandidateUser, HRUser, User


class UserRegistrationRequest(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    password: str = Field(default=..., description="Пароль пользователя")
    first_name: str | None = Field(default=None, description="Имя пользователя")
    last_name: str | None = Field(default=None, description="Фамилия пользователя")


class HRUserRegistrationRequest(UserRegistrationRequest):
    def to_schema(self) -> User:
        return HRUser(
            login=self.login,
            password=self.password,
            first_name=self.first_name if self.first_name else "",
            last_name=self.last_name if self.last_name else "",
            role=UserRoleEnum.HR,
        )


class CandidateUserRegistrationRequest(UserRegistrationRequest):
    def to_schema(self) -> User:
        return CandidateUser(
            login=self.login,
            password=self.password,
            first_name=self.first_name if self.first_name else "",
            last_name=self.last_name if self.last_name else "",
            role=UserRoleEnum.CANDIDATE,
        )


class UserResponse(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    first_name: str = Field(default=..., description="Имя пользователя")
    last_name: str = Field(default=..., description="Фамилия пользователя")
    role: str = Field(default=..., description="Роль пользователя")

    @classmethod
    def from_schema(cls, user: User) -> "UserResponse":
        return cls(
            login=user.login,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        )


class UserLoginRequest(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    password: str = Field(default=..., description="Пароль пользователя")


class UserTokenResponse(BoundaryModel):
    token: str
