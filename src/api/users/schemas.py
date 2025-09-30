from pydantic import Field

from src.api.artifacts.schemas import ArtifactResponse
from src.api.boundary import BoundaryModel
from src.api.competencies.schemas import CompetencyResponse, UserCompetencyResponse
from src.api.skills.schemas import SkillResponse
from src.core.missions.schemas import CompetencyReward, Mission, SkillReward
from src.core.tasks.schemas import UserTask
from src.core.users.enums import UserRoleEnum
from src.core.users.schemas import CandidateUser, HRUser, User


class UserRegistrationRequest(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    password: str = Field(default=..., description="Пароль пользователя")
    first_name: str | None = Field(default=None, description="Имя пользователя")
    last_name: str | None = Field(default=None, description="Фамилия пользователя")


class HRUserRegistrationRequest(UserRegistrationRequest):
    def to_schema(self) -> User:
        return HRUser(
            login=self.login,
            password=self.password,
            first_name=self.first_name if self.first_name else "",
            last_name=self.last_name if self.last_name else "",
            role=UserRoleEnum.HR,
        )


class CandidateUserRegistrationRequest(UserRegistrationRequest):
    def to_schema(self) -> User:
        return CandidateUser(
            login=self.login,
            password=self.password,
            first_name=self.first_name if self.first_name else "",
            last_name=self.last_name if self.last_name else "",
            role=UserRoleEnum.CANDIDATE,
        )


class UserResponse(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    first_name: str = Field(default=..., description="Имя пользователя")
    last_name: str = Field(default=..., description="Фамилия пользователя")
    role: str = Field(default=..., description="Роль пользователя")

    @classmethod
    def from_schema(cls, user: User) -> "UserResponse":
        return cls(
            login=user.login,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
        )


class UsersListResponse(BoundaryModel):
    users: list[UserResponse] = Field(default_factory=list, description="Список пользователей")

    @classmethod
    def from_schema(cls, users: list[User]) -> "UsersListResponse":
        return cls(users=[UserResponse.from_schema(user) for user in users])


class UserDetailedResponse(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    first_name: str = Field(default=..., description="Имя пользователя")
    last_name: str = Field(default=..., description="Фамилия пользователя")
    role: str = Field(default=..., description="Роль пользователя")
    rank_id: int = Field(default=..., description="ID ранга пользователя")
    exp: int = Field(default=..., description="Опыт пользователя")
    mana: int = Field(default=..., description="Мана пользователя")
    artifacts: list[ArtifactResponse] = Field(
        default_factory=list, description="Артефакты пользователя"
    )
    competencies: list[UserCompetencyResponse] = Field(
        default_factory=list, description="Компетенции пользователя"
    )

    @classmethod
    def from_schema(cls, user: User) -> "UserDetailedResponse":
        return cls(
            login=user.login,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            rank_id=user.rank_id,
            exp=user.exp,
            mana=user.mana,
            artifacts=[
                ArtifactResponse.from_schema(artifact) for artifact in (user.artifacts or [])
            ],
            competencies=[
                UserCompetencyResponse.from_schema(competency)
                for competency in (user.competencies or [])
            ],
        )


class UserLoginRequest(BoundaryModel):
    login: str = Field(default=..., description="Логин пользователя")
    password: str = Field(default=..., description="Пароль пользователя")


class UserTokenResponse(BoundaryModel):
    token: str


class UserUpdateRequest(BoundaryModel):
    first_name: str | None = Field(default=None, description="Имя пользователя")
    last_name: str | None = Field(default=None, description="Фамилия пользователя")
    password: str | None = Field(default=None, description="Пароль пользователя")
    mana: int | None = Field(default=None, description="Мана пользователя")
    rank_id: int | None = Field(default=None, description="ID ранга пользователя")
    exp: int | None = Field(default=None, description="Опыт пользователя")

    def to_schema(self, login: str, current_user: User) -> User:
        return User(
            login=login,
            first_name=self.first_name if self.first_name is not None else current_user.first_name,
            last_name=self.last_name if self.last_name is not None else current_user.last_name,
            password=self.password if self.password is not None else current_user.password,
            role=current_user.role,
            rank_id=self.rank_id if self.rank_id is not None else current_user.rank_id,
            exp=self.exp if self.exp is not None else current_user.exp,
            mana=self.mana if self.mana is not None else current_user.mana,
        )


class UserTaskResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор задачи")
    title: str = Field(default=..., description="Название задачи")
    description: str = Field(default=..., description="Описание задачи")
    is_completed: bool = Field(default=..., description="Статус выполнения задачи")

    @classmethod
    def from_schema(cls, user_task: UserTask) -> "UserTaskResponse":
        return cls(
            id=user_task.id,
            title=user_task.title,
            description=user_task.description,
            is_completed=user_task.is_completed,
        )


class UserMissionResponse(BoundaryModel):
    id: int = Field(default=..., description="Идентификатор миссии")
    title: str = Field(default=..., description="Название миссии")
    description: str = Field(default=..., description="Описание миссии")
    reward_xp: int = Field(default=..., description="Награда в опыте")
    reward_mana: int = Field(default=..., description="Награда в мане")
    rank_requirement: int = Field(default=..., description="Требуемый ранг")
    season_id: int = Field(default=..., description="ID ветки миссий")
    category: str = Field(default=..., description="Категория миссии")
    is_completed: bool = Field(default=False, description="Показатель выполнения миссии")
    tasks: list["UserTaskResponse"] = Field(default_factory=list, description="Задачи миссии")
    reward_artifacts: list[ArtifactResponse] = Field(
        default_factory=list, description="Артефакты-награды"
    )
    reward_competencies: list["CompetencyRewardResponse"] = Field(
        default_factory=list, description="Награды в компетенциях"
    )
    reward_skills: list["SkillRewardResponse"] = Field(
        default_factory=list, description="Награды в скиллах"
    )

    @classmethod
    def from_schema(cls, mission: Mission) -> "UserMissionResponse":
        return cls(
            id=mission.id,
            title=mission.title,
            description=mission.description,
            reward_xp=mission.reward_xp,
            reward_mana=mission.reward_mana,
            rank_requirement=mission.rank_requirement,
            season_id=mission.season_id,
            category=mission.category,
            is_completed=mission.is_completed,
            tasks=[
                UserTaskResponse.from_schema(user_task=task) for task in (mission.user_tasks or [])
            ],
            reward_artifacts=[
                ArtifactResponse.from_schema(artifact=artifact)
                for artifact in (mission.reward_artifacts or [])
            ],
            reward_competencies=[
                CompetencyRewardResponse.from_schema(reward_competencies)
                for reward_competencies in (mission.reward_competencies or [])
            ],
            reward_skills=[
                SkillRewardResponse.from_schema(reward_skill)
                for reward_skill in (mission.reward_skills or [])
            ],
        )


class CompetencyRewardResponse(BoundaryModel):
    competency: CompetencyResponse
    level_increase: int

    @classmethod
    def from_schema(cls, competency_reward: CompetencyReward) -> "CompetencyRewardResponse":
        return cls(
            competency=CompetencyResponse.from_schema(competency_reward.competency),
            level_increase=competency_reward.level_increase,
        )


class SkillRewardResponse(BoundaryModel):
    skill: SkillResponse
    level_increase: int

    @classmethod
    def from_schema(cls, skill_reward: SkillReward) -> "SkillRewardResponse":
        return cls(
            skill=SkillResponse.from_schema(skill_reward.skill),
            level_increase=skill_reward.level_increase,
        )
