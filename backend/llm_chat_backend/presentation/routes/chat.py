from typing import Annotated

from fastapi import APIRouter, Depends

from llm_chat_backend.application.chat import ChatUsecase
from llm_chat_backend.application.response import ResponseUsecase
from llm_chat_backend.dependencies import injector
from llm_chat_backend.domain.model.chat import Chat

router = APIRouter(prefix="/chats")


@router.get("/")
async def list_chats(
    usecase: Annotated[ChatUsecase, Depends(lambda _: injector.get(ChatUsecase))],
):
    raise NotImplementedError()


@router.post("/")
async def create_chat(
    usecase: Annotated[ChatUsecase, Depends(lambda _: injector.get(ChatUsecase))],
) -> Chat:
    raise NotImplementedError()


@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: str,
    usecase: Annotated[ChatUsecase, Depends(lambda _: injector.get(ChatUsecase))],
):
    raise NotImplementedError()


@router.delete("/")
async def delete_chats(
    usecase: Annotated[ChatUsecase, Depends(lambda _: injector.get(ChatUsecase))],
):
    raise NotImplementedError()


@router.patch("/{chat_id}")
async def update_chat_title(
    chat_id: str,
    title: str,
    usecase: Annotated[ChatUsecase, Depends(lambda _: injector.get(ChatUsecase))],
):
    raise NotImplementedError()


@router.get("/{chat_id}")
async def get_chat_detail(
    chat_id: str,
    usecase: Annotated[ChatUsecase, Depends(lambda _: injector.get(ChatUsecase))],
):
    raise NotImplementedError()


@router.post("/{chat_id}/messages")
async def response(
    chat_id: str,
    usecase: Annotated[
        ResponseUsecase, Depends(lambda _: injector.get(ResponseUsecase))
    ],
):
    raise NotImplementedError()
