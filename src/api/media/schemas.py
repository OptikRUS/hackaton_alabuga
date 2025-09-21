from pydantic import Field

from src.api.boundary import BoundaryModel
from src.core.media.schemas import FileObject


class FileObjectResponse(BoundaryModel):
    key: str = Field(default=..., description="Идентификатор файла")
    url: str = Field(default=..., description="Ссылка на файл")
    size: int | None = Field(default=..., description="Размер файла")
    etag: str = Field(default=..., description="Е-тэг файла")
    content_type: str | None = Field(default=..., description="Тип файла")

    @classmethod
    def from_schema(cls, file_object: FileObject) -> "FileObjectResponse":
        return cls(
            key=file_object.key,
            url=file_object.url,
            size=file_object.size,
            etag=file_object.etag,
            content_type=file_object.content_type,
        )
