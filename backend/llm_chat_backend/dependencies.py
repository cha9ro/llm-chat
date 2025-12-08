from injector import Binder, Injector, Module


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # binder.bind(IChatRepository, to=ChatRepository)
        pass


injector = Injector([AppModule()])


def get_injector() -> Injector:
    return injector
