import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNameAlreadyExistError, MissionNotFoundError
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage_helper.insert_season(season=self.factory.season(name="TEST"))
        inserted_branch = await self.storage_helper.get_branch_by_name(name="TEST")
        assert inserted_branch is not None
        self.created_branch = inserted_branch.to_schema()

    async def test_get_mission_by_id(self) -> None:
        inserted_mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST",
                description="Test description",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        assert inserted_mission is not None

        mission = await self.storage.get_mission_by_id(mission_id=inserted_mission.id)

        assert mission is not None
        assert mission.title == "TEST"
        assert mission.description == "Test description"
        assert mission.reward_xp == 100
        assert mission.reward_mana == 50
        assert mission.rank_requirement == 1
        assert mission.season_id == self.created_branch.id
        assert mission.category == MissionCategoryEnum.QUEST

    async def test_get_mission_by_id_with_tasks(self) -> None:
        inserted_mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        task_1 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST1", description="TEST1")
        )
        task_2 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST2", description="TEST2")
        )
        assert inserted_mission is not None
        assert task_1 is not None
        assert task_2 is not None
        await self.storage.add_task_to_mission(mission_id=inserted_mission.id, task_id=task_1.id)
        await self.storage.add_task_to_mission(mission_id=inserted_mission.id, task_id=task_2.id)

        mission = await self.storage.get_mission_by_id(mission_id=inserted_mission.id)

        assert mission is not None
        assert mission == self.factory.mission(
            mission_id=inserted_mission.id,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.created_branch.id,
            category=MissionCategoryEnum.QUEST,
            tasks=[task_1.to_schema(), task_2.to_schema()],
            reward_artifacts=[],
            reward_competencies=[],
            reward_skills=[],
        )

    async def test_get_mission_by_id_with_artifacts(self) -> None:
        inserted_mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        artifact_1 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="TEST",
            )
        )
        artifact_2 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST2",
                description="TEST2",
                rarity=ArtifactRarityEnum.RARE,
                image_url="TEST2",
            )
        )
        assert inserted_mission is not None
        assert artifact_1 is not None
        assert artifact_2 is not None
        await self.storage.add_artifact_to_mission(
            mission_id=inserted_mission.id,
            artifact_id=artifact_1.id,
        )
        await self.storage.add_artifact_to_mission(
            mission_id=inserted_mission.id,
            artifact_id=artifact_2.id,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=inserted_mission.id
        )
        mission = mission_model.to_schema() if mission_model else None

        assert mission is not None
        assert mission == self.factory.mission(
            mission_id=inserted_mission.id,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.created_branch.id,
            category=MissionCategoryEnum.QUEST,
            tasks=[],
            reward_artifacts=[artifact_1.to_schema(), artifact_2.to_schema()],
            reward_competencies=[],
            reward_skills=[],
        )

    async def test_get_mission_by_id_with_entities(self) -> None:
        inserted_mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        task_1 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST1", description="TEST1")
        )
        task_2 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST2", description="TEST2")
        )
        artifact_1 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="TEST",
            )
        )
        artifact_2 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST2",
                description="TEST2",
                rarity=ArtifactRarityEnum.RARE,
                image_url="TEST2",
            )
        )
        assert inserted_mission is not None
        assert task_1 is not None
        assert task_2 is not None
        assert artifact_1 is not None
        assert artifact_2 is not None
        await self.storage.add_task_to_mission(mission_id=inserted_mission.id, task_id=task_1.id)
        await self.storage.add_task_to_mission(mission_id=inserted_mission.id, task_id=task_2.id)
        await self.storage.add_artifact_to_mission(
            mission_id=inserted_mission.id,
            artifact_id=artifact_1.id,
        )
        await self.storage.add_artifact_to_mission(
            mission_id=inserted_mission.id,
            artifact_id=artifact_2.id,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=inserted_mission.id
        )
        mission = mission_model.to_schema() if mission_model else None

        assert mission is not None
        assert mission == self.factory.mission(
            mission_id=inserted_mission.id,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.created_branch.id,
            category=MissionCategoryEnum.QUEST,
            tasks=[task_1.to_schema(), task_2.to_schema()],
            reward_artifacts=[artifact_1.to_schema(), artifact_2.to_schema()],
            reward_competencies=[],
            reward_skills=[],
        )

    async def test_get_mission_by_id_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.storage.get_mission_by_id(mission_id=999)

    async def test_get_mission_by_title(self) -> None:
        await self.storage_helper.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=0,
                    title="TEST",
                    description="Test description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    season_id=self.created_branch.id,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        mission = await self.storage.get_mission_by_title(title="TEST")

        assert mission is not None
        assert mission.title == "TEST"
        assert mission.description == "Test description"
        assert mission.reward_xp == 100
        assert mission.reward_mana == 50
        assert mission.rank_requirement == 1
        assert mission.season_id == self.created_branch.id
        assert mission.category == MissionCategoryEnum.QUEST

    async def test_get_mission_by_title_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.storage.get_mission_by_title(title="NON_EXISTENT")

    async def test_insert_mission(self) -> None:
        await self.storage.insert_mission(
            mission=(
                self.factory.mission(
                    title="TEST_MISSION",
                    description="Test description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    season_id=self.created_branch.id,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        result = await self.storage_helper.get_mission_by_title(title="TEST_MISSION")
        assert result is not None
        assert result.title == "TEST_MISSION"
        assert result.description == "Test description"
        assert result.reward_xp == 100
        assert result.reward_mana == 50
        assert result.rank_requirement == 1
        assert result.branch_id == self.created_branch.id
        assert result.category == MissionCategoryEnum.QUEST

    async def test_insert_mission_already_exists(self) -> None:
        mission = self.factory.mission(
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.created_branch.id,
            category=MissionCategoryEnum.QUEST,
        )
        await self.storage_helper.insert_mission(mission=mission)

        with pytest.raises(MissionNameAlreadyExistError):
            await self.storage.insert_mission(mission=mission)

    async def test_list_missions(self) -> None:
        await self.storage_helper.insert_mission(
            mission=(
                self.factory.mission(
                    title="TEST1",
                    description="Description 1",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    season_id=self.created_branch.id,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )
        await self.storage_helper.insert_mission(
            mission=(
                self.factory.mission(
                    title="TEST2",
                    description="Description 2",
                    reward_xp=200,
                    reward_mana=100,
                    rank_requirement=2,
                    season_id=self.created_branch.id,
                    category=MissionCategoryEnum.LECTURE,
                )
            )
        )

        missions = await self.storage.list_missions()

        assert len(missions.values) == 2
        missions.values[0].title = "TEST1"
        missions.values[0].description = "Description 1"
        missions.values[0].reward_xp = 100
        missions.values[0].reward_mana = 50
        missions.values[0].rank_requirement = 1
        missions.values[0].season_id = self.created_branch.id
        missions.values[0].category = MissionCategoryEnum.QUEST
        missions.values[1].title = "TEST2"
        missions.values[1].description = "Description 2"
        missions.values[1].reward_xp = 200
        missions.values[1].reward_mana = 100
        missions.values[1].rank_requirement = 2
        missions.values[1].season_id = self.created_branch.id
        missions.values[1].category = MissionCategoryEnum.LECTURE

    async def test_list_empty_missions(self) -> None:
        result = await self.storage.list_missions()

        assert len(result.values) == 0

    async def test_update_mission(self) -> None:
        await self.storage_helper.insert_mission(
            mission=(
                self.factory.mission(
                    title="TEST1",
                    description="Original description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    season_id=self.created_branch.id,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        stored_mission = await self.storage_helper.get_mission_by_title(title="TEST1")
        assert stored_mission is not None

        await self.storage.update_mission(
            mission=(
                self.factory.mission(
                    mission_id=stored_mission.id,
                    title="TEST2",
                    description="Updated description",
                    reward_xp=150,
                    reward_mana=75,
                    rank_requirement=2,
                    season_id=self.created_branch.id,
                    category=MissionCategoryEnum.LECTURE,
                )
            )
        )

        mission = await self.storage_helper.get_mission_by_id(mission_id=stored_mission.id)
        assert mission is not None
        assert mission.title == "TEST2"
        assert mission.description == "Updated description"
        assert mission.reward_xp == 150
        assert mission.reward_mana == 75
        assert mission.rank_requirement == 2
        assert mission.branch_id == self.created_branch.id
        assert mission.category == MissionCategoryEnum.LECTURE

    async def test_delete_mission(self) -> None:
        await self.storage_helper.insert_mission(
            mission=(
                self.factory.mission(
                    title="TEST",
                    description="Test description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    season_id=self.created_branch.id,
                    category=MissionCategoryEnum.LECTURE,
                )
            )
        )
        stored_mission = await self.storage_helper.get_mission_by_title(title="TEST")
        assert stored_mission is not None

        await self.storage.delete_mission(mission_id=stored_mission.id)

        with pytest.raises(MissionNotFoundError):
            await self.storage.get_mission_by_id(mission_id=stored_mission.id)

    async def test_delete_mission_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.storage.delete_mission(mission_id=999)

    async def test_get_missions_by_rank(self) -> None:
        rank_1 = await self.storage_helper.insert_rank(
            rank=self.factory.rank(name="Bronze", required_xp=100)
        )
        rank_2 = await self.storage_helper.insert_rank(
            rank=self.factory.rank(name="Silver", required_xp=200)
        )
        assert rank_1 is not None
        assert rank_2 is not None
        mission_1 = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="Bronze Mission 1",
                description="Bronze mission description",
                reward_xp=50,
                reward_mana=25,
                rank_requirement=rank_1.id,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        mission_2 = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="Bronze Mission 2",
                description="Another bronze mission",
                reward_xp=75,
                reward_mana=30,
                rank_requirement=rank_1.id,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.LECTURE,
            )
        )
        mission_3 = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="Silver Mission",
                description="Silver mission description",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=rank_2.id,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        assert mission_1 is not None
        assert mission_2 is not None
        assert mission_3 is not None

        # Получаем миссии для первого ранга
        bronze_missions = await self.storage.get_missions_by_rank(rank_id=rank_1.id)

        assert len(bronze_missions.values) == 2
        assert bronze_missions.values[0].title == "Bronze Mission 1"
        assert bronze_missions.values[0].description == "Bronze mission description"
        assert bronze_missions.values[0].reward_xp == 50
        assert bronze_missions.values[0].reward_mana == 25
        assert bronze_missions.values[0].rank_requirement == rank_1.id
        assert bronze_missions.values[0].season_id == self.created_branch.id
        assert bronze_missions.values[0].category == MissionCategoryEnum.QUEST
        assert bronze_missions.values[1].title == "Bronze Mission 2"
        assert bronze_missions.values[1].description == "Another bronze mission"
        assert bronze_missions.values[1].reward_xp == 75
        assert bronze_missions.values[1].reward_mana == 30
        assert bronze_missions.values[1].rank_requirement == rank_1.id
        assert bronze_missions.values[1].season_id == self.created_branch.id
        assert bronze_missions.values[1].category == MissionCategoryEnum.LECTURE

        silver_missions = await self.storage.get_missions_by_rank(rank_id=rank_2.id)

        assert len(silver_missions.values) == 1
        assert silver_missions.values[0].title == "Silver Mission"
        assert silver_missions.values[0].description == "Silver mission description"
        assert silver_missions.values[0].reward_xp == 100
        assert silver_missions.values[0].reward_mana == 50
        assert silver_missions.values[0].rank_requirement == rank_2.id
        assert silver_missions.values[0].season_id == self.created_branch.id
        assert silver_missions.values[0].category == MissionCategoryEnum.QUEST

    async def test_get_missions_by_rank_empty_result(self) -> None:
        rank = await self.storage_helper.insert_rank(
            rank=self.factory.rank(name="Gold", required_xp=500)
        )
        assert rank is not None

        missions = await self.storage.get_missions_by_rank(rank_id=rank.id)

        assert len(missions.values) == 0

    async def test_get_missions_by_rank_with_entities(self) -> None:
        rank = await self.storage_helper.insert_rank(
            rank=self.factory.rank(name="Test Rank", required_xp=100)
        )
        assert rank is not None
        mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="Test Mission",
                description="Test mission with entities",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=rank.id,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        assert mission is not None
        task_1 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="Task 1", description="First task")
        )
        task_2 = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="Task 2", description="Second task")
        )
        assert task_1 is not None
        assert task_2 is not None
        artifact_1 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="Artifact 1",
                description="First artifact",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="test1.jpg",
            )
        )
        artifact_2 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="Artifact 2",
                description="Second artifact",
                rarity=ArtifactRarityEnum.RARE,
                image_url="test2.jpg",
            )
        )
        assert artifact_1 is not None
        assert artifact_2 is not None
        await self.storage.add_task_to_mission(mission_id=mission.id, task_id=task_1.id)
        await self.storage.add_task_to_mission(mission_id=mission.id, task_id=task_2.id)
        await self.storage.add_artifact_to_mission(mission_id=mission.id, artifact_id=artifact_1.id)
        await self.storage.add_artifact_to_mission(mission_id=mission.id, artifact_id=artifact_2.id)
        mission_by_id = await self.storage.get_mission_by_id(mission_id=mission.id)
        assert mission_by_id.tasks is not None
        assert mission_by_id.reward_artifacts is not None
        assert len(mission_by_id.tasks) == 2
        assert len(mission_by_id.reward_artifacts) == 2

        missions = await self.storage.get_missions_by_rank(rank_id=rank.id)

        assert len(missions.values) == 1
        retrieved_mission = missions.values[0]
        assert retrieved_mission.title == "Test Mission"
        assert retrieved_mission.description == "Test mission with entities"
        assert retrieved_mission.reward_xp == 100
        assert retrieved_mission.reward_mana == 50
        assert retrieved_mission.rank_requirement == rank.id
        assert retrieved_mission.season_id == self.created_branch.id
        assert retrieved_mission.category == MissionCategoryEnum.QUEST
        assert retrieved_mission.tasks is not None
        assert retrieved_mission.reward_artifacts is not None
        assert len(retrieved_mission.tasks) == 2
        assert retrieved_mission.tasks[0].title == "Task 1"
        assert retrieved_mission.tasks[0].description == "First task"
        assert retrieved_mission.tasks[1].title == "Task 2"
        assert retrieved_mission.tasks[1].description == "Second task"
        assert len(retrieved_mission.reward_artifacts) == 2
        assert retrieved_mission.reward_artifacts[0].title == "Artifact 1"
        assert retrieved_mission.reward_artifacts[0].description == "First artifact"
        assert retrieved_mission.reward_artifacts[0].rarity == ArtifactRarityEnum.COMMON
        assert retrieved_mission.reward_artifacts[0].image_url == "test1.jpg"
        assert retrieved_mission.reward_artifacts[1].title == "Artifact 2"
        assert retrieved_mission.reward_artifacts[1].description == "Second artifact"
        assert retrieved_mission.reward_artifacts[1].rarity == ArtifactRarityEnum.RARE
        assert retrieved_mission.reward_artifacts[1].image_url == "test2.jpg"

    async def test_get_missions_by_rank_different_ranks_filtering(self) -> None:
        rank_1 = await self.storage_helper.insert_rank(
            rank=self.factory.rank(name="Novice", required_xp=0)
        )
        rank_2 = await self.storage_helper.insert_rank(
            rank=self.factory.rank(name="Apprentice", required_xp=100)
        )
        rank_3 = await self.storage_helper.insert_rank(
            rank=self.factory.rank(name="Expert", required_xp=500)
        )
        assert rank_1 is not None
        assert rank_2 is not None
        assert rank_3 is not None
        novice_mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="Novice Mission",
                description="For beginners",
                reward_xp=25,
                reward_mana=10,
                rank_requirement=rank_1.id,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        apprentice_mission_1 = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="Apprentice Mission 1",
                description="For apprentices",
                reward_xp=50,
                reward_mana=20,
                rank_requirement=rank_2.id,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.LECTURE,
            )
        )
        apprentice_mission_2 = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="Apprentice Mission 2",
                description="Another apprentice mission",
                reward_xp=75,
                reward_mana=30,
                rank_requirement=rank_2.id,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        expert_mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="Expert Mission",
                description="For experts only",
                reward_xp=200,
                reward_mana=100,
                rank_requirement=rank_3.id,
                season_id=self.created_branch.id,
                category=MissionCategoryEnum.QUEST,
            )
        )
        assert novice_mission is not None
        assert apprentice_mission_1 is not None
        assert apprentice_mission_2 is not None
        assert expert_mission is not None
        novice_missions = await self.storage.get_missions_by_rank(rank_id=rank_1.id)
        assert len(novice_missions.values) == 1
        assert novice_missions.values[0].title == "Novice Mission"

        apprentice_missions = await self.storage.get_missions_by_rank(rank_id=rank_2.id)

        assert len(apprentice_missions.values) == 2
        assert apprentice_missions.values[0].title == "Apprentice Mission 1"
        assert apprentice_missions.values[0].description == "For apprentices"
        assert apprentice_missions.values[0].reward_xp == 50
        assert apprentice_missions.values[0].reward_mana == 20
        assert apprentice_missions.values[0].rank_requirement == rank_2.id
        assert apprentice_missions.values[0].season_id == self.created_branch.id
        assert apprentice_missions.values[0].category == MissionCategoryEnum.LECTURE
        assert apprentice_missions.values[1].title == "Apprentice Mission 2"
        assert apprentice_missions.values[1].description == "Another apprentice mission"
        assert apprentice_missions.values[1].reward_xp == 75
        assert apprentice_missions.values[1].reward_mana == 30
        assert apprentice_missions.values[1].rank_requirement == rank_2.id
        assert apprentice_missions.values[1].season_id == self.created_branch.id
        assert apprentice_missions.values[1].category == MissionCategoryEnum.QUEST

        expert_missions = await self.storage.get_missions_by_rank(rank_id=rank_3.id)

        assert len(expert_missions.values) == 1
        assert expert_missions.values[0].title == "Expert Mission"
        assert expert_missions.values[0].description == "For experts only"
        assert expert_missions.values[0].reward_xp == 200
        assert expert_missions.values[0].reward_mana == 100
        assert expert_missions.values[0].rank_requirement == rank_3.id
        assert expert_missions.values[0].season_id == self.created_branch.id
        assert expert_missions.values[0].category == MissionCategoryEnum.QUEST
        novice_titles = [mission.title for mission in novice_missions.values]
        apprentice_titles = [mission.title for mission in apprentice_missions.values]
        expert_titles = [mission.title for mission in expert_missions.values]
        for novice_title in novice_titles:
            assert novice_title not in apprentice_titles
        for novice_title in novice_titles:
            assert novice_title not in expert_titles
        for apprentice_title in apprentice_titles:
            assert apprentice_title not in expert_titles
