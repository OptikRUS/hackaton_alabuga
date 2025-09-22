from dataclasses import dataclass, field

from src.core.artifacts.exceptions import (
    ArtifactNotFoundError,
    ArtifactTitleAlreadyExistError,
)
from src.core.artifacts.schemas import Artifact, Artifacts
from src.core.competitions.exceptions import (
    CompetitionNameAlreadyExistError,
    CompetitionNotFoundError,
)
from src.core.competitions.schemas import Competition, Competitions
from src.core.missions.exceptions import (
    MissionBranchNameAlreadyExistError,
    MissionBranchNotFoundError,
    MissionNameAlreadyExistError,
    MissionNotFoundError,
)
from src.core.missions.schemas import (
    Mission,
    MissionBranch,
    MissionBranches,
    Missions,
)
from src.core.ranks.exceptions import (
    RankCompetitionMinLevelTooHighError,
    RankNameAlreadyExistError,
    RankNotFoundError,
)
from src.core.ranks.schemas import Rank, RankCompetitionRequirement, Ranks
from src.core.skills.exceptions import (
    SkillNameAlreadyExistError,
    SkillNotFoundError,
)
from src.core.skills.schemas import Skill, Skills
from src.core.storages import (
    ArtifactStorage,
    CompetitionStorage,
    MissionStorage,
    RankStorage,
    SkillStorage,
    UserStorage,
)
from src.core.tasks.exceptions import (
    TaskNameAlreadyExistError,
    TaskNotFoundError,
)
from src.core.tasks.schemas import (
    MissionTask,
    MissionTasks,
)
from src.core.users.exceptions import UserAlreadyExistError, UserNotFoundError
from src.core.users.schemas import User


@dataclass
class StorageMock(
    UserStorage, MissionStorage, ArtifactStorage, CompetitionStorage, SkillStorage, RankStorage
):
    user_table: dict[str, User] = field(default_factory=dict)
    mission_branch_table: dict[str, MissionBranch] = field(default_factory=dict)
    mission_table: dict[int, Mission] = field(default_factory=dict)
    task_table: dict[int, MissionTask] = field(default_factory=dict)
    artifact_table: dict[int, Artifact] = field(default_factory=dict)
    competition_table: dict[int, Competition] = field(default_factory=dict)
    skill_table: dict[int, Skill] = field(default_factory=dict)
    rank_table: dict[int, Rank] = field(default_factory=dict)
    missions_tasks_relations: dict[int, set[int]] = field(default_factory=dict)
    missions_artifacts_relations: dict[int, set[int]] = field(default_factory=dict)
    users_artifacts_relations: dict[str, set[int]] = field(default_factory=dict)
    missions_competitions_rewards: dict[int, dict[int, int]] = field(default_factory=dict)
    missions_skills_rewards: dict[int, dict[int, int]] = field(default_factory=dict)
    competitions_skills_relations: dict[int, set[int]] = field(default_factory=dict)
    ranks_missions_requirements: dict[int, set[int]] = field(default_factory=dict)
    ranks_competitions_requirements: dict[int, dict[int, int]] = field(default_factory=dict)

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

    async def insert_mission_branch(self, branch: MissionBranch) -> None:
        try:
            self.mission_branch_table[branch.name]
            raise MissionBranchNameAlreadyExistError
        except KeyError:
            self.mission_branch_table[branch.name] = branch

    async def get_mission_branch_by_name(self, name: str) -> MissionBranch:
        try:
            return self.mission_branch_table[name]
        except KeyError as error:
            raise MissionBranchNotFoundError from error

    async def get_mission_branch_by_id(self, branch_id: int) -> MissionBranch:
        for branch in self.mission_branch_table.values():
            if branch.id == branch_id:
                return branch
        raise MissionBranchNotFoundError

    async def list_mission_branches(self) -> MissionBranches:
        return MissionBranches(values=list(self.mission_branch_table.values()))

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
                branch_id=mission.branch_id,
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

    async def update_mission_branch(self, branch: MissionBranch) -> None:
        try:
            existing_branch = self.mission_branch_table[branch.name]
            if existing_branch.id != branch.id:
                raise MissionBranchNameAlreadyExistError
        except KeyError:
            pass
        # Найти ветку по ID и обновить
        for name, existing_branch in self.mission_branch_table.items():
            if existing_branch.id == branch.id:
                del self.mission_branch_table[name]
                self.mission_branch_table[branch.name] = branch
                return
        raise MissionBranchNotFoundError

    async def delete_mission_branch(self, branch_id: int) -> None:
        for name, branch in self.mission_branch_table.items():
            if branch.id == branch_id:
                del self.mission_branch_table[name]
                return
        raise MissionBranchNotFoundError

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

    # ArtifactStorage methods
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
        self, mission_id: int, competition_id: int, level_increase: int
    ) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id not in self.missions_competitions_rewards:
            self.missions_competitions_rewards[mission_id] = {}
        self.missions_competitions_rewards[mission_id][competition_id] = level_increase

    async def remove_competency_reward_from_mission(
        self, mission_id: int, competition_id: int
    ) -> None:
        if mission_id not in self.mission_table:
            raise MissionNotFoundError
        if mission_id in self.missions_competitions_rewards:
            self.missions_competitions_rewards[mission_id].pop(competition_id, None)
            if not self.missions_competitions_rewards[mission_id]:
                del self.missions_competitions_rewards[mission_id]

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

    # CompetitionStorage methods
    async def insert_competition(self, competition: Competition) -> None:
        for existing in self.competition_table.values():
            if existing.name == competition.name:
                raise CompetitionNameAlreadyExistError
        self.competition_table[competition.id] = competition

    async def get_competition_by_id(self, competition_id: int) -> Competition:
        try:
            return self.competition_table[competition_id]
        except KeyError as error:
            raise CompetitionNotFoundError from error

    async def get_competition_by_name(self, name: str) -> Competition:
        for competition in self.competition_table.values():
            if competition.name == name:
                return competition
        raise CompetitionNotFoundError

    async def list_competitions(self) -> Competitions:
        return Competitions(values=list(self.competition_table.values()))

    async def update_competition(self, competition: Competition) -> None:
        if competition.id not in self.competition_table:
            raise CompetitionNotFoundError
        self.competition_table[competition.id] = competition

    async def delete_competition(self, competition_id: int) -> None:
        try:
            del self.competition_table[competition_id]
        except KeyError as error:
            raise CompetitionNotFoundError from error
        self.competitions_skills_relations.pop(competition_id, None)

    async def add_skill_to_competition(self, competition_id: int, skill_id: int) -> None:
        if competition_id not in self.competition_table:
            raise CompetitionNotFoundError
        if skill_id not in self.skill_table:
            raise SkillNotFoundError
        if competition_id not in self.competitions_skills_relations:
            self.competitions_skills_relations[competition_id] = set()
        self.competitions_skills_relations[competition_id].add(skill_id)

    async def remove_skill_from_competition(self, competition_id: int, skill_id: int) -> None:
        if competition_id not in self.competition_table:
            raise CompetitionNotFoundError
        if skill_id not in self.skill_table:
            raise SkillNotFoundError
        if competition_id in self.competitions_skills_relations:
            self.competitions_skills_relations[competition_id].discard(skill_id)
            if not self.competitions_skills_relations[competition_id]:
                del self.competitions_skills_relations[competition_id]

    # SkillStorage methods
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
        # Remove from any competition relations
        for comp_id, skills in list(self.competitions_skills_relations.items()):
            skills.discard(skill_id)
            if not skills:
                del self.competitions_skills_relations[comp_id]

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

        comp_reqs = self.ranks_competitions_requirements.get(rank_id, {})
        reqs: list[RankCompetitionRequirement] = []
        for comp_id, min_level in comp_reqs.items():
            if comp_id in self.competition_table:
                comp = self.competition_table[comp_id]
                reqs.append(RankCompetitionRequirement(competition=comp, min_level=min_level))

        return Rank(
            id=rank.id,
            name=rank.name,
            required_xp=rank.required_xp,
            required_missions=missions,
            required_competitions=reqs,
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
        self.ranks_competitions_requirements.pop(rank_id, None)

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

    async def add_required_competition_to_rank(
        self, rank_id: int, competition_id: int, min_level: int
    ) -> None:
        if rank_id not in self.rank_table:
            raise RankNotFoundError
        if competition_id not in self.competition_table:
            raise CompetitionNotFoundError
        competition = self.competition_table[competition_id]
        if min_level > competition.max_level:
            raise RankCompetitionMinLevelTooHighError
        if rank_id not in self.ranks_competitions_requirements:
            self.ranks_competitions_requirements[rank_id] = {}
        self.ranks_competitions_requirements[rank_id][competition_id] = min_level

    async def remove_required_competition_from_rank(
        self, rank_id: int, competition_id: int
    ) -> None:
        if rank_id not in self.rank_table:
            raise RankNotFoundError
        if competition_id not in self.competition_table:
            raise CompetitionNotFoundError
        if rank_id in self.ranks_competitions_requirements:
            self.ranks_competitions_requirements[rank_id].pop(competition_id, None)
            if not self.ranks_competitions_requirements[rank_id]:
                del self.ranks_competitions_requirements[rank_id]
