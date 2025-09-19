from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.app import create_app
from src.config.settings import settings
from src.migrations.commands import migrate


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield
    await app.state.dishka_container.close()


def start_service() -> None:
    migrate(revision="heads", db_url=settings.DATABASE.URL.get_secret_value())
    uvicorn.run(
        app=create_app(lifespan=lifespan),
        host=settings.APP.ADDRESS,
        port=settings.APP.PORT,
        access_log=False,
    )


if __name__ == "__main__":
    start_service()
