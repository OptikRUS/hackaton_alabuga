import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.missions.exceptions import MissionNotCompletedError
from src.core.missions.use_cases import ApproveUserMissionUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestApproveUserMissionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = ApproveUserMissionUseCase(
            mission_storage=self.storage,
            artifact_storage=self.storage,
            user_storage=self.storage,
            competency_storage=self.storage,
            rank_storage=self.storage,
        )
        self.test_user = self.factory.candidate(login="test_user", exp=100, mana=50)
        self.beginner_rank = self.factory.rank(rank_id=1, name="Beginner", required_xp=0)
        self.intermediate_rank = self.factory.rank(rank_id=2, name="Intermediate", required_xp=200)
        await self.storage.insert_user(user=self.test_user)
        await self.storage.insert_rank(rank=self.beginner_rank)
        await self.storage.insert_rank(rank=self.intermediate_rank)

    async def test_approve_completed_mission_rewards_user(self) -> None:
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=1,
                title="Task 1",
                description="First task",
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=2,
                title="Task 2",
                description="Second task",
            )
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Test Mission",
                description="Test Description",
                reward_xp=200,
                reward_mana=100,
                tasks=[
                    self.factory.mission_task(
                        task_id=1,
                        title="Task 1",
                        description="First task",
                    ),
                    self.factory.mission_task(
                        task_id=2,
                        title="Task 2",
                        description="Second task",
                    ),
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.add_task_to_mission(mission_id=1, task_id=2)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")
        await self.storage.update_user_task_completion(task_id=2, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        updated_user = await self.storage.get_user_by_login("test_user")
        assert updated_user.exp == 300  # 100 + 200
        assert updated_user.mana == 150  # 50 + 100

    async def test_approve_incomplete_mission_raises_error(self) -> None:
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=1,
                title="Task 1",
                description="First task",
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=2,
                title="Task 2",
                description="Second task",
            )
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Test Mission",
                description="Test Description",
                reward_xp=200,
                reward_mana=100,
                tasks=[
                    self.factory.mission_task(
                        task_id=1,
                        title="Task 1",
                        description="First task",
                    ),
                    self.factory.mission_task(
                        task_id=2,
                        title="Task 2",
                        description="Second task",
                    ),
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.add_task_to_mission(mission_id=1, task_id=2)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        with pytest.raises(MissionNotCompletedError):
            await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что награды не начислены
        updated_user = await self.storage.get_user_by_login("test_user")
        assert updated_user.exp == 100  # без изменений
        assert updated_user.mana == 50  # без изменений

    async def test_approve_mission_with_artifact_rewards(self) -> None:
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="Rare Sword",
                description="A powerful sword",
                rarity=ArtifactRarityEnum.RARE,
            )
        )
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=2,
                title="Magic Ring",
                description="A magical ring",
                rarity=ArtifactRarityEnum.EPIC,
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Artifact Mission",
                description="Mission with artifact rewards",
                reward_xp=200,
                reward_mana=100,
                reward_artifacts=[
                    (
                        self.factory.artifact(
                            artifact_id=1,
                            title="Rare Sword",
                            description="A powerful sword",
                            rarity=ArtifactRarityEnum.RARE,
                        )
                    ),
                    (
                        self.factory.artifact(
                            artifact_id=2,
                            title="Magic Ring",
                            description="A magical ring",
                            rarity=ArtifactRarityEnum.EPIC,
                        )
                    ),
                ],
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что артефакты добавлены пользователю
        user_artifacts = await self.storage.get_user_artifacts(user_login="test_user")
        assert len(user_artifacts.values) == 2
        assert user_artifacts.values[0].id == 1
        assert user_artifacts.values[1].id == 2

    async def test_approve_mission_with_competency_rewards(self) -> None:
        await self.storage.insert_competency(
            competency=self.factory.competency(competency_id=1, name="Programming", max_level=100)
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Competency Mission",
                description="Mission with competency rewards",
                reward_xp=200,
                reward_mana=100,
                reward_competencies=[
                    self.factory.competency_reward(
                        competency=(
                            self.factory.competency(
                                competency_id=1, name="Programming", max_level=100
                            )
                        ),
                        level_increase=5,
                    )
                ],
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что компетенция добавлена пользователю
        user_competencies = await self.storage.get_user_competencies(user_login="test_user")
        assert len(user_competencies.values) == 1
        assert user_competencies.values[0].id == 1
        assert user_competencies.values[0].user_level == 5

    async def test_approve_mission_with_skill_rewards(self) -> None:
        # Создаем компетенцию и навык
        await self.storage.insert_competency(
            competency=self.factory.competency(
                competency_id=1,
                name="Programming",
                max_level=100,
                skills=[self.factory.skill(skill_id=1, name="Python", max_level=50)],
            )
        )
        await self.storage.insert_skill(
            skill=self.factory.skill(skill_id=1, name="Python", max_level=50)
        )
        await self.storage.add_skill_to_competency(competency_id=1, skill_id=1)
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Skill Mission",
                description="Mission with skill rewards",
                reward_xp=200,
                reward_mana=100,
                reward_skills=[
                    self.factory.skill_reward(
                        skill=(self.factory.skill(skill_id=1, name="Python", max_level=50)),
                        level_increase=3,
                    )
                ],
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что навык добавлен пользователю
        user_skills = await self.storage.get_user_skills(user_login="test_user")
        assert len(user_skills.values) == 1
        assert user_skills.values[0].id == 1
        assert user_skills.values[0].user_level == 3

    async def test_approve_mission_with_rank_upgrade(self) -> None:
        user_with_rank = self.factory.candidate(login="test_user", exp=100, mana=50, rank_id=1)
        await self.storage.update_user(user_with_rank)
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=2, title="New Task", description="Task for new rank"
            )
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=2,
                title="New Rank Mission",
                description="Mission for new rank",
                rank_requirement=2,
                tasks=[
                    (
                        self.factory.mission_task(
                            task_id=2, title="New Task", description="Task for new rank"
                        )
                    )
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=2, task_id=2)

        # Создаем текущую миссию
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Current Mission",
                description="Current mission",
                reward_xp=200,  # Достаточно для повышения ранга
                reward_mana=100,
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем повышение ранга
        updated_user = await self.storage.get_user_by_login("test_user")
        assert updated_user.rank_id == 2  # Ранг повышен
        assert updated_user.exp == 300  # 100 + 200

        # Проверяем, что новая миссия разблокирована
        user_tasks = await self.storage.get_user_tasks(user_login="test_user")
        assert len(user_tasks) == 2  # Старая + новая задача
        assert user_tasks[0].id == 1
        assert user_tasks[1].id == 2

    async def test_approve_mission_without_rank_upgrade(self) -> None:
        await self.storage.update_user(
            user=self.factory.candidate(login="test_user", exp=100, mana=50, rank_id=1)
        )
        await self.storage.insert_rank(
            rank=self.factory.rank(rank_id=3, name="Advanced", required_xp=500)
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Small Mission",
                description="Mission with small reward",
                reward_xp=50,  # Недостаточно для повышения ранга
                reward_mana=25,
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что ранг не изменился
        updated_user = await self.storage.get_user_by_login("test_user")
        assert updated_user.rank_id == 1  # Ранг не изменился
        assert updated_user.exp == 150  # 100 + 50

    async def test_approve_mission_with_all_rewards(self) -> None:
        await self.storage.update_user(
            user=self.factory.candidate(login="test_user", exp=100, mana=50, rank_id=1)
        )
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="Test Artifact",
                description="Test",
                rarity=ArtifactRarityEnum.COMMON,
            )
        )
        await self.storage.insert_competency(
            competency=(
                self.factory.competency(
                    competency_id=1,
                    name="Programming",
                    max_level=100,
                    skills=[(self.factory.skill(skill_id=1, name="Python", max_level=50))],
                )
            )
        )
        await self.storage.insert_skill(
            skill=(self.factory.skill(skill_id=1, name="Python", max_level=50))
        )
        await self.storage.add_skill_to_competency(competency_id=1, skill_id=1)
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Full Reward Mission",
                description="Mission with all rewards",
                reward_xp=200,
                reward_mana=100,
                reward_artifacts=[
                    (
                        self.factory.artifact(
                            artifact_id=1,
                            title="Test Artifact",
                            description="Test",
                            rarity=ArtifactRarityEnum.COMMON,
                        )
                    )
                ],
                reward_competencies=[
                    self.factory.competency_reward(
                        competency=(
                            self.factory.competency(
                                competency_id=1,
                                name="Programming",
                                max_level=100,
                                skills=[
                                    (self.factory.skill(skill_id=1, name="Python", max_level=50))
                                ],
                            )
                        ),
                        level_increase=2,
                    )
                ],
                reward_skills=[
                    self.factory.skill_reward(
                        skill=(self.factory.skill(skill_id=1, name="Python", max_level=50)),
                        level_increase=1,
                    )
                ],
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем все награды
        updated_user = await self.storage.get_user_by_login("test_user")
        assert updated_user.exp == 300  # 100 + 200
        assert updated_user.mana == 150  # 50 + 100

        # Проверяем артефакт
        user_artifacts = await self.storage.get_user_artifacts(user_login="test_user")
        assert len(user_artifacts.values) == 1
        assert user_artifacts.values[0].id == 1

        # Проверяем компетенцию
        user_competencies = await self.storage.get_user_competencies(user_login="test_user")
        assert len(user_competencies.values) == 1
        assert user_competencies.values[0].id == 1
        assert user_competencies.values[0].user_level == 2

        # Проверяем навык
        user_skills = await self.storage.get_user_skills(user_login="test_user")
        assert len(user_skills.values) == 1
        assert user_skills.values[0].id == 1
        assert user_skills.values[0].user_level == 1

    async def test_approve_mission_with_empty_rewards(self) -> None:
        """Тест одобрения миссии без наград"""

        # Создаем миссию без наград
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="No Reward Mission",
                description="Mission without rewards",
                reward_xp=0,
                reward_mana=0,
                reward_artifacts=None,
                reward_competencies=None,
                reward_skills=None,
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что пользователь не изменился
        updated_user = await self.storage.get_user_by_login("test_user")
        assert updated_user.exp == 100  # без изменений
        assert updated_user.mana == 50  # без изменений

        # Проверяем, что никаких наград не добавлено
        user_artifacts = await self.storage.get_user_artifacts(user_login="test_user")
        assert len(user_artifacts.values) == 0

        user_competencies = await self.storage.get_user_competencies(user_login="test_user")
        assert len(user_competencies.values) == 0

        user_skills = await self.storage.get_user_skills(user_login="test_user")
        assert len(user_skills.values) == 0

    async def test_approve_mission_with_multiple_artifacts(self) -> None:
        artifacts = [
            self.factory.artifact(
                artifact_id=i,
                title=f"Artifact {i}",
                description=f"Description {i}",
                rarity=ArtifactRarityEnum.COMMON,
            )
            for i in range(1, 6)
        ]

        for artifact in artifacts:
            await self.storage.insert_artifact(artifact=artifact)

        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Multi Artifact Mission",
                description="Mission with multiple artifacts",
                reward_xp=100,
                reward_mana=50,
                reward_artifacts=artifacts,
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что все артефакты добавлены
        user_artifacts = await self.storage.get_user_artifacts(user_login="test_user")
        assert len(user_artifacts.values) == 5
        for i in range(5):
            assert user_artifacts.values[i].id == i + 1

    async def test_approve_mission_with_multiple_competencies(self) -> None:
        """Тест начисления нескольких компетенций"""
        competencies = [
            self.factory.competency(competency_id=i, name=f"Competency {i}", max_level=100)
            for i in range(1, 4)
        ]
        for competency in competencies:
            await self.storage.insert_competency(competency=competency)

        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Multi Competency Mission",
                description="Mission with multiple competencies",
                reward_xp=100,
                reward_mana=50,
                reward_competencies=[
                    self.factory.competency_reward(competency=comp, level_increase=2)
                    for comp in competencies
                ],
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что все компетенции добавлены
        user_competencies = await self.storage.get_user_competencies(user_login="test_user")
        assert len(user_competencies.values) == 3
        competency_ids = {comp.id for comp in user_competencies.values}
        assert competency_ids == {1, 2, 3}
        # Проверяем уровни
        for comp in user_competencies.values:
            assert comp.user_level == 2

    async def test_approve_mission_with_multiple_skills(self) -> None:
        # Создаем компетенцию и несколько навыков
        skills = [
            self.factory.skill(skill_id=i, name=f"Skill {i}", max_level=50) for i in range(1, 4)
        ]
        competency = self.factory.competency(
            competency_id=1, name="Programming", max_level=100, skills=skills
        )
        await self.storage.insert_competency(competency=competency)
        for skill in skills:
            await self.storage.insert_skill(skill=skill)
            await self.storage.add_skill_to_competency(competency_id=1, skill_id=skill.id)
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Multi Skill Mission",
                description="Mission with multiple skills",
                reward_xp=100,
                reward_mana=50,
                reward_skills=[
                    self.factory.skill_reward(skill=skill, level_increase=1) for skill in skills
                ],
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        await self.use_case.execute(mission_id=1, user_login="test_user")

        # Проверяем, что все навыки добавлены
        user_skills = await self.storage.get_user_skills(user_login="test_user")
        assert len(user_skills.values) == 3
        skill_ids = {skill.id for skill in user_skills.values}
        assert skill_ids == {1, 2, 3}
        # Проверяем уровни
        for user_skill in user_skills.values:
            assert user_skill.user_level == 1

    async def test_approve_mission_already_approved(self) -> None:
        """Тест повторного одобрения уже одобренной миссии"""

        # Создаем миссию
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(task_id=1, title="Task 1", description="First task")
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Test Mission",
                description="Test Description",
                reward_xp=200,
                reward_mana=100,
                tasks=[
                    self.factory.mission_task(task_id=1, title="Task 1", description="First task")
                ],
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)
        await self.storage.update_user_task_completion(task_id=1, user_login="test_user")

        # Первое одобрение
        await self.use_case.execute(mission_id=1, user_login="test_user")
        user_after_first = await self.storage.get_user_by_login("test_user")
        first_exp = user_after_first.exp
        first_mana = user_after_first.mana

        # Второе одобрение (должно снова начислить награды)
        await self.use_case.execute(mission_id=1, user_login="test_user")
        user_after_second = await self.storage.get_user_by_login("test_user")

        # Проверяем, что награды начислены повторно
        assert user_after_second.exp == first_exp + 200
        assert user_after_second.mana == first_mana + 100
