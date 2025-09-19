from dataclasses import dataclass

from src.core.password import PasswordService
from src.core.storages import UserStorage
from src.core.use_case import UseCase
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User


@dataclass
class CreateUserUseCase(UseCase):
    storage: UserStorage
    password_service: PasswordService

    async def execute(self, user: User) -> None:
        try:
            await self.storage.get_user_by_login(login=user.login)
            raise UserAlreadyExistError
        except UserNotFoundError:
            user.password = self.password_service.generate_password_hash(password=user.password)
            await self.storage.insert_user(user=user)


@dataclass
class LoginUserUseCase(UseCase):
    storage: UserStorage
    password_service: PasswordService

    async def execute(self, login: str, password: str) -> str:
        user = await self.storage.get_user_by_login(login=login)
        self.password_service.verify_password_hash(password=password, hashed_password=user.password)
        return self.password_service.encode(payload={"login": user.login})


@dataclass
class GetUserUseCase(UseCase):
    storage: UserStorage

    async def execute(self, login: str) -> User:
        return await self.storage.get_user_by_login(login)
