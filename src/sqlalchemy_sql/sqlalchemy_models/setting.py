"""
Admin domain models.
"""

from __future__ import annotations

import logging

from sqlalchemy import Column, Integer, String, text

# from sqlalchemy.dialects.mysql import LONGTEXT
from ..shared.engine import BaseDb

logger = logging.getLogger(__name__)


class LanguageSettingRecord(BaseDb):
    """
    CREATE TABLE IF NOT EXISTS language_settings (
        id int NOT NULL AUTO_INCREMENT,
        lang_code varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        move_dots tinyint DEFAULT '0',
        expend tinyint DEFAULT '0',
        add_en_lang tinyint DEFAULT '0',
        PRIMARY KEY (id),
        UNIQUE KEY lang_code (lang_code)
    )
    """

    __tablename__ = "language_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lang_code = Column(String(20), unique=True, nullable=True)
    move_dots = Column(Integer, default=0, server_default=text("0"))
    expend = Column(Integer, default=0, server_default=text("0"))
    add_en_lang = Column(Integer, default=0, server_default=text("0"))

    def __init__(self, **kwargs):
        # Apply Python-level defaults for fields not provided
        if "move_dots" not in kwargs:
            kwargs["move_dots"] = 0
        if "expend" not in kwargs:
            kwargs["expend"] = 0
        if "add_en_lang" not in kwargs:
            kwargs["add_en_lang"] = 0
        super().__init__(**kwargs)


__all__ = [
    "LanguageSettingRecord",
]
