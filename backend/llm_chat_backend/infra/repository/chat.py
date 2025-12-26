from __future__ import annotations

import json
from datetime import datetime
from typing import Self

from injector import inject
from sqlalchemy import Column, DateTime, Text, delete
from sqlmodel import Field, SQLModel, col, select

from llm_chat_backend.domain.model.chat import (
    Chat,
    ChatDetail,
    Content,
    Message,
    MessageRole,
)
from llm_chat_backend.domain.repository.chat import IChatRepository
from llm_chat_backend.infra.database.sqlite import SQLiteConnection


class ChatTable(SQLModel, table=True):
    __tablename__ = "chats"  # pyright: ignore[reportAssignmentType]

    id: str = Field(primary_key=True, index=True)
    user_id: str = Field(index=True)
    title: str | None = Field(default=None)
    created_at: str
    updated_at: str

    @classmethod
    def from_model(cls, chat: Chat) -> Self:
        return cls(
            id=chat.id,
            user_id=chat.user_id,
            title=chat.title,
            created_at=chat.created_at.isoformat(),
            updated_at=chat.updated_at.isoformat(),
        )

    def to_model(self) -> Chat:
        return Chat(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            created_at=datetime.fromisoformat(self.created_at),
            updated_at=datetime.fromisoformat(self.updated_at),
        )


class MessageTable(SQLModel, table=True):
    __tablename__ = "messages"  # pyright: ignore[reportAssignmentType]

    id: str = Field(primary_key=True, index=True)
    chat_id: str = Field(foreign_key="chats.id", index=True)
    role: str = Field(index=True)
    content: str = Field(sa_column=Column(Text, nullable=False))
    created_at: str = Field(sa_column=Column(DateTime, nullable=False, index=True))

    @classmethod
    def from_model(cls, message: Message) -> Self:
        raw_content = [item.model_dump_json() for item in message.content]
        return cls(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role.value,
            content=json.dumps(raw_content),
            created_at=message.created_at.isoformat(),
        )

    def to_model(self) -> Message:
        raw_content = json.loads(self.content) if self.content else []
        content_items = [Content.model_validate_json(item) for item in raw_content]
        return Message(
            id=self.id,
            chat_id=self.chat_id,
            role=MessageRole(self.role),
            content=content_items,
            created_at=datetime.fromisoformat(self.created_at),
        )


class ChatRepository(IChatRepository):
    """SQLModel-powered persistence for chats and messages."""

    @inject
    def __init__(self, connection: SQLiteConnection) -> None:
        self._connection = connection

    def create_chat(self, chat: Chat) -> Chat:
        chat_row = ChatTable.from_model(chat)
        with self._connection.session() as session:
            session.add(chat_row)
            session.commit()
        return chat

    def list_chat_detail(self, chat_id: str) -> ChatDetail:
        with self._connection.session() as session:
            chat_row = session.get(ChatTable, chat_id)
            if chat_row is None:
                raise LookupError(f"Chat {chat_id} not found")

            message_rows = session.exec(
                select(MessageTable)
                .where(MessageTable.chat_id == chat_id)
                .order_by(MessageTable.created_at)
            ).all()

        chat = chat_row.to_model()
        messages = [row.to_model() for row in message_rows]
        return ChatDetail(**chat.model_dump(), messages=messages)

    def list_chats(self, user_id: str, limit: int = 10, offset: int = 0) -> list[Chat]:
        with self._connection.session() as session:
            rows = session.exec(
                select(ChatTable)
                .where(ChatTable.user_id == user_id)
                .order_by(ChatTable.updated_at)
                .offset(offset)
                .limit(limit)
            ).all()
        return [row.to_model() for row in rows]

    def update_chat_title(self, chat_id: str, title: str) -> Chat:
        with self._connection.session() as session:
            chat_row = session.get(ChatTable, chat_id)
            if chat_row is None:
                raise LookupError(f"Chat {chat_id} not found")

            chat_row.title = title
            chat_row.updated_at = datetime.now().isoformat()
            session.add(chat_row)
            session.commit()
            session.refresh(chat_row)
        return chat_row.to_model()

    def delete_chat(self, chat_id: str) -> None:
        with self._connection.session() as session:
            chat_row = session.get(ChatTable, chat_id)
            if chat_row is None:
                raise LookupError(f"Chat {chat_id} not found")
            session.delete(chat_row)
            session.commit()

    def delete_chats(self, user_id: str) -> None:
        with self._connection.session() as session:
            session.exec(delete(ChatTable).where(col(ChatTable.user_id) == user_id))
            session.commit()
