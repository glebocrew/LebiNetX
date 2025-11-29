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


class Post(BaseModel):
    postId: str
    userId: str
    title: str
    content: str
    createdAt: datetime
    updatedAt: datetime
