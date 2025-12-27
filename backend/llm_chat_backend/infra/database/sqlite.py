from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from injector import inject
from pydantic_settings import BaseSettings
from sqlmodel import Session, SQLModel, create_engine

from llm_chat_backend.config import ENV_FILE


class SQLiteConfig(BaseSettings):
    model_config = {
        "env_prefix": "SQLITE_",
        "env_file": ENV_FILE,
        "env_file_encoding": "utf-8",
    }

    db_path: str | Path = ".data/chat.db"
    echo: bool = False

    # Connection pooling settings (for future PostgreSQL migration)
    pool_size: int = 5
    max_overflow: int = 10
    pool_pre_ping: bool = True
    pool_recycle: int = 3600  # Recycle connections after 1 hour


class SQLiteConnection:
    """Shared SQLModel engine/session factory for SQLite usage.

    Note: SQLite has limited connection pooling support. The pool settings
    are configured here for future PostgreSQL migration but may not have
    the same effect with SQLite.
    """

    @inject
    def __init__(self, config: SQLiteConfig) -> None:
        self._db_path = str(config.db_path)
        self._engine = create_engine(
            f"sqlite:///{self._db_path}",
            echo=config.echo,
            connect_args={"check_same_thread": False},
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_pre_ping=config.pool_pre_ping,
            pool_recycle=config.pool_recycle,
        )

    @contextmanager
    def session(self) -> Iterator[Session]:
        with Session(self._engine) as session:
            yield session

    def create_all(self) -> None:
        SQLModel.metadata.create_all(self._engine)

    def dispose(self) -> None:
        self._engine.dispose()
