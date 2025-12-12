from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Chat(BaseModel):
    id: str
    user_id: str
    title: str | None = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class MessageRole(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ContentType(str, Enum):
    TEXT = "text"


class Content(BaseModel):
    type: ContentType
    content: str  # For image and file types, this could be Base64 encoded string


class Message(BaseModel):
    id: str
    chat_id: str
    role: MessageRole
    content: list[Content]
    created_at: datetime = datetime.now()


class ChatDetail(Chat):
    messages: list[Message]
