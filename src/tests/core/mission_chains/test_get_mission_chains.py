import pytest

from src.core.mission_chains.use_cases import GetMissionChainsUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetMissionChainsUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetMissionChainsUseCase(storage=self.storage)

    async def test_get_mission_chains(self) -> None:
        await self.storage.insert_mission_chain(
            mission_chain=(
                self.factory.mission_chain(
                    chain_id=1,
                    name="CHAIN_1",
                    description="Description 1",
                    reward_xp=200,
                    reward_mana=100,
                )
            )
        )
        await self.storage.insert_mission_chain(
            mission_chain=(
                self.factory.mission_chain(
                    chain_id=2,
                    name="CHAIN_2",
                    description="Description 2",
                    reward_xp=300,
                    reward_mana=150,
                )
            )
        )

        mission_chains = await self.use_case.execute()

        assert len(mission_chains.values) == 2
        assert mission_chains == self.factory.mission_chains(
            values=[
                self.factory.mission_chain(
                    chain_id=1,
                    name="CHAIN_1",
                    description="Description 1",
                    reward_xp=200,
                    reward_mana=100,
                ),
                self.factory.mission_chain(
                    chain_id=2,
                    name="CHAIN_2",
                    description="Description 2",
                    reward_xp=300,
                    reward_mana=150,
                ),
            ]
        )

    async def test_get_empty_mission_chains(self) -> None:
        result = await self.use_case.execute()
        assert len(result.values) == 0
