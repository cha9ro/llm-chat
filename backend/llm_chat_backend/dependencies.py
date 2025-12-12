from injector import Binder, Injector, Module, singleton

from llm_chat_backend.application.chat import ChatUsecase
from llm_chat_backend.application.response import ResponseUsecase
from llm_chat_backend.domain.repository.chat import IChatRepository
from llm_chat_backend.infra.repository.chat import ChatRepository


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # application
        binder.bind(ChatUsecase, to=ChatUsecase, scope=singleton)
        binder.bind(ResponseUsecase, to=ResponseUsecase, scope=singleton)

        # repository
        binder.bind(IChatRepository, to=ChatRepository, scope=singleton)


injector = Injector([AppModule()])


def get_injector() -> Injector:
    return injector
