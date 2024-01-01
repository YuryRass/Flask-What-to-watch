from datetime import datetime, timezone
from random import randrange

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
# Задаётся конкретное значение для конфигурационного ключа
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Opinion(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(Text, unique=True)
    source: Mapped[str | None] = mapped_column(String(256))
    timestamp: Mapped[datetime] = mapped_column(index=True, default=now_utc)


@app.route("/")
def index_view():
    # Определяется количество мнений в базе данных
    # quantity = db.session.scalar(select(func.count()).select_from(Opinion))
    quantity = db.session.scalar(text("SELECT COUNT(*) FROM opinion"))
    # Если мнений нет,
    if not quantity:
        # то возвращается сообщение
        return "В базе данных мнений о фильмах нет!"
    # Иначе выбирается случайное число в диапазоне от 0 и до quantity
    offset_value = randrange(quantity)
    # И определяется случайный объект
    opinion: Opinion = Opinion.query.offset(offset_value).first()
    return render_template("opinion.html", opinion=opinion)


@app.route("/add")
def add_opinion_view():
    # И тут тоже
    return render_template("add_opinion.html")


if __name__ == "__main__":
    app.run()
