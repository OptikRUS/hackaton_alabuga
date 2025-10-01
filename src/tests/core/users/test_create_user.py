import pytest

from src.core.users.exceptions import UserAlreadyExistError
from src.core.users.use_cases import CreateUserUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock
from src.tests.mocks.user_password import UserPasswordServiceMock


class TestCreateUserUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.password_service = UserPasswordServiceMock()
        self.use_case = CreateUserUseCase(
            user_storage=self.storage,
            rank_storage=self.storage,
            mission_storage=self.storage,
            password_service=self.password_service,
        )

    async def test_create_user(self) -> None:
        await self.storage.insert_rank(
            rank=self.factory.rank(rank_id=1, name="Test Rank", required_xp=0)
        )
        await self.use_case.execute(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        created_user = await self.storage.get_user_by_login(login="TEST")
        assert created_user.login == "TEST"
        assert created_user.first_name == "TEST"
        assert created_user.last_name == "TEST"
        assert created_user.password == "TEST"  # noqa: S105
        assert created_user.rank_id == 1  # Должен получить первый ранг (0 XP)
        assert created_user.exp == 0
        assert created_user.mana == 0

    async def test_create_user_with_rank_assignment(self) -> None:
        await self.storage.insert_rank(
            rank=self.factory.rank(rank_id=1, name="Junior", required_xp=0)
        )
        await self.storage.insert_rank(
            rank=self.factory.rank(rank_id=2, name="Middle", required_xp=100)
        )
        await self.storage.insert_rank(
            rank=self.factory.rank(rank_id=3, name="Senior", required_xp=500)
        )

        await self.use_case.execute(
            user=self.factory.user(
                login="TEST_MIDDLE",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
                exp=150,
            )
        )

        created_user = await self.storage.get_user_by_login(login="TEST_MIDDLE")
        assert created_user.rank_id == 2  # Middle ранг (100 XP)
        assert created_user.exp == 150

    async def test_create_user_with_mission_assignment(self) -> None:
        await self.storage.insert_rank(
            rank=self.factory.rank(rank_id=1, name="Test Rank", required_xp=0)
        )
        await self.storage.insert_mission(
            mission=self.factory.mission(
                mission_id=1,
                title="Test Mission",
                description="Test Description",
                rank_requirement=1,
            )
        )
        await self.storage.insert_mission_task(
            task=self.factory.mission_task(
                task_id=1,
                title="Test Task",
                description="Test Task Description",
            )
        )
        await self.storage.add_task_to_mission(mission_id=1, task_id=1)

        await self.use_case.execute(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        user_tasks = await self.storage.get_user_tasks(user_login="TEST")
        assert len(user_tasks) == 1
        assert user_tasks[0].id == 1
        assert user_tasks[0].title == "Test Task"
        assert user_tasks[0].description == "Test Task Description"
        assert user_tasks[0].is_completed is False

    async def test_create_user_already_exists(self) -> None:
        await self.storage.insert_user(
            user=self.factory.user(
                login="TEST",
                password="TEST",
                first_name="TEST",
                last_name="TEST",
            )
        )

        with pytest.raises(UserAlreadyExistError):
            await self.use_case.execute(
                user=self.factory.user(
                    login="TEST",
                    password="TEST",
                    first_name="TEST",
                    last_name="TEST",
                )
            )
