from fastapi import FastAPI

from llm_chat_backend.presentation.routes import chat


def create_app() -> FastAPI:
    app = FastAPI(title="LLM Chat Backend", version="0.1.0")

    app.include_router(chat.router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "llm_chat_backend.presentation.routes.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
