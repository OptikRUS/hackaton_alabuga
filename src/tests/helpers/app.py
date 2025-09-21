from dataclasses import dataclass
from typing import cast
from unittest.mock import AsyncMock

from dishka import AsyncContainer

from src.core.use_case import UseCase
from src.services.minio import MinioService


@dataclass(kw_only=True)
class ContainerHelper:
    container: AsyncContainer

    async def override_use_case(self, use_case: type[UseCase]) -> AsyncMock:
        mocked_use_case = await self.container.get(use_case)
        return cast("AsyncMock", mocked_use_case)

    async def override_minio_service(self, service: type[MinioService]) -> AsyncMock:
        mocked_service = await self.container.get(service)
        return cast("AsyncMock", mocked_service)
