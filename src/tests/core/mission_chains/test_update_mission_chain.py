import pytest

from src.core.mission_chains.exceptions import (
    MissionChainNameAlreadyExistError,
    MissionChainNotFoundError,
)
from src.core.mission_chains.use_cases import UpdateMissionChainUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateMissionChainUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateMissionChainUseCase(storage=self.storage)

    async def test_update_mission_chain(self) -> None:
        await self.storage.insert_mission_chain(
            mission_chain=(
                self.factory.mission_chain(
                    chain_id=1,
                    name="OLD_CHAIN",
                    description="Old description",
                    reward_xp=100,
                    reward_mana=50,
                )
            )
        )

        mission_chain = await self.use_case.execute(
            mission_chain=(
                self.factory.mission_chain(
                    chain_id=1,
                    name="NEW_CHAIN",
                    description="New description",
                    reward_xp=200,
                    reward_mana=100,
                )
            )
        )

        assert mission_chain == self.factory.mission_chain(
            chain_id=1,
            name="NEW_CHAIN",
            description="New description",
            reward_xp=200,
            reward_mana=100,
            missions=[],
            dependencies=[],
        )

    async def test_update_mission_chain_name_already_exists(self) -> None:
        await self.storage.insert_mission_chain(
            mission_chain=(
                self.factory.mission_chain(
                    chain_id=1,
                    name="EXISTING_CHAIN",
                    description="Existing description",
                    reward_xp=100,
                    reward_mana=50,
                )
            )
        )
        await self.storage.insert_mission_chain(
            mission_chain=(
                self.factory.mission_chain(
                    chain_id=2,
                    name="ANOTHER_CHAIN",
                    description="Another description",
                    reward_xp=200,
                    reward_mana=100,
                )
            )
        )

        with pytest.raises(MissionChainNameAlreadyExistError):
            await self.use_case.execute(
                mission_chain=(
                    self.factory.mission_chain(
                        chain_id=2,
                        name="EXISTING_CHAIN",
                        description="Updated description",
                        reward_xp=300,
                        reward_mana=150,
                    )
                )
            )

    async def test_update_mission_chain_not_found(self) -> None:
        with pytest.raises(MissionChainNotFoundError):
            await self.use_case.execute(
                mission_chain=(
                    self.factory.mission_chain(
                        chain_id=999,
                        name="NONEXISTENT_CHAIN",
                        description="Description",
                        reward_xp=100,
                        reward_mana=50,
                    )
                )
            )
