from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    """
        USER{
        VARCHAR(36) userId
        VARCHAR(50) nickname
        VARCHAR(50) email
        DATETIME createdAt
        DATETIME updatedAt
        BLOB avatar
    }
    """
    userId: str
    nickname: str
    email: str
    createdAt: datetime
    updatedAt: datetime
    avatar: bytes