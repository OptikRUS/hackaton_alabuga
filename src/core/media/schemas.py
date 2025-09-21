from dataclasses import dataclass


@dataclass
class FileObject:
    key: str
    url: str
    size: int | None
    etag: str
    content_type: str | None


@dataclass
class FileMetadata:
    file_size: int
    media_type: str
