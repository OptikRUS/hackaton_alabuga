import pytest

from src.core.mission_chains.exceptions import MissionChainNotFoundError
from src.core.mission_chains.use_cases import DeleteMissionChainUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestDeleteMissionChainUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = DeleteMissionChainUseCase(storage=self.storage)

    async def test_delete_mission_chain(self) -> None:
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

        await self.use_case.execute(chain_id=1)
        # Test passes if no exception is raised

    async def test_delete_mission_chain_not_found(self) -> None:
        with pytest.raises(MissionChainNotFoundError):
            await self.use_case.execute(chain_id=999)
