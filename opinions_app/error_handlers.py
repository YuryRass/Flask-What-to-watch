from flask import Response, json, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None) -> None:
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def __str__(self) -> str:
        return json.dumps({"message": self.message}, ensure_ascii=False)


# Обработчик кастомного исключения для API
@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage):
    return Response(
        str(error),
        status=error.status_code,
        content_type="application/json; charset=utf-8",
    )


# Тут декорируется обработчик и указывается код нужной ошибки
@app.errorhandler(404)
def page_not_found(error):
    # В качестве ответа возвращается собственный шаблон
    # и код ошибки
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    # В таких случаях можно откатить незафиксированные изменения в БД
    db.session.rollback()
    return render_template("500.html"), 500
