from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import OpinionForm
from .models import Opinion


def random_opinion():
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion: Opinion = Opinion.query.offset(offset_value).first()
        return opinion


@app.route("/")
def index_view():
    """Случайный вывод мнения о фильме"""
    opinion: Opinion | None = random_opinion()
    if opinion:
        return render_template("opinion.html", opinion=opinion)
    abort(404)


@app.route("/add", methods=["GET", "POST"])
def add_opinion_view():
    """Добавление отзыва о фильме"""
    form = OpinionForm()
    # Если ошибок не возникло, то
    if form.validate_on_submit():
        text = form.text.data
        # Если в БД уже есть мнение с текстом, который ввёл пользователь,
        if Opinion.query.filter_by(text=text).first() is not None:
            # вызвать функцию flash и передать соответствующее сообщение
            flash("Такое мнение уже было оставлено ранее!")
            # и вернуть пользователя на страницу «Добавить новое мнение»
            return render_template("add_opinion.html", form=form)

        # нужно создать новый экземпляр класса Opinion
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data,
        )
        db.session.add(opinion)
        db.session.commit()
        # Затем перейти на страницу добавленного мнения
        return redirect(url_for("opinion_view", id=opinion.id))
    # Иначе просто отрисовать страницу с формой
    return render_template("add_opinion.html", form=form)


@app.route("/opinions/<int:id>")
def opinion_view(id):
    """Отображение отзыва по его ID"""
    opinion = db.get_or_404(
        Opinion,
        id,
        description=f"Opinion id {id} doesn't exist!",
    )
    return render_template("opinion.html", opinion=opinion)
