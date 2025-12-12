from llm_chat_backend.domain.model.chat import Message


class ResponseUsecase:
    def response(self, message: Message) -> str:
        raise NotImplementedError()
