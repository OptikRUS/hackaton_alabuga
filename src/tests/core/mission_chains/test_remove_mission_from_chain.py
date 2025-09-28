import pytest

from src.core.mission_chains.use_cases import RemoveMissionFromChainUseCase
from src.core.missions.enums import MissionCategoryEnum
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestRemoveMissionFromChainUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = RemoveMissionFromChainUseCase(storage=self.storage)
        await self.storage.insert_season(season=self.factory.season(season_id=1, name="TEST"))
        await self.storage.insert_mission_chain(
            mission_chain=(
                self.factory.mission_chain(
                    chain_id=1,
                    name="TEST_CHAIN",
                    description="Test chain description",
                    reward_xp=200,
                    reward_mana=100,
                )
            )
        )
        await self.storage.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=1,
                    title="TEST_MISSION",
                    description="Test mission description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    season_id=1,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )
        await self.storage.add_mission_to_chain(chain_id=1, mission_id=1)

    async def test_remove_mission_from_chain(self) -> None:
        mission_chain = await self.use_case.execute(chain_id=1, mission_id=1)

        assert mission_chain.id == 1
        assert mission_chain.name == "TEST_CHAIN"
        assert mission_chain.missions is not None
        assert len(mission_chain.missions) == 0
