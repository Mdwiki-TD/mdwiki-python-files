from __future__ import annotations

import logging

from sqlalchemy import Column, DateTime, Integer, String, func, text

from ..shared.engine import BaseDb

logger = logging.getLogger(__name__)


class UserRecord(BaseDb):
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id int NOT NULL AUTO_INCREMENT,
        username varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
        email varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        wiki varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
        user_group varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Uncategorized',
        reg_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id)
    )
    """

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, default="")
    wiki = Column(String(255), nullable=False, default="")
    user_group = Column(String(120), nullable=False, default="Uncategorized", server_default=text("'Uncategorized'"))
    reg_date = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    def __init__(self, **kwargs):
        # Apply Python-level defaults for fields not provided
        if "email" not in kwargs:
            kwargs["email"] = ""
        if "wiki" not in kwargs:
            kwargs["wiki"] = ""
        if "user_group" not in kwargs:
            kwargs["user_group"] = "Uncategorized"
        super().__init__(**kwargs)


__all__ = [
    "UserRecord",
]
