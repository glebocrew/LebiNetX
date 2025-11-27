from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    userId: str
    nickname: str
    email: str
    pwd: str
    createdAt: datetime
    updatedAt: datetime
    avatar: bytes
