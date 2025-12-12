from enum import Enum
from typing import Any, ClassVar

from pydantic import BaseModel


class ResponseStatus(str, Enum):
    STARTED = "started"
    REASONING = "reasoning"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    TOOL_CALL_STARTED = "tool_call_started"
    TOOL_CALL_COMPLETED = "tool_call_completed"


class Citation(BaseModel):
    title: str
    url: str | None
    cited_text: str | None


class CompletedContent(BaseModel):
    content: str
    citations: list[Citation] | None = None


class BaseResponse(BaseModel):
    status: ClassVar[ResponseStatus]


class StartedResponse(BaseResponse):
    status: ClassVar[ResponseStatus] = ResponseStatus.STARTED


class ReasoningResponse(BaseResponse):
    status: ClassVar[ResponseStatus] = ResponseStatus.REASONING
    content: str


class RespondingResponse(BaseResponse):
    status: ClassVar[ResponseStatus] = ResponseStatus.GENERATING
    delta: str


class CompletedResponse(BaseResponse):
    status: ClassVar[ResponseStatus] = ResponseStatus.COMPLETED
    content: CompletedContent


class FailedResponse(BaseResponse):
    status: ClassVar[ResponseStatus] = ResponseStatus.FAILED
    error: str


class CanceledResponse(BaseResponse):
    status: ClassVar[ResponseStatus] = ResponseStatus.CANCELED


class ToolCallStartedResponse(BaseResponse):
    status: ClassVar[ResponseStatus] = ResponseStatus.TOOL_CALL_STARTED
    tool_name: str
    tool_call_id: str
    tool_arguments: dict[str, Any]


class ToolCallCompletedResponse(BaseResponse):
    status: ClassVar[ResponseStatus] = ResponseStatus.TOOL_CALL_COMPLETED
    tool_name: str
    tool_call_id: str
    result: str
