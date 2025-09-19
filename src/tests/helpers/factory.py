from src.core.missions.schemas import MissionBranch, MissionBranches
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
        return MissionBranches(values=values if values else [cls.mission_branch()])
