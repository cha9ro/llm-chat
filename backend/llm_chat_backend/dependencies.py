from functools import lru_cache

from injector import Binder, Injector, Module, singleton

from llm_chat_backend.application.chat import ChatUsecase
from llm_chat_backend.application.response import ResponseUsecase
from llm_chat_backend.domain.repository.chat import IChatRepository
from llm_chat_backend.infra.database.sqlite import SQLiteConfig
from llm_chat_backend.infra.repository.chat import ChatRepository


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # application
        binder.bind(ChatUsecase, to=ChatUsecase, scope=singleton)
        binder.bind(ResponseUsecase, to=ResponseUsecase, scope=singleton)

        # repository
        binder.bind(IChatRepository, to=ChatRepository, scope=singleton)

        # config
        binder.bind(SQLiteConfig, to=SQLiteConfig(), scope=singleton)


def create_injector() -> Injector:
    return Injector([AppModule()])


@lru_cache(maxsize=1)
def get_injector() -> Injector:
    return create_injector()
