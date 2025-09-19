from dataclasses import dataclass
from typing import cast
from unittest.mock import AsyncMock

from dishka import AsyncContainer

from src.core.use_case import UseCase


@dataclass(kw_only=True)
class ContainerHelper:
    container: AsyncContainer

    async def override_use_case(self, use_case: type[UseCase]) -> AsyncMock:
        mocked_use_case = await self.container.get(use_case)
        return cast("AsyncMock", mocked_use_case)
