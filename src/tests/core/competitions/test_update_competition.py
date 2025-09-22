import pytest

from src.core.competitions.exceptions import (
    CompetitionNameAlreadyExistError,
    CompetitionNotFoundError,
)
from src.core.competitions.use_cases import UpdateCompetitionUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateCompetitionUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateCompetitionUseCase(storage=self.storage)

    async def test_update_competition(self) -> None:
        await self.storage.insert_competition(
            self.factory.competition(competition_id=1, name="ML", max_level=100)
        )

        updated = await self.use_case.execute(
            competition=self.factory.competition(
                competition_id=1, name="ML Advanced", max_level=150
            )
        )

        assert updated == self.factory.competition(
            competition_id=1, name="ML Advanced", max_level=150
        )

    async def test_update_competition_name_already_exist(self) -> None:
        await self.storage.insert_competition(
            self.factory.competition(competition_id=1, name="ML", max_level=100)
        )
        await self.storage.insert_competition(
            self.factory.competition(competition_id=2, name="Web", max_level=50)
        )

        with pytest.raises(CompetitionNameAlreadyExistError):
            await self.use_case.execute(
                competition=self.factory.competition(competition_id=2, name="ML", max_level=60)
            )

    async def test_update_competition_not_found(self) -> None:
        with pytest.raises(CompetitionNotFoundError):
            await self.use_case.execute(
                competition=self.factory.competition(
                    competition_id=999, name="Unknown", max_level=10
                )
            )
