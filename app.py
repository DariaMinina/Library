import json

from flask import Flask, render_template, session  # глобальный объект приложения импортируем
from search.search import search
from scenario_auth.routes import auth_app
from scenario_order.routes import basket_app


app = Flask(__name__)  # __name__ имя модуля, точка входа
app.register_blueprint(search, url_prefix='/search')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(basket_app, url_prefix="/new_order")

app.config['SECRET_KEY'] = 'I am the only one'
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))

app.config['DB_CONFIG'] = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'Library'
}


@app.route("/")  # @ - декоратор, на входящий урл будет срабатывать эта функция, обработчик
def navbar():
    if 'client_id' in session:
        session.pop('client_id')
    if 'basket' in session:
        session.pop('basket')
    return render_template("navbar.html")


@app.route("/exit")
def exit():
    for key in list(session.keys()):
        session.pop(key)
    return render_template("exit.html", text='Вы вышли из системы.')


if __name__ == "__main__":
    app.debug = True
    app.run(host="127.0.0.1", port=5012)
