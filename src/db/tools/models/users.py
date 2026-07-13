"""
QID domain models - SQLAlchemy ORM.
"""

from __future__ import annotations

from typing import Any
from datetime import datetime

from sqlalchemy import String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class UserRecord(Base):
    """
    Stable user identity — source of truth for user_id and username.

    CREATE TABLE IF NOT EXISTS users (
        user_id int NOT NULL AUTO_INCREMENT,
        username varchar(255) NOT NULL,
        created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
        email varchar(255) NOT NULL DEFAULT '',
        wiki varchar(255) NOT NULL DEFAULT '',
        user_group varchar(120) NOT NULL DEFAULT 'Uncategorized',
        PRIMARY KEY (user_id),
        UNIQUE KEY uq_users_username (username)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    email: Mapped[str] = mapped_column(String(255), nullable=False, default="", server_default=text("''"))
    wiki: Mapped[str] = mapped_column(String(255), nullable=False, default="", server_default=text("''"))
    user_group: Mapped[str] = mapped_column(
        String(120), nullable=False, default="Uncategorized", server_default=text("'Uncategorized'")
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.current_timestamp())

    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.email = kwargs.get("email") or ""
        self.wiki = kwargs.get("wiki") or ""
        self.user_group = kwargs.get("user_group") or "Uncategorized"

    def to_dict(self) -> dict[str, Any]:
        """Serializes the pure model instance into a dictionary."""
        data: dict[str, Any] = {}
        table_keys = [
            "user_id",
            "username",
            "email",
            "wiki",
            "user_group",
            "created_at",
        ]
        for column in table_keys:
            value = getattr(self, column)
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            data[column] = value

        return data



__all__ = [
    "UserRecord",
]
