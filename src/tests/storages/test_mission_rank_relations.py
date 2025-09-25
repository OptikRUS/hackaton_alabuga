import pytest

from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionRankRelations(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        rank = await self.storage_helper.insert_rank(
            rank=self.factory.rank(name="TEST_RANK", required_xp=1000)
        )
        assert rank is not None
        self.inserted_rank = rank

    async def test_add_required_mission_to_rank(self) -> None:
        branch = await self.storage_helper.insert_branch(
            branch=self.factory.season(name="TEST_BRANCH")
        )
        assert branch is not None
        mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST_MISSION",
                description="TEST_DESCRIPTION",
                season_id=branch.id,
            )
        )
        assert mission is not None

        await self.storage.add_required_mission_to_rank(
            rank_id=self.inserted_rank.id,
            mission_id=mission.id,
        )

        rank_model = await self.storage_helper.get_rank_by_id_with_entities(
            rank_id=self.inserted_rank.id
        )
        rank_schema = rank_model.to_schema() if rank_model else None
        assert rank_schema is not None
        assert rank_schema.name == "TEST_RANK"
        assert rank_schema.required_xp == 1000
        assert rank_schema.required_missions == [mission.to_schema()]

    async def test_remove_required_mission_from_rank(self) -> None:
        branch = await self.storage_helper.insert_branch(
            branch=self.factory.season(name="TEST_BRANCH")
        )
        assert branch is not None
        mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST_MISSION",
                description="TEST_DESCRIPTION",
                season_id=branch.id,
            )
        )
        assert mission is not None

        await self.storage.add_required_mission_to_rank(
            rank_id=self.inserted_rank.id,
            mission_id=mission.id,
        )

        await self.storage.remove_required_mission_from_rank(
            rank_id=self.inserted_rank.id,
            mission_id=mission.id,
        )

        rank_model = await self.storage_helper.get_rank_by_id_with_entities(
            rank_id=self.inserted_rank.id
        )
        rank_schema = rank_model.to_schema() if rank_model else None
        assert rank_schema is not None
        assert rank_schema.required_missions is not None
        assert len(rank_schema.required_missions) == 0

    async def test_add_multiple_required_missions_to_rank(self) -> None:
        branch = await self.storage_helper.insert_branch(
            branch=self.factory.season(name="TEST_BRANCH")
        )
        assert branch is not None

        mission_1 = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST_MISSION_1",
                description="TEST_DESCRIPTION_1",
                season_id=branch.id,
            )
        )
        mission_2 = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST_MISSION_2",
                description="TEST_DESCRIPTION_2",
                season_id=branch.id,
            )
        )
        assert mission_1 is not None
        assert mission_2 is not None

        await self.storage.add_required_mission_to_rank(
            rank_id=self.inserted_rank.id,
            mission_id=mission_1.id,
        )
        await self.storage.add_required_mission_to_rank(
            rank_id=self.inserted_rank.id,
            mission_id=mission_2.id,
        )

        rank_model = await self.storage_helper.get_rank_by_id_with_entities(
            rank_id=self.inserted_rank.id
        )
        assert rank_model is not None
        rank_schema = rank_model.to_schema()
        assert rank_schema is not None
        assert rank_schema.required_missions is not None
        assert len(rank_schema.required_missions) == 2
        assert rank_schema.required_missions == [mission_1.to_schema(), mission_2.to_schema()]
