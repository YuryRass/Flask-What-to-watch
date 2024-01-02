from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from . import db


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Opinion(db.Model):
    """Отзыв на фильм"""
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(Text, unique=True)
    source: Mapped[str | None] = mapped_column(String(256))
    timestamp: Mapped[datetime] = mapped_column(index=True, default=now_utc)
    added_by: Mapped[str] = mapped_column(String(64))

    def update(self, data: dict) -> None:
        """Изменение атрибутов модели"""
        opinion_attrs = [clmn.key for clmn in self.__table__.columns]
        for attr in opinion_attrs:
            setattr(self, attr, data.get(attr, getattr(self, attr)))

    def filling(self, data: dict) -> None:
        """Заполнение новыми данными объекта модели"""
        for field in ["title", "text", "source", "added_by"]:
            if field in data:
                setattr(self, field, data[field])
