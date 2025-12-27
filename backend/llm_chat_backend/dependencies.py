from threading import Lock

from injector import Binder, Injector, Module, singleton

from llm_chat_backend.application.chat import ChatUsecase
from llm_chat_backend.application.response import ResponseUsecase
from llm_chat_backend.domain.repository.chat import IChatRepository
from llm_chat_backend.infra.database.sqlite import SQLiteConfig, SQLiteConnection
from llm_chat_backend.infra.repository.chat import ChatRepository


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # config
        binder.bind(SQLiteConfig, to=SQLiteConfig, scope=singleton)

        # database
        binder.bind(SQLiteConnection, to=SQLiteConnection, scope=singleton)

        # repository
        binder.bind(IChatRepository, to=ChatRepository, scope=singleton)

        # application
        binder.bind(ChatUsecase, to=ChatUsecase, scope=singleton)
        binder.bind(ResponseUsecase, to=ResponseUsecase, scope=singleton)


def create_injector() -> Injector:
    return Injector([AppModule()])


# Thread-safe singleton injector
_injector: Injector | None = None
_injector_lock = Lock()


def get_injector() -> Injector:
    """Get the singleton injector instance in a thread-safe manner."""
    global _injector
    if _injector is None:
        with _injector_lock:
            # Double-check locking pattern
            if _injector is None:
                _injector = create_injector()
    return _injector
