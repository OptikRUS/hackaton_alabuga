from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, PrimaryKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.schemas import Artifact
from src.core.competencies.schemas import Competency
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.schemas import CompetencyReward, Mission, SkillReward
from src.core.ranks.schemas import Rank, RankCompetencyRequirement
from src.core.seasons.schemas import Season
from src.core.skills.schemas import Skill
from src.core.tasks.schemas import MissionTask
from src.core.users.enums import UserRoleEnum
from src.core.users.schemas import CandidateUser, User


class Base(DeclarativeBase): ...


class UserModel(Base):
    __tablename__ = "users_user"
    __table_args__ = (
        PrimaryKeyConstraint(
            "login",
            name="pk_users_user_table",
        ),
    )

    login: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column()
    rank_id: Mapped[int] = mapped_column()
    exp: Mapped[int] = mapped_column()
    mana: Mapped[int] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()

    artifacts: Mapped[list["ArtifactModel"]] = relationship(
        "ArtifactModel",
        secondary="artifacts_users_artifacts",
        back_populates="users",
        lazy="selectin",
    )

    @classmethod
    def from_schema(cls, user: User) -> "UserModel":
        return cls(
            login=user.login,
            first_name=user.first_name,
            last_name=user.last_name,
            password=user.password,
            role=user.role,
        )

    def to_schema(self) -> User:
        return User(
            login=self.login,
            password=self.password,
            role=UserRoleEnum(self.role),
            first_name=self.first_name,
            last_name=self.last_name,
        )

    def to_candidate_schema(self) -> CandidateUser:
        return CandidateUser(
            login=self.login,
            password=self.password,
            role=UserRoleEnum(self.role),
            rank_id=self.rank_id,
            exp=self.exp,
            mana=self.mana,
            first_name=self.first_name,
            last_name=self.last_name,
            artifacts=[artifact.to_schema() for artifact in self.artifacts],
        )


class MissionBranchModel(Base):
    __tablename__ = "missions_branch"
    __table_args__ = (UniqueConstraint("name", name="uq_missions_branch_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    missions: Mapped[list["MissionModel"]] = relationship(cascade="all, delete-orphan")

    @classmethod
    def from_schema(cls, branch: Season) -> "MissionBranchModel":
        return cls(
            id=branch.id,
            name=branch.name,
            start_date=branch.start_date,
            end_date=branch.end_date,
        )

    def to_schema(self) -> Season:
        return Season(
            id=self.id,
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
        )


class MissionModel(Base):
    __tablename__ = "missions_mission"
    __table_args__ = (UniqueConstraint("title", name="uq_missions_branch_title"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column()
    reward_xp: Mapped[int] = mapped_column()
    reward_mana: Mapped[int] = mapped_column()
    rank_requirement: Mapped[int] = mapped_column()
    category: Mapped[str] = mapped_column(String(100))

    branch_id: Mapped[int] = mapped_column(ForeignKey(MissionBranchModel.id, ondelete="CASCADE"))

    tasks: Mapped[list["MissionTaskModel"]] = relationship(
        "MissionTaskModel",
        secondary="missions_missions_tasks",
        back_populates="missions",
        lazy="selectin",
    )

    artifacts: Mapped[list["ArtifactModel"]] = relationship(
        "ArtifactModel",
        secondary="artifacts_missions_artifacts",
        back_populates="missions",
        lazy="selectin",
    )

    competency_rewards: Mapped[list["MissionCompetencyRewardModel"]] = relationship(
        "MissionCompetencyRewardModel",
        back_populates="mission",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    skill_rewards: Mapped[list["MissionSkillRewardModel"]] = relationship(
        "MissionSkillRewardModel",
        back_populates="mission",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @classmethod
    def from_schema(cls, mission: Mission) -> "MissionModel":
        return cls(
            title=mission.title,
            description=mission.description,
            reward_xp=mission.reward_xp,
            reward_mana=mission.reward_mana,
            rank_requirement=mission.rank_requirement,
            branch_id=mission.season_id,
            category=mission.category,
        )

    def to_schema(self) -> Mission:
        return Mission(
            id=self.id,
            title=self.title,
            description=self.description,
            reward_xp=self.reward_xp,
            reward_mana=self.reward_mana,
            rank_requirement=self.rank_requirement,
            season_id=self.branch_id,
            category=MissionCategoryEnum(self.category),
            tasks=[task.to_schema() for task in self.tasks],
            reward_artifacts=[artifact.to_schema() for artifact in self.artifacts],
            reward_competencies=[
                CompetencyReward(
                    competency=r.competency.to_schema(), level_increase=r.level_increase
                )
                for r in self.competency_rewards
            ],
            reward_skills=[
                SkillReward(skill=r.skill.to_schema(), level_increase=r.level_increase)
                for r in self.skill_rewards
            ],
        )


class MissionTaskModel(Base):
    __tablename__ = "missions_mission_task"
    __table_args__ = (UniqueConstraint("title", name="uq_missions_task_title"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column()

    missions: Mapped[list["MissionModel"]] = relationship(
        MissionModel,
        secondary="missions_missions_tasks",
        back_populates="tasks",
        lazy="selectin",
    )

    @classmethod
    def from_schema(cls, task: MissionTask) -> "MissionTaskModel":
        return cls(title=task.title, description=task.description)

    def to_schema(self) -> MissionTask:
        return MissionTask(
            id=self.id,
            title=self.title,
            description=self.description,
        )


class MissionTaskRelationModel(Base):
    __tablename__ = "missions_missions_tasks"
    __table_args__ = (
        PrimaryKeyConstraint(
            "task_id",
            "mission_id",
            name="pk_missions_mission_tasks",
        ),
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey(MissionTaskModel.id, ondelete="CASCADE"),
        primary_key=True,
    )
    mission_id: Mapped[int] = mapped_column(
        ForeignKey(MissionModel.id, ondelete="CASCADE"),
        primary_key=True,
    )


class CompetencyModel(Base):
    __tablename__ = "competencies_competency"
    __table_args__ = (UniqueConstraint("name", name="uq_competencies_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    max_level: Mapped[int] = mapped_column()

    skills: Mapped[list["SkillModel"]] = relationship(
        "SkillModel",
        secondary="competencies_competencies_skills",
        lazy="selectin",
    )

    @classmethod
    def from_schema(cls, competency: Competency) -> "CompetencyModel":
        return cls(id=competency.id, name=competency.name, max_level=competency.max_level)

    def to_schema(self) -> Competency:
        return Competency(
            id=self.id,
            name=self.name,
            max_level=self.max_level,
            skills=[skill.to_schema() for skill in self.skills],
        )


class RankModel(Base):
    __tablename__ = "ranks_rank"
    __table_args__ = (UniqueConstraint("name", name="uq_ranks_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    required_xp: Mapped[int] = mapped_column()

    required_missions: Mapped[list["MissionModel"]] = relationship(
        "MissionModel",
        secondary="rank_required_mission",
        lazy="selectin",
    )

    required_competencies_rel: Mapped[list["RankCompetencyRequirementModel"]] = relationship(
        "RankCompetencyRequirementModel",
        back_populates="rank",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    @classmethod
    def from_schema(cls, rank: Rank) -> "RankModel":
        return cls(id=rank.id, name=rank.name, required_xp=rank.required_xp)

    def to_schema(self) -> Rank:
        return Rank(
            id=self.id,
            name=self.name,
            required_xp=self.required_xp,
            required_missions=[mission.to_schema() for mission in self.required_missions],
            required_competencies=[
                RankCompetencyRequirement(
                    competency=rel.competency.to_schema(), min_level=rel.min_level
                )
                for rel in self.required_competencies_rel
            ],
        )


class RankCompetencyRequirementModel(Base):
    __tablename__ = "ranks_competencies_requirements"
    __table_args__ = (
        PrimaryKeyConstraint(
            "rank_id",
            "competency_id",
            name="pk_ranks_competencies_requirements",
        ),
    )

    rank_id: Mapped[int] = mapped_column(
        ForeignKey(RankModel.id, ondelete="CASCADE"),
        primary_key=True,
    )
    competency_id: Mapped[int] = mapped_column(
        ForeignKey(CompetencyModel.id, ondelete="CASCADE"),
        primary_key=True,
    )
    min_level: Mapped[int] = mapped_column()

    competency: Mapped["CompetencyModel"] = relationship()
    rank: Mapped["RankModel"] = relationship(back_populates="required_competencies_rel")


class SkillModel(Base):
    __tablename__ = "skills_skill"
    __table_args__ = (UniqueConstraint("name", name="uq_skills_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    max_level: Mapped[int] = mapped_column()

    @classmethod
    def from_schema(cls, skill: Skill) -> "SkillModel":
        return cls(id=skill.id, name=skill.name, max_level=skill.max_level)

    def to_schema(self) -> Skill:
        return Skill(id=self.id, name=self.name, max_level=self.max_level)


class ArtifactModel(Base):
    __tablename__ = "artifacts_artifact"
    __table_args__ = (UniqueConstraint("title", name="uq_artifacts_artifact_title"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column()
    rarity: Mapped[str] = mapped_column(String(100))
    image_url: Mapped[str] = mapped_column()

    missions: Mapped[list["MissionModel"]] = relationship(
        "MissionModel",
        secondary="artifacts_missions_artifacts",
        back_populates="artifacts",
        lazy="selectin",
    )

    users: Mapped[list["UserModel"]] = relationship(
        "UserModel",
        secondary="artifacts_users_artifacts",
        back_populates="artifacts",
        lazy="selectin",
    )

    @classmethod
    def from_schema(cls, artifact: Artifact) -> "ArtifactModel":
        return cls(
            title=artifact.title,
            description=artifact.description,
            rarity=artifact.rarity,
            image_url=artifact.image_url,
        )

    def to_schema(self) -> Artifact:
        return Artifact(
            id=self.id,
            title=self.title,
            description=self.description,
            rarity=ArtifactRarityEnum(self.rarity),
            image_url=self.image_url,
        )


class ArtifactMissionRelationModel(Base):
    __tablename__ = "artifacts_missions_artifacts"
    __table_args__ = (
        PrimaryKeyConstraint(
            "artifact_id",
            "mission_id",
            name="pk_artifacts_missions_artifacts",
        ),
    )

    artifact_id: Mapped[int] = mapped_column(
        ForeignKey(ArtifactModel.id, ondelete="CASCADE"),
        primary_key=True,
    )
    mission_id: Mapped[int] = mapped_column(
        ForeignKey(MissionModel.id, ondelete="CASCADE"),
        primary_key=True,
    )


class ArtifactUserRelationModel(Base):
    __tablename__ = "artifacts_users_artifacts"
    __table_args__ = (
        PrimaryKeyConstraint(
            "artifact_id",
            "user_login",
            name="pk_artifacts_users_artifacts",
        ),
    )

    artifact_id: Mapped[int] = mapped_column(
        ForeignKey(ArtifactModel.id, ondelete="CASCADE"),
        primary_key=True,
    )
    user_login: Mapped[str] = mapped_column(
        ForeignKey(UserModel.login, ondelete="CASCADE"),
        primary_key=True,
    )


class RankMissionRelationModel(Base):
    __tablename__ = "rank_required_mission"
    __table_args__ = (
        PrimaryKeyConstraint(
            "rank_id",
            "mission_id",
            name="pk_rank_required_mission",
        ),
    )

    rank_id: Mapped[int] = mapped_column(
        ForeignKey(RankModel.id, ondelete="CASCADE"),
        primary_key=True,
    )
    mission_id: Mapped[int] = mapped_column(
        ForeignKey(MissionModel.id, ondelete="CASCADE"),
        primary_key=True,
    )


class CompetencySkillRelationModel(Base):
    __tablename__ = "competencies_competencies_skills"
    __table_args__ = (
        PrimaryKeyConstraint(
            "competency_id",
            "skill_id",
            name="pk_competencies_competencies_skills",
        ),
    )

    competency_id: Mapped[int] = mapped_column(
        ForeignKey(CompetencyModel.id, ondelete="CASCADE"),
        primary_key=True,
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey(SkillModel.id, ondelete="CASCADE"),
        primary_key=True,
    )


class MissionCompetencyRewardModel(Base):
    __tablename__ = "missions_competencies_rewards"
    __table_args__ = (
        PrimaryKeyConstraint(
            "mission_id",
            "competency_id",
            name="pk_missions_competencies_rewards",
        ),
    )

    mission_id: Mapped[int] = mapped_column(
        ForeignKey(MissionModel.id, ondelete="CASCADE"), primary_key=True
    )
    competency_id: Mapped[int] = mapped_column(
        ForeignKey(CompetencyModel.id, ondelete="CASCADE"), primary_key=True
    )
    level_increase: Mapped[int] = mapped_column()

    mission: Mapped["MissionModel"] = relationship(back_populates="competency_rewards")
    competency: Mapped["CompetencyModel"] = relationship()


class MissionSkillRewardModel(Base):
    __tablename__ = "missions_skills_rewards"
    __table_args__ = (
        PrimaryKeyConstraint(
            "mission_id",
            "skill_id",
            name="pk_missions_skills_rewards",
        ),
    )

    mission_id: Mapped[int] = mapped_column(
        ForeignKey(MissionModel.id, ondelete="CASCADE"), primary_key=True
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey(SkillModel.id, ondelete="CASCADE"), primary_key=True
    )
    level_increase: Mapped[int] = mapped_column()

    mission: Mapped["MissionModel"] = relationship(back_populates="skill_rewards")
    skill: Mapped["SkillModel"] = relationship()
