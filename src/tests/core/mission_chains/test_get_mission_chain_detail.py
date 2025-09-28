import pytest

from src.core.mission_chains.exceptions import MissionChainNotFoundError
from src.core.mission_chains.use_cases import GetMissionChainDetailUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetMissionChainDetailUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetMissionChainDetailUseCase(storage=self.storage)

    async def test_get_mission_chain_detail(self) -> None:
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

        mission_chain = await self.use_case.execute(chain_id=1)

        assert mission_chain == self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
            missions=[],
            dependencies=[],
            mission_orders=[],
        )

    async def test_get_mission_chain_detail_not_found(self) -> None:
        with pytest.raises(MissionChainNotFoundError):
            await self.use_case.execute(chain_id=999)
