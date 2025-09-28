import pytest

from src.core.mission_chains.exceptions import (
    MissionChainNameAlreadyExistError,
    MissionChainNotFoundError,
)
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestMissionChainStorage(StorageFixture, FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage_helper.insert_season(season=self.factory.season(name="TEST"))
        inserted_branch = await self.storage_helper.get_branch_by_name(name="TEST")
        assert inserted_branch is not None
        self.created_branch = inserted_branch.to_schema()

    async def test_insert_mission_chain(self) -> None:
        mission_chain = self.factory.mission_chain(
            chain_id=0,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        await self.storage.insert_mission_chain(mission_chain=mission_chain)

        result = await self.storage.get_mission_chain_by_name(name="TEST_CHAIN")
        assert result.name == "TEST_CHAIN"
        assert result.description == "Test chain description"
        assert result.reward_xp == 200
        assert result.reward_mana == 100

    async def test_get_mission_chain_by_name(self) -> None:
        mission_chain = self.factory.mission_chain(
            chain_id=0,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        await self.storage.insert_mission_chain(mission_chain=mission_chain)

        result = await self.storage.get_mission_chain_by_name(name="TEST_CHAIN")
        assert result.name == "TEST_CHAIN"
        assert result.description == "Test chain description"
        assert result.reward_xp == 200
        assert result.reward_mana == 100

    async def test_get_mission_chain_by_name_not_found(self) -> None:
        with pytest.raises(MissionChainNotFoundError):
            await self.storage.get_mission_chain_by_name(name="NONEXISTENT_CHAIN")

    async def test_get_mission_chain_by_id(self) -> None:
        mission_chain = self.factory.mission_chain(
            chain_id=0,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        await self.storage.insert_mission_chain(mission_chain=mission_chain)
        inserted_chain = await self.storage.get_mission_chain_by_name(name="TEST_CHAIN")

        result = await self.storage.get_mission_chain_by_id(chain_id=inserted_chain.id)
        assert result.id == inserted_chain.id
        assert result.name == "TEST_CHAIN"
        assert result.description == "Test chain description"
        assert result.reward_xp == 200
        assert result.reward_mana == 100

    async def test_get_mission_chain_by_id_not_found(self) -> None:
        with pytest.raises(MissionChainNotFoundError):
            await self.storage.get_mission_chain_by_id(chain_id=999)

    async def test_list_mission_chains(self) -> None:
        chain1 = self.factory.mission_chain(
            chain_id=0,
            name="CHAIN_1",
            description="Description 1",
            reward_xp=200,
            reward_mana=100,
        )
        chain2 = self.factory.mission_chain(
            chain_id=0,
            name="CHAIN_2",
            description="Description 2",
            reward_xp=300,
            reward_mana=150,
        )

        await self.storage.insert_mission_chain(mission_chain=chain1)
        await self.storage.insert_mission_chain(mission_chain=chain2)

        result = await self.storage.list_mission_chains()
        assert len(result.values) == 2
        assert any(chain.name == "CHAIN_1" for chain in result.values)
        assert any(chain.name == "CHAIN_2" for chain in result.values)

    async def test_list_empty_mission_chains(self) -> None:
        result = await self.storage.list_mission_chains()
        assert len(result.values) == 0

    async def test_update_mission_chain(self) -> None:
        mission_chain = self.factory.mission_chain(
            chain_id=0,
            name="OLD_CHAIN",
            description="Old description",
            reward_xp=100,
            reward_mana=50,
        )

        await self.storage.insert_mission_chain(mission_chain=mission_chain)
        inserted_chain = await self.storage.get_mission_chain_by_name(name="OLD_CHAIN")

        updated_chain = self.factory.mission_chain(
            chain_id=inserted_chain.id,
            name="NEW_CHAIN",
            description="New description",
            reward_xp=200,
            reward_mana=100,
        )

        await self.storage.update_mission_chain(mission_chain=updated_chain)

        result = await self.storage.get_mission_chain_by_id(chain_id=inserted_chain.id)
        assert result.name == "NEW_CHAIN"
        assert result.description == "New description"
        assert result.reward_xp == 200
        assert result.reward_mana == 100

    async def test_update_mission_chain_name_already_exists(self) -> None:
        chain1 = self.factory.mission_chain(
            chain_id=0,
            name="CHAIN_1",
            description="Description 1",
            reward_xp=200,
            reward_mana=100,
        )
        chain2 = self.factory.mission_chain(
            chain_id=0,
            name="CHAIN_2",
            description="Description 2",
            reward_xp=300,
            reward_mana=150,
        )

        await self.storage.insert_mission_chain(mission_chain=chain1)
        await self.storage.insert_mission_chain(mission_chain=chain2)

        inserted_chain2 = await self.storage.get_mission_chain_by_name(name="CHAIN_2")

        updated_chain = self.factory.mission_chain(
            chain_id=inserted_chain2.id,
            name="CHAIN_1",  # Trying to use existing name
            description="Updated description",
            reward_xp=400,
            reward_mana=200,
        )

        with pytest.raises(MissionChainNameAlreadyExistError):
            await self.storage.update_mission_chain(mission_chain=updated_chain)

    async def test_delete_mission_chain(self) -> None:
        mission_chain = self.factory.mission_chain(
            chain_id=0,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        await self.storage.insert_mission_chain(mission_chain=mission_chain)
        inserted_chain = await self.storage.get_mission_chain_by_name(name="TEST_CHAIN")

        await self.storage.delete_mission_chain(chain_id=inserted_chain.id)

        with pytest.raises(MissionChainNotFoundError):
            await self.storage.get_mission_chain_by_id(chain_id=inserted_chain.id)

    async def test_delete_mission_chain_not_found(self) -> None:
        with pytest.raises(MissionChainNotFoundError):
            await self.storage.delete_mission_chain(chain_id=999)

    async def test_add_mission_to_chain(self) -> None:
        mission_chain = self.factory.mission_chain(
            chain_id=0,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )
        mission = self.factory.mission(
            mission_id=0,
            title="TEST_MISSION",
            description="Test mission description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.created_branch.id,
        )

        await self.storage.insert_mission_chain(mission_chain=mission_chain)
        await self.storage.insert_mission(mission=mission)

        inserted_chain = await self.storage.get_mission_chain_by_name(name="TEST_CHAIN")
        inserted_mission = await self.storage.get_mission_by_title(title="TEST_MISSION")

        await self.storage.add_mission_to_chain(
            chain_id=inserted_chain.id, mission_id=inserted_mission.id
        )

        result = await self.storage.get_mission_chain_by_id(chain_id=inserted_chain.id)
        assert result.missions is not None
        assert len(result.missions) == 1
        assert result.missions[0].id == inserted_mission.id
        assert result.missions[0].title == "TEST_MISSION"

    async def test_remove_mission_from_chain(self) -> None:
        mission_chain = self.factory.mission_chain(
            chain_id=0,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )
        mission = self.factory.mission(
            mission_id=0,
            title="TEST_MISSION",
            description="Test mission description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.created_branch.id,
        )

        await self.storage.insert_mission_chain(mission_chain=mission_chain)
        await self.storage.insert_mission(mission=mission)

        inserted_chain = await self.storage.get_mission_chain_by_name(name="TEST_CHAIN")
        inserted_mission = await self.storage.get_mission_by_title(title="TEST_MISSION")

        await self.storage.add_mission_to_chain(
            chain_id=inserted_chain.id, mission_id=inserted_mission.id
        )

        await self.storage.remove_mission_from_chain(
            chain_id=inserted_chain.id, mission_id=inserted_mission.id
        )

        result = await self.storage.get_mission_chain_by_id(chain_id=inserted_chain.id)
        assert result.missions is not None
        assert len(result.missions) == 0

    async def test_add_mission_dependency(self) -> None:
        mission_chain = self.factory.mission_chain(
            chain_id=0,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )
        mission1 = self.factory.mission(
            mission_id=0,
            title="MISSION_1",
            description="First mission",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.created_branch.id,
        )
        mission2 = self.factory.mission(
            mission_id=0,
            title="MISSION_2",
            description="Second mission",
            reward_xp=150,
            reward_mana=75,
            rank_requirement=2,
            season_id=self.created_branch.id,
        )

        await self.storage.insert_mission_chain(mission_chain=mission_chain)
        await self.storage.insert_mission(mission=mission1)
        await self.storage.insert_mission(mission=mission2)

        inserted_chain = await self.storage.get_mission_chain_by_name(name="TEST_CHAIN")
        inserted_mission1 = await self.storage.get_mission_by_title(title="MISSION_1")
        inserted_mission2 = await self.storage.get_mission_by_title(title="MISSION_2")

        await self.storage.add_mission_dependency(
            chain_id=inserted_chain.id,
            mission_id=inserted_mission2.id,
            prerequisite_mission_id=inserted_mission1.id,
        )

        result = await self.storage.get_mission_chain_by_id(chain_id=inserted_chain.id)
        assert result.dependencies is not None
        assert len(result.dependencies) == 1
        assert result.dependencies[0].mission_id == inserted_mission2.id
        assert result.dependencies[0].prerequisite_mission_id == inserted_mission1.id

    async def test_remove_mission_dependency(self) -> None:
        mission_chain = self.factory.mission_chain(
            chain_id=0,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )
        mission1 = self.factory.mission(
            mission_id=0,
            title="MISSION_1",
            description="First mission",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            season_id=self.created_branch.id,
        )
        mission2 = self.factory.mission(
            mission_id=0,
            title="MISSION_2",
            description="Second mission",
            reward_xp=150,
            reward_mana=75,
            rank_requirement=2,
            season_id=self.created_branch.id,
        )

        await self.storage.insert_mission_chain(mission_chain=mission_chain)
        await self.storage.insert_mission(mission=mission1)
        await self.storage.insert_mission(mission=mission2)

        inserted_chain = await self.storage.get_mission_chain_by_name(name="TEST_CHAIN")
        inserted_mission1 = await self.storage.get_mission_by_title(title="MISSION_1")
        inserted_mission2 = await self.storage.get_mission_by_title(title="MISSION_2")

        await self.storage.add_mission_dependency(
            chain_id=inserted_chain.id,
            mission_id=inserted_mission2.id,
            prerequisite_mission_id=inserted_mission1.id,
        )

        await self.storage.remove_mission_dependency(
            chain_id=inserted_chain.id,
            mission_id=inserted_mission2.id,
            prerequisite_mission_id=inserted_mission1.id,
        )

        result = await self.storage.get_mission_chain_by_id(chain_id=inserted_chain.id)
        assert result.dependencies is not None
        assert len(result.dependencies) == 0
