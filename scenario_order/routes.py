from flask import Blueprint, render_template, session, request, redirect, url_for, current_app
from scenario_auth.sql_provider import SQLProvider
from database import make_update, work_with_db
from scenario_order.utils import add_to_basket, clear_basket, clear_client
import datetime


basket_app = Blueprint('basket', __name__, template_folder='templates')
provider = SQLProvider("scenario_order/sql/")


@basket_app.route('/', methods=['GET', 'POST'])
def client_order():
    if request.method == "GET":
        sql = provider.get('client_list.sql')
        clients = work_with_db(current_app.config['DB_CONFIG'], sql)
        return render_template("choose_client.html", clients=clients)
    else:
        client_id = request.form['client_id']
        session['client_id'] = client_id
        if not client_id:
            return 'clients not found'
        return redirect(url_for('basket.list_order_handler'))


@basket_app.route('/order-menu', methods=['GET', 'POST'])
def list_order_handler():
    sql = provider.get('final_client.sql', id_client=session.get('client_id'))
    result = work_with_db(current_app.config['DB_CONFIG'], sql)
    client_name = result[0]['name']
    genres = ['Romance', 'Fantasy', 'YA(Young Adult)', 'Biography', 'Adventure']
    if request.method == "GET":
        point = request.args.get('point', None)
        current_basket = session.get('basket', [])
        if point:
            sql = provider.get('book_list_romance.sql', rom=point)
        else:
            sql = provider.get('books_list.sql')
        books = work_with_db(current_app.config['DB_CONFIG'], sql)
        return render_template("book_order_list.html", books=books, basket=current_basket, genres=genres, client=client_name)
    else:
        book_id = request.form['book_id']
        sql = provider.get('order_book.sql', book_id=book_id)
        books = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not books:
            return 'Books not found'
        add_to_basket(books)
        return redirect(url_for('basket.list_order_handler'))


@basket_app.route('/basket', methods=['GET', 'POST'])
def basket():
    if request.method == 'GET':
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('list.sql'))
        return render_template('list.html', items=items, heads=['Мебель', "Цена"])
    else:
        item_id = request.form.get("item_id")
        i_id = int(item_id)
        sql = provider.get('delete_item.sql', item_id=i_id)
        response = make_update(current_app.config['DB_CONFIG'], sql)
    return redirect(url_for('basket.basket'))


@basket_app.route('/order-menu-genre', methods=['GET', 'POST'])
def book_genre():
    if request.method == "GET":
        current_basket = session.get('basket', [])
        sql = provider.get('books_list.sql')
        books = work_with_db(current_app.config['DB_CONFIG'], sql)
        return render_template("book_order_list.html", books=books, basket=current_basket)
    else:
        if request.form['genre_book']:
            return redirect(url_for('basket.book_genre'))
        book_id = request.form['book_id']
        sql = provider.get('order_book.sql', book_id=book_id)
        books = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not books:
            return 'Books not found'
        add_to_basket(books)
        return redirect(url_for('basket.list_order_handler'))


@basket_app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "GET":
        return render_template("insert_item.html")
    else:
        item_name = request.form.get('item_name')
        price = request.form.get('price')
        sql = provider.get('insert.sql', item_name=item_name, price=price)
        response = make_update(current_app.config['DB_CONFIG'], sql)
    return redirect(url_for('basket.basket'))


@basket_app.route('/buy')
def buy_basket_handler():
    current_basket = session.get('basket', [])
    if current_basket:
        now = datetime.datetime.now()
        sql = provider.get('insert_order_client.sql', current_time=now, id_client=session.get('client_id'))
        response = make_update(current_app.config['DB_CONFIG'], sql)
        sql2 = provider.get('take_order_id.sql', id_client=session.get('client_id'))
        id_order = work_with_db(current_app.config['DB_CONFIG'], sql2)
        int_id = id_order[0]['order_id']
        for book in current_basket:
            sql3 = provider.get('insert_basket_order.sql', id_Order=int_id, book_Id=book['idbook'], book_Name=book['Name'], book_Genre=book['Genre'])
            response = make_update(current_app.config['DB_CONFIG'], sql3)
        return redirect(url_for('basket.success'))
    return redirect(url_for('basket.list_order_handler'))


@basket_app.route('/success', methods=['GET', 'POST'])
def success():
    sql = provider.get('final_client.sql', id_client=session.get('client_id'))
    result = work_with_db(current_app.config['DB_CONFIG'], sql)
    client_name = result[0]['name']
    text = "Составлен заказ для читателя "
    clear_client()
    return render_template("success_order.html", text=text, user=client_name)


@basket_app.route('/buy2')
def buy_basket_handler2():
    current_basket = session.get('basket', [])
    if current_basket:
        dict_of_items = {}
        print(current_basket)
        for product in current_basket:
            id = product['item_id']
            if id not in dict_of_items:
                dict_of_items[id] = 1
            elif id in dict_of_items:
                dict_of_items[id] += 1
        for key in dict_of_items:
            sql = provider.get('insert_basket.sql', item_id=key, amount=dict_of_items[key])
            response = make_update(current_app.config['DB_CONFIG'], sql)
        return redirect(url_for('basket.clear_basket_handler'))
    return redirect(url_for('basket.list_order_handler'))


@basket_app.route('/clear')
def clear_basket_handler():
    clear_basket()
    return redirect(url_for('basket.list_order_handler'))
