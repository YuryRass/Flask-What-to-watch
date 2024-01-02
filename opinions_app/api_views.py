from flask import Response, json, request

from . import app, db
from .models import Opinion
from .views import random_opinion


@app.route("/api/get-random-opinion/", methods=["GET"])
def get_random_opinion():
    """Выводит случаный отзыв о фильме"""
    opinion = random_opinion()

    json_string = json.dumps({"opinion": opinion}, ensure_ascii=False)

    response = Response(
        json_string,
        status=201,
        content_type="application/json; charset=utf-8",
    )
    return response


@app.route("/api/opinions/", methods=["GET"])
def get_opinions():
    """Вывод всех отзывов"""
    opinions = Opinion.query.all()
    opinions_list = json.dumps(
        {"opinions": opinions},
        ensure_ascii=False,
    )

    response = Response(
        opinions_list,
        status=200,
        content_type="application/json; charset=utf-8",
    )
    return response


@app.route("/api/opinions/", methods=["POST"])
def add_opinion():
    """Добавление отзыва на фильм"""
    data = request.get_json()
    # Создание нового пустого отзыва
    opinion = Opinion()
    # Наполнение его данными из запроса
    opinion.filling(data)
    # Сохрание в БД
    db.session.add(opinion)
    db.session.commit()
    # JSON вывод
    json_string = json.dumps({"opinion": opinion}, ensure_ascii=False)

    response = Response(
        json_string,
        status=201,
        content_type="application/json; charset=utf-8",
    )
    return response


@app.route("/api/opinions/<int:id>/", methods=["GET"])
def get_opinion(id):
    """Вывод отзыва по его ID"""
    # Получить объект по id или выбросить ошибку
    opinion = Opinion.query.get_or_404(id)
    json_string = json.dumps({"opinion": opinion}, ensure_ascii=False)
    # creating a Response object to set the content type and the encoding
    response = Response(
        json_string,
        status=200,
        content_type="application/json; charset=utf-8",
    )
    return response


@app.route("/api/opinions/<int:id>/", methods=["PATCH"])
def update_opinion(id):
    """Изменение параметров отзыва"""
    data: dict = request.get_json()
    opinion: Opinion | None = Opinion.query.get_or_404(id)

    # изменяем атрибуты отзыва
    opinion.update(data)
    db.session.commit()

    # JSON вывод
    json_string = json.dumps({"opinion": opinion}, ensure_ascii=False)

    response = Response(
        json_string,
        status=201,
        content_type="application/json; charset=utf-8",
    )
    return response


@app.route("/api/opinions/<int:id>/", methods=["DELETE"])
def delete_opinion(id):
    """Удаление отзыва"""
    opinion = Opinion.query.get_or_404(id)
    db.session.delete(opinion)
    db.session.commit()

    return "", 204
