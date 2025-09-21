import pytest

from src.core.competencies.use_cases import GetCompetenciesUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestGetCompetenciesUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = GetCompetenciesUseCase(storage=self.storage)

    async def test_get_competencies(self) -> None:
        await self.storage.insert_competency(
            self.factory.competency(competency_id=1, name="ML", max_level=100)
        )
        await self.storage.insert_competency(
            self.factory.competency(competency_id=2, name="Web", max_level=50)
        )

        competencies = await self.use_case.execute()

        assert len(competencies.values) == 2
        assert competencies.values[0] == self.factory.competency(
            competency_id=1, name="ML", max_level=100
        )
        assert competencies.values[1] == self.factory.competency(
            competency_id=2, name="Web", max_level=50
        )

    # TODO: добавить тест на пустой результат
