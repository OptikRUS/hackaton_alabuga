from sqlalchemy import ForeignKey, PrimaryKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.schemas import Mission, MissionBranch
from src.core.users.enums import UserRoleEnum
from src.core.users.schemas import User


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

    @classmethod
    def from_schema(cls, user: User) -> "UserModel":
        return cls(
            login=user.login,
            password=user.password,
            role=user.role,
            rank_id=user.rank_id,
            exp=user.exp,
            mana=user.mana,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    def to_schema(self) -> User:
        return User(
            login=self.login,
            password=self.password,
            role=UserRoleEnum(self.role),
            rank_id=self.rank_id,
            exp=self.exp,
            mana=self.mana,
            first_name=self.first_name,
            last_name=self.last_name,
        )


class MissionBranchModel(Base):
    __tablename__ = "missions_branch"
    __table_args__ = (UniqueConstraint("name", name="uq_missions_branch_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))

    missions: Mapped[list["MissionModel"]] = relationship(cascade="all, delete-orphan")

    @classmethod
    def from_schema(cls, branch: MissionBranch) -> "MissionBranchModel":
        return cls(id=branch.id, name=branch.name)

    def to_schema(self) -> MissionBranch:
        return MissionBranch(id=self.id, name=self.name)


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

    @classmethod
    def from_schema(cls, mission: Mission) -> "MissionModel":
        return cls(
            title=mission.title,
            description=mission.description,
            reward_xp=mission.reward_xp,
            reward_mana=mission.reward_mana,
            rank_requirement=mission.rank_requirement,
            branch_id=mission.branch_id,
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
            branch_id=self.branch_id,
            category=MissionCategoryEnum(self.category),
        )
