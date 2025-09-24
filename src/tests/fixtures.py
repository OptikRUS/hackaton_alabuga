import pytest
from dishka import AsyncContainer
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from src.tests.helpers.api import APIHelper
from src.tests.helpers.app import ContainerHelper
from src.tests.helpers.factory import FactoryHelper
from src.tests.helpers.storage import StorageHelper


class APIFixture:
    api: APIHelper
    hr_api: APIHelper
    candidate_api: APIHelper

    @pytest.fixture(autouse=True)
    def _api_setup(
        self,
        app: FastAPI,
        no_auth_client: TestClient,
        hr_client: TestClient,
        candidate_client: TestClient,
    ) -> None:
        self.hr_api = APIHelper(client=hr_client)
        self.candidate_api = APIHelper(client=candidate_client)
        self.api = APIHelper(client=no_auth_client)


class FactoryFixture:
    factory: FactoryHelper

    @pytest.fixture(autouse=True)
    def fixture_setup_factory(self) -> None:
        self.factory = FactoryHelper()


class ContainerFixture:
    container: ContainerHelper

    @pytest.fixture(autouse=True)
    def _setup_app(self, container: AsyncContainer) -> None:
        self.container = ContainerHelper(container=container)


class StorageFixture:
    storage_helper: StorageHelper

    @pytest.fixture(autouse=True)
    def _storage_setup(self, session: AsyncSession) -> None:
        self.storage_helper = StorageHelper(session=session)
