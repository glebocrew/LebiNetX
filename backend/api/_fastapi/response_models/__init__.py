from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    userId: str
    nickname: str
    email: str
    createdAt: datetime
    updatedAt: datetime
    avatar: bytes
