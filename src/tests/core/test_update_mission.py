import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionBranchNotFoundError, MissionNameAlreadyExistError
from src.core.missions.use_cases import UpdateMissionUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateMissionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateMissionUseCase(storage=self.storage)
        await self.storage.insert_mission_branch(
            branch=self.factory.mission_branch(branch_id=1, name="TEST")
        )

    async def test_update_mission(self) -> None:
        await self.storage.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=1,
                    title="ORIGINAL_MISSION",
                    description="Original description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    branch_id=1,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        updated_mission = await self.use_case.execute(
            mission=(
                self.factory.mission(
                    mission_id=1,
                    title="UPDATED_MISSION",
                    description="Updated description",
                    reward_xp=150,
                    reward_mana=75,
                    rank_requirement=2,
                    branch_id=1,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        assert updated_mission == self.factory.mission(
            mission_id=1,
            title="UPDATED_MISSION",
            description="Updated description",
            reward_xp=150,
            reward_mana=75,
            rank_requirement=2,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
            tasks=[],
        )

    async def test_update_mission_title_already_exist(self) -> None:
        await self.storage.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=2,
                    title="EXISTING_MISSION",
                    description="Existing description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    branch_id=1,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        with pytest.raises(MissionNameAlreadyExistError):
            await self.use_case.execute(
                mission=(
                    self.factory.mission(
                        mission_id=1,
                        title="EXISTING_MISSION",  # Same title as existing
                        description="Updated description",
                        reward_xp=150,
                        reward_mana=75,
                        rank_requirement=2,
                        branch_id=1,
                        category=MissionCategoryEnum.QUEST,
                    )
                )
            )

    async def test_update_mission_branch_not_found(self) -> None:
        with pytest.raises(MissionBranchNotFoundError):
            await self.use_case.execute(
                mission=(
                    self.factory.mission(
                        mission_id=1,
                        title="TEST_MISSION",
                        description="Test description",
                        reward_xp=100,
                        reward_mana=50,
                        rank_requirement=1,
                        branch_id=999,
                        category=MissionCategoryEnum.QUEST,
                    )
                )
            )
