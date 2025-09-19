from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.storages import UserStorage
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User
from src.storages.models import UserModel


@dataclass
class DatabaseStorage(UserStorage):
    session: AsyncSession

    async def insert_user(self, user: User) -> None:
        query = insert(UserModel).values(
            {
                "login": user.login,
                "password": user.password,
                "role": user.role,
                "rank_id": user.rank_id,
                "exp": user.exp,
                "mana": user.mana,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        )
        try:
            await self.session.execute(query)
        except IntegrityError as error:
            # TODO: Можно проверить на UniqueViolationError
            raise UserAlreadyExistError from error

    async def get_user_by_login(self, login: str) -> User:
        query = select(UserModel).where(UserModel.login == login)
        user = await self.session.scalar(query)
        if user is None:
            raise UserNotFoundError
        return user.to_schema()
