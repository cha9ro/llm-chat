from enum import Enum
from typing import ClassVar

from pydantic import BaseModel


class InferenceStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class BaseInferenceResponse(BaseModel):
    status: ClassVar[InferenceStatus]


class InferenceInResponse(BaseModel):
    status: ClassVar[InferenceStatus] = InferenceStatus.IN_PROGRESS


class InferenceCompletedResponse(BaseModel):
    status: ClassVar[InferenceStatus] = InferenceStatus.COMPLETED


class InferenceFailedResponse(BaseModel):
    status: ClassVar[InferenceStatus] = InferenceStatus.FAILED
