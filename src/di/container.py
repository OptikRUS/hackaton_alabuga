from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.di.providers import (
    ArtifactProvider,
    AuthProvider,
    DatabaseProvider,
    FileStorageProvider,
    MissionProvider,
    UserProvider,
)


def build_container() -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        AuthProvider(),
        UserProvider(),
        MissionProvider(),
        ArtifactProvider(),
        FileStorageProvider(),
        DatabaseProvider(),
    )
