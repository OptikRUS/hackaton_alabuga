import uuid
from collections.abc import AsyncGenerator, AsyncIterator
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import IO, Any

from aiobotocore.client import AioBaseClient
from botocore.exceptions import ClientError

from src.config.settings import settings
from src.core.file_storage import FileStorage
from src.core.media.exceptions import MediaNotFoundError
from src.core.media.schemas import FileMetadata, FileObject


@dataclass
class MinioService(FileStorage):
    minio_connection: AioBaseClient
    server_url: str = settings.SERVER.URL
    region_name: str = settings.MINIO.REGION
    bucket: str = settings.MINIO.BUCKET
    chunck_size: int = 65536

    @property
    def media_url_prefix(self) -> str:
        return f"{self.server_url}/media"

    async def get_file_metadata(self, key: str) -> FileMetadata:
        response = await self.minio_connection.head_object(Bucket=self.bucket, Key=key)
        return FileMetadata(file_size=response["ContentLength"], media_type=response["ContentType"])

    async def ensure_bucket(self) -> None:
        buckets = await self.minio_connection.list_buckets()
        if not any(b["Name"] == self.bucket for b in buckets.get("Buckets", [])):
            create_params: dict[str, Any] = {"Bucket": self.bucket}
            if self.region_name and self.region_name != "us-east-1":
                create_params["CreateBucketConfiguration"] = {
                    "LocationConstraint": self.region_name
                }
            await self.minio_connection.create_bucket(**create_params)

    async def upload_file_stream(
        self,
        file_name: str,
        file_stream: AsyncIterator[bytes] | IO[bytes],
        content_type: str | None = None,
        file_size: int | None = None,
    ) -> FileObject:
        extra_args: dict[str, Any] = {}
        if content_type:
            extra_args["ContentType"] = content_type

        unique_key = self._generate_unique_key(file_name=file_name)
        resp = await self.minio_connection.put_object(
            Bucket=self.bucket, Key=unique_key, Body=file_stream, **extra_args
        )

        return FileObject(
            key=unique_key,
            url=self._build_url(unique_key),
            etag=resp.get("ETag", "").strip('"'),
            content_type=content_type,
            size=file_size,
        )

    async def download_file(self, key: str) -> AsyncGenerator[bytes]:
        try:
            obj = await self.minio_connection.get_object(Bucket=self.bucket, Key=key)
            async with obj["Body"] as response:
                async for chunk in response.content.iter_chunked(self.chunck_size):
                    if not chunk:
                        continue
                    yield chunk
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise MediaNotFoundError from e
            raise

    async def delete_file(self, key: str) -> None:
        await self.minio_connection.delete_object(Bucket=self.bucket, Key=key)

    def _build_url(self, key: str) -> str:
        base = self.media_url_prefix.rstrip("/")
        return f"{base}/{key.lstrip('/')}"

    @staticmethod
    def _generate_unique_key(file_name: str) -> str:
        timestamp = datetime.now(UTC)
        date_path = timestamp.strftime("%Y/%m/%d")
        filename = file_name.lstrip("/").rsplit("/", 1)[-1]

        return f"{date_path}/{timestamp.strftime('%H%M%S')}_{uuid.uuid4()}_{filename}"
