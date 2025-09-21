import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.core.artifacts.exceptions import ArtifactNotFoundError
from src.core.artifacts.use_cases import RemoveArtifactFromMissionUseCase
from src.core.missions.enums import MissionCategoryEnum
from src.core.missions.exceptions import MissionNotFoundError
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestRemoveArtifactFromMissionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = RemoveArtifactFromMissionUseCase(
            storage=self.storage, mission_storage=self.storage
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="TEST",
                description="TEST",
                reward_xp=100,
                reward_mana=50,
                category=MissionCategoryEnum.QUEST,
            )
        )
        await self.storage.insert_artifact(
            artifact=self.factory.artifact(
                artifact_id=1,
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="https://example.com/image.jpg",
            )
        )

    async def test_execute_success(self):
        result = await self.use_case.execute(mission_id=1, artifact_id=1)

        assert result == self.factory.mission(
            mission_id=1,
            title="TEST",
            description="TEST",
            reward_xp=100,
            reward_mana=50,
            category=MissionCategoryEnum.QUEST,
            tasks=[],
        )

    async def test_execute_mission_not_found(self):
        with pytest.raises(MissionNotFoundError):
            await self.use_case.execute(mission_id=999, artifact_id=1)

    async def test_execute_artifact_not_found(self):
        with pytest.raises(ArtifactNotFoundError):
            await self.use_case.execute(mission_id=1, artifact_id=999)
