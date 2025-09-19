from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.types import Lifespan

from src.api.exceptions import exception_handlers
from src.api.openapi import generate_custom_openapi
from src.api.routers import root_router
from src.di.container import build_container


def create_app(lifespan: Lifespan[FastAPI] | None = None) -> FastAPI:
    app = FastAPI(
        exception_handlers=exception_handlers,
        lifespan=lifespan,
        swagger_ui_parameters={
            "filter": True,
            "defaultModelsExpandDepth": 0,
            "displayRequestDuration": True,
        },
    )
    container = build_container()
    setup_dishka(container=container, app=app)
    app.openapi = generate_custom_openapi(app=app)  # type: ignore[method-assign]

    app.include_router(root_router)
    return app
