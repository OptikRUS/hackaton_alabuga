import pytest

from src.core.competencies.exceptions import CompetencyNotFoundError
from src.core.competencies.use_cases import GetCompetencyDetailUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetCompetenciesDetailUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetCompetencyDetailUseCase(storage=self.storage)

    async def test_get_competency_detail(self) -> None:
        await self.storage.insert_competency(
            competency=self.factory.competency(competency_id=1, name="ML", max_level=100)
        )

        competency = await self.use_case.execute(competency_id=1)

        assert competency == self.factory.competency(competency_id=1, name="ML", max_level=100)

    async def test_get_competency_not_found(self) -> None:
        with pytest.raises(CompetencyNotFoundError):
            await self.use_case.execute(competency_id=999)
