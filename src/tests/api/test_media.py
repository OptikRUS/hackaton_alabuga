import pytest
from httpx import codes

from src.core.media.exceptions import MediaNotFoundError
from src.core.media.schemas import FileMetadata, FileObject
from src.services.minio import MinioService
from src.tests.fixtures import APIFixture, ContainerFixture


class TestUploadFileAPI(APIFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.minio_service = await self.container.override_minio_service(MinioService)

    def test_upload_file(self) -> None:
        self.minio_service.upload_file_stream.return_value = FileObject(
            key="TEST",
            url="http://test-url/test-key",
            size=len(b"test file content"),
            etag="TEST",
            content_type="text/plain",
        )

        response = self.api.upload_file(
            file_content=b"test file content",
            filename="test.txt",
            content_type="text/plain",
        )

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "key": "TEST",
            "url": "http://test-url/test-key",
            "size": len(b"test file content"),
            "etag": "TEST",
            "contentType": "text/plain",
        }
        self.minio_service.upload_file_stream.assert_called_once()
        call_args = self.minio_service.upload_file_stream.call_args
        assert call_args.kwargs["file_name"] == "test.txt"
        assert call_args.kwargs["content_type"] == "text/plain"
        assert call_args.kwargs["file_size"] == len(b"test file content")
        assert hasattr(call_args.kwargs["file_stream"], "read")

    def test_upload_file_with_different_content_type(self) -> None:
        self.minio_service.upload_file_stream.return_value = FileObject(
            key="test-key-pdf",
            url="http://test-url/test-key-pdf",
            size=len(b"test file content"),
            etag="test-etag",
            content_type="application/pdf",
        )

        response = self.api.upload_file(
            file_content=b"test file content",
            filename="document.pdf",
            content_type="application/pdf",
        )

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "key": "test-key-pdf",
            "url": "http://test-url/test-key-pdf",
            "size": len(b"test file content"),
            "etag": "test-etag",
            "contentType": "application/pdf",
        }
        self.minio_service.upload_file_stream.assert_called_once()
        call_args = self.minio_service.upload_file_stream.call_args
        assert call_args.kwargs["file_name"] == "document.pdf"
        assert call_args.kwargs["content_type"] == "application/pdf"
        assert call_args.kwargs["file_size"] == len(b"test file content")
        assert hasattr(call_args.kwargs["file_stream"], "read")

    def test_upload_image_file(self) -> None:
        self.minio_service.upload_file_stream.return_value = FileObject(
            key="image-key",
            url="http://test-url/image-key",
            size=100,
            etag="image-etag",
            content_type="image/jpeg",
        )

        response = self.api.upload_file(
            file_content=b"fake image content",
            filename="test.jpg",
            content_type="image/jpeg",
        )

        assert response.status_code == codes.CREATED
        assert response.json() == {
            "key": "image-key",
            "url": "http://test-url/image-key",
            "size": 100,
            "etag": "image-etag",
            "contentType": "image/jpeg",
        }
        self.minio_service.upload_file_stream.assert_called_once()
        call_args = self.minio_service.upload_file_stream.call_args
        assert call_args.kwargs["file_name"] == "test.jpg"
        assert call_args.kwargs["content_type"] == "image/jpeg"
        assert call_args.kwargs["file_size"] == len(b"fake image content")
        assert hasattr(call_args.kwargs["file_stream"], "read")


class TestDownloadFileAPI(APIFixture, ContainerFixture):
    @pytest.fixture(autouse=True)
    async def setup(self) -> None:
        self.minio_service = await self.container.override_minio_service(MinioService)

    def test_download_file(self) -> None:
        self.minio_service.get_file_metadata.return_value = FileMetadata(
            file_size=(len(b"test file content")),
            media_type="text/plain",
        )
        self.minio_service.download_file.return_value = iter([b"test file content"])

        response = self.api.download_file(key="test-file.txt")

        assert response.status_code == codes.OK
        assert response.content == b"test file content"
        assert response.headers["content-type"].startswith("text/plain")
        assert response.headers["content-disposition"] == 'attachment; filename="test-file.txt"'
        assert response.headers["content-length"] == str(len(b"test file content"))
        assert response.headers["cache-control"] == "public, max-age=3600"

        self.minio_service.get_file_metadata.assert_called_once()
        self.minio_service.get_file_metadata.assert_awaited_once_with(key="test-file.txt")
        self.minio_service.download_file.assert_called_once_with("test-file.txt")

    def test_download_image_file(self) -> None:
        self.minio_service.get_file_metadata.return_value = FileMetadata(
            file_size=(len(b"fake image content")),
            media_type="image/jpeg",
        )
        self.minio_service.download_file.return_value = iter([b"fake image content"])

        response = self.api.download_file(key="test-image.jpg")

        assert response.status_code == codes.OK
        assert response.content == b"fake image content"
        assert response.headers["content-type"].startswith("image/jpeg")
        assert response.headers["content-disposition"] == 'inline; filename="test-image.jpg"'
        assert response.headers["content-length"] == str(len(b"fake image content"))
        assert response.headers["cache-control"] == "public, max-age=3600"

        self.minio_service.get_file_metadata.assert_called_once()
        self.minio_service.get_file_metadata.assert_awaited_once_with(key="test-image.jpg")
        self.minio_service.download_file.assert_called_once_with("test-image.jpg")

    def test_download_file_with_nested_path(self) -> None:
        self.minio_service.get_file_metadata.return_value = FileMetadata(
            file_size=(len(b"test file content")),
            media_type="text/plain",
        )
        self.minio_service.download_file.return_value = iter([b"test file content"])

        response = self.api.download_file(key="folder/subfolder/test-file.txt")

        assert response.status_code == codes.OK
        assert response.content == b"test file content"
        assert response.headers["content-disposition"] == 'attachment; filename="test-file.txt"'
        self.minio_service.get_file_metadata.assert_called_once()
        self.minio_service.get_file_metadata.assert_awaited_once_with(
            key="folder/subfolder/test-file.txt",
        )
        self.minio_service.download_file.assert_called_once_with("folder/subfolder/test-file.txt")

    def test_download_file_not_found(self) -> None:
        self.minio_service.get_file_metadata.side_effect = MediaNotFoundError

        response = self.api.download_file(key="non-existent-file.txt")

        assert response.status_code == codes.NOT_FOUND
        assert response.json() == {"detail": MediaNotFoundError.detail}
        self.minio_service.get_file_metadata.assert_called_once()
        self.minio_service.get_file_metadata.assert_awaited_once_with(key="non-existent-file.txt")
        self.minio_service.download_file.assert_not_called()
