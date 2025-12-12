from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from llm_chat_backend.application.chat import ChatUsecase
from llm_chat_backend.application.response import ResponseUsecase
from llm_chat_backend.dependencies import get_injector
from llm_chat_backend.domain.model.chat import Chat, ChatDetail


class ChatCreateRequest(BaseModel):
    user_id: str = Field(..., description="Owner of the chat session")
    title: str | None = Field(
        default=None, description="Optional title for the chat session"
    )


class ChatTitleUpdateRequest(BaseModel):
    user_id: str = Field(..., description="Owner of the chat session")
    title: str = Field(..., min_length=1, description="New chat title")


router = APIRouter(prefix="/chats")
injector = get_injector()


@router.get("")
async def list_chats(
    usecase: Annotated[ChatUsecase, Depends(lambda: injector.get(ChatUsecase))],
    user_id: str = Query(..., description="Owner whose chats are requested"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of chats"),
    offset: int = Query(0, ge=0, description="Number of chats to skip"),
) -> list[Chat]:
    try:
        return usecase.list_chats(user_id=user_id, limit=limit, offset=offset)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_chat(
    request: ChatCreateRequest,
    usecase: Annotated[ChatUsecase, Depends(lambda: injector.get(ChatUsecase))],
) -> Chat:
    return usecase.create_chat(user_id=request.user_id, title=request.title)


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chat(
    usecase: Annotated[ChatUsecase, Depends(lambda: injector.get(ChatUsecase))],
    chat_id: str,
    user_id: str = Query(..., description="Owner whose chat should be deleted"),
) -> None:
    try:
        usecase.delete_chat(user_id=user_id, chat_id=chat_id)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)
        ) from exc


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chats(
    usecase: Annotated[ChatUsecase, Depends(lambda: injector.get(ChatUsecase))],
    user_id: str = Query(..., description="Owner whose chats should be deleted"),
) -> None:
    usecase.delete_chats(user_id=user_id)


@router.patch("/{chat_id}")
async def update_chat_title(
    usecase: Annotated[ChatUsecase, Depends(lambda: injector.get(ChatUsecase))],
    chat_id: str,
    request: ChatTitleUpdateRequest,
) -> Chat:
    try:
        return usecase.update_chat_title(
            user_id=request.user_id, chat_id=chat_id, title=request.title
        )
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)
        ) from exc


@router.get("/{chat_id}")
async def get_chat_detail(
    usecase: Annotated[ChatUsecase, Depends(lambda: injector.get(ChatUsecase))],
    chat_id: str,
    user_id: str = Query(..., description="Owner whose chat should be retrieved"),
    limit: int = Query(
        10, ge=0, le=200, description="Maximum number of messages (0 for all)"
    ),
    offset: int = Query(0, ge=0, description="Number of messages to skip"),
) -> ChatDetail:
    try:
        return usecase.get_chat_detail(
            user_id=user_id, chat_id=chat_id, limit=limit, offset=offset
        )
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.post("/{chat_id}/messages")
async def response(
    chat_id: str,
    usecase: Annotated[ResponseUsecase, Depends(lambda: injector.get(ResponseUsecase))],
) -> StreamingResponse:
    raise NotImplementedError()
