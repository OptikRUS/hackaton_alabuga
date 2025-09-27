import pytest
from httpx import codes

from src.core.exceptions import PermissionDeniedError
from src.core.mission_chains.exceptions import InvalidMissionOrderError
from src.core.mission_chains.use_cases import UpdateMissionOrderInChainUseCase
from src.tests.fixtures import APIFixture, ContainerFixture, FactoryFixture


class TestUpdateMissionOrderInChainAPI(APIFixture, FactoryFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.use_case = await self.container.override_use_case(UpdateMissionOrderInChainUseCase)

    def test_not_auth(self) -> None:
        response = self.api.update_mission_order_in_chain(chain_id=1, mission_id=1, new_order=2)

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": "Not authenticated"}

    def test_candidate_forbidden(self) -> None:
        response = self.candidate_api.update_mission_order_in_chain(
            chain_id=1, mission_id=1, new_order=2
        )

        assert response.status_code == codes.FORBIDDEN
        assert response.json() == {"detail": PermissionDeniedError.detail}

    def test_update_mission_order_success(self) -> None:
        """Тест успешного обновления порядка миссии"""
        # Настраиваем мок для возврата правильного объекта
        self.use_case.execute.return_value = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain description",
            reward_xp=200,
            reward_mana=100,
        )

        response = self.hr_api.update_mission_order_in_chain(chain_id=1, mission_id=1, new_order=2)

        assert response.status_code == codes.OK
        # Проверяем, что возвращается обновленная цепочка миссий
        assert "id" in response.json()
        assert "missionOrders" in response.json()
        # Проверяем, что use case был вызван s pravilnymi параметрами
        self.use_case.execute.assert_called_once()
        self.use_case.execute.assert_awaited_once_with(chain_id=1, mission_id=1, new_order=2)

    def test_update_mission_order_invalid_order(self) -> None:
        """Тест валидации неверного порядка через API"""
        # Настраиваем мок для выброса исключения
        self.use_case.execute.side_effect = InvalidMissionOrderError

        response = self.hr_api.update_mission_order_in_chain(chain_id=1, mission_id=1, new_order=0)

        assert response.status_code == codes.BAD_REQUEST
        assert response.json() == {"detail": InvalidMissionOrderError.detail}
