from dataclasses import dataclass

from src.core.artifacts.schemas import Artifact
from src.core.competencies.schemas import UserCompetency
from src.core.skills.schemas import UserSkill
from src.core.users.enums import UserRoleEnum


@dataclass
class User:
    login: str
    first_name: str
    last_name: str
    password: str
    role: UserRoleEnum
    rank_id: int
    exp: int
    mana: int
    artifacts: list[Artifact] | None = None
    competencies: list[UserCompetency] | None = None
    skills: list[UserSkill] | None = None


@dataclass
class HRUser(User):
    role: UserRoleEnum = UserRoleEnum.HR
    rank_id: int = 1
    exp: int = 0
    mana: int = 0


@dataclass
class CandidateUser(User):
    role: UserRoleEnum = UserRoleEnum.CANDIDATE
    rank_id: int = 1
    exp: int = 0
    mana: int = 0
