from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.tools.models.base import Base


class Archive(Base):
    __tablename__ = "archives"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    archiveurl: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Archive(id={self.id!r}, url={self.url!r}, archiveurl={self.archiveurl!r})"


__all__ = [
    "Archive",
]
