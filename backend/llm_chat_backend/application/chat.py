from llm_chat_backend.domain.model.chat import Chat, ChatDetail


class ChatUsecase:
    def create_chat(self, user_id: str) -> Chat:
        raise NotImplementedError()

    def list_chats(self, user_id: str, limit: int = 10, offset: int = 0) -> list[Chat]:
        raise NotImplementedError()

    def delete_chat(self, user_id: str, chat_id: str) -> None:
        raise NotImplementedError()

    def delete_chats(self, user_id: str) -> None:
        raise NotImplementedError()

    def update_chat_title(self, chat_id: str, title: str) -> Chat:
        raise NotImplementedError()

    def get_chat_detail(
        self, chat_id: str, limit: int = 10, offset: int = 0
    ) -> ChatDetail:
        raise NotImplementedError()
