from sqlalchemy import String, BLOB, DateTime
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
    createdAt: Mapped[datetime] = mapped_column(DateTime)
    updatedAt: Mapped[datetime] = mapped_column(DateTime)
    avatar: Mapped[bytes] = mapped_column(BLOB)
