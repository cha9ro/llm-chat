from injector import Binder, Injector, Module, singleton

from llm_chat_backend.application.chat import ChatUsecase
from llm_chat_backend.application.response import ResponseUsecase


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ChatUsecase, to=ChatUsecase, scope=singleton)
        binder.bind(ResponseUsecase, to=ResponseUsecase, scope=singleton)
        pass


injector = Injector([AppModule()])


def get_injector() -> Injector:
    return injector
