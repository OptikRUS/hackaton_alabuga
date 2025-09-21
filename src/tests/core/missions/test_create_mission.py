import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionBranchNotFoundError, MissionNameAlreadyExistError
from src.core.missions.use_cases import CreateMissionUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestCreateMissionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = CreateMissionUseCase(storage=self.storage)
        await self.storage.insert_mission_branch(
            branch=self.factory.mission_branch(branch_id=1, name="TEST")
        )

    async def test_create_mission(self) -> None:
        mission = await self.use_case.execute(
            mission=(
                self.factory.mission(
                    mission_id=0,
                    title="TEST_MISSION",
                    description="Test description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    branch_id=1,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        assert mission == self.factory.mission(
            mission_id=0,
            title="TEST_MISSION",
            description="Test description",
            reward_xp=100,
            reward_mana=50,
            rank_requirement=1,
            branch_id=1,
            category=MissionCategoryEnum.QUEST,
        )

    async def test_create_mission_name_already_exist(self) -> None:
        await self.storage.insert_mission(
            mission=(
                self.factory.mission(
                    mission_id=0,
                    title="TEST_MISSION",
                    description="Test description",
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
                        mission_id=0,
                        title="TEST_MISSION",
                        description="Test description",
                        reward_xp=100,
                        reward_mana=50,
                        rank_requirement=1,
                        branch_id=1,
                        category=MissionCategoryEnum.QUEST,
                    )
                )
            )

    async def test_create_mission_branch_not_found(self) -> None:
        with pytest.raises(MissionBranchNotFoundError):
            await self.use_case.execute(
                mission=(
                    self.factory.mission(
                        mission_id=0,
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
