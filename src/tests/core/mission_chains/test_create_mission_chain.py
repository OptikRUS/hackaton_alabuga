import pytest

from src.core.mission_chains.exceptions import MissionChainNameAlreadyExistError
from src.core.mission_chains.use_cases import CreateMissionChainUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateMissionChainUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateMissionChainUseCase(storage=self.storage)

    async def test_create_mission_chain(self) -> None:
        mission_chain = await self.use_case.execute(
            mission_chain=(
                self.factory.mission_chain(
                    chain_id=0,
                    name="TEST_CHAIN",
                    description="Test chain description",
                    reward_xp=200,
                    reward_mana=100,
                )
            )
        )

        assert mission_chain == self.factory.mission_chain(
            chain_id=0,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
            missions=[],
            dependencies=[],
            mission_orders=[],
        )

    async def test_create_mission_chain_name_already_exists(self) -> None:
        await self.storage.insert_mission_chain(
            mission_chain=(
                self.factory.mission_chain(
                    chain_id=0,
                    name="TEST_CHAIN",
                    description="Test chain description",
                    reward_xp=200,
                    reward_mana=100,
                )
            )
        )

        with pytest.raises(MissionChainNameAlreadyExistError):
            await self.use_case.execute(
                mission_chain=(
                    self.factory.mission_chain(
                        chain_id=0,
                        name="TEST_CHAIN",
                        description="Test chain description",
                        reward_xp=200,
                        reward_mana=100,
                    )
                )
            )
