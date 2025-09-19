from collections.abc import AsyncGenerator, Generator
from copy import copy

import jwt as pyjwt
import pytest
import pytest_asyncio
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import Headers
from sqlalchemy import NullPool, delete
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from src.api.app import create_app
from src.api.auth.schemas import JwtUser
from src.config.settings import settings
from src.core.users.enums import UserRoleEnum
from src.migrations.commands import downgrade, migrate
from src.storages.database import async_session
from src.storages.database_storage import DatabaseStorage
from src.storages.models import MissionBranchModel, UserModel
from src.tests.mocks.providers import AuthProviderMock, MissionProviderMock, UserProviderMock


@pytest.fixture
async def container() -> AsyncGenerator[AsyncContainer]:
    container = make_async_container(
        FastapiProvider(),
        UserProviderMock(),
        MissionProviderMock(),
        AuthProviderMock(),
    )
    yield container
    await container.close()


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture(scope="session")
def jwt_user() -> JwtUser:
    return JwtUser(login="test_user", role=UserRoleEnum.CANDIDATE)


@pytest.fixture(scope="session")
def auth_token(jwt_user: JwtUser) -> str:
    token = pyjwt.encode(
        jwt_user.model_dump(),
        key=settings.AUTH.PRIVATE_KEY.get_secret_value(),
        algorithm=settings.AUTH.ALGORITHM,
    )
    return f"Bearer {token}"


@pytest.fixture
def no_auth_client(app: FastAPI, container: AsyncContainer) -> Generator[TestClient]:
    setup_dishka(container, app)
    with TestClient(app) as no_auth_client:
        yield no_auth_client


@pytest.fixture
def client(no_auth_client: TestClient, auth_token: str) -> Generator[TestClient]:
    client = copy(no_auth_client)
    client.headers = Headers({"Authorization": auth_token, "Content-Type": "application/json"})
    yield client
    client.headers = Headers()


@pytest.fixture(scope="session", autouse=True)
def setup_migrations() -> Generator[None]:
    migrate("heads", settings.DATABASE.URL.get_secret_value())
    yield
    downgrade("base", settings.DATABASE.URL.get_secret_value())


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(settings.DATABASE.URL.get_secret_value(), poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest.fixture
async def clear_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.execute(delete(UserModel))
        await conn.execute(delete(MissionBranchModel))


@pytest.fixture
async def session(engine: AsyncEngine, clear_tables: None) -> AsyncGenerator:
    _ = clear_tables
    async with async_session(bind=engine) as db:
        yield db
        await db.commit()


@pytest.fixture
def storage(session: AsyncSession) -> DatabaseStorage:
    return DatabaseStorage(session=session)
