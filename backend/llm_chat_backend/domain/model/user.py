from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    id: str
    username: str
    role: UserRole
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
