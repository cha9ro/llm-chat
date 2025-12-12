from abc import ABC, abstractmethod

from llm_chat_backend.domain.model.chat import Chat, ChatDetail, Message


class IChatRepository(ABC):
    @abstractmethod
    def create_chat(self, chat: Chat) -> Chat:
        pass

    @abstractmethod
    def list_chat_detail(self, chat_id: str) -> ChatDetail:
        pass

    @abstractmethod
    def list_chats(self, user_id: str, limit: int = 10, offset: int = 0) -> list[Chat]:
        pass

    @abstractmethod
    def update_chat_title(self, chat_id: str, title: str) -> Chat:
        pass

    @abstractmethod
    def delete_chat(self, chat_id: str) -> None:
        pass

    @abstractmethod
    def delete_chats(self, user_id: str, chat_id: str) -> None:
        pass


class IMessageRepository(ABC):
    @abstractmethod
    def create_message(self, message: Message) -> Message:
        pass
