from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.schemas import Artifact, Artifacts
from src.core.competitions.schemas import Competition, Competitions
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.schemas import (
    CompetitionReward,
    Mission,
    MissionBranch,
    MissionBranches,
    Missions,
    SkillReward,
)
from src.core.ranks.schemas import Rank, RankCompetitionRequirement, Ranks
from src.core.skills.schemas import Skill, Skills
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
        artifacts: list[Artifact] | None = None,
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
            artifacts=artifacts,
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
        reward_artifacts: list[Artifact] | None = None,
        reward_competitions: list[CompetitionReward] | None = None,
        reward_skills: list[SkillReward] | None = None,
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
            reward_artifacts=reward_artifacts,
            reward_competitions=reward_competitions,
            reward_skills=reward_skills,
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

    @classmethod
    def artifact(
        cls,
        artifact_id: int = 0,
        title: str = "TEST",
        description: str = "TEST",
        rarity: ArtifactRarityEnum = ArtifactRarityEnum.COMMON,
        image_url: str = "https://example.com/image.jpg",
    ) -> Artifact:
        return Artifact(
            id=artifact_id,
            title=title,
            description=description,
            rarity=rarity,
            image_url=image_url,
        )

    @classmethod
    def artifacts(cls, values: list[Artifact]) -> Artifacts:
        return Artifacts(values=values)

    @classmethod
    def skill(
        cls,
        skill_id: int = 0,
        name: str = "TEST",
        max_level: int = 100,
    ) -> Skill:
        return Skill(id=skill_id, name=name, max_level=max_level)

    @classmethod
    def skills(cls, values: list[Skill]) -> Skills:
        return Skills(values=values)

    @classmethod
    def competition(
        cls,
        competition_id: int = 0,
        name: str = "TEST",
        max_level: int = 100,
        skills: list[Skill] | None = None,
    ) -> Competition:
        return Competition(
            id=competition_id,
            name=name,
            max_level=max_level,
            skills=skills,
        )

    @classmethod
    def competitions(cls, values: list[Competition]) -> Competitions:
        return Competitions(values=values)

    @classmethod
    def rank(
        cls,
        rank_id: int = 0,
        name: str = "TEST",
        required_xp: int = 0,
        required_missions: list[Mission] | None = None,
        required_competitions: list[RankCompetitionRequirement] | None = None,
    ) -> Rank:
        return Rank(
            id=rank_id,
            name=name,
            required_xp=required_xp,
            required_missions=required_missions or [],
            required_competitions=required_competitions or [],
        )

    @classmethod
    def ranks(cls, values: list[Rank]) -> Ranks:
        return Ranks(values=values)
