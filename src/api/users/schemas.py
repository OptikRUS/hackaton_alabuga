from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.users.schemas import User


class UserRegistrationRequest(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    password: str = Field(default=..., description="Пароль пользователя")
    first_name: str | None = Field(default=None, description="Имя пользователя")
    last_name: str | None = Field(default=None, description="Фамилия пользователя")

    def to_schema(self) -> User:
        return User(
            login=self.login,
            password=self.password,
            first_name=self.first_name if self.first_name else "",
            last_name=self.last_name if self.last_name else "",
        )


class UserResponse(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    first_name: str = Field(default=..., description="Имя пользователя")
    last_name: str = Field(default=..., description="Фамилия пользователя")
    role: str = Field(default=..., description="Роль пользователя")
    rank_id: int = Field(default=..., description="Идентификатор ранга")
    exp: int = Field(default=..., description="Опыт пользователя")
    mana: int = Field(default=..., description="Мана пользователя")

    @classmethod
    def from_schema(cls, user: User) -> "UserResponse":
        return cls(
            login=user.login,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            rank_id=user.rank_id,
            exp=user.exp,
            mana=user.mana,
        )


class UserLoginRequest(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    password: str = Field(default=..., description="Пароль пользователя")


class UserTokenResponse(BoundaryModel):
    token: str
