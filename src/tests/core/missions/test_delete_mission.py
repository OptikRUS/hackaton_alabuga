import pytest

from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError
from src.core.missions.use_cases import DeleteMissionUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestDeleteMissionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = DeleteMissionUseCase(storage=self.storage)

    async def test_delete_mission(self) -> None:
        await self.storage.insert_mission(
            mission=(
                self.factory.mission(
                    title="TEST_MISSION",
                    description="Test description",
                    reward_xp=100,
                    reward_mana=50,
                    rank_requirement=1,
                    season_id=1,
                    category=MissionCategoryEnum.QUEST,
                )
            )
        )

        mission = await self.storage.get_mission_by_title(title="TEST_MISSION")
        assert mission.title == "TEST_MISSION"

        await self.use_case.execute(mission_id=mission.id)

        with pytest.raises(MissionNotFoundError):
            await self.storage.get_mission_by_id(mission_id=1)

    async def test_delete_mission_not_found(self) -> None:
        with pytest.raises(MissionNotFoundError):
            await self.use_case.execute(mission_id=999)
