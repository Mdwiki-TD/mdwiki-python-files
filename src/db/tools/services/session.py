import os
from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_tools_db_url() -> str:
    user = os.getenv("TOOL_TOOLSDB_USER", "root")
    password = os.getenv("TOOL_TOOLSDB_PASSWORD", "root")
    host = os.getenv("TOOL_TOOLSDB_HOST", "127.0.0.1")
    dbname = os.getenv("TOOL_TOOLSDB_DBNAME", "s57081__svgdb")

    # Toolforge usually uses MySQL/MariaDB
    return f"mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8mb4"


engine = create_engine(get_tools_db_url(), pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


@contextmanager
def get_session() -> Generator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


__all__ = [
    "get_tools_db_url",
    "get_session",
]
