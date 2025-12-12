from abc import ABC, abstractmethod
from typing import Any, Generator

from llm_chat_backend.domain.model.chat import Message


class IResponseRepository(ABC):
    @abstractmethod
    def stream_response(
        self, chat_id: str, message: Message
    ) -> Generator[dict[str, Any], None, None]:
        pass
