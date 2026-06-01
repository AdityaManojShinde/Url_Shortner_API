from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from datetime import datetime, timezone

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4,primary_key=True)
    email: str = Field(
        index=True,
        unique=True, 
        nullable=False
        )
    password_hash: str = Field(nullable=False)
    urls: list["ShortUrl"] = Relationship(back_populates="user", cascade_delete=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )

class ShortUrl(SQLModel, table=True):
    __tablename__ = "short_urls"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID | None = Field(
        foreign_key="users.id",
        default=None, 
        index=True, 
        nullable=True, 
        ondelete="CASCADE"
        )
    url: str = Field(
        nullable=False,
        description="url mapped to short code"
        )
    short_code: str = Field(
        unique=True,
        index=True,
        nullable=False,
        description="short code mapped to a url"
        )
    user: User | None = Relationship(back_populates="urls")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )
    
    