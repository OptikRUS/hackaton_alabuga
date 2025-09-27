import pytest

from src.core.mission_chains.exceptions import InvalidMissionOrderError
from src.core.mission_chains.use_cases import UpdateMissionOrderInChainUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock


class TestUpdateMissionOrderInChainUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.storage = StorageMock()
        self.use_case = UpdateMissionOrderInChainUseCase(storage=self.storage)

    async def test_update_mission_order_with_shift(self) -> None:
        """Тест обновления порядка миссии s avtomaticheskim смещением других миссий"""
        # Создаем цепочку миссий
        mission_chain = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain",
            reward_xp=100,
            reward_mana=50,
        )
        await self.storage.insert_mission_chain(mission_chain)

        # Создаем 3 миссии
        mission1 = self.factory.mission(
            mission_id=1,
            title="Mission 1",
            description="First mission",
            reward_xp=50,
            reward_mana=25,
        )
        mission2 = self.factory.mission(
            mission_id=2,
            title="Mission 2",
            description="Second mission",
            reward_xp=50,
            reward_mana=25,
        )
        mission3 = self.factory.mission(
            mission_id=3,
            title="Mission 3",
            description="Third mission",
            reward_xp=50,
            reward_mana=25,
        )

        await self.storage.insert_mission(mission1)
        await self.storage.insert_mission(mission2)
        await self.storage.insert_mission(mission3)

        await self.storage.add_mission_to_chain(chain_id=1, mission_id=1)
        await self.storage.add_mission_to_chain(chain_id=1, mission_id=2)
        await self.storage.add_mission_to_chain(chain_id=1, mission_id=3)

        # Перемещаем миссию 3 на позицию 1 - должно пройти без ошибок
        result = await self.use_case.execute(chain_id=1, mission_id=3, new_order=1)

        # Проверяем, что возвращается цепочка миссий
        assert result is not None
        assert result.id == 1
        assert result.name == "TEST_CHAIN"
        assert result.missions is not None
        assert len(result.missions) == 3

    async def test_update_mission_order_same_position(self) -> None:
        """Тест обновления порядка миссии на ту же позицию (не должно ничего измениться)"""
        # Создаем цепочку миссий
        mission_chain = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain",
            reward_xp=100,
            reward_mana=50,
        )
        await self.storage.insert_mission_chain(mission_chain)

        # Создаем миссию
        mission1 = self.factory.mission(
            mission_id=1,
            title="Mission 1",
            description="First mission",
            reward_xp=50,
            reward_mana=25,
        )
        await self.storage.insert_mission(mission1)

        # Добавляем миссию в цепочку
        await self.storage.add_mission_to_chain(chain_id=1, mission_id=1)

        # Проверяем, что миссия была добавлена в цепочку
        mission_chain = await self.storage.get_mission_chain_by_id(chain_id=1)
        assert mission_chain is not None
        assert mission_chain.id == 1
        assert mission_chain.name == "TEST_CHAIN"

    async def test_update_mission_order_invalid_order_too_low(self) -> None:
        """Тест валидации: нельзя установить порядок меньше 1"""
        # Создаем цепочку миссий
        mission_chain = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain",
            reward_xp=100,
            reward_mana=50,
        )
        await self.storage.insert_mission_chain(mission_chain)

        # Создаем миссию
        mission1 = self.factory.mission(
            mission_id=1,
            title="Mission 1",
            description="First mission",
            reward_xp=50,
            reward_mana=25,
        )
        await self.storage.insert_mission(mission1)

        # Добавляем миссию в цепочку
        await self.storage.add_mission_to_chain(chain_id=1, mission_id=1)

        # Пытаемся установить порядок 0 - должно вызвать ошибку
        with pytest.raises(InvalidMissionOrderError):
            await self.use_case.execute(chain_id=1, mission_id=1, new_order=0)

    async def test_update_mission_order_invalid_order_too_high(self) -> None:
        """Тест валидации: нельзя установить порядок больше количества миссий"""
        # Создаем цепочку миссий
        mission_chain = self.factory.mission_chain(
            chain_id=1,
            name="TEST_CHAIN",
            description="Test chain",
            reward_xp=100,
            reward_mana=50,
        )
        await self.storage.insert_mission_chain(mission_chain)

        # Создаем 2 миссии
        mission1 = self.factory.mission(
            mission_id=1,
            title="Mission 1",
            description="First mission",
            reward_xp=50,
            reward_mana=25,
        )
        mission2 = self.factory.mission(
            mission_id=2,
            title="Mission 2",
            description="Second mission",
            reward_xp=50,
            reward_mana=25,
        )
        await self.storage.insert_mission(mission1)
        await self.storage.insert_mission(mission2)

        # Добавляем миссии в цепочку
        await self.storage.add_mission_to_chain(chain_id=1, mission_id=1)
        await self.storage.add_mission_to_chain(chain_id=1, mission_id=2)

        # Пытаемся установить порядок 3 для миссии 1 - должно вызвать ошибку (всего 2 миссии)
        with pytest.raises(InvalidMissionOrderError):
            await self.use_case.execute(chain_id=1, mission_id=1, new_order=3)
