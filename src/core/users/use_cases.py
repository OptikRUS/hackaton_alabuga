from dataclasses import dataclass

from src.core.competencies.schemas import UserCompetency
from src.core.password import PasswordService
from src.core.skills.schemas import UserSkill
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
        return self.password_service.encode(payload={"login": user.login, "role": user.role})


@dataclass
class GetUserUseCase(UseCase):
    storage: UserStorage

    async def execute(self, login: str) -> User:
        return await self.storage.get_user_by_login(login)


@dataclass
class GetUserWithRelationsUseCase(UseCase):
    storage: UserStorage

    async def execute(self, login: str) -> User:
        return await self.storage.get_user_by_login_with_relations(login)


@dataclass
class ListUsersUseCase(UseCase):
    storage: UserStorage

    async def execute(self) -> list[User]:
        return await self.storage.list_users()


@dataclass
class AddCompetencyToUserUseCase(UseCase):
    storage: UserStorage

    async def execute(self, user_login: str, competency_id: int, level: int = 0) -> None:
        await self.storage.add_competency_to_user(
            user_login=user_login, competency_id=competency_id, level=level
        )


@dataclass
class RemoveCompetencyFromUserUseCase(UseCase):
    storage: UserStorage

    async def execute(self, user_login: str, competency_id: int) -> None:
        await self.storage.remove_competency_from_user(
            user_login=user_login, competency_id=competency_id
        )


@dataclass
class UpdateUserCompetencyLevelUseCase(UseCase):
    storage: UserStorage

    async def execute(self, user_login: str, competency_id: int, level: int) -> None:
        await self.storage.update_user_competency_level(
            user_login=user_login, competency_id=competency_id, level=level
        )


@dataclass
class AddSkillToUserUseCase(UseCase):
    storage: UserStorage

    async def execute(
        self, user_login: str, skill_id: int, competency_id: int, level: int = 0
    ) -> None:
        await self.storage.add_skill_to_user(
            user_login=user_login, skill_id=skill_id, competency_id=competency_id, level=level
        )


@dataclass
class RemoveSkillFromUserUseCase(UseCase):
    storage: UserStorage

    async def execute(self, user_login: str, skill_id: int, competency_id: int) -> None:
        await self.storage.remove_skill_from_user(
            user_login=user_login, skill_id=skill_id, competency_id=competency_id
        )


@dataclass
class UpdateUserSkillLevelUseCase(UseCase):
    storage: UserStorage

    async def execute(self, user_login: str, skill_id: int, competency_id: int, level: int) -> None:
        await self.storage.update_user_skill_level(
            user_login=user_login, skill_id=skill_id, competency_id=competency_id, level=level
        )


@dataclass
class GetUserCompetenciesUseCase(UseCase):
    storage: UserStorage

    async def execute(self, user_login: str) -> list[UserCompetency]:
        user = await self.storage.get_user_by_login_with_relations(login=user_login)
        return user.competencies or []


@dataclass
class GetUserSkillsUseCase(UseCase):
    storage: UserStorage

    async def execute(self, user_login: str) -> list[UserSkill]:
        user = await self.storage.get_user_by_login_with_relations(login=user_login)
        return user.skills or []
