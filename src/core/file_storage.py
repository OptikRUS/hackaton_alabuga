from abc import ABCMeta, abstractmethod
from collections.abc import AsyncIterator
from typing import IO

from src.core.media.schemas import FileMetadata, FileObject


class FileStorage(metaclass=ABCMeta):
    @abstractmethod
    async def get_file_metadata(self, key: str) -> FileMetadata:
        raise NotImplementedError

    @abstractmethod
    async def upload_file_stream(
        self,
        key: str,
        file_stream: AsyncIterator[bytes] | IO[bytes],
        content_type: str,
        file_size: int | None = None,
    ) -> FileObject:
        raise NotImplementedError

    @abstractmethod
    def download_file(self, key: str) -> AsyncIterator[bytes]:
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, key: str) -> None:
        raise NotImplementedError
