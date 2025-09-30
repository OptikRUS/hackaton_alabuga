from dataclasses import dataclass, field
from typing import cast

from src.core.artifacts.exceptions import ArtifactNotFoundError, ArtifactTitleAlreadyExistError
from src.core.artifacts.schemas import Artifact, Artifacts
from src.core.competencies.exceptions import (
    CompetencyNameAlreadyExistError,
    CompetencyNotFoundError,
)
from src.core.competencies.schemas import Competencies, Competency
from src.core.mission_chains.exceptions import (
    MissionChainMissionAlreadyExistsError,
    MissionChainNameAlreadyExistError,
    MissionChainNotFoundError,
    MissionDependencyAlreadyExistsError,
)
from src.core.mission_chains.schemas import MissionChain, MissionChains, MissionDependency
from src.core.missions.exceptions import MissionNameAlreadyExistError, MissionNotFoundError
from src.core.missions.schemas import Mission, Missions
from src.core.ranks.exceptions import (
    RankCompetencyMinLevelTooHighError,
    RankNameAlreadyExistError,
    RankNotFoundError,
)
from src.core.ranks.schemas import Rank, RankCompetencyRequirement, Ranks
from src.core.seasons.exceptions import SeasonNameAlreadyExistError, SeasonNotFoundError
from src.core.seasons.schemas import Season, Seasons
from src.core.skills.exceptions import SkillNameAlreadyExistError, SkillNotFoundError
from src.core.skills.schemas import Skill, Skills
from src.core.storages import (
    ArtifactStorage,
    CompetencyStorage,
    MissionStorage,
    RankStorage,
    SkillStorage,
    StoreStorage,
    UserStorage,
)
from src.core.store.exceptions import StoreItemNotFoundError, StoreItemTitleAlreadyExistError
from src.core.store.schemas import StoreItem, StoreItems, StorePurchase
from src.core.tasks.exceptions import TaskNameAlreadyExistError, TaskNotFoundError
from src.core.tasks.schemas import MissionTask, MissionTasks, UserTask
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import CandidateUser, HRUser, User


@dataclass
class StorageMock(
    UserStorage,
    MissionStorage,
    ArtifactStorage,
    CompetencyStorage,
    SkillStorage,
    RankStorage,
    StoreStorage,
):
    user_table: dict[str, User | CandidateUser | HRUser] = field(default_factory=dict)
    season_table: dict[str, Season] = field(default_factory=dict)
    mission_table: dict[int, Mission] = field(default_factory=dict)
    task_table: dict[int, MissionTask] = field(default_factory=dict)
    artifact_table: dict[int, Artifact] = field(default_factory=dict)
    competencies_table: dict[int, Competency] = field(default_factory=dict)
    skill_table: dict[int, Skill] = field(default_factory=dict)
    rank_table: dict[int, Rank] = field(default_factory=dict)
    missions_tasks_relations: dict[int, set[int]] = field(default_factory=dict)
    missions_artifacts_relations: dict[int, set[int]] = field(default_factory=dict)
    users_artifacts_relations: dict[str, set[int]] = field(default_factory=dict)
    missions_competencies_rewards: dict[int, dict[int, int]] = field(default_factory=dict)
    missions_skills_rewards: dict[int, dict[int, int]] = field(default_factory=dict)
    competencies_skills_relations: dict[int, set[int]] = field(default_factory=dict)
    ranks_missions_requirements: dict[int, set[int]] = field(default_factory=dict)
    ranks_competencies_requirements: dict[int, dict[int, int]] = field(default_factory=dict)
    mission_chain_table: dict[int, MissionChain] = field(default_factory=dict)
    mission_chains_missions_relations: dict[int, set[int]] = field(default_factory=dict)
    mission_dependencies: dict[int, set[tuple[int, int]]] = field(default_factory=dict)
    users_tasks_relations: dict[str, dict[int, bool]] = field(default_factory=dict)
    store_item_table: dict[int, StoreItem] = field(default_factory=dict)
    users_competencies_relations: dict[str, dict[int, int]] = field(default_factory=dict)
    users_skills_relations: dict[str, dict[int, dict[int, int]]] = field(default_factory=dict)

    async def insert_user(self, user: User) -> None:
        try:
            self.user_table[user.login]
            raise UserAlreadyExistError
        except KeyError:
            self.user_table[user.login] = user

    async def get_user_by_login(self, login: str) -> User:
        try:
            return self.user_table[login]
        except KeyError as error:
            raise UserNotFoundError from error

    async def get_candidate_by_login(self, login: str) -> CandidateUser:
        try:
            return cast("CandidateUser", self.user_table[login])
        except KeyError as error:
            raise UserNotFoundError from error

    async def insert_season(self, season: Season) -> None:
        try:
            self.season_table[season.name]
            raise SeasonNameAlreadyExistError
        except KeyError:
            self.season_table[season.name] = season

    async def get_season_by_name(self, name: str) -> Season:
        try:
            return self.season_table[name]
        except KeyError as error:
            raise SeasonNotFoundError from error

    async def get_season_by_id(self, season_id: int) -> Season:
        for branch in self.season_table.values():
            if branch.id == season_id:
                return branch
        raise SeasonNotFoundError

    async def list_seasons(self) -> Seasons:
        return Seasons(values=list(self.season_table.values()))

    async def insert_mission(self, mission: Mission) -> None:
        for existing_mission in self.mission_table.values():
            if existing_mission.title == mission.title:
                raise MissionNameAlreadyExistError
        self.mission_table[mission.id] = mission

    async def get_mission_by_id(self, mission_id: int) -> Mission:
        try:
            mission = self.mission_table[mission_id]
            # Добавляем связанные задачи
            task_ids = self.missions_tasks_relations.get(mission_id, set())
            tasks = [self.task_table[task_id] for task_id in task_ids if task_id in self.task_table]
            return Mission(
                id=mission.id,
                title=mission.title,
                description=mission.description,
                reward_xp=mission.reward_xp,
                reward_mana=mission.reward_mana,
                rank_requirement=mission.rank_requirement,
                season_id=mission.season_id,
                category=mission.category,
                tasks=tasks,
            )
        except KeyError as error:
            raise MissionNotFoundError from error

    async def get_mission_by_title(self, title: str) -> Mission:
        for mission in self.mission_table.values():
            if mission.title == title:
                return mission
        raise MissionNotFoundError

    async def list_missions(self) -> Missions:
        return Missions(values=list(self.mission_table.values()))

    async def update_mission(self, mission: Mission) -> None:
        if mission.id not in self.mission_table:
            raise MissionNotFoundError
        self.mission_table[mission.id] = mission

    async def delete_mission(self, mission_id: int) -> None:
        try:
            del self.mission_table[mission_id]
        except KeyError as error:
            raise MissionNotFoundError from error

    async def update_season(self, branch: Season) -> None:
        try:
            existing_branch = self.season_table[branch.name]
            if existing_branch.id != branch.id:
                raise SeasonNameAlreadyExistError
        except KeyError:
            pass
        # Найти ветку по ID и обновить
        for name, existing_branch in self.season_table.items():
            if existing_branch.id == branch.id:
                del self.season_table[name]
                self.season_table[branch.name] = branch
                return
        raise SeasonNotFoundError

    async def delete_season(self, season_id: int) -> None:
        for name, branch in self.season_table.items():
            if branch.id == season_id:
                del self.season_table[name]
                return
        raise SeasonNotFoundError

    async def insert_mission_task(self, task: MissionTask) -> None:
        for existing_task in self.task_table.values():
            if existing_task.title == task.title:
                raise TaskNameAlreadyExistError
        self.task_table[task.id] = task

    async def get_mission_task_by_id(self, task_id: int) -> MissionTask:
        try:
            return self.task_table[task_id]
        except KeyError as error:
            raise TaskNotFoundError from error

    async def get_mission_task_by_title(self, title: str) -> MissionTask:
        for task in self.task_table.values():
            if task.title == title:
                return task
        raise TaskNotFoundError

    async def list_mission_tasks(self) -> MissionTasks:
        return MissionTasks(values=list(self.task_table.values()))

    async def update_mission_task(self, task: MissionTask) -> None:
        if task.id not in self.task_table:
            raise TaskNotFoundError
        self.task_table[task.id] = task

    async def delete_mission_task(self, task_id: int) -> None:
        try:
            del self.task_table[task_id]
        except KeyError as error:
            raise TaskNotFoundError from error

    async def add_task_to_mission(self, mission_id: int, task_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if task_id not in self.task_table:
            raise TaskNotFoundError

        if mission_id not in self.missions_tasks_relations:
            self.missions_tasks_relations[mission_id] = set()
        self.missions_tasks_relations[mission_id].add(task_id)

    async def remove_task_from_mission(self, mission_id: int, task_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if task_id not in self.task_table:
            raise TaskNotFoundError

        if mission_id in self.missions_tasks_relations:
            self.missions_tasks_relations[mission_id].discard(task_id)
            if not self.missions_tasks_relations[mission_id]:
                del self.missions_tasks_relations[mission_id]

    async def insert_artifact(self, artifact: Artifact) -> None:
        for existing_artifact in self.artifact_table.values():
            if existing_artifact.title == artifact.title:
                raise ArtifactTitleAlreadyExistError

        # Generate ID if not provided
        if artifact.id == 0:
            artifact_id = max(self.artifact_table.keys(), default=0) + 1
            artifact = Artifact(
                id=artifact_id,
                title=artifact.title,
                description=artifact.description,
                rarity=artifact.rarity,
                image_url=artifact.image_url,
            )

        self.artifact_table[artifact.id] = artifact

    async def get_artifact_by_id(self, artifact_id: int) -> Artifact:
        try:
            return self.artifact_table[artifact_id]
        except KeyError as error:
            raise ArtifactNotFoundError from error

    async def get_artifact_by_title(self, title: str) -> Artifact:
        for artifact in self.artifact_table.values():
            if artifact.title == title:
                return artifact
        raise ArtifactNotFoundError

    async def list_artifacts(self) -> Artifacts:
        return Artifacts(values=list(self.artifact_table.values()))

    async def update_artifact(self, artifact: Artifact) -> None:
        if artifact.id not in self.artifact_table:
            raise ArtifactNotFoundError
        self.artifact_table[artifact.id] = artifact

    async def delete_artifact(self, artifact_id: int) -> None:
        try:
            del self.artifact_table[artifact_id]
        except KeyError as error:
            raise ArtifactNotFoundError from error

    async def add_artifact_to_mission(self, mission_id: int, artifact_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if artifact_id not in self.artifact_table:
            raise ArtifactNotFoundError

        if mission_id not in self.missions_artifacts_relations:
            self.missions_artifacts_relations[mission_id] = set()
        self.missions_artifacts_relations[mission_id].add(artifact_id)

    async def remove_artifact_from_mission(self, mission_id: int, artifact_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if artifact_id not in self.artifact_table:
            raise ArtifactNotFoundError

        if mission_id in self.missions_artifacts_relations:
            self.missions_artifacts_relations[mission_id].discard(artifact_id)
            if not self.missions_artifacts_relations[mission_id]:
                del self.missions_artifacts_relations[mission_id]

    async def add_artifact_to_user(self, user_login: str, artifact_id: int) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if artifact_id not in self.artifact_table:
            raise ArtifactNotFoundError

        if user_login not in self.users_artifacts_relations:
            self.users_artifacts_relations[user_login] = set()
        self.users_artifacts_relations[user_login].add(artifact_id)

    async def remove_artifact_from_user(self, user_login: str, artifact_id: int) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if artifact_id not in self.artifact_table:
            raise ArtifactNotFoundError

        if user_login in self.users_artifacts_relations:
            self.users_artifacts_relations[user_login].discard(artifact_id)
            if not self.users_artifacts_relations[user_login]:
                del self.users_artifacts_relations[user_login]

    # New methods for competency and skill rewards
    async def add_competency_reward_to_mission(
        self, mission_id: int, competency_id: int, level_increase: int
    ) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id not in self.missions_competencies_rewards:
            self.missions_competencies_rewards[mission_id] = {}
        self.missions_competencies_rewards[mission_id][competency_id] = level_increase

    async def remove_competency_reward_from_mission(
        self, mission_id: int, competency_id: int
    ) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id in self.missions_competencies_rewards:
            self.missions_competencies_rewards[mission_id].pop(competency_id, None)
            if not self.missions_competencies_rewards[mission_id]:
                del self.missions_competencies_rewards[mission_id]

    async def add_skill_reward_to_mission(
        self, mission_id: int, skill_id: int, level_increase: int
    ) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id not in self.missions_skills_rewards:
            self.missions_skills_rewards[mission_id] = {}
        self.missions_skills_rewards[mission_id][skill_id] = level_increase

    async def remove_skill_reward_from_mission(self, mission_id: int, skill_id: int) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id in self.missions_skills_rewards:
            self.missions_skills_rewards[mission_id].pop(skill_id, None)
            if not self.missions_skills_rewards[mission_id]:
                del self.missions_skills_rewards[mission_id]

    # CompetencyStorage methods
    async def insert_competency(self, competency: Competency) -> None:
        for existing in self.competencies_table.values():
            if existing.name == competency.name:
                raise CompetencyNameAlreadyExistError
        self.competencies_table[competency.id] = competency

    async def get_competency_by_id(self, competency_id: int) -> Competency:
        try:
            return self.competencies_table[competency_id]
        except KeyError as error:
            raise CompetencyNotFoundError from error

    async def get_competency_by_name(self, name: str) -> Competency:
        for competency in self.competencies_table.values():
            if competency.name == name:
                return competency
        raise CompetencyNotFoundError

    async def list_competencies(self) -> Competencies:
        return Competencies(values=list(self.competencies_table.values()))

    async def update_competency(self, competency: Competency) -> None:
        if competency.id not in self.competencies_table:
            raise CompetencyNotFoundError
        self.competencies_table[competency.id] = competency

    async def delete_competency(self, competency_id: int) -> None:
        try:
            del self.competencies_table[competency_id]
        except KeyError as error:
            raise CompetencyNotFoundError from error
        self.competencies_skills_relations.pop(competency_id, None)

    async def add_skill_to_competency(self, competency_id: int, skill_id: int) -> None:
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError
        if skill_id not in self.skill_table:
            raise SkillNotFoundError
        if competency_id not in self.competencies_skills_relations:
            self.competencies_skills_relations[competency_id] = set()
        self.competencies_skills_relations[competency_id].add(skill_id)

    async def remove_skill_from_competency(self, competency_id: int, skill_id: int) -> None:
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError
        if skill_id not in self.skill_table:
            raise SkillNotFoundError
        if competency_id in self.competencies_skills_relations:
            self.competencies_skills_relations[competency_id].discard(skill_id)
            if not self.competencies_skills_relations[competency_id]:
                del self.competencies_skills_relations[competency_id]

    async def insert_skill(self, skill: Skill) -> None:
        for existing in self.skill_table.values():
            if existing.name == skill.name:
                raise SkillNameAlreadyExistError
        self.skill_table[skill.id] = skill

    async def get_skill_by_id(self, skill_id: int) -> Skill:
        try:
            return self.skill_table[skill_id]
        except KeyError as error:
            raise SkillNotFoundError from error

    async def get_skill_by_name(self, name: str) -> Skill:
        for skill in self.skill_table.values():
            if skill.name == name:
                return skill
        raise SkillNotFoundError

    async def list_skills(self) -> Skills:
        return Skills(values=list(self.skill_table.values()))

    async def update_skill(self, skill: Skill) -> None:
        if skill.id not in self.skill_table:
            raise SkillNotFoundError
        self.skill_table[skill.id] = skill

    async def delete_skill(self, skill_id: int) -> None:
        try:
            del self.skill_table[skill_id]
        except KeyError as error:
            raise SkillNotFoundError from error
        # Remove from any competency relations
        for comp_id, skills in list(self.competencies_skills_relations.items()):
            skills.discard(skill_id)
            if not skills:
                del self.competencies_skills_relations[comp_id]

    # RankStorage methods
    async def insert_rank(self, rank: Rank) -> None:
        for existing in self.rank_table.values():
            if existing.name == rank.name:
                raise RankNameAlreadyExistError
        self.rank_table[rank.id] = rank

    async def get_rank_by_id(self, rank_id: int) -> Rank:
        try:
            rank = self.rank_table[rank_id]
        except KeyError as error:
            raise RankNotFoundError from error

        mission_ids = self.ranks_missions_requirements.get(rank_id, set())
        missions = [self.mission_table[mid] for mid in mission_ids if mid in self.mission_table]

        comp_reqs = self.ranks_competencies_requirements.get(rank_id, {})
        reqs: list[RankCompetencyRequirement] = []
        for comp_id, min_level in comp_reqs.items():
            if comp_id in self.competencies_table:
                comp = self.competencies_table[comp_id]
                reqs.append(RankCompetencyRequirement(competency=comp, min_level=min_level))

        return Rank(
            id=rank.id,
            name=rank.name,
            required_xp=rank.required_xp,
            required_missions=missions,
            required_competencies=reqs,
        )

    async def get_rank_by_name(self, name: str) -> Rank:
        for rank in self.rank_table.values():
            if rank.name == name:
                return await self.get_rank_by_id(rank.id)
        raise RankNotFoundError

    async def list_ranks(self) -> Ranks:
        return Ranks(values=list(self.rank_table.values()))

    async def update_rank(self, rank: Rank) -> None:
        if rank.id not in self.rank_table:
            raise RankNotFoundError
        self.rank_table[rank.id] = rank

    async def delete_rank(self, rank_id: int) -> None:
        try:
            del self.rank_table[rank_id]
        except KeyError as error:
            raise RankNotFoundError from error
        self.ranks_missions_requirements.pop(rank_id, None)
        self.ranks_competencies_requirements.pop(rank_id, None)

    async def add_required_mission_to_rank(self, rank_id: int, mission_id: int) -> None:
        if rank_id not in self.rank_table:
            raise RankNotFoundError
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if rank_id not in self.ranks_missions_requirements:
            self.ranks_missions_requirements[rank_id] = set()
        self.ranks_missions_requirements[rank_id].add(mission_id)

    async def remove_required_mission_from_rank(self, rank_id: int, mission_id: int) -> None:
        if rank_id not in self.rank_table:
            raise RankNotFoundError
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if rank_id in self.ranks_missions_requirements:
            self.ranks_missions_requirements[rank_id].discard(mission_id)
            if not self.ranks_missions_requirements[rank_id]:
                del self.ranks_missions_requirements[rank_id]

    async def add_required_competency_to_rank(
        self, rank_id: int, competency_id: int, min_level: int
    ) -> None:
        if rank_id not in self.rank_table:
            raise RankNotFoundError
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError
        competency = self.competencies_table[competency_id]
        if min_level > competency.max_level:
            raise RankCompetencyMinLevelTooHighError
        if rank_id not in self.ranks_competencies_requirements:
            self.ranks_competencies_requirements[rank_id] = {}
        self.ranks_competencies_requirements[rank_id][competency_id] = min_level

    async def remove_required_competency_from_rank(self, rank_id: int, competency_id: int) -> None:
        if rank_id not in self.rank_table:
            raise RankNotFoundError
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError
        if rank_id in self.ranks_competencies_requirements:
            self.ranks_competencies_requirements[rank_id].pop(competency_id, None)
            if not self.ranks_competencies_requirements[rank_id]:
                del self.ranks_competencies_requirements[rank_id]

    # Mission chain methods
    async def insert_mission_chain(self, mission_chain: MissionChain) -> None:
        for existing in self.mission_chain_table.values():
            if existing.name == mission_chain.name:
                raise MissionChainNameAlreadyExistError
        self.mission_chain_table[mission_chain.id] = mission_chain

    async def get_mission_chain_by_id(self, chain_id: int) -> MissionChain:
        try:
            base_chain = self.mission_chain_table[chain_id]
            # Get missions for this chain
            missions: list[Mission] = []
            if chain_id in self.mission_chains_missions_relations:
                missions.extend(
                    self.mission_table[mission_id]
                    for mission_id in self.mission_chains_missions_relations[chain_id]
                    if mission_id in self.mission_table
                )

            # Get dependencies for this chain
            dependencies = []
            if chain_id in self.mission_dependencies:
                for mission_id, prerequisite_mission_id in self.mission_dependencies[chain_id]:
                    dependencies.append(
                        MissionDependency(
                            mission_id=mission_id, prerequisite_mission_id=prerequisite_mission_id
                        )
                    )

            return MissionChain(
                id=base_chain.id,
                name=base_chain.name,
                description=base_chain.description,
                reward_xp=base_chain.reward_xp,
                reward_mana=base_chain.reward_mana,
                missions=missions,
                dependencies=dependencies,
                mission_orders=[],  # V moke мы не отслеживаем порядки детально
            )
        except KeyError as error:
            raise MissionChainNotFoundError from error

    async def get_mission_chain_by_name(self, name: str) -> MissionChain:
        for chain_id, base_chain in self.mission_chain_table.items():
            if base_chain.name == name:
                # Get missions for this chain
                missions: list[Mission] = []
                if chain_id in self.mission_chains_missions_relations:
                    missions.extend(
                        self.mission_table[mission_id]
                        for mission_id in self.mission_chains_missions_relations[chain_id]
                        if mission_id in self.mission_table
                    )

                # Get dependencies for this chain
                dependencies = []
                if chain_id in self.mission_dependencies:
                    for mission_id, prerequisite_mission_id in self.mission_dependencies[chain_id]:
                        dependencies.append(
                            MissionDependency(
                                mission_id=mission_id,
                                prerequisite_mission_id=prerequisite_mission_id,
                            )
                        )

                return MissionChain(
                    id=base_chain.id,
                    name=base_chain.name,
                    description=base_chain.description,
                    reward_xp=base_chain.reward_xp,
                    reward_mana=base_chain.reward_mana,
                    missions=missions,
                    dependencies=dependencies,
                    mission_orders=[],  # V moke мы не отслеживаем порядки детально
                )
        raise MissionChainNotFoundError

    async def list_mission_chains(self) -> MissionChains:
        return MissionChains(values=list(self.mission_chain_table.values()))

    async def update_mission_chain(self, mission_chain: MissionChain) -> None:
        if mission_chain.id not in self.mission_chain_table:
            raise MissionChainNotFoundError
        self.mission_chain_table[mission_chain.id] = mission_chain

    async def delete_mission_chain(self, chain_id: int) -> None:
        try:
            del self.mission_chain_table[chain_id]
        except KeyError as error:
            raise MissionChainNotFoundError from error

    async def add_mission_to_chain(self, chain_id: int, mission_id: int) -> None:
        if chain_id not in self.mission_chains_missions_relations:
            self.mission_chains_missions_relations[chain_id] = set()
        if mission_id in self.mission_chains_missions_relations[chain_id]:
            raise MissionChainMissionAlreadyExistsError
        self.mission_chains_missions_relations[chain_id].add(mission_id)

    async def remove_mission_from_chain(self, chain_id: int, mission_id: int) -> None:
        if chain_id not in self.mission_chain_table:
            raise MissionChainNotFoundError
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if chain_id in self.mission_chains_missions_relations:
            self.mission_chains_missions_relations[chain_id].discard(mission_id)
            if not self.mission_chains_missions_relations[chain_id]:
                del self.mission_chains_missions_relations[chain_id]

    async def add_mission_dependency(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> None:
        if chain_id not in self.mission_dependencies:
            self.mission_dependencies[chain_id] = set()
        if (mission_id, prerequisite_mission_id) in self.mission_dependencies[chain_id]:
            raise MissionDependencyAlreadyExistsError
        self.mission_dependencies[chain_id].add((mission_id, prerequisite_mission_id))

    async def remove_mission_dependency(
        self, chain_id: int, mission_id: int, prerequisite_mission_id: int
    ) -> None:
        if chain_id not in self.mission_chain_table:
            raise MissionChainNotFoundError
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if prerequisite_mission_id not in self.mission_table:
            raise MissionNotFoundError
        if chain_id in self.mission_dependencies:
            self.mission_dependencies[chain_id].discard((mission_id, prerequisite_mission_id))
            if not self.mission_dependencies[chain_id]:
                del self.mission_dependencies[chain_id]

    async def update_mission_order_in_chain(
        self, chain_id: int, mission_id: int, new_order: int
    ) -> None:
        if chain_id not in self.mission_chains_missions_relations:
            raise MissionChainNotFoundError

        if mission_id not in self.mission_chains_missions_relations[chain_id]:
            raise MissionNotFoundError

    async def add_user_task(self, user_login: str, user_task: UserTask) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if user_task.id not in self.task_table:
            raise TaskNotFoundError

        if user_login not in self.users_tasks_relations:
            self.users_tasks_relations[user_login] = {}
        self.users_tasks_relations[user_login][user_task.id] = user_task.is_completed

    async def get_user_mission(self, mission_id: int, user_login: str) -> Mission:
        mission = await self.get_mission_by_id(mission_id)
        user_login = str(user_login)
        task_ids = self.missions_tasks_relations.get(mission_id, set())
        user_tasks = []
        for task_id in task_ids:
            if task_id in self.task_table:
                task = self.task_table[task_id]
                is_completed = False

                if (
                    user_login in self.users_tasks_relations
                    and task_id in self.users_tasks_relations[user_login]
                ):
                    is_completed = self.users_tasks_relations[user_login][task_id]

                user_task = UserTask(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    is_completed=is_completed,
                )
                user_tasks.append(user_task)
        return Mission(
            id=mission.id,
            title=mission.title,
            description=mission.description,
            reward_xp=mission.reward_xp,
            reward_mana=mission.reward_mana,
            rank_requirement=mission.rank_requirement,
            season_id=mission.season_id,
            category=mission.category,
            user_tasks=user_tasks,
        )

    async def insert_store_item(self, store_item: StoreItem) -> None:
        for existing in self.store_item_table.values():
            if existing.title == store_item.title:
                raise StoreItemTitleAlreadyExistError
        self.store_item_table[store_item.id] = store_item

    async def get_store_item_by_id(self, store_item_id: int) -> StoreItem:
        try:
            return self.store_item_table[store_item_id]
        except KeyError as error:
            raise StoreItemNotFoundError from error

    async def get_store_item_by_title(self, title: str) -> StoreItem:
        for store_item in self.store_item_table.values():
            if store_item.title == title:
                return store_item
        raise StoreItemNotFoundError

    async def list_store_items(self) -> StoreItems:
        return StoreItems(values=list(self.store_item_table.values()))

    async def update_store_item(self, store_item: StoreItem) -> None:
        if store_item.id not in self.store_item_table:
            raise StoreItemNotFoundError
        self.store_item_table[store_item.id] = store_item

    async def delete_store_item(self, store_item_id: int) -> None:
        try:
            del self.store_item_table[store_item_id]
        except KeyError as error:
            raise StoreItemNotFoundError from error

    async def purchase_store_item(self, purchase: StorePurchase, mana_count: int) -> None:
        store_item = self.store_item_table[purchase.store_item_id]
        updated_store_item = StoreItem(
            id=store_item.id,
            title=store_item.title,
            price=store_item.price,
            stock=store_item.stock - 1,
        )
        self.store_item_table[purchase.store_item_id] = updated_store_item

        user = self.user_table[purchase.user_login]
        if isinstance(user, CandidateUser):
            updated_user = CandidateUser(
                login=user.login,
                first_name=user.first_name,
                last_name=user.last_name,
                password=user.password,
                role=user.role,
                rank_id=user.rank_id,
                exp=user.exp,
                mana=user.mana - mana_count,
                artifacts=user.artifacts,
            )
            self.user_table[purchase.user_login] = updated_user

    # UserStorage methods for competencies and skills
    async def get_user_by_login_with_relations(self, login: str) -> User:
        try:
            return self.user_table[login]
        except KeyError as error:
            raise UserNotFoundError from error

    async def list_users(self) -> list[User]:
        return list(self.user_table.values())

    async def add_competency_to_user(
        self, user_login: str, competency_id: int, level: int = 0
    ) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError

        if user_login not in self.users_competencies_relations:
            self.users_competencies_relations[user_login] = {}
        self.users_competencies_relations[user_login][competency_id] = level

    async def remove_competency_from_user(self, user_login: str, competency_id: int) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError

        if user_login in self.users_competencies_relations:
            self.users_competencies_relations[user_login].pop(competency_id, None)
            if not self.users_competencies_relations[user_login]:
                del self.users_competencies_relations[user_login]

    async def update_user_competency_level(
        self, user_login: str, competency_id: int, level: int
    ) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError

        if user_login not in self.users_competencies_relations:
            raise UserNotFoundError
        if competency_id not in self.users_competencies_relations[user_login]:
            raise UserNotFoundError

        self.users_competencies_relations[user_login][competency_id] = level

    async def add_skill_to_user(
        self, user_login: str, skill_id: int, competency_id: int, level: int = 0
    ) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if skill_id not in self.skill_table:
            raise SkillNotFoundError
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError

        if user_login not in self.users_skills_relations:
            self.users_skills_relations[user_login] = {}
        if skill_id not in self.users_skills_relations[user_login]:
            self.users_skills_relations[user_login][skill_id] = {}
        self.users_skills_relations[user_login][skill_id][competency_id] = level

    async def remove_skill_from_user(
        self, user_login: str, skill_id: int, competency_id: int
    ) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if skill_id not in self.skill_table:
            raise SkillNotFoundError
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError

        if (
            user_login in self.users_skills_relations
            and skill_id in self.users_skills_relations[user_login]
        ):
            self.users_skills_relations[user_login][skill_id].pop(competency_id, None)
            if not self.users_skills_relations[user_login][skill_id]:
                del self.users_skills_relations[user_login][skill_id]
            if not self.users_skills_relations[user_login]:
                del self.users_skills_relations[user_login]

    async def update_user_skill_level(
        self, user_login: str, skill_id: int, competency_id: int, level: int
    ) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError
        if skill_id not in self.skill_table:
            raise SkillNotFoundError
        if competency_id not in self.competencies_table:
            raise CompetencyNotFoundError

        if user_login not in self.users_skills_relations:
            raise UserNotFoundError
        if skill_id not in self.users_skills_relations[user_login]:
            raise UserNotFoundError
        if competency_id not in self.users_skills_relations[user_login][skill_id]:
            raise UserNotFoundError

        self.users_skills_relations[user_login][skill_id][competency_id] = level

    async def update_user(self, user: User) -> None:
        if user.login not in self.user_table:
            raise UserNotFoundError
        self.user_table[user.login] = user

    async def get_mission_by_task(self, task_id: int) -> Mission:
        for mission_id, task_ids in self.missions_tasks_relations.items():
            if task_id in task_ids:
                return await self.get_mission_by_id(mission_id)
        raise MissionNotFoundError

    async def update_user_task_completion(self, task_id: int, user_login: str) -> None:
        if user_login not in self.users_tasks_relations:
            self.users_tasks_relations[user_login] = {}
        self.users_tasks_relations[user_login][task_id] = True

    async def update_user_exp_and_mana(
        self, user_login: str, exp_increase: int, mana_increase: int
    ) -> None:
        if user_login not in self.user_table:
            raise UserNotFoundError

        user = self.user_table[user_login]
        if hasattr(user, "exp") and hasattr(user, "mana"):
            if hasattr(user, "artifacts"):
                updated_user = type(user)(
                    login=user.login,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    password=user.password,
                    role=user.role,
                    rank_id=user.rank_id,
                    exp=user.exp + exp_increase,
                    mana=user.mana + mana_increase,
                    artifacts=user.artifacts,
                )
            else:
                # Для обычного User
                updated_user = type(user)(
                    login=user.login,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    password=user.password,
                    role=user.role,
                    rank_id=user.rank_id,
                    exp=user.exp + exp_increase,
                    mana=user.mana + mana_increase,
                )
            self.user_table[user_login] = updated_user
