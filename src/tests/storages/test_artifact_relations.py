import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestArtifactRelations(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        branch = await self.storage_helper.insert_branch(
            branch=self.factory.mission_branch(name="TEST")
        )
        assert branch is not None
        mission = await self.storage_helper.insert_mission(
            mission=self.factory.mission(
                title="TEST",
                description="TEST",
                branch_id=branch.id,
            )
        )
        assert mission is not None
        self.inserted_mission = mission.to_schema()

    async def test_add_artifact_to_mission(self) -> None:
        artifact = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="TEST",
            )
        )
        assert artifact is not None
        await self.storage.add_artifact_to_mission(
            mission_id=self.inserted_mission.id,
            artifact_id=artifact.id,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        mission = mission_model.to_schema() if mission_model else None

        assert mission is not None
        assert mission.title == "TEST"
        assert mission.description == "TEST"
        assert mission.reward_artifacts == [artifact.to_schema()]

    async def test_remove_artifact_from_mission(self) -> None:
        artifact = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="TEST",
            )
        )
        assert artifact is not None
        await self.storage.add_artifact_to_mission(
            mission_id=self.inserted_mission.id,
            artifact_id=artifact.id,
        )

        await self.storage.remove_artifact_from_mission(
            mission_id=self.inserted_mission.id,
            artifact_id=artifact.id,
        )

        mission_model = await self.storage_helper.get_mission_by_id_with_entities(
            mission_id=self.inserted_mission.id
        )
        mission = mission_model.to_schema() if mission_model else None
        assert mission is not None
        assert mission.reward_artifacts is not None
        assert len(mission.reward_artifacts) == 0

    async def test_add_artifact_to_user(self) -> None:
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="TEST",
                password="password",
                first_name="TEST",
                last_name="TEST",
            )
        )
        artifact_1 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="TEST",
            )
        )
        artifact_2 = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST2",
                description="TEST2",
                rarity=ArtifactRarityEnum.RARE,
                image_url="TEST2",
            )
        )
        assert artifact_1 is not None
        assert artifact_2 is not None

        await self.storage.add_artifact_to_user(user_login="TEST", artifact_id=artifact_1.id)
        await self.storage.add_artifact_to_user(user_login="TEST", artifact_id=artifact_2.id)

        user = await self.storage_helper.get_user_by_login(login="TEST")
        assert user is not None
        assert user.login == "TEST"
        assert len(user.artifacts) == 2
        assert user.artifacts == [artifact_1, artifact_2]

    async def test_remove_artifact_from_user(self) -> None:
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="TEST",
                password="password",
                first_name="TEST",
                last_name="TEST",
            )
        )
        artifact = await self.storage_helper.insert_artifact(
            artifact=self.factory.artifact(
                title="TEST",
                description="TEST",
                rarity=ArtifactRarityEnum.COMMON,
                image_url="TEST",
            )
        )
        assert artifact is not None
        await self.storage.add_artifact_to_user(user_login="TEST", artifact_id=artifact.id)

        await self.storage.remove_artifact_from_user(user_login="TEST", artifact_id=artifact.id)

        user = await self.storage_helper.get_user_by_login(login="TEST")
        assert user is not None
        assert user.login == "TEST"
        assert len(user.artifacts) == 0
