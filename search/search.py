from flask import Blueprint, render_template, request, current_app
from database import work_with_db
from search.sql_provider import SQLProvider
from access import login_permission_required

search = Blueprint('search', __name__, template_folder='templates', static_folder='../mybulma/css')

provider = SQLProvider("search/sql/")


@search.route('/')
@login_permission_required
def main():
    return render_template("navbar_search.html")


@search.route('/search-id', methods=['GET', 'POST'])
@login_permission_required
def search_id():
    if request.method == "POST":
        heads = ['ID издательства', 'Название', 'Город', 'Дата заключения договора', 'Дата расторжения договора']
        year = request.form.get('year')
        month = request.form.get('month')
        submit = request.form.get('submit')
        if submit:
            sql = provider.get('all.sql')
        else:
            sql = provider.get('ik1.sql', year=year, month=month)
        if not sql:
            return 'Bad'
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not result:
            return render_template("ik1.html", error='Ошибка')
        return render_template("ik1_result.html", data=result, year=year, month=month, heads=heads)
    return render_template("ik1.html")


@search.route('/search-date', methods=['GET', 'POST'])
def search_date():
    if request.method == "POST":
        heads = ['Название', 'Дата расторжения договора']
        year = request.form.get('year')
        sql = provider.get('ik2.sql', year=year)
        if not sql:
            return 'Bad'
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not result:
            return render_template("ik2.html", error='Ошибка')
        return render_template("ik2_result.html", data=result, year=year, heads=heads)
    return render_template("ik2.html")


@search.route('/search-city', methods=['GET', 'POST'])
def search_city():
    if request.method == "POST":
        heads = ['Город', 'Количество издательств']
        city = request.form.get('city')
        sql = provider.get('ik3.sql', city=city)
        if not sql:
            return 'Bad'
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not result:
            return render_template("ik3.html", error='Ошибка')
        return render_template("ik3_result.html", data=result, city=city, heads=heads)
    return render_template("ik3.html")


@search.route('/search-gbook', methods=['GET', 'POST'])
def search_gbook():
    if request.method == "POST":
        heads = ['Название книги', 'Автор', 'Жанр']
        genre = request.form.get('genre')
        sql = provider.get('ik4.sql', genre=genre)
        if not sql:
            return 'Bad'
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not result:
            return render_template("ik4.html", error='Ошибка')
        return render_template("ik4_result.html", data=result, genre=genre, heads=heads)
    return render_template("ik4.html")


@search.route('/search-genre', methods=['GET', 'POST'])
def search_genre():
    if request.method == "POST":
        heads = ['Жанр', 'Количество книг']
        genre = request.form.get('genre')
        sql = provider.get('ik5.sql', genre=genre)
        if not sql:
            return 'Bad'
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not result:
            return render_template("ik5.html", error='Ошибка')
        return render_template("ik5_result.html", data=result, genre=genre, heads=heads)
    return render_template("ik5.html")


@search.route('/search-min', methods=['GET', 'POST'])
def search_min():
    if request.method == "POST":
        heads = ['Название книги', 'Цена', 'Издательство']
        name = request.form.get('name')
        sql = provider.get('ik6.sql', name1=name)
        if not sql:
            return 'Bad'
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not result:
            return render_template("ik6.html", error='Ошибка')
        return render_template("ik6_result.html", data=result, name=name, heads=heads)
    return render_template("ik6.html")

