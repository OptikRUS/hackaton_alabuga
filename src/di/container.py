from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.di.providers import AuthProvider, DatabaseProvider, UserProvider


def build_container() -> AsyncContainer:
    return make_async_container(
        FastapiProvider(),
        AuthProvider(),
        UserProvider(),
        DatabaseProvider(),
    )
