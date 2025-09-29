from datetime import UTC, datetime

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.schemas import Artifact, Artifacts
from src.core.competencies.schemas import Competencies, Competency, UserCompetency
from src.core.mission_chains.schemas import (
    MissionChain,
    MissionChainMission,
    MissionChains,
    MissionDependency,
)
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.schemas import (
    CompetencyReward,
    Mission,
    Missions,
    SkillReward,
)
from src.core.ranks.schemas import Rank, RankCompetencyRequirement, Ranks
from src.core.seasons.schemas import Season, Seasons
from src.core.skills.schemas import Skill, Skills
from src.core.store.schemas import StoreItem, StoreItems, StorePurchase
from src.core.tasks.schemas import (
    MissionTask,
    MissionTasks,
    UserTask,
)
from src.core.users.enums import UserRoleEnum
from src.core.users.schemas import CandidateUser, HRUser, User


class FactoryHelper:
    @classmethod
    def user(
        cls,
        login: str = "TEST",
        first_name: str = "TEST",
        last_name: str = "TEST",
        password: str = "TEST",  # noqa: S107
        role: UserRoleEnum = UserRoleEnum.HR,
    ) -> User:
        return User(
            login=login,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            rank_id=1,
            exp=0,
            mana=0,
            artifacts=[],
            competencies=[],
            skills=[],
        )

    @classmethod
    def hr_user(
        cls,
        login: str = "TEST",
        first_name: str = "TEST",
        last_name: str = "TEST",
        password: str = "TEST",  # noqa: S107
    ) -> HRUser:
        return HRUser(
            login=login,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=UserRoleEnum.HR,
        )

    @classmethod
    def candidate(
        cls,
        login: str = "TEST",
        first_name: str = "TEST",
        last_name: str = "TEST",
        password: str = "TEST",  # noqa: S107
        role: UserRoleEnum = UserRoleEnum.CANDIDATE,
        rank_id: int = 1,
        exp: int = 0,
        mana: int = 0,
        artifacts: list[Artifact] | None = None,
        competencies: list[UserCompetency] | None = None,
    ) -> CandidateUser:
        return CandidateUser(
            login=login,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            rank_id=rank_id,
            exp=exp,
            mana=mana,
            artifacts=artifacts,
            competencies=competencies,
        )

    @classmethod
    def season(
        cls,
        season_id: int = 0,
        name: str = "TEST",
        start_date: str = "2025-10-25T06:55:47Z",
        end_date: str = "2025-10-25T06:55:47Z",
    ) -> Season:
        return Season(
            id=season_id,
            name=name,
            start_date=datetime.fromisoformat(start_date).replace(tzinfo=UTC),
            end_date=datetime.fromisoformat(end_date).replace(tzinfo=UTC),
        )

    @classmethod
    def seasons(cls, values: list[Season]) -> Seasons:
        return Seasons(values=values if values else [])

    @classmethod
    def mission(
        cls,
        mission_id: int = 0,
        title: str = "TEST",
        description: str = "TEST",
        reward_xp: int = 100,
        reward_mana: int = 50,
        rank_requirement: int = 1,
        season_id: int = 1,
        category: MissionCategoryEnum = MissionCategoryEnum.QUEST,
        tasks: list[MissionTask] | None = None,
        reward_artifacts: list[Artifact] | None = None,
        reward_competencies: list[CompetencyReward] | None = None,
        reward_skills: list[SkillReward] | None = None,
    ) -> Mission:
        return Mission(
            id=mission_id,
            title=title,
            description=description,
            reward_xp=reward_xp,
            reward_mana=reward_mana,
            rank_requirement=rank_requirement,
            season_id=season_id,
            category=category,
            tasks=tasks,
            reward_artifacts=reward_artifacts,
            reward_competencies=reward_competencies,
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
    def user_mission(
        cls,
        mission_id: int = 0,
        title: str = "TEST",
        description: str = "TEST",
        reward_xp: int = 100,
        reward_mana: int = 50,
        rank_requirement: int = 1,
        season_id: int = 1,
        category: MissionCategoryEnum = MissionCategoryEnum.QUEST,
        tasks: list[MissionTask] | None = None,
        user_tasks: list[UserTask] | None = None,
        reward_artifacts: list[Artifact] | None = None,
        reward_competencies: list[CompetencyReward] | None = None,
        reward_skills: list[SkillReward] | None = None,
    ) -> Mission:
        return Mission(
            id=mission_id,
            title=title,
            description=description,
            reward_xp=reward_xp,
            reward_mana=reward_mana,
            rank_requirement=rank_requirement,
            season_id=season_id,
            category=category,
            tasks=tasks,
            user_tasks=user_tasks or [],
            reward_artifacts=reward_artifacts,
            reward_competencies=reward_competencies,
            reward_skills=reward_skills,
        )

    @classmethod
    def user_task(
        cls,
        task_id: int = 0,
        title: str = "TEST",
        description: str = "TEST",
        is_completed: bool = False,
    ) -> UserTask:
        return UserTask(id=task_id, title=title, description=description, is_completed=is_completed)

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
    def competency(
        cls,
        competency_id: int = 0,
        name: str = "TEST",
        max_level: int = 100,
        skills: list[Skill] | None = None,
    ) -> Competency:
        return Competency(
            id=competency_id,
            name=name,
            max_level=max_level,
            skills=skills,
        )

    @classmethod
    def competencies(cls, values: list[Competency]) -> Competencies:
        return Competencies(values=values)

    @classmethod
    def rank(
        cls,
        rank_id: int = 0,
        name: str = "TEST",
        required_xp: int = 0,
        required_missions: list[Mission] | None = None,
        required_competencies: list[RankCompetencyRequirement] | None = None,
    ) -> Rank:
        return Rank(
            id=rank_id,
            name=name,
            required_xp=required_xp,
            required_missions=required_missions or [],
            required_competencies=required_competencies or [],
        )

    @classmethod
    def ranks(cls, values: list[Rank]) -> Ranks:
        return Ranks(values=values)

    @classmethod
    def mission_chain(
        cls,
        chain_id: int = 0,
        name: str = "TEST_CHAIN",
        description: str = "Test chain description",
        reward_xp: int = 200,
        reward_mana: int = 100,
        missions: list[Mission] | None = None,
        dependencies: list[MissionDependency] | None = None,
        mission_orders: list[MissionChainMission] | None = None,
    ) -> MissionChain:
        return MissionChain(
            id=chain_id,
            name=name,
            description=description,
            reward_xp=reward_xp,
            reward_mana=reward_mana,
            missions=missions,
            dependencies=dependencies,
            mission_orders=mission_orders,
        )

    @classmethod
    def mission_chains(cls, values: list[MissionChain]) -> MissionChains:
        return MissionChains(values=values)

    @classmethod
    def mission_dependency(
        cls,
        mission_id: int = 1,
        prerequisite_mission_id: int = 2,
    ) -> MissionDependency:
        return MissionDependency(
            mission_id=mission_id,
            prerequisite_mission_id=prerequisite_mission_id,
        )

    @classmethod
    def competency_reward(
        cls,
        competency: Competency | None = None,
        level_increase: int = 1,
    ) -> CompetencyReward:
        if competency is None:
            competency = cls.competency()
        return CompetencyReward(competency=competency, level_increase=level_increase)

    @classmethod
    def skill_reward(
        cls,
        skill: Skill | None = None,
        level_increase: int = 1,
    ) -> SkillReward:
        if skill is None:
            skill = cls.skill()
        return SkillReward(skill=skill, level_increase=level_increase)

    @classmethod
    def store_item(
        cls,
        store_item_id: int = 0,
        title: str = "TEST",
        price: int = 100,
        stock: int = 10,
    ) -> StoreItem:
        return StoreItem(
            id=store_item_id,
            title=title,
            price=price,
            stock=stock,
        )

    @classmethod
    def store_items(cls, values: list[StoreItem]) -> StoreItems:
        return StoreItems(values=values)

    @classmethod
    def store_purchase(
        cls,
        user_login: str = "test_user",
        store_item_id: int = 1,
    ) -> StorePurchase:
        return StorePurchase(user_login=user_login, store_item_id=store_item_id)
