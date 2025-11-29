from sqlalchemy import String, BLOB, DateTime, Text, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    userId: Mapped[str] = mapped_column(String(36), primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    pwd: Mapped[str] = mapped_column(String(50))
    createdAt: Mapped[datetime] = mapped_column(DateTime)
    updatedAt: Mapped[datetime] = mapped_column(DateTime)
    avatar: Mapped[bytes] = mapped_column(BLOB)


class Post(Base):
    __tablename__ = "posts"

    postId: Mapped[str] = mapped_column(String(36), primary_key=True)
    userId: Mapped[str] = mapped_column(String(36), nullable=False)
    title: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    createdAt: Mapped[datetime] = mapped_column(DateTime)
    updatedAt: Mapped[datetime] = mapped_column(DateTime)


class PostReaction(Base):
    __tablename__ = "post_reactions"

    reactionId: Mapped[str] = mapped_column(String(36), nullable=False)
    postId: Mapped[str] = mapped_column(String(36), primary_key=True)
    reaction: Mapped[int] = mapped_column(
        Integer
    )  # the table of values of rections will be further
