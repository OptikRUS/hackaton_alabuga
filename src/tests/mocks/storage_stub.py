from dataclasses import dataclass, field

from src.core.storages import UserStorage
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User


@dataclass
class StorageMock(UserStorage):
    user_table: dict[str, User] = field(default_factory=dict)

    async def insert_user(self, user: User) -> None:
        try:
            self.user_table[user.login]
            raise UserAlreadyExistError
        except KeyError:
            self.user_table[user.login] = user

    async def get_user_by_login(self, login: str) -> User:
        try:
            return self.user_table[login]
        except KeyError as error:
            raise UserNotFoundError from error
