import pytest

from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionTaskRelations(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        branch = await self.storage_helper.insert_season(season=self.factory.season(name="TEST"))
        assert branch is not None
        mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                season_id=branch.id,
            )
        )
        assert mission is not None
        self.inserted_mission = mission

    async def test_add_task_to_mission(self) -> None:
        task = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST_TASK", description="TEST_DESCRIPTION")
        )
        assert task is not None

        await self.storage.add_task_to_mission(mission_id=self.inserted_mission.id, task_id=task.id)

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        mission = mission_model.to_schema() if mission_model else None
        assert mission is not None
        assert mission.title == "TEST"
        assert mission.description == "TEST"
        assert mission.tasks is not None
        assert len(mission.tasks) == 1
        assert mission.tasks == [task.to_schema()]

    async def test_remove_task_from_mission(self) -> None:
        task = await self.storage_helper.insert_task(
            task=self.factory.mission_task(title="TEST_TASK", description="TEST_DESCRIPTION")
        )
        assert task is not None
        await self.storage.add_task_to_mission(mission_id=self.inserted_mission.id, task_id=task.id)

        await self.storage.remove_task_from_mission(
            mission_id=self.inserted_mission.id,
            task_id=task.id,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        mission = mission_model.to_schema() if mission_model else None
        assert mission is not None
        assert mission.tasks is not None
        assert len(mission.tasks) == 0
