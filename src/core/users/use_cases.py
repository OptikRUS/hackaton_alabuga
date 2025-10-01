from dataclasses import dataclass

from src.core.competencies.schemas import UserCompetency
from src.core.password import PasswordService
from src.core.skills.schemas import UserSkill
from src.core.storages import MissionStorage, RankStorage, UserStorage
from src.core.tasks.schemas import UserTask
from src.core.use_case import UseCase
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User


@dataclass
class CreateUserUseCase(UseCase):
    user_storage: UserStorage
    rank_storage: RankStorage
    mission_storage: MissionStorage
    password_service: PasswordService

    async def execute(self, user: User) -> None:
        try:
            await self.user_storage.get_user_by_login(login=user.login)
            raise UserAlreadyExistError
        except UserNotFoundError:
            user.password = self.password_service.generate_password_hash(password=user.password)
            ranks = await self.rank_storage.list_ranks()
            new_rank = ranks.get_available_rank(exp=user.exp)
            user.rank_id = new_rank.id
            await self.user_storage.insert_user(user=user)
            await self._add_new_rank_missions(user_login=user.login, rank_id=user.rank_id)

    async def _add_new_rank_missions(self, user_login: str, rank_id: int) -> None:
        available_missions = await self.mission_storage.get_missions_by_rank(rank_id=rank_id)
        for mission in available_missions.values:
            if mission.tasks is not None:
                for task in mission.tasks:
                    await self.mission_storage.add_user_task(
                        user_login=user_login,
                        user_task=UserTask(
                            id=task.id,
                            title=task.title,
                            description=task.description,
                            is_completed=False,
                        ),
                    )


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


@dataclass
class UpdateUserUseCase(UseCase):
    storage: UserStorage
    password_service: PasswordService

    async def execute(self, user: User) -> None:
        await self.storage.get_user_by_login(login=user.login)

        if user.password:
            user.password = self.password_service.generate_password_hash(password=user.password)

        await self.storage.update_user(user=user)
