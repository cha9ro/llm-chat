from datetime import datetime
from uuid import uuid4

from injector import inject

from llm_chat_backend.domain.model.chat import Chat, ChatDetail
from llm_chat_backend.domain.repository.chat import IChatRepository


class ChatUsecase:
    @inject
    def __init__(self, chat_repository: IChatRepository) -> None:
        self._chat_repository = chat_repository

    def create_chat(self, user_id: str, title: str | None = None) -> Chat:
        now = datetime.now()
        chat = Chat(
            id=str(uuid4()),
            user_id=user_id,
            title=title,
            created_at=now,
            updated_at=now,
        )
        return self._chat_repository.create_chat(chat)

    def list_chats(self, user_id: str, limit: int = 10, offset: int = 0) -> list[Chat]:
        if limit < 0 or offset < 0:
            raise ValueError("limit and offset must be positive integers")
        return self._chat_repository.list_chats(
            user_id=user_id, limit=limit, offset=offset
        )

    def delete_chat(self, user_id: str, chat_id: str) -> None:
        chat = self._chat_repository.list_chat_detail(chat_id)
        if chat.user_id != user_id:
            raise PermissionError("Chat does not belong to the user")
        self._chat_repository.delete_chat(chat_id)

    def delete_chats(self, user_id: str) -> None:
        self._chat_repository.delete_chats(user_id)

    def update_chat_title(self, user_id: str, chat_id: str, title: str) -> Chat:
        chat = self._chat_repository.list_chat_detail(chat_id)
        if chat.user_id != user_id:
            raise PermissionError("Chat does not belong to the user")
        return self._chat_repository.update_chat_title(chat_id, title)

    def get_chat_detail(
        self, user_id: str, chat_id: str, limit: int = 10, offset: int = 0
    ) -> ChatDetail:
        if limit < 0 or offset < 0:
            raise ValueError("limit and offset must be positive integers")
        chat = self._chat_repository.list_chat_detail(chat_id)
        if chat.user_id != user_id:
            raise PermissionError("Chat does not belong to the user")

        if limit == 0 and offset == 0:
            return chat

        end = offset + limit if limit else None
        sliced_messages = chat.messages[offset:end]
        return ChatDetail(
            **chat.model_dump(exclude={"messages"}),
            messages=sliced_messages,
        )
