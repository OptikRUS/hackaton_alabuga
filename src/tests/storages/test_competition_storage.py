import pytest

from src.core.competitions.exceptions import (
    CompetitionNameAlreadyExistError,
    CompetitionNotFoundError,
)
from src.storages.database_storage import DatabaseStorage
from src.tests.fixtures import FactoryFixture, StorageFixture


class TestCompetitionStorage(FactoryFixture, StorageFixture):
    @pytest.fixture(autouse=True)
    async def setup(self, storage: DatabaseStorage) -> None:
        self.storage = storage
        await self.storage.insert_competition(self.factory.competition(name="ML", max_level=100))
        self.created = await self.storage.get_competition_by_name(name="ML")

    async def test_get_competition_by_id(self) -> None:
        competition = await self.storage.get_competition_by_id(competition_id=self.created.id)
        assert competition == self.factory.competition(
            competition_id=self.created.id, name="ML", max_level=100, skills=[]
        )

    async def test_get_competition_by_name(self) -> None:
        competition = await self.storage.get_competition_by_name(name="ML")
        assert competition == self.factory.competition(
            competition_id=self.created.id, name="ML", max_level=100, skills=[]
        )

    async def test_insert_competition(self) -> None:
        await self.storage.insert_competition(self.factory.competition(name="Web", max_level=50))
        competition = await self.storage.get_competition_by_name(name="Web")
        assert competition.name == "Web"
        assert competition.max_level == 50

    async def test_insert_competition_with_duplicate_name(self) -> None:
        with pytest.raises(CompetitionNameAlreadyExistError):
            await self.storage.insert_competition(
                self.factory.competition(name="ML", max_level=110)
            )

    async def test_list_competitions(self) -> None:
        await self.storage.insert_competition(self.factory.competition(name="Web", max_level=50))
        competitions = await self.storage.list_competitions()
        assert len(competitions.values) >= 2

    async def test_update_competition(self) -> None:
        await self.storage.update_competition(
            self.factory.competition(
                competition_id=self.created.id, name="ML Advanced", max_level=150
            )
        )
        updated = await self.storage.get_competition_by_id(competition_id=self.created.id)
        assert updated.name == "ML Advanced"
        assert updated.max_level == 150

    async def test_update_competition_with_duplicate_name(self) -> None:
        await self.storage.insert_competition(self.factory.competition(name="Web", max_level=50))
        web = await self.storage.get_competition_by_name(name="Web")
        with pytest.raises(CompetitionNameAlreadyExistError):
            await self.storage.update_competition(
                self.factory.competition(competition_id=web.id, name="ML", max_level=60)
            )

    async def test_delete_competition(self) -> None:
        await self.storage.delete_competition(competition_id=self.created.id)
        with pytest.raises(CompetitionNotFoundError):
            await self.storage.get_competition_by_id(competition_id=self.created.id)

    async def test_get_competition_not_found_by_id(self) -> None:
        with pytest.raises(CompetitionNotFoundError):
            await self.storage.get_competition_by_id(competition_id=999)

    async def test_get_competition_not_found_by_name(self) -> None:
        with pytest.raises(CompetitionNotFoundError):
            await self.storage.get_competition_by_name(name="NONEXISTENT")

    async def test_update_competition_not_found(self) -> None:
        with pytest.raises(CompetitionNotFoundError):
            await self.storage.update_competition(
                self.factory.competition(competition_id=999, name="Unknown", max_level=10)
            )

    async def test_delete_competition_not_found(self) -> None:
        with pytest.raises(CompetitionNotFoundError):
            await self.storage.delete_competition(competition_id=999)
