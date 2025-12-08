from abc import ABC, abstractmethod
from typing import Generator

from llm_chat_backend.domain.model.chat import Message
from llm_chat_backend.domain.model.inference import BaseInferenceResponse


class IInferenceRepository(ABC):
    @abstractmethod
    def response(self, chat_id: str, message: Message) -> BaseInferenceResponse:
        pass

    @abstractmethod
    def stream_response(self, chat_id: str, message: Message) -> Generator[str, None, None]:
        pass

    @abstractmethod
    async def async_response(self, chat_id: str, message: Message) -> str:
        pass

    @abstractmethod
    async def async_stream_response(self, chat_id: str, message: Message) -> Generator[str, None, None]:
        pass
