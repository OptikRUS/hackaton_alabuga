from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.api.app import create_app
from src.config.logger import configure_logging
from src.config.settings import settings
from src.migrations.commands import migrate
from src.services.minio import MinioService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    async with app.state.dishka_container() as container:
        minio_service = await container.get(MinioService)
        await minio_service.ensure_bucket()
    yield
    await app.state.dishka_container.close()


def start_service() -> None:
    configure_logging(cfg=settings.LOGGER)
    migrate(revision="heads", db_url=settings.DATABASE.URL.get_secret_value())
    uvicorn.run(
        app=create_app(lifespan=lifespan),
        host=settings.APP.ADDRESS,
        port=settings.APP.PORT,
        access_log=True,
        log_config=None,
    )


if __name__ == "__main__":
    start_service()
