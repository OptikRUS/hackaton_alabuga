from sqlalchemy import PrimaryKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.missions.schemas import MissionBranch
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

    @classmethod
    def from_schema(cls, branch: MissionBranch) -> "MissionBranchModel":
        return cls(id=branch.id, name=branch.name)

    def to_schema(self) -> MissionBranch:
        return MissionBranch(id=self.id, name=self.name)
