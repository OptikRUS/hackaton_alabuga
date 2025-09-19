from abc import ABCMeta, abstractmethod

from src.core.users.schemas import User


class UserStorage(metaclass=ABCMeta):
    @abstractmethod
    async def insert_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_login(self, login: str) -> User:
        raise NotImplementedError
