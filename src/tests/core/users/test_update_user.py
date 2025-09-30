import pytest

from src.core.users.exceptions import UserNotFoundError
from src.core.users.use_cases import UpdateUserUseCase
from src.tests.fixtures import FactoryFixture
from src.tests.mocks.storage_stub import StorageMock
from src.tests.mocks.user_password import UserPasswordServiceMock


class TestUpdateUserUseCase(FactoryFixture):
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.storage = StorageMock()
        self.password_service = UserPasswordServiceMock()
        self.use_case = UpdateUserUseCase(
            storage=self.storage,
            password_service=self.password_service,
        )

    async def test_update_user_success(self) -> None:
        original_user = self.factory.user(
            login="TEST",
            password="old_password",
            first_name="OldName",
            last_name="OldLastName",
            rank_id=1,
            exp=100,
            mana=50,
        )

        await self.storage.insert_user(user=original_user)

        updated_user = self.factory.user(
            login="TEST",
            password="new_password",
            first_name="NewName",
            last_name="NewLastName",
            rank_id=2,
            exp=200,
            mana=100,
        )

        await self.use_case.execute(user=updated_user)

        updated_user_from_storage = await self.storage.get_user_by_login(login="TEST")
        assert updated_user_from_storage.first_name == "NewName"
        assert updated_user_from_storage.last_name == "NewLastName"
        assert updated_user_from_storage.rank_id == 2
        assert updated_user_from_storage.exp == 200
        assert updated_user_from_storage.mana == 100

    async def test_update_user_not_found(self) -> None:
        updated_user = self.factory.user(
            login="NONEXISTENT",
            password="new_password",
            first_name="NewName",
            last_name="NewLastName",
        )

        with pytest.raises(UserNotFoundError):
            await self.use_case.execute(user=updated_user)

    async def test_update_user_without_password_change(self) -> None:
        original_user = self.factory.user(
            login="TEST",
            password="original_password",
            first_name="OriginalName",
            last_name="OriginalLastName",
            rank_id=1,
            exp=100,
            mana=50,
        )

        await self.storage.insert_user(user=original_user)

        updated_user = self.factory.user(
            login="TEST",
            password="original_password",
            first_name="NewName",
            last_name="NewLastName",
            rank_id=2,
            exp=200,
            mana=100,
        )

        await self.use_case.execute(user=updated_user)

        updated_user_from_storage = await self.storage.get_user_by_login(login="TEST")
        assert updated_user_from_storage.first_name == "NewName"
        assert updated_user_from_storage.last_name == "NewLastName"
        assert updated_user_from_storage.rank_id == 2
        assert updated_user_from_storage.exp == 200
        assert updated_user_from_storage.mana == 100

    async def test_update_user_partial_update(self) -> None:
        original_user = self.factory.user(
            login="TEST",
            password="original_password",
            first_name="OriginalName",
            last_name="OriginalLastName",
            rank_id=1,
            exp=100,
            mana=50,
        )

        await self.storage.insert_user(user=original_user)

        updated_user = self.factory.user(
            login="TEST",
            password="original_password",
            first_name="NewName",
            last_name="OriginalLastName",
            rank_id=1,
            exp=100,
            mana=50,
        )

        await self.use_case.execute(user=updated_user)

        updated_user_from_storage = await self.storage.get_user_by_login(login="TEST")
        assert updated_user_from_storage.first_name == "NewName"
        assert updated_user_from_storage.last_name == "OriginalLastName"
        assert updated_user_from_storage.rank_id == 1
        assert updated_user_from_storage.exp == 100
        assert updated_user_from_storage.mana == 50
