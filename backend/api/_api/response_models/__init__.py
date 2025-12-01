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


class Hashtag(BaseModel):
    hashtagId: str
    postId: str
    hashtag: str


class PostReaction(BaseModel):
    reactionId: str
    postId: str
    userId: str
    reaction: int


class CommentReaction(BaseModel):
    reactionId: str
    commentId: str
    userId: str
    reaction: int


class Comment(BaseModel):
    commentId: str
    postId: str
    userId: str
    content: str
