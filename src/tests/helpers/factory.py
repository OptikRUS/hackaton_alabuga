from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.schemas import (
    Mission,
    MissionBranch,
    MissionBranches,
    Missions,
)
from src.core.tasks.schemas import (
    MissionTask,
    MissionTasks,
)
from src.core.users.enums import UserRoleEnum
from src.core.users.schemas import User


class FactoryHelper:
    @classmethod
    def user(
        cls,
        login: str = "TEST",
        first_name: str = "TEST",
        last_name: str = "TEST",
        password: str = "TEST",  # noqa: S107
        role: UserRoleEnum = UserRoleEnum.CANDIDATE,
        rank_id: int = 0,
        exp: int = 0,
        mana: int = 0,
    ) -> User:
        return User(
            login=login,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            rank_id=rank_id,
            exp=exp,
            mana=mana,
        )

    @classmethod
    def mission_branch(cls, branch_id: int = 0, name: str = "TEST") -> MissionBranch:
        return MissionBranch(id=branch_id, name=name)

    @classmethod
    def mission_branches(cls, values: list[MissionBranch]) -> MissionBranches:
        return MissionBranches(values=values if values else [])

    @classmethod
    def mission(
        cls,
        mission_id: int = 0,
        title: str = "TEST",
        description: str = "TEST",
        reward_xp: int = 100,
        reward_mana: int = 50,
        rank_requirement: int = 1,
        branch_id: int = 1,
        category: MissionCategoryEnum = MissionCategoryEnum.QUEST,
        tasks: list[MissionTask] | None = None,
    ) -> Mission:
        return Mission(
            id=mission_id,
            title=title,
            description=description,
            reward_xp=reward_xp,
            reward_mana=reward_mana,
            rank_requirement=rank_requirement,
            branch_id=branch_id,
            category=category,
            tasks=tasks,
        )

    @classmethod
    def mission_task(
        cls,
        task_id: int = 0,
        title: str = "TEST",
        description: str = "TEST",
    ) -> MissionTask:
        return MissionTask(id=task_id, title=title, description=description)

    @classmethod
    def missions(cls, values: list[Mission]) -> Missions:
        return Missions(values=values)

    @classmethod
    def mission_tasks(cls, values: list[MissionTask]) -> MissionTasks:
        return MissionTasks(values=values)
