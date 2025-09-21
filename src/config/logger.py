import logging
import logging.config
from collections.abc import Callable
from typing import cast
from uuid import UUID

import orjson
import structlog
from sqlalchemy import log as sa_log
from structlog.processors import (
    CallsiteParameter,
    CallsiteParameterAdder,
)

from src.config.settings import LoggingConfig

logger = logging.getLogger(__name__)


ProcessorType = Callable[
    [
        structlog.types.WrappedLogger,
        str,
        structlog.types.EventDict,
    ],
    str | bytes,
]


def additionally_serialize(obj: object) -> str:
    if isinstance(obj, UUID):
        return str(obj)

    logger.warning("Type is not JSON serializable: %s", type(obj), extra={"obj": repr(obj)})
    return repr(obj)


def serialize_to_json(data: object, default: Callable[[object], str] | None = None) -> str:
    serializer = default or additionally_serialize
    return orjson.dumps(data, default=serializer).decode()


def get_render_processor(
    *,
    render_json_logs: bool = False,
    serializer: Callable[..., str | bytes] = serialize_to_json,
    colors: bool = True,
) -> ProcessorType:
    if render_json_logs:
        return structlog.processors.JSONRenderer(serializer=serializer)
    return structlog.dev.ConsoleRenderer(colors=colors)


def _mute_sa_default_handler(logger: logging.Logger) -> None:  # noqa: ARG001
    """Disable SQLAlchemy default handler added to the provided logger."""
    return


def configure_logging(cfg: LoggingConfig) -> None:
    # Mute SQLAlchemy default logger handler
    sa_log._add_default_handler = _mute_sa_default_handler  # noqa: SLF001  # type: ignore[assignment]

    common_processors = (
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.ExtraAdder(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=True),
        structlog.contextvars.merge_contextvars,
        structlog.processors.format_exc_info,
        CallsiteParameterAdder(
            (
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.LINENO,
            ),
        ),
    )
    structlog_processors = (
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    )
    logging_processors = (structlog.stdlib.ProcessorFormatter.remove_processors_meta,)
    logging_console_processors = (
        *logging_processors,
        get_render_processor(render_json_logs=cfg.RENDER_JSON_LOGS, colors=True),
    )
    logging_file_processors = (
        *logging_processors,
        get_render_processor(render_json_logs=cfg.RENDER_JSON_LOGS, colors=False),
    )

    handler = logging.StreamHandler()
    handler.set_name("default")
    handler.setLevel(cfg.LEVEL)
    console_formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=cast("tuple[structlog.types.Processor, ...]", common_processors),
        processors=logging_console_processors,
    )
    handler.setFormatter(console_formatter)

    handlers: list[logging.Handler] = [handler]
    if cfg.PATH:
        cfg.PATH.parent.mkdir(parents=True, exist_ok=True)
        log_path = cfg.PATH / "logs.log" if cfg.PATH.is_dir() else cfg.PATH

        file_handler = logging.FileHandler(log_path)
        file_handler.set_name("file")
        file_handler.setLevel(cfg.LEVEL)
        file_formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=cast("tuple[structlog.types.Processor, ...]", common_processors),
            processors=logging_file_processors,
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)

    logging.basicConfig(handlers=handlers, level=cfg.LEVEL)
    structlog.configure(
        processors=cast(
            "tuple[structlog.types.Processor, ...]", common_processors + structlog_processors
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
