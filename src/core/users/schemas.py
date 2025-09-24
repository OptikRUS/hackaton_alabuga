from dataclasses import dataclass

from src.core.artifacts.schemas import Artifact
from src.core.users.enums import UserRoleEnum


@dataclass
class User:
    login: str
    first_name: str
    last_name: str
    password: str
    role: UserRoleEnum


@dataclass
class HRUser(User):
    role: UserRoleEnum = UserRoleEnum.HR


@dataclass
class CandidateUser(User):
    role: UserRoleEnum = UserRoleEnum.CANDIDATE
    rank_id: int = 0
    exp: int = 0
    mana: int = 0
    artifacts: list[Artifact] | None = None
