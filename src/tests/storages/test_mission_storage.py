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
        await self.storage_helper.insert_branch(branch=self.factory.mission_branch(name="TEST"))
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
                branch_id=self.created_branch.id,
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
        assert mission.branch_id == self.created_branch.id
        assert mission.category == MissionCategoryEnum.QUEST

    async def test_get_mission_by_id_with_tasks(self) -> None:
        inserted_mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                rank_requirement=1,
                branch_id=self.created_branch.id,
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
            branch_id=self.created_branch.id,
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
                branch_id=self.created_branch.id,
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
            branch_id=self.created_branch.id,
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
                branch_id=self.created_branch.id,
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
            branch_id=self.created_branch.id,
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
                    branch_id=self.created_branch.id,
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
        assert mission.branch_id == self.created_branch.id
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
                    branch_id=self.created_branch.id,
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

    async def test_insert_mission_already_exist(self) -> None:
        mission = self.factory.mission(
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=self.created_branch.id,
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
                    branch_id=self.created_branch.id,
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
                    branch_id=self.created_branch.id,
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
        missions.values[0].branch_id = self.created_branch.id
        missions.values[0].category = MissionCategoryEnum.QUEST
        missions.values[1].title = "TEST2"
        missions.values[1].description = "Description 2"
        missions.values[1].reward_xp = 200
        missions.values[1].reward_mana = 100
        missions.values[1].rank_requirement = 2
        missions.values[1].branch_id = self.created_branch.id
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
                    branch_id=self.created_branch.id,
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
                    branch_id=self.created_branch.id,
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
                    branch_id=self.created_branch.id,
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
