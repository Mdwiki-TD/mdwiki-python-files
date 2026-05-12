"""Application configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass

# --- Data Classes for Configuration Sections ---


@dataclass(frozen=True)
class DbConfig:
    db_name: str
    db_host: str
    db_user: str | None
    db_password: str | None

    def to_dict(self) -> dict:
        return {
            "db_name": self.db_name,
            "db_host": self.db_host,
            "db_user": self.db_user,
            "db_password": self.db_password,
        }


# --- Configuration Loaders ---


def _load_database_config() -> DbConfig:
    return DbConfig(
        db_name=os.getenv("DB_NAME", ""),
        db_host=os.getenv("DB_HOST_TOOLS", ""),
        db_user=os.getenv("TOOL_TOOLSDB_USER", None),
        db_password=os.getenv("TOOL_TOOLSDB_PASSWORD", None),
    )


database_data = _load_database_config()


def has_db_config() -> bool:
    """Return True when database connection details are configured."""
    return bool(database_data.db_host)
