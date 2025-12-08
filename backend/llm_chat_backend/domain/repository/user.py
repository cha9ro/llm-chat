from abc import ABC, abstractmethod

from llm_chat_backend.domain.model.user import User


class IUserRepository(ABC):
    @abstractmethod
    def list_users(self, limit: int = 10, offset: int = 0) -> list[User]:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        pass
