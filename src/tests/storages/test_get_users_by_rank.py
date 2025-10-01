import pytest

from src.core.artifacts.enums import ArtifactRarityEnum
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestGetUsersByRank(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage_helper.insert_rank(self.factory.rank(name="Bronze", required_xp=100))
        await self.storage_helper.insert_rank(self.factory.rank(name="Silver", required_xp=200))
        await self.storage_helper.insert_rank(self.factory.rank(name="Gold", required_xp=300))
        bronze_rank = await self.storage_helper.get_rank_by_name(name="Bronze")
        silver_rank = await self.storage_helper.get_rank_by_name(name="Silver")
        gold_rank = await self.storage_helper.get_rank_by_name(name="Gold")
        assert bronze_rank is not None
        assert silver_rank is not None
        assert gold_rank is not None
        self.bronze_rank = bronze_rank
        self.silver_rank = silver_rank
        self.gold_rank = gold_rank

    async def test_get_users_by_existing_rank(self) -> None:
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="user1",
                first_name="John",
                last_name="Doe",
                rank_id=self.bronze_rank.id,
            )
        )
        await self.storage_helper.insert_user(
            user=self.factory.user(
                login="user2",
                first_name="Jane",
                last_name="Smith",
                rank_id=self.bronze_rank.id,
            )
        )

        users = await self.storage.get_users_by_rank(rank_id=self.bronze_rank.id)

        assert len(users) == 2
        assert users[0].login in ["user1", "user2"]
        assert users[1].login in ["user1", "user2"]
        assert users[0].rank_id == self.bronze_rank.id
        assert users[1].rank_id == self.bronze_rank.id

    async def test_get_users_by_rank_empty_result(self) -> None:
        users = await self.storage.get_users_by_rank(rank_id=self.gold_rank.id)

        assert users == []

    async def test_get_users_by_different_ranks(self) -> None:
        await self.storage_helper.insert_user(
            self.factory.user(
                login="bronze_user",
                first_name="Bronze",
                last_name="User",
                rank_id=self.bronze_rank.id,
            )
        )
        await self.storage_helper.insert_user(
            self.factory.user(
                login="silver_user",
                first_name="Silver",
                last_name="User",
                rank_id=self.silver_rank.id,
            )
        )
        await self.storage_helper.insert_user(
            self.factory.user(
                login="gold_user",
                first_name="Gold",
                last_name="User",
                rank_id=self.gold_rank.id,
            )
        )

        bronze_users = await self.storage.get_users_by_rank(rank_id=self.bronze_rank.id)
        silver_users = await self.storage.get_users_by_rank(rank_id=self.silver_rank.id)
        gold_users = await self.storage.get_users_by_rank(rank_id=self.gold_rank.id)

        assert len(bronze_users) == 1
        assert bronze_users[0].login == "bronze_user"
        assert bronze_users[0].rank_id == self.bronze_rank.id

        assert len(silver_users) == 1
        assert silver_users[0].login == "silver_user"
        assert silver_users[0].rank_id == self.silver_rank.id

        assert len(gold_users) == 1
        assert gold_users[0].login == "gold_user"
        assert gold_users[0].rank_id == self.gold_rank.id

    async def test_get_users_by_rank_with_relations(self) -> None:
        artifact = await self.storage_helper.insert_artifact(
            self.factory.artifact(
                title="Test Artifact",
                description="Test Description",
                rarity=ArtifactRarityEnum.RARE,
                image_url="https://example.com/artifact.jpg",
            )
        )
        assert artifact is not None
        await self.storage_helper.insert_competency(
            competency=self.factory.competency(name="Python", max_level=5)
        )
        competency = await self.storage_helper.get_competency_by_name(name="Python")
        assert competency is not None
        await self.storage_helper.insert_skill(self.factory.skill(name="Programming", max_level=10))
        skill = await self.storage_helper.get_skill_by_name(name="Programming")
        assert skill is not None
        await self.storage_helper.insert_user(
            self.factory.user(
                login="user_with_relations",
                first_name="Test",
                last_name="User",
                rank_id=self.bronze_rank.id,
            )
        )
        await self.storage_helper.add_artifact_to_user(
            user_login="user_with_relations",
            artifact_id=artifact.id,
        )
        await self.storage_helper.add_competency_to_user(
            user_login="user_with_relations",
            competency_id=competency.id,
            level=3,
        )
        await self.storage_helper.add_skill_to_user(
            user_login="user_with_relations",
            skill_id=skill.id,
            competency_id=competency.id,
            level=5,
        )

        users = await self.storage.get_users_by_rank(rank_id=self.bronze_rank.id)

        assert len(users) == 1
        user = users[0]
        assert user.login == "user_with_relations"
        assert user.rank_id == self.bronze_rank.id
        assert user.artifacts is not None
        assert len(user.artifacts) == 1
        assert user.artifacts[0].id == artifact.id
        assert user.artifacts[0].title == "Test Artifact"
        assert user.competencies is not None
        assert len(user.competencies) == 1
        assert user.competencies[0].id == competency.id
        assert user.competencies[0].name == "Python"
        assert user.skills is not None
        assert len(user.skills) == 1
        assert user.skills[0].id == skill.id
        assert user.skills[0].name == "Programming"

    async def test_get_users_by_rank_multiple_users_same_rank(self) -> None:
        users_data = [
            ("user1", "Alice", "Johnson"),
            ("user2", "Bob", "Brown"),
            ("user3", "Charlie", "Davis"),
        ]
        for login, first_name, last_name in users_data:
            await self.storage_helper.insert_user(
                user=self.factory.user(
                    login=login,
                    first_name=first_name,
                    last_name=last_name,
                    rank_id=self.silver_rank.id,
                )
            )

        users = await self.storage.get_users_by_rank(rank_id=self.silver_rank.id)

        assert len(users) == 3
        for user in users:
            assert user.rank_id == self.silver_rank.id

        logins = [user.login for user in users]
        assert len(logins) == 3
        assert users[0].login == "user1"
        assert users[1].login == "user2"
        assert users[2].login == "user3"

    async def test_get_users_by_nonexistent_rank_id(self) -> None:
        nonexistent_rank_id = 99999
        users = await self.storage.get_users_by_rank(rank_id=nonexistent_rank_id)

        assert users == []
